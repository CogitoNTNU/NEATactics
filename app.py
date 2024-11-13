import eventlet
eventlet.monkey_patch()

import base64
from io import BytesIO
import pickle
import time
from flask import Flask, render_template, jsonify, request
from flask_socketio import SocketIO, emit, join_room, leave_room

import os
import sys
import threading
import queue
import subprocess
import logging
import re
from PIL import Image
import numpy as np

# Import your custom modules
from src.genetics.genome import Genome
from src.genetics.traverse import Traverse
from src.environments.fitness_function import Fitness
from src.environments.mario_env import MarioJoypadSpace
from src.environments.debug_env import env_debug_init
from src.visualization.visualize_genome import visualize_genome
from src.utils.utils import save_state_as_png, insert_input

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'  # Replace with your secret key
socketio = SocketIO(app, cors_allowed_origins="*")  # Enable CORS if needed

# Initialize logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s')

# Global variables
training_thread = None
current_training_status = {
    'is_training': False,
    'current_generation': 0,
    'best_fitness': 0,
    'avg_fitness': 0,
    'min_fitness': 0,
    'history': {}
}

# Modify the frame_queues initialization to use NEAT names instead of session IDs
frame_queues = {}

class FitnessFileHandler(FileSystemEventHandler):
    def __init__(self, neat_name):
        self.neat_name = neat_name
        self.last_modified_time = None
        self.last_content = None
        
    def on_modified(self, event):
        if not event.is_directory and event.src_path.endswith('fitness_values.txt'):
            # Add a small delay to ensure file writing is complete
            time.sleep(0.1)
            
            try:
                # Read current content
                with open(event.src_path, 'r') as f:
                    current_content = f.read()
                
                # Only process if content has actually changed
                if current_content != self.last_content:
                    self.last_content = current_content
                    logging.info(f"Detected meaningful change in: {event.src_path}")
                    
                    # Parse the fitness data
                    generations, best_fitnesses, avg_fitnesses, min_fitnesses = parse_fitness_file(self.neat_name)
                    
                    if generations:  # Only update if we have data
                        status_update = {
                            'current_generation': generations[-1],
                            'best_fitness': best_fitnesses[-1],
                            'avg_fitness': avg_fitnesses[-1],
                            'min_fitness': min_fitnesses[-1],
                            'history': {
                                'generations': generations,
                                'best_fitnesses': best_fitnesses,
                                'avg_fitnesses': avg_fitnesses,
                                'min_fitnesses': min_fitnesses
                            }
                        }
                        
                        logging.info(f"Emitting training_status_update to room {self.neat_name}")
                        socketio.emit('training_status_update', status_update, room=self.neat_name)
                    
            except Exception as e:
                logging.error(f"Error processing fitness file update: {e}")
                logging.exception("Exception details:")

def start_file_watcher(neat_name):
    fitness_file_path = os.path.join('data', neat_name, 'fitness', 'fitness_values.txt')
    fitness_dir = os.path.dirname(fitness_file_path)

    if not os.path.exists(fitness_dir):
        os.makedirs(fitness_dir, exist_ok=True)
        logging.info(f"Created fitness directory: {fitness_dir}")

    event_handler = FitnessFileHandler(neat_name)
    observer = Observer()
    observer.schedule(event_handler, path=fitness_dir, recursive=False)
    observer.start()
    logging.info(f"Started file watcher on {fitness_file_path}")
    return observer  # Return the observer so we can stop it later if needed

# Keep track of active observers
file_watchers = {}

@socketio.on('join_neat_room')
def handle_join_neat_room(data):
    neat_name = data.get('neat_name')
    if neat_name:
        # Initialize frame queue for this NEAT instance if it doesn't exist
        if neat_name not in frame_queues:
            frame_queues[neat_name] = queue.Queue()
        join_room(neat_name)
        logging.info(f"Client {request.sid} joined room {neat_name}")

