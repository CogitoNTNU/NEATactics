import pygame.image
import main as neat_test_file
import pygame
import sys
import threading
import os
import argparse

import src.utils.config as conf
import pickle
import src.utils.utils as util



class GenomeManager:
    def __init__(self, folder_path):
        """
        Initialize the GenomeManager to load genome objects from a folder.
        
        :param folder_path: Path to the folder containing the genome files.
        """
        self.folder_path = folder_path
        self.genomes = []

    def load_genomes(self):
        """
        Load all genome objects from the specified folder.
        """
        for filename in os.listdir(self.folder_path):
            file_path = os.path.join(self.folder_path, filename)
            
            # Open and load the genome object using pickle
            with open(file_path, 'rb') as file:
                genome_object = pickle.load(file)

                # Append the loaded genome object to the list
                self.genomes.append((genome_object, int(str(file_path).split("_")[-1][:-4])))

    def get_genomes(self):
        """
        Returns the list of loaded genome objects.
        """
        return self.genomes

class Settings():
    def __init__(self):
        self.fps = 60
        self.default_x_size = 2560
        self.default_y_size = 1600
        self.fullscreen = False
        self.fs_start_time = 0
        self.fs_is_pressed = False
        self.fs_delay = 20
        self.sc_selector = 0  # 0 = main, 1 = training, 2 = settings, etc.

        # Colors
        self.DARK_BLUE = (0x13, 0x39, 0x5B)
        self.LIGHT_BLUE = (0x30, 0xB3, 0xEC)
        self.WHITE = (0xFF, 0xFF, 0xFF)
        self.ORANGE = (0xFF, 0x63, 0x48)
        self.RED = (0xFF, 0x47, 0x57)
        self.BLUE = (0x1E, 0x90, 0xFF)

        # Button and font settings
        self.background_color = self.DARK_BLUE
        self.button_color = self.BLUE
        self.hover_color = self.LIGHT_BLUE
        self.pressed_color = self.DARK_BLUE
        self.text_color = self.WHITE
        self.input_field_bg = self.ORANGE
        self.input_field_active_bg = self.RED
        pygame.font.init()
        self.normal_font = pygame.font.Font(None, 36)
        self.big_font = pygame.font.Font(None, 72)


