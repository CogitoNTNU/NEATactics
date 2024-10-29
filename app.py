from flask import Flask, logging, render_template, jsonify, request
import os
from datetime import datetime
import threading
import queue
import re
import subprocess

import sys
import os

# Add this to your Flask app
import numpy
print("Numpy path:", numpy.__file__)

print("Python executable:", sys.executable)
print("Python path:", sys.path)
print("Working directory:", os.getcwd())

app = Flask(__name__)
training_thread = None
message_queue = queue.Queue()
current_training_status = {
    'is_training': False,
    'current_generation': 0,
    'best_fitness': 0,
    'avg_fitness': 0,
    'min_fitness': 0
}

def get_neat_populations():
    """Get list of NEAT populations from the data directory"""
    directory = 'data/'
    neat_dirs = []
    
    try:
        for d in os.listdir(directory):
            if os.path.isdir(os.path.join(directory, d)) and d != 'trained_population':
                neat_dirs.append(d)
    except FileNotFoundError:
        print(f"Directory not found: {directory}")
        return []
    
    print(f"Available NEAT directories: {neat_dirs}")  # Debugging line
    return neat_dirs

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
        print(f"Fitness file not found: {fitness_file_path}")
        return [], [], [], []
    
    return generations, best_fitnesses, avg_fitnesses, min_fitnesses

@app.route('/')
def home():
    neat_dirs = get_neat_populations()
    return render_template('index.html', neat_dirs=neat_dirs)

@app.route('/api/create_neat', methods=['POST'])
def create_neat():
    data = request.json
    neat_name = data.get('neat_name')
    generations = int(data.get('generations', 10))
    
    if not neat_name:
        return jsonify({'status': 'error', 'message': 'Name is required'})
    
    def training_wrapper():
        try:
            # Get the path to the Python interpreter that's currently running
            python_executable = sys.executable
            subprocess.run([python_executable, 'main.py', '-n', neat_name, 'train', '-g', str(generations)])
        finally:
            current_training_status['is_training'] = False
    
    training_thread = threading.Thread(target=training_wrapper)
    training_thread.start()
    
    return jsonify({'status': 'success', 'message': f'Created new NEAT instance: {neat_name}'})

@app.route('/api/play_genome', methods=['POST'])
def play_genome():
    data = request.json
    neat_name = data.get('neat_name')
    from_gen = data.get('from_gen')
    to_gen = data.get('to_gen')
    
    if not all([neat_name, from_gen, to_gen]):
        return jsonify({'status': 'error', 'message': 'Missing required parameters'}), 400
    
    try:
        from_gen = int(from_gen)
        to_gen = int(to_gen)
    except ValueError:
        return jsonify({'status': 'error', 'message': 'Generation numbers must be integers'}), 400
    
    python_executable = sys.executable  # Path to the current Python interpreter
    main_py_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'main.py')  # Absolute path to main.py
    
    def play_genome_wrapper():
        try:
            subprocess.run(
                [python_executable, main_py_path, '-n', neat_name, 'play', '-f', str(from_gen), '-t', str(to_gen)],
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            # Optionally, communicate the error back to the frontend via a message queue or other means
        finally:
            current_training_status['is_training'] = False
    
    # Check if a training or playing process is already running
    if training_thread and training_thread.is_alive():
        return jsonify({'status': 'error', 'message': 'Another process is currently running. Please wait.'}), 400
    
    # Start the subprocess in a new thread to avoid blocking
    play_thread = threading.Thread(target=play_genome_wrapper)
    play_thread.start()
    
    # Update the training status
    current_training_status['is_training'] = True
    
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

if __name__ == '__main__':
    app.run(debug=True, port=5000)