# GUI

- [GUI](#gui)
  - [Purpose](#purpose)
  - [Structure](#structure)
  - [Usage](#usage)
    - [Running the GUI](#running-the-gui)
    - [Main Menu](#main-menu)
    - [Training Scene](#training-scene)
    - [Settings Scene](#settings-scene)
    - [Watch Best Genome Scene](#watch-best-genome-scene)
    - [Visualize Best Genome Scene](#visualize-best-genome-scene)
  - [Modules and Classes](#modules-and-classes)
    - [`gui_with_pygame.py`](#gui_with_pygamepy)
      - [Classes](#classes)
      - [Key Methods](#key-methods)
    - [`Scene.py`](#scenepy)
      - [`Scene` Class](#scene-class)
  - [Note](#note)

## Purpose

The `GUI` folder contains a Pygame-based graphical user interface for interacting with the NEAT (NeuroEvolution of Augmenting Topologies) algorithm applied to the Super Mario Bros game. It provides an interactive platform to:

- **Train neural networks** using the NEAT algorithm.
- **Adjust configuration settings** for the NEAT parameters.
- **Watch genomes** play the game.
- **Visualize neural network structures** of genomes.

This GUI aims to make it easier to experiment with different settings, observe the training process, and understand how genomes evolve over time.

## Structure

- `gui_with_pygame.py`: The main script that runs the GUI application. It defines classes for UI elements and manages scenes, event handling, and rendering.
- `Scene.py`: Contains the `Scene` class for managing different scenes within the GUI. *(Note: This file may not be actively used in the current version.)*
- `README.md`: Documentation for the `GUI` folder (this file).

## Usage

### Running the GUI

To start the GUI application, run the `gui_with_pygame.py` script from the root directory:

```zsh
python gui_with_pygame.py
```

Ensure that all dependencies are installed, including `pygame` and any custom modules referenced in the code.

### Main Menu

Upon launching the application, you will see the main menu with the following options:

- **Train!**: Navigate to the training scene to configure and start training neural networks.
- **Settings**: Adjust advanced NEAT configuration parameters.
- **Watch best gene**: Select and watch genomes play the game.
- **Visualize best genome**: Visualize the neural network structure of the best-performing genome.

### Training Scene

In the training scene, you can set the following training parameters:

- **Population size**: Number of genomes in each generation.
- **Mutation rate**: The probability of mutations occurring during evolution.
- **Generations**: The number of generations to train.

**Actions:**

- **Start Training**: Begins the training process with the specified parameters.
- **Back to Menu**: Returns to the main menu.

*Note:* Training will invoke the `neat_test_file.main()` function. Ensure that `neat_test_file.py` is properly implemented and accessible.

### Settings Scene

Adjust advanced configuration settings for the NEAT algorithm:

- **c1, c2, c3**: Compatibility coefficients used in speciation.
- **Genomic Distance Threshold**: Threshold for determining species separation.
- **Population Size**: Default population size for training.
- **Generations**: Default number of generations for training.

**Actions:**

- **Apply Changes**: Saves the new settings to the configuration.
- **Back**: Returns to the main menu.

*Note:* Enter valid numerical values to avoid input errors.

### Watch Best Genome Scene

Select genomes from a list to watch them play the game.

**Features:**

- **Genome List**: A scrollable list of genomes with their IDs and fitness scores.
- **Selectable Items**: Click on a genome item to select or deselect it.
- **Run Selected Genomes**: Starts the simulation for the selected genomes.

**Actions:**

- **Run Selected Genomes**: Executes the selected genomes in the game environment.
- **Back**: Returns to the main menu.

*Note:* The actual implementation of running and displaying genomes playing the game should be added to the `run_selected_genomes` method.

### Visualize Best Genome Scene

Visualize the neural network structure of a genome.

**Features:**

- **Input Field**: Specify which frame or genome to visualize.
- **Show Visualization**: Displays the neural network structure.

**Actions:**

- **Show Visualization**: Generates and displays the visualization.
- **Back**: Returns to the main menu.

*Note:* The visualization functionality should be implemented in the `visualize_genomes` method, integrating with the appropriate visualization tools.

## Modules and Classes

### `gui_with_pygame.py`

This script contains the main classes and functions for the GUI application.

#### Classes

- **Settings**
  - Manages configuration settings, such as FPS, screen size, colors, and fonts.
- **Game**
  - The core class that initializes Pygame, manages scenes, handles events, and runs the main loop.
- **Button**
  - Represents interactive buttons with hover and click effects.
- **InputField**
  - Allows user input through text fields.
- **TextDisplay**
  - Displays static or dynamic text on the screen.
- **SelectableListItem**
  - Represents an item in a selectable list (e.g., genomes).
- **GenomeViewer**
  - Manages a list of `SelectableListItem` objects, allowing users to select genomes.

#### Key Methods

- **event_handler**
  - Handles Pygame events such as mouse clicks and key presses.
- **update_screen**
  - Renders the current scene based on the `sc_selector` attribute.
- **tick**
  - Runs each frame: handles events, updates the screen, and maintains FPS.

### `Scene.py`

Contains the `Scene` class for managing different scenes within the GUI.

#### `Scene` Class

- **Attributes**
  - `scene_number`: Identifier for the scene.
  - `UI_elements`: List of UI elements in the scene.
  - `active`: Whether the scene is currently active.
  - `bg_color`: Background color of the scene.
- **Methods**
  - `add_UI_element(element)`: Adds a UI element to the scene.
  - `populate_UI()`: Draws all UI elements on the screen.
  - `change_active(is_active)`: Activates or deactivates the scene.
  - `update_screen()`: Updates the scene if it is active.

*Note:* This class is currently not integrated into the main `Game` class but may be utilized in future development.

## Note

- **Development Status**: The GUI is currently in development. Some features may not be fully implemented or functional.
- **Code Structure**: The `gui_with_pygame.py` script is currently located in the root folder but may be moved to the `GUI` folder in future updates.
- **Dependencies**: Ensure that all custom modules (e.g., `neat_test_file`, `src.utils.config`) are accessible and properly implemented.
- **Future Updates**: The GUI may undergo restructuring to improve modularity and integration with the rest of the project.

---

By utilizing the GUI application, you can interactively train and visualize neural networks using the NEAT algorithm in the context of the Super Mario Bros game. The interface allows for easy experimentation with different parameters and provides a foundation for further development and customization.