class SelectableListItem:
    """Represents a genome item that can be selected, with a checkbox."""
    def __init__(self, x, y, width, height, genome_id, fitness, font, text_color, bg_color, selected_color, checkbox_size=20):
        self.rect = pygame.Rect(x, y, width, height)
        self.id = genome_id
        self.fitness = fitness
        self.font = font
        self.text_color = text_color
        self.bg_color = bg_color
        self.selected_color = selected_color
        self.selected = False
        self.checkbox_size = checkbox_size
        self.checkbox_rect = pygame.Rect(x + width - checkbox_size - 10, y + (height - checkbox_size) // 2, checkbox_size, checkbox_size)

    def draw(self, screen):
        # Draw background based on whether it's selected
        color = self.selected_color if self.selected else self.bg_color
        pygame.draw.rect(screen, color, self.rect)

        # Draw checkbox
        pygame.draw.rect(screen, (255, 255, 255), self.checkbox_rect, 2)  # Checkbox border
        if self.selected:
            pygame.draw.rect(screen, (0, 255, 0), self.checkbox_rect.inflate(-4, -4))  # Filled when selected

        # Display genome info
        text = f"Generation: {self.id}, Fitness: {round(self.fitness)}"
        text_surface = self.font.render(text, True, self.text_color)
        screen.blit(text_surface, (self.rect.x + 10, self.rect.y + 10))

    def handle_event(self, event):
        # Toggle selection when clicked
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and self.rect.collidepoint(event.pos):
                self.selected = not self.selected


class ScrollableList:
    def __init__(self, x, y, width, height, items, font, text_color, bg_color, selected_color, visible_count=10, padding=10):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.items = items
        self.font = font
        self.text_color = text_color
        self.bg_color = bg_color
        self.selected_color = selected_color
        self.visible_count = visible_count
        self.scroll_offset = 0  # This tracks where we are in the list
        self.padding = padding  # Distance between items
        # Create a base list of items without positioning them

        self.list_items = [
            SelectableListItem(
                x, y, width, (height - (visible_count - 1) * padding) // visible_count,  # Adjust height to account for padding
                genome_id=item[1], fitness=item[0].fitness_value, font=font, text_color=text_color, 
                bg_color=bg_color, selected_color=selected_color
            ) for item in self.items
        ]

    def draw(self, screen):
        # Draw only the visible items, adjusting their position based on scroll_offset and adding padding
        for i in range(self.scroll_offset, min(self.scroll_offset + self.visible_count, len(self.list_items))):
            list_item = self.list_items[i]
            # Adjust y position with padding
            list_item.rect.y = self.y + (i - self.scroll_offset) * (list_item.rect.height + self.padding)
            list_item.checkbox_rect.y = list_item.rect.y + (list_item.rect.height - list_item.checkbox_size) // 2
            list_item.draw(screen)

    def scroll(self, direction):
        # Scroll up (scroll_offset decreases)
        if direction == "up" and self.scroll_offset > 0:
            self.scroll_offset -= 1
        # Scroll down (scroll_offset increases)
        elif direction == "down" and self.scroll_offset < len(self.list_items) - self.visible_count:
            self.scroll_offset += 1

    def handle_event(self, event):
        # Pass the event to all visible list items
        for i in range(self.scroll_offset, min(self.scroll_offset + self.visible_count, len(self.list_items))):
            list_item = self.list_items[i]
            list_item.handle_event(event)

        # Handle scrolling with arrow keys
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.scroll("up")
            elif event.key == pygame.K_DOWN:
                self.scroll("down")
        
        # Handle scrolling with mouse wheel
        if event.type == pygame.MOUSEWHEEL:
            if event.y > 0:
                self.scroll("up")
            elif event.y < 0:
                self.scroll("down")
    

    def get_selected_genomes(self):
        # Return a list of selected genome IDs
        print(f"Item: {self.items[0]}")
        return [item[1] for item in self.items if item[0].selected]


class GenomeViewer:
    def __init__(self, genomes, font, text_color, bg_color, selected_color):
        self.genomes = genomes
        self.items = []
        self.font = font
        self.text_color = text_color
        self.bg_color = bg_color
        self.selected_color = selected_color

        # Populate the list with genome items
        self.populate_genomes()

    def populate_genomes(self):
        self.items.clear()
        y_position = 50
        for genome, file_path in self.genomes:
            genome_generation = file_path
            fitness = genome.fitness_value
            item = SelectableListItem(100, y_position, 400, 50, genome_generation, fitness, self.font, self.text_color, self.bg_color, self.selected_color)
            self.items.append((item, file_path))
            y_position += 60

    def draw(self, screen):
        for item in self.items:
            item = item[0]
            item.draw(screen)

    def handle_event(self, event):
        for item in self.items:
            item = item[0]
            item.handle_event(event)

    def get_selected_genomes(self):
        # Return a list of selected genome IDs
        return [item[1] for item in self.items if item[0].selected]


class Button:
    def __init__(self, x, y, width, height, text, font, text_color, button_color, hover_color, pressed_color, action=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = font
        self.text_color = text_color
        self.button_color = button_color
        self.hover_color = hover_color
        self.pressed_color = pressed_color
        self.action = action
        self.pressed = False

    def draw(self, screen):
        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()[0]

        # Check if the mouse is over the button
        if self.rect.collidepoint(mouse_pos):
            if mouse_pressed:
                pygame.draw.rect(screen, self.pressed_color, self.rect, border_radius=10)  # Pressed
                self.pressed = True
            else:
                pygame.draw.rect(screen, self.hover_color, self.rect, border_radius=10)  # Hover
                if self.pressed:  # Released
                    if self.action is not None:
                        self.action()  # Call action
                    self.pressed = False
        else:
            pygame.draw.rect(screen, self.button_color, self.rect, border_radius=10)  # Normal

        # Render the text
        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)


class InputField:
    def __init__(self, x, y, width, height, font, text_color, input_field_bg=None, input_field_active_bg=None, initial_text=""):
        self.rect = pygame.Rect(x, y, width, height)
        self.font = font
        self.text_color = text_color
        self.text = initial_text
        self.active = False
        self.color_inactive = (200, 200, 200)
        self.color_active = (255, 255, 255)
        self.color = self.color_inactive
        self.bg_color = input_field_bg
        self.active_bg = input_field_active_bg

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Toggle the active state if clicked on the input box
            if self.rect.collidepoint(event.pos):
                self.active = not self.active
            else:
                self.active = False
            self.color = self.color_active if self.active else self.color_inactive

        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    print(self.text)
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect, 2)        
        if self.bg_color is not None:
            pygame.draw.rect(screen, self.bg_color, self.rect)
        text_surface = self.font.render(self.text, True, self.text_color)
        screen.blit(text_surface, (self.rect.x+5, self.rect.y+5))