@socketio.on('leave_neat_room')
def handle_leave_neat_room(data):
    neat_name = data.get('neat_name')
    if neat_name:
        leave_room(neat_name)
        logging.info(f"Client {request.sid} left room {neat_name}")
        # Only remove the frame queue if no clients are left in the room
        room = socketio.server.manager.rooms.get('', {}).get(neat_name, set())
        if not room:
            frame_queues.pop(neat_name, None)
            logging.info(f"Removed frame queue for {neat_name}")
            
# Function to get NEAT populations
def get_neat_populations():
    """Get list of NEAT populations from the data directory"""
    directory = 'data/'
    neat_dirs = []
    
    try:
        for d in os.listdir(directory):
            if os.path.isdir(os.path.join(directory, d)) and d != 'trained_population':
                neat_dirs.append(d)
    except FileNotFoundError:
        logging.error(f"Directory not found: {directory}")
        return []
    
    logging.info(f"Available NEAT directories: {neat_dirs}")
    return neat_dirs

# Function to parse fitness file
def parse_fitness_file(neat_name):
    """Parse fitness values from the fitness file"""
    fitness_file_path = f'data/{neat_name}/fitness/fitness_values.txt'
    generations = []
    best_fitnesses = []
    avg_fitnesses = []
    min_fitnesses = []
    
    if not os.path.exists(fitness_file_path):
        logging.error(f"Fitness file not found: {fitness_file_path}")
        return [], [], [], []
    
    try:
        with open(fitness_file_path, 'r') as f:
            for line in f:
                logging.debug(f"Parsing line: {line.strip()}")
                pattern = r'Generation: (\d+) - Best: ([\d.-]+) - Avg: ([\d.-]+) - Min: ([\d.-]+)'
                match = re.match(pattern, line)
                if match:
                    gen, best, avg, min_fit = match.groups()
                    generations.append(int(gen))
                    best_fitnesses.append(float(best))
                    avg_fitnesses.append(float(avg))
                    min_fitnesses.append(float(min_fit))
                else:
                    logging.warning(f"Line did not match pattern: {line.strip()}")
    except Exception as e:
        logging.error(f"Failed to parse fitness file: {e}")
    
    logging.info(f"Parsed {len(generations)} generations from fitness file.")
    return generations, best_fitnesses, avg_fitnesses, min_fitnesses

# Route for the home page
@app.route('/')
def home():
    neat_dirs = get_neat_populations()
    return render_template('index.html', neat_dirs=neat_dirs)

@socketio.on('connect')
def handle_connect():
    logging.info(f"Client connected: {request.sid}")
    # We don't initialize frame queues here anymore

@socketio.on('disconnect')
def handle_disconnect():
    # Remove the frame queue for this client
    frame_queues.pop(request.sid, None)
    logging.info(f"Client disconnected: {request.sid}")

# API route to play genome
@app.route('/api/play_genome', methods=['POST'])
def play_genome():
    data = request.json
    neat_name = data.get('neat_name')
    from_gen = data.get('from_gen')
    to_gen = data.get('to_gen')
    
    if not all([neat_name, from_gen, to_gen]):
        logging.warning("Missing parameters in play_genome request.")
        return jsonify({'status': 'error', 'message': 'Missing required parameters'}), 400
    
    try:
        from_gen = int(from_gen)
        to_gen = int(to_gen)
    except ValueError:
        logging.warning("Invalid generation numbers provided.")
        return jsonify({'status': 'error', 'message': 'Generation numbers must be integers'}), 400
    
    main_py_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'main.py')  # Absolute path to main.py
    
    # Ensure main.py exists
    if not os.path.isfile(main_py_path):
        logging.error(f"main.py not found at {main_py_path}")
        return jsonify({'status': 'error', 'message': 'Internal server error'}), 500
    
    # Check if a process is already running
    global training_thread
    if training_thread and training_thread.is_alive():
        logging.warning("Attempted to play genomes while another process is in progress.")
        return jsonify({'status': 'error', 'message': 'Another process is currently running. Please wait.'}), 400
    
    # Start a new thread for playing genomes
    play_thread = threading.Thread(target=play_genome_wrapper, args=(neat_name, from_gen, to_gen))
    play_thread.start()
    
    # Update the training status
    current_training_status['is_training'] = True
    logging.info("Started play_genome_wrapper thread and set is_training to True.")
    
    return jsonify({
        'status': 'success',
        'message': f'Playing genomes from generation {from_gen} to {to_gen} for NEAT instance: {neat_name}'
    }), 200

