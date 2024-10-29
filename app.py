import eventlet
eventlet.monkey_patch()

from flask import Flask, render_template, jsonify, request
from flask_socketio import SocketIO, emit

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
from src.visualization.visualize_genome import visualize_genome
from src.utils.utils import save_state_as_png, insert_input

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

# Dictionary to keep track of frame queues per client
frame_queues = {}

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
    
    try:
        with open(fitness_file_path, 'r') as f:
            for line in f:
                pattern = r'Generation: (\d+) - Best: ([\d.-]+) - Avg: ([\d.-]+) - Min: ([\d.-]+)'
                match = re.match(pattern, line)
                if match:
                    gen, best, avg, min_fit = match.groups()
                    generations.append(int(gen))
                    best_fitnesses.append(float(best))
                    avg_fitnesses.append(float(avg))
                    min_fitnesses.append(float(min_fit))
    except FileNotFoundError:
        logging.error(f"Fitness file not found: {fitness_file_path}")
        return [], [], [], []
    
    return generations, best_fitnesses, avg_fitnesses, min_fitnesses

# Route for the home page
@app.route('/')
def home():
    neat_dirs = get_neat_populations()
    return render_template('index.html', neat_dirs=neat_dirs)

# SocketIO event handlers
@socketio.on('connect')
def handle_connect():
    # Initialize a frame queue for this client
    frame_queues[request.sid] = queue.Queue()
    logging.info(f"Client connected: {request.sid}")

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
    
    python_executable = sys.executable  # Path to the current Python interpreter
    main_py_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'main.py')  # Absolute path to main.py
    
    # Ensure main.py exists
    if not os.path.isfile(main_py_path):
        logging.error(f"main.py not found at {main_py_path}")
        return jsonify({'status': 'error', 'message': 'Internal server error'}), 500
    
    # Check if a process is already running
    if training_thread and training_thread.is_alive():
        logging.warning("Attempted to play genomes while another process is in progress.")
        return jsonify({'status': 'error', 'message': 'Another process is currently running. Please wait.'}), 400
    
    # Start a new thread for playing genomes
    play_thread = threading.Thread(target=play_genome_wrapper, args=(neat_name, from_gen, to_gen))
    play_thread.start()
    
    # Update the training status
    current_training_status['is_training'] = True
    
    return jsonify({
        'status': 'success',
        'message': f'Playing genomes from generation {from_gen} to {to_gen} for NEAT instance: {neat_name}'
    }), 200

def play_genome_wrapper(neat_name, from_gen, to_gen):
    try:
        # Initialize the environment and genome
        env, initial_state = env_debug_init()
        genome = load_genome(neat_name, from_gen)  # Implement this function as per your project
        # Assuming 'load_genome' loads a genome from a specific generation
        # If not, adjust accordingly
        
        # Start frame streaming in a separate thread
        sid = get_current_sid()  # Implement a way to get the current client's SID
        if sid is None:
            logging.error("No client SID found for streaming frames.")
            return
        
        # Start the frame sending thread
        streaming_thread = threading.Thread(target=stream_frames, args=(sid,))
        streaming_thread.start()
        
        # Run the game and capture frames
        fitness_value = run_game_debug(env, initial_state, genome, num=0, visualize=True, frame_queue=frame_queues[sid])
        logging.info(f"Game run completed with fitness: {fitness_value}")
        
    except Exception as e:
        logging.error(f"Error in play_genome_wrapper: {e}")
    finally:
        current_training_status['is_training'] = False

def stream_frames(sid):
    frame_queue = frame_queues.get(sid)
    if frame_queue is None:
        logging.error(f"No frame queue found for SID: {sid}")
        return
    
    while current_training_status['is_training']:
        try:
            # Get the next frame from the queue
            frame = frame_queue.get(timeout=1)
            # Emit the frame to the client
            socketio.emit('frame', {'data': frame}, room=sid)
        except queue.Empty:
            continue
        except Exception as e:
            logging.error(f"Error streaming frames to SID {sid}: {e}")
            break

# Function to get the current client's SID
def get_current_sid():
    # This function needs to be implemented to retrieve the client's SID
    # It can be passed as a parameter or managed via a global variable
    # For simplicity, this example assumes a single client
    if frame_queues:
        return next(iter(frame_queues.keys()))
    return None

# Function to load a genome (implement as per your project structure)
def load_genome(neat_name, generation):
    # Placeholder implementation
    # Replace with actual genome loading logic
    return Genome(0) # Replace 0 with the appropriate id value

# Modified run_game_debug function
def run_game_debug(env: MarioJoypadSpace, initial_state: np.ndarray, genome: Genome, num: int, visualize: bool = True, frame_queue=None) -> float:
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
            # Convert the frame to a PIL Image
            img = Image.fromarray(frame)
            buffer = BytesIO()
            img.save(buffer, format='JPEG')
            frame_data = buffer.getvalue()
            base64_frame = base64.b64encode(frame_data).decode('utf-8')
            
            # Put the encoded frame into the queue
            frame_queue.put(base64_frame)
        
        # Optional visualization
        if visualize and i % 10000 == 0:
            save_state_as_png(0, sr.state)
            visualize_genome(genome, 0)
        
        # Calculate fitness
        fitness.calculate_fitness(sr.info, action)
        fitness_val: float = fitness.get_fitness()
        logging.info(f"Fitness: {fitness_val}")
        
        if fitness_val > last_fitness_val:
            last_fitness_val = fitness_val
            stagnation_counter = 0
        else:
            stagnation_counter += 1
        
        if sr.info["life"] == 1 or stagnation_counter > 150:
            env.close()
            return fitness.get_fitness()
        
        i += 1
        insert_input(genome, sr.state)

if __name__ == '__main__':
    socketio.run(app, debug=True, port=5000)