class TextDisplay:
    def __init__(self, x, y, text, font, text_color, bg_color=None, center=False):
        self.x = x
        self.y = y
        self.text = text
        self.font = font
        self.text_color = text_color
        self.bg_color = bg_color  # Background color, if specified
        self.center = center  # Center the text if needed
        self.population_field = None
        self.mutation_field = None
        self.generation_field = None

    def draw(self, screen):
        # Render the text
        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect()

        # Center text if necessary
        if self.center:
            text_rect.center = (self.x, self.y)
        else:
            text_rect.topleft = (self.x, self.y)

        # Draw the background rectangle if a background color is specified
        if self.bg_color is not None:
            pygame.draw.rect(screen, self.bg_color, text_rect)

        # Blit the text surface to the screen
        screen.blit(text_surface, text_rect)


class ImageSprite:
    def __init__(self, image_path, position=(0, 0), scale=None):
        """
        Initializes the ImageSprite object.
        
        :param image_path: Path to the image file.
        :param position: A tuple (x, y) representing the top-left corner of the image.
        :param scale: A tuple (width, height) to scale the image. If None, the image is used at its original size.
        """
        self.image_path = image_path
        self.position = position
        self.scale = scale

        # Load the image
        self.image = pygame.image.load(self.image_path)
        
        # If scaling is specified, scale the image
        if self.scale:
            self.image = pygame.transform.scale(self.image, self.scale)
        
        # Get the image rect for easier position management
        self.rect = self.image.get_rect(topleft=self.position)
    
    def set_position(self, new_position):
        """
        Set a new position for the image sprite.
        """
        self.position = new_position
        self.rect.topleft = self.position
    
    def draw(self, surface):
        """
        Draw the image sprite onto the provided surface.
        
        :param surface: The pygame surface to draw the image on.
        """
        surface.blit(self.image, self.rect)