@app.route('/api/training_status')
def get_training_status():
    neat_name = request.args.get('neat_name', 'latest')
    
    generations, best_fitnesses, avg_fitnesses, min_fitnesses = parse_fitness_file(neat_name)
    
    if generations:
        current_training_status.update({
            'current_generation': generations[-1],
            'best_fitness': best_fitnesses[-1],
            'avg_fitness': avg_fitnesses[-1],
            'min_fitness': min_fitnesses[-1]
        })
    
    current_training_status.update({
        'history': {
            'generations': generations,
            'best_fitnesses': best_fitnesses,
            'avg_fitnesses': avg_fitnesses,
            'min_fitnesses': min_fitnesses
        }
    })
    
    return jsonify(current_training_status)

def play_genome_wrapper(neat_name, from_gen, to_gen): 
    try:
        # Start frame streaming in a separate thread
        streaming_thread = threading.Thread(target=stream_frames, args=(neat_name,))
        streaming_thread.start()
        logging.info(f"Started streaming_thread for NEAT: {neat_name}")

        # Loop over generations
        for gen in range(from_gen, to_gen + 1):
            try:
                # Load genome for current generation
                genome = load_genome(neat_name, gen)
                logging.info(f"Playing genome from generation {gen}")

                # Initialize the environment and get the initial state
                env, initial_state = env_debug_init()

                # Run the game and capture frames
                fitness_value = run_game_debug(env, initial_state, genome, neat_name, visualize=True, frame_queue=frame_queues.get(neat_name))
                logging.info(f"Game run completed for generation {gen} with fitness: {fitness_value}")

                # Optional: Introduce a delay between genomes
                time.sleep(1)

            except FileNotFoundError:
                logging.error(f"Genome file for generation {gen} not found.")
            except Exception as e:
                logging.error(f"Error running genome for generation {gen}: {e}")
                logging.exception("Exception occurred while running genome")

    except Exception as e:
        logging.error(f"Error in play_genome_wrapper: {e}")
        logging.exception("Exception occurred in play_genome_wrapper")
    finally:
        current_training_status['is_training'] = False
        logging.info("play_genome_wrapper completed and is_training set to False.")

def stream_frames(neat_name):
    frame_queue = frame_queues.get(neat_name)
    if frame_queue is None:
        logging.error(f"No frame queue found for NEAT: {neat_name}")
        return
    
    logging.info(f"Started streaming frames for NEAT: {neat_name}")
    while current_training_status['is_training']:
        try:
            # Get the next frame from the queue
            frame = frame_queue.get(timeout=1)
            if frame is None:
                logging.info("Received termination signal for streaming frames.")
                break
            # Emit the frame to the client(s) in the specific room
            socketio.emit('frame', {'data': frame}, room=neat_name)
        except queue.Empty:
            continue
        except Exception as e:
            logging.error(f"Error streaming frames to NEAT {neat_name}: {e}")
            break
    logging.info(f"Stopped streaming frames for NEAT: {neat_name}")

# Function to load a genome (implement as per your project structure)
def load_genome(neat_name, generation):
    # Placeholder implementation
    # Replace with actual genome loading logic
    if generation == -1:  # Find the genome from the latest generation.
        files = os.listdir(f'data/{neat_name}/good_genomes')
        pattern = re.compile(r'best_genome_(\d+).obj')
        generations = []
        for file in files:
            match = pattern.match(file)
            if match:
                generations.append(int(match.group(1)))
        if generations:
            generation = max(generations)
            logging.info(f"Loading best genome from generation: {generation}")
        else:
            raise FileNotFoundError("No valid genome files found in 'data/good_genomes'.")
    
    genome_path = f'data/{neat_name}/good_genomes/best_genome_{generation}.obj'
    if not os.path.exists(genome_path):
        raise FileNotFoundError(f"Genome file does not exist: {genome_path}")
    
    with open(genome_path, 'rb') as f:
        genome = pickle.load(f)
    logging.info(f"Loaded genome from {genome_path}")
    return genome

