import pygame
import sys
import neat_test_file
import src.utils.config as conf

class Settings():
    def __init__(self):
        self.fps = 60
        self.default_x_size = 1000
        self.default_y_size = 500
        self.fullscreen = False
        self.fs_start_time = 0
        self.fs_is_pressed = False
        self.fs_delay = 20
        self.sc_selector = 0  # 0 = main, 1 = training, 2 = settings, etc.

        # Colors
        self.DARK_BLUE = (8, 19, 169)
        self.GREEN = (8, 166, 11)
        self.YELLOW = (255, 226, 10)
        self.LIGHT_BLUE = (173, 216, 230)
        self.WHITE = (255, 255, 255)
        self.GRAY = (200, 200, 200)

        # Button and font settings
        self.button_color = (100, 200, 255)
        self.hover_color = (150, 230, 255)
        self.pressed_color = (50, 150, 200)
        self.text_color = (255, 255, 255)
        self.input_field_bg = (58,100,30)
        self.input_field_active_bg = (78, 100, 30)
        pygame.font.init()
        self.font = pygame.font.Font(None, 36)

class SelectableListItem:
    """Represents a genome item that can be selected."""
    def __init__(self, x, y, width, height, genome_id, fitness, font, text_color, bg_color, selected_color):
        self.rect = pygame.Rect(x, y, width, height)
        self.genome_id = genome_id
        self.fitness = fitness
        self.font = font
        self.text_color = text_color
        self.bg_color = bg_color
        self.selected_color = selected_color
        self.selected = False

    def draw(self, screen):
        # Draw background based on whether it's selected
        color = self.selected_color if self.selected else self.bg_color
        pygame.draw.rect(screen, color, self.rect)

        # Display genome info
        text = f"ID: {self.genome_id}, Fitness: {self.fitness}"
        text_surface = self.font.render(text, True, self.text_color)
        screen.blit(text_surface, (self.rect.x + 10, self.rect.y + 10))

    def handle_event(self, event):
        # Toggle selection when clicked
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and self.rect.collidepoint(event.pos):
                self.selected = not self.selected


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
        for genome in self.genomes:
            genome_id = genome['id']
            fitness = genome['fitness']
            item = SelectableListItem(100, y_position, 400, 50, genome_id, fitness, self.font, self.text_color, self.bg_color, self.selected_color)
            self.items.append(item)
            y_position += 60

    def draw(self, screen):
        for item in self.items:
            item.draw(screen)

    def handle_event(self, event):
        for item in self.items:
            item.handle_event(event)

    def get_selected_genomes(self):
        # Return a list of selected genome IDs
        return [item.genome_id for item in self.items if item.selected]


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

        # Main menu buttons
        self.main_menu_buttons = [
            Button(140, 100, 200, 100, "Train!", st.font, st.text_color, st.button_color, st.hover_color, st.pressed_color, self.train_scene),
            Button(460, 100, 200, 100, "Settings", st.font, st.text_color, st.button_color, st.hover_color, st.pressed_color, self.settings_scene),
            Button(140, 250, 200, 100, "Watch best gene", st.font, st.text_color, st.button_color, st.hover_color, st.pressed_color, self.watch_gene_scene),
            Button(460, 250, 200, 100, "Visualize best genome", st.font, st.text_color, st.button_color, st.hover_color, st.pressed_color, self.visualize_action),
            TextDisplay(300, 30, "Neat Tactics!", st.font, st.text_color, bg_color=st.DARK_BLUE)
        ]

        # Training scene UI elements
        self.training_input_fields= [InputField(140, 100, 200, 50, st.font, st.text_color, initial_text="Population size"),
                           InputField(140, 170, 200, 50, st.font, st.text_color, initial_text="Mutation rate"),
                           InputField(140, 240, 200, 50, st.font, st.text_color, initial_text="Generations")]
        self.training_UI = [
                           Button(460, 170, 200, 50, "Start Training", st.font, st.text_color, st.button_color, st.hover_color, st.pressed_color, self.start_training),
                           Button(460, 300, 200, 50, "Back to Menu", st.font, st.text_color, st.button_color, st.hover_color, st.pressed_color, self.main_menu_scene)]

        # Settings scene
        self.settings_input_fields = [
            InputField(200, 50, 200, 30, st.font, st.text_color, st.input_field_bg, st.input_field_active_bg, str(self.config.c1)),
            InputField(200, 100, 200, 30, st.font, st.text_color, st.input_field_bg, st.input_field_active_bg, str(self.config.c2)),
            InputField(200, 150, 200, 30, st.font, st.text_color, st.input_field_bg, st.input_field_active_bg, str(self.config.c3)),
            InputField(200, 200, 200, 30, st.font, st.text_color, st.input_field_bg, st.input_field_active_bg, str(self.config.genomic_distance_threshold)),
            InputField(200, 250, 200, 30, st.font, st.text_color, st.input_field_bg, st.input_field_active_bg, str(self.config.population_size)),
            InputField(200, 300, 200, 30, st.font, st.text_color, st.input_field_bg, st.input_field_active_bg, str(self.config.generations))
        ]

        
        self.apply_button = Button(200, 350, 200, 50, "Apply Changes", st.font, st.text_color, st.button_color, st.hover_color, st.pressed_color, self.apply_changes)
        self.settings_back_button = Button(200, 450, 200, 50, "Back", st.font, st.text_color, st.button_color, st.hover_color, st.pressed_color, self.main_menu_scene)
        
        self.input_titles = [
            TextDisplay(50, 50, "c1:", st.font, st.text_color),
            TextDisplay(50, 100, "c2:", st.font, st.text_color),
            TextDisplay(50, 150, "c3:", st.font, st.text_color),
            TextDisplay(50, 200, "Genomic Distance Threshold:", st.font, st.text_color),
            TextDisplay(50, 250, "Population Size:", st.font, st.text_color),
            TextDisplay(50, 300, "Generations:", st.font, st.text_color)
        ]

        # watching genomes
        self.genomes = [
            {"id": 1, "fitness": 1.2},
            {"id": 2, "fitness": 3.4},
            {"id": 3, "fitness": 2.8},
            {"id": 4, "fitness": 4.1},
            {"id": 5, "fitness": 1.5},
        ]

        # Genome viewer
        self.genome_viewer = GenomeViewer(self.genomes, st.font, st.text_color, st.input_field_bg, st.input_field_active_bg)

        # Run button
        self.run_button = Button(600, 350, 200, 50, "Run Selected Genomes", st.font, st.text_color, st.button_color, st.hover_color, st.pressed_color, self.run_selected_genomes)




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


    def train_scene(self):
        st.sc_selector = 1

    def main_menu_scene(self):
        st.sc_selector = 0
 
    def settings_scene(self):
        st.sc_selector = 2
    
    def watch_gene_scene(self):
        st.sc_selector = 3


    def visualize_action(self):
        print("Visualizing genome...")
    
    def run_selected_genomes(self):
        # Get the selected genome IDs and run them
        selected_genomes = self.genome_viewer.get_selected_genomes()
        print(f"Running genomes: {selected_genomes}")
        # Add logic here to execute the selected genomes (e.g., visualize, simulate, etc.)
    
    def watch_genome_scene(self):
        self.screen.fill(st.DARK_BLUE)

        # Draw the genome viewer list
        self.genome_viewer.draw(self.screen)

        # Draw the run button
        self.run_button.draw(self.screen)




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
        population = self.population_field.text
        mutation_rate = self.mutation_field.text
        generations = self.generation_field.text
        print(f"Starting training with Population: {population}, Mutation Rate: {mutation_rate}, Generations: {generations}")
        # Insert your training code here (e.g. NEAT training)
        neat_test_file.main()
    

    def draw_settings_scene(self):
        self.screen.fill(st.DARK_BLUE)

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
            self.screen.fill(st.LIGHT_BLUE)
            for button in self.main_menu_buttons:
                button.draw(self.screen)
        elif st.sc_selector == 1:
            # Train scene
            self.screen.fill(st.LIGHT_BLUE)

            for element in self.training_input_fields:
                element.draw(self.screen)
            for element in self.training_UI:
                element.draw(self.screen)
        elif st.sc_selector == 2:
            self.draw_settings_scene()
        elif st.sc_selector == 3:
            self.watch_genome_scene()

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
