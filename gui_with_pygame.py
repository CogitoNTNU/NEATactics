import pygame
import pygame.display
import sys
import neat_test_file

class Settings():
    def __init__(self):
        # Settings for the game
        self.fps = 60
        self.default_x_size = 1000
        self.default_y_size = 500
        self.fullscreen = False

        # timers info
        self.fs_start_time = 0
        self.fs_is_pressed = False
        self.fs_delay = 20

        # Different scenes
        """
        0 = main
        1 = settings
        2 = level selector
        10 - 99 = levels
        """
        self.sc_selector = 0

        # Colors
        self.DARK_BLUE = (8, 19, 169)
        self.GREEN = (8, 166, 11)
        self.YELLOW = (255, 226, 10)

        # Button
        self.button_color = (100, 200, 255)
        self.hover_color = (150, 230, 255)
        self.pressed_color = (50, 150, 200)
        self.text_color = (255, 255, 255)
        pygame.font.init()
        self.font = pygame.font.Font(None, 36)



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
                pygame.draw.rect(screen, self.pressed_color, self.rect)  # Change color when pressed
                self.pressed = True
            else:
                pygame.draw.rect(screen, self.hover_color, self.rect)  # Change color when hovered
                if self.pressed:  # If released after being pressed, trigger the action
                    if self.action is not None:
                        self.action()  # Call the given function
                    self.pressed = False
        else:
            pygame.draw.rect(screen, self.button_color, self.rect)  # Normal state

        # Render the text on the button
        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and self.rect.collidepoint(event.pos):  # If left-clicked inside the button
                if self.action:
                    self.action()

class Game():
    def __init__(self):
        pygame.init()

        # Pygame stuff
        self.monitor_size = [pygame.display.Info().current_w, pygame.display.Info().current_h]
        self.screen = pygame.display.set_mode((st.default_x_size, st.default_y_size), pygame.RESIZABLE)
        pygame.display.set_caption("Arrow Game")

        # timer stuff
        self.clock = pygame.time.Clock()
        self.frame = 0



    def event_handler(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.VIDEORESIZE:
                if not st.fullscreen:
                    self.screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
                    st.default_x_size = self.screen.get_width()
                    st.default_y_size = self.screen.get_height()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and self.button1.rect.collidepoint(event.pos):  # If left-clicked inside the button
                    if self.button1.action:
                        self.button1.action()


    def check_keys(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            pygame.quit()
            sys.exit()
        if keys[pygame.K_f]:
            self.toggle_fullscreen()
        if keys[pygame.K_PLUS]:
            st.sc_selector += 1
        if keys[pygame.K_MINUS]:
            st.sc_selector -= 1

    def toggle_fullscreen(self):
        if st.fs_is_pressed == False:
            st.fs_start_time = self.frame
            st.fullscreen = not st.fullscreen
            if st.fullscreen:
                self.screen = pygame.display.set_mode(self.monitor_size, pygame.FULLSCREEN)
            else:
                self.screen = pygame.display.set_mode((st.default_x_size, st.default_y_size),
                                                      pygame.RESIZABLE)
        st.fs_is_pressed = True
        if self.frame - st.fs_start_time > st.fs_delay:
            st.fs_is_pressed = False

    def update_screen(self):
        if st.sc_selector == 0:
            self.screen.fill(st.DARK_BLUE)
            self.button1 = Button(140, 100, 200,100,"Hei", st.font, st.text_color, st.button_color, st.hover_color, st.pressed_color, neat_test_file.main)
            self.button1.draw(screen=self.screen)
            
            print("main menu scene")
        elif st.sc_selector == 1:
            self.screen.fill(st.GREEN)
            print("settings scene")
        elif st.sc_selector == 2:
            self.screen.fill(st.YELLOW)
            print("level selector scene")


        pygame.display.flip()



    def tick(self):
        self.event_handler()
        self.check_keys()
        self.update_screen()
        

        self.frame += 1
        self.clock.tick(st.fps)

    def gameplay(self):
        pass
        # TODO Add gameplay


st = Settings()
def main():
    game = Game()
    
    while True:
        game.tick()

if __name__ == "__main__":
    main()