# Modified run_game_debug function
def run_game_debug(env: MarioJoypadSpace, initial_state: np.ndarray, genome: Genome, neat_name: str, visualize: bool = True, frame_queue=None) -> float:
    forward = Traverse(genome)
    fitness = Fitness()
    insert_input(genome, initial_state)
    last_fitness_val: float = 0
    stagnation_counter: float = 0
    i = 0
    
    while True:
        action = forward.traverse()
        time.sleep(0.01)
        sr = env.step(action)  # State, Reward, Done, Info
        
        # Capture frame as RGB array
        frame = env.render(mode='rgb_array')
        
        if frame_queue is not None:
            try:
                # Convert the frame to a PIL Image
                img = Image.fromarray(frame)
                buffer = BytesIO()
                img.save(buffer, format='JPEG')
                frame_data = buffer.getvalue()
                base64_frame = base64.b64encode(frame_data).decode('utf-8')
                
                # Put the encoded frame into the queue
                frame_queue.put(base64_frame)
                logging.debug(f"Frame queued for NEAT.")
            except Exception as e:
                logging.error(f"Error encoding frame: {e}")
        
        # Optional visualization
        if visualize and i % 10000 == 0:
            save_state_as_png(0, sr.state, neat_name)
            visualize_genome(genome, neat_name, 0)
        
        # Calculate fitness
        fitness.calculate_fitness(sr.info, action)
        fitness_val: float = fitness.get_fitness()
        
        if fitness_val > last_fitness_val:
            last_fitness_val = fitness_val
            stagnation_counter = 0
        else:
            stagnation_counter += 1
        
        if sr.info["life"] == 1 or stagnation_counter > 150:
            env.close()
            logging.info(f"Exiting game loop for NEAT {neat_name} with fitness {fitness_val}")
            return fitness.get_fitness()
        
        i += 1
        insert_input(genome, sr.state)

# API route to create NEAT instance
@app.route('/api/create_neat', methods=['POST'])
def create_neat():
    data = request.json
    neat_name = data.get('neat_name')
    generations = int(data.get('generations', 10))

    if not neat_name:
        return jsonify({'status': 'error', 'message': 'Name is required'}), 400

    logging.info(f"Creating new NEAT instance: {neat_name} with {generations} generations.")

    def training_wrapper():
        try:
            # Start the file watcher in a separate thread
            file_watcher_thread = threading.Thread(target=start_file_watcher, args=(neat_name,))
            file_watcher_thread.daemon = True  # Daemonize thread to exit when main thread exits
            file_watcher_thread.start()
            logging.info("File watcher thread started.")

            # Run the training process
            python_executable = sys.executable
            main_py_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'main.py')
            if not os.path.isfile(main_py_path):
                logging.error(f"main.py not found at {main_py_path}")
                return

            subprocess.run([python_executable, main_py_path, '-n', neat_name, 'train', '-g', str(generations)], check=True)
            logging.info("Training process completed.")
        except subprocess.CalledProcessError as e:
            logging.error(f"Training process failed: {e}")
        except Exception as e:
            logging.error(f"Unexpected error in training_wrapper: {e}")
            logging.exception("Exception occurred in training_wrapper")
        finally:
            current_training_status['is_training'] = False
            logging.info("Training status set to False.")

    global training_thread
    training_thread = threading.Thread(target=training_wrapper)
    training_thread.start()
    current_training_status['is_training'] = True
    logging.info("Training thread started and is_training set to True.")

    return jsonify({'status': 'success', 'message': f'Created new NEAT instance: {neat_name}'}), 200

if __name__ == '__main__':
    logging.info("Starting Flask-SocketIO server.")
    socketio.run(app, debug=True, use_reloader=False, port=5000)