class Game():
    def __init__(self):
        self.config= conf.Config()
        pygame.init()

        # Pygame screen setup
        self.monitor_size = [pygame.display.Info().current_w, pygame.display.Info().current_h]
        self.screen = pygame.display.set_mode((st.default_x_size, st.default_y_size), pygame.RESIZABLE)
        pygame.display.set_caption("Neat Tactics")

        # timer
        self.clock = pygame.time.Clock()
        self.frame = 0

        # Threading
        self.is_processing = False
        self.process_thread = None

        # Main menu buttons
        self.main_menu_buttons = [
            Button(140, 100, 200, 100, "Train!", st.normal_font, st.text_color, st.button_color, st.hover_color, st.pressed_color, self.train_scene),
            Button(460, 100, 200, 100, "Settings", st.normal_font, st.text_color, st.button_color, st.hover_color, st.pressed_color, self.settings_scene),
            Button(140, 250, 200, 100, "Watch best gene", st.normal_font, st.text_color, st.button_color, st.hover_color, st.pressed_color, self.watch_gene_scene),
            Button(460, 250, 200, 100, "Visualize best genome", st.normal_font, st.text_color, st.button_color, st.hover_color, st.pressed_color, self.visualize_genome_scene),
            TextDisplay(300, 30, "Neat Tactics!", st.big_font, st.DARK_BLUE, bg_color=st.LIGHT_BLUE)
        ]

        # Training scene UI elements
        self.training_input_fields= [InputField(140, 100, 200, 50, st.normal_font, st.text_color, initial_text="Population size"),
                           InputField(140, 170, 200, 50, st.normal_font, st.text_color, initial_text="Mutation rate"),
                           InputField(140, 240, 200, 50, st.normal_font, st.text_color, initial_text="Generations")]
        self.training_UI = [
                           Button(460, 170, 200, 50, "Start Training", st.normal_font, st.text_color, st.button_color, st.hover_color, st.pressed_color, self.start_training_process),
                           Button(460, 300, 200, 50, "Back to Menu", st.normal_font, st.text_color, st.button_color, st.hover_color, st.pressed_color, self.main_menu_scene)]
        try:
            self.fitness_graph = ImageSprite("data/latest/fitness/fitness_plot.png", (700, 100))
        except:
            print("ERROR: Could not find image path")
            self.fitness_graph = ImageSprite("data/genome_frames/genome_0.png", (700, 100))


        

        # Settings scene
        self.settings_input_fields = [
            InputField(200, 50, 200, 30, st.normal_font, st.text_color, st.input_field_bg, st.input_field_active_bg, str(self.config.c1)),
            InputField(200, 100, 200, 30, st.normal_font, st.text_color, st.input_field_bg, st.input_field_active_bg, str(self.config.c2)),
            InputField(200, 150, 200, 30, st.normal_font, st.text_color, st.input_field_bg, st.input_field_active_bg, str(self.config.c3)),
            InputField(200, 200, 200, 30, st.normal_font, st.text_color, st.input_field_bg, st.input_field_active_bg, str(self.config.genomic_distance_threshold)),
            InputField(200, 250, 200, 30, st.normal_font, st.text_color, st.input_field_bg, st.input_field_active_bg, str(self.config.population_size)),
            InputField(200, 300, 200, 30, st.normal_font, st.text_color, st.input_field_bg, st.input_field_active_bg, str(self.config.generations))
        ]

        
        self.apply_button = Button(200, 350, 200, 50, "Apply Changes", st.normal_font, st.text_color, st.button_color, st.hover_color, st.pressed_color, self.apply_changes)
        self.settings_back_button = Button(200, 450, 200, 50, "Back", st.normal_font, st.text_color, st.button_color, st.hover_color, st.pressed_color, self.main_menu_scene)
        
        self.input_titles = [
            TextDisplay(50, 50, "c1:", st.normal_font, st.text_color),
            TextDisplay(50, 100, "c2:", st.normal_font, st.text_color),
            TextDisplay(50, 150, "c3:", st.normal_font, st.text_color),
            TextDisplay(50, 200, "Genomic Distance Threshold:", st.normal_font, st.text_color),
            TextDisplay(50, 250, "Population Size:", st.normal_font, st.text_color),
            TextDisplay(50, 300, "Generations:", st.normal_font, st.text_color)
        ]


        genome_folder = 'data/latest/good_genomes'
        genome_manager = GenomeManager(genome_folder)

        # Load all genome objects from the folder
        genome_manager.load_genomes()

        # Get the list of loaded genome objects
        loaded_genomes = genome_manager.get_genomes()

        self.genomes = []
        # Use the loaded genome objects (printing as an example)
        for genome in loaded_genomes:
            self.genomes.append(genome)
            print(genome)

        ## Genome viewer
        self.genome_viewer = GenomeViewer(self.genomes, st.normal_font, st.text_color, st.input_field_bg, st.input_field_active_bg)

        self.watch_genes_visualize = ImageSprite("data/genome_frames/genome_0.png", (600, 100), (600, 400))

        ## Run button
        self.run_button = Button(600, 20, 200, 50, "Run Selected Genomes", st.normal_font, st.text_color, st.button_color, st.hover_color, st.pressed_color, self.run_selected_genomes)
        self.watch_back_button = Button(600, 600, 200, 50, "Back", st.normal_font, st.text_color, st.button_color, st.hover_color, st.pressed_color, self.main_menu_scene)

        #Visualize best genome
        self.visualize_back_button = Button(50, 50, 150, 50, "Back", st.normal_font, st.text_color, st.button_color, st.hover_color, st.pressed_color, self.main_menu_scene)
        self.show_visualization_button = Button(100, 350, 200, 50, "Show Visualization", st.normal_font, st.text_color, st.button_color, st.hover_color, st.pressed_color, self.visualize_genomes)
        self.get_which_frames_to_show_input = InputField(400, 350, 150, 50, st.normal_font, st.text_color, st.input_field_bg, st.input_field_active_bg, initial_text="0")

        self.scrollable_list = ScrollableList(50, 50, 500, 500, self.genomes, st.normal_font, st.text_color, st.button_color, st.hover_color, visible_count=10, padding=10)

        self.logo_sprite = ImageSprite("docs/images/logo light blue name white.png", (50, 450), (200, 200))

    def event_handler(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if st.sc_selector == 1:  # Train scene
                for input_field in self.training_input_fields:
                    input_field.handle_event(event)
            if st.sc_selector == 2:
                for input_field in self.settings_input_fields:
                    input_field.handle_event(event)
            if st.sc_selector == 3:
                self.genome_viewer.handle_event(event)
                self.scrollable_list.handle_event(event)
            if st.sc_selector == 4:
                self.get_which_frames_to_show_input.handle_event(event)


    def visualize_genomes(self):
        print("visualizing genomes...")

    def main_menu_scene(self):
        st.sc_selector = 0

    def train_scene(self):
        st.sc_selector = 1

    def settings_scene(self):
        st.sc_selector = 2
    
    def watch_gene_scene(self):
        st.sc_selector = 3

    def visualize_genome_scene(self):
        st.sc_selector = 4
    
    def run_selected_genomes(self):
        # Get the selected genome IDs and run them
        selected_genomes = self.scrollable_list.get_selected_genomes()
        
        print(f"Running genomes: {selected_genomes}")
        # Add logic here to execute the selected genomes (e.g., visualize, simulate, etc.)
        for i in selected_genomes:
            from_gen = i
            to_gen = i
            neat_test_file.test_genome(from_gen, to_gen, "")


    def watch_genome_scene(self):
        self.screen.fill(st.background_color)

        # Draw the genome viewer list
        self.genome_viewer.draw(self.screen)
        self.scrollable_list.draw(self.screen)

        # Draw the buttons
        self.run_button.draw(self.screen)
        self.watch_back_button.draw(self.screen)

        # Visualize while watching
        
        self.watch_genes_visualize.draw(self.screen)

    def start_watching_process(self):
        """Start a long-running process in a separate thread."""
        if not self.is_processing:
            self.process_thread = threading.Thread(target=self.watching_process)
            self.process_thread.start()
    
    def start_training_process(self):
        """Start a long-running process in a separate thread."""
        if not self.is_processing:
            self.process_thread = threading.Thread(target=self.training_process)
            self.process_thread.start()
    
    def watching_process(self):
        """Simulate a long-running process that takes time."""
        self.is_processing = True
        self.run_selected_genomes()  # Simulate a process that takes 5 seconds
        print("Long process completed")
        self.is_processing = False

    def training_process(self):
        """Simulate a long-running process that takes time."""
        self.is_processing = True
        self.start_training()  # Simulate a process that takes 5 seconds
        print("Long process completed")
        self.is_processing = False




    def draw_visualize_genome_scene(self):
        """Draw the 'Visualize Best Genome' scene."""
        self.screen.fill(st.background_color)

        # Draw the back button
        self.visualize_back_button.draw(self.screen)

        # Draw the show visualization button
        self.show_visualization_button.draw(self.screen)

        # Draw the input field for the frame selection
        self.get_which_frames_to_show_input.draw(self.screen)


    def apply_changes(self):
        # Try to apply changes from input fields to config
        try:
            self.config.c1 = float(self.settings_input_fields[0].text)
            self.config.c2 = float(self.settings_input_fields[1].text)
            self.config.c3 = float(self.settings_input_fields[2].text)
            self.config.genomic_distance_threshold = float(self.settings_input_fields[3].text)
            self.config.population_size = int(self.settings_input_fields[4].text)
            self.config.generations = int(self.settings_input_fields[5].text)
            print("Settings applied successfully!")
        except ValueError:
            print("Invalid input! Please enter valid numbers.")

    def start_training(self):
        population = self.training_input_fields[0].text
        mutation_rate = self.training_input_fields[1].text
        generations = self.training_input_fields[2].text
        print(f"Starting training with Population: {population}, Mutation Rate: {mutation_rate}, Generations: {generations}")
        # Insert your training code here (e.g. NEAT training)


        parser = argparse.ArgumentParser(description="Train or Test Genomes")
        subparsers = parser.add_subparsers(dest="command", help="Choose 'train', 'test', 'graph', or 'play'")
    
        # Train command (runs main())
        train_parser = subparsers.add_parser('train', help="Run the training process")
        train_parser.add_argument('-n', '--neat_name', type=str, default='', help="The name of the NEAT object to load from 'trained_population/'")
        train_parser.add_argument('-g', '--n_generations', type=int, default=-1, help="The number of generations to train for")
        
        sim_args = ["train", "-g", generations]
        args=parser.parse_args(sim_args)

        neat_test_file.main(args=args)
    

    def draw_settings_scene(self):
        self.screen.fill(st.background_color)

        # Draw titles and input fields
        for title in self.input_titles:
            title.draw(self.screen)
        for input_field in self.settings_input_fields:
            input_field.draw(self.screen)

        # Draw the Apply Changes button
        self.apply_button.draw(self.screen)
        self.settings_back_button.draw(self.screen)


    def update_screen(self):
        if st.sc_selector == 0:
            # Main menu scene
            self.screen.fill(st.background_color)
            for button in self.main_menu_buttons:
                button.draw(self.screen)
        elif st.sc_selector == 1:
            # Train scene
            self.screen.fill(st.background_color)

            for element in self.training_input_fields:
                element.draw(self.screen)
            for element in self.training_UI:
                element.draw(self.screen)
            
            try:
                self.fitness_graph = ImageSprite("data/latest/fitness/fitness_plot.png", (700, 100))
            except:
                pass
            self.fitness_graph.draw(self.screen)
            

        elif st.sc_selector == 2:
            self.draw_settings_scene()
        elif st.sc_selector == 3:
            self.watch_genome_scene()
        elif st.sc_selector == 4:
            self.draw_visualize_genome_scene()
        
        self.logo_sprite.draw(self.screen)

        pygame.display.flip()

    def tick(self):
        self.event_handler()
        self.update_screen()
        self.clock.tick(st.fps)


st = Settings()

def main():
    game = Game()

    while True:
        game.tick()

if __name__ == "__main__":
    main()
