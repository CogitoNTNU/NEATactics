from gui_with_pygame import Game

class Scene():
    def __init__(self, scene_number):
        self.scene_number = scene_number
        self.UI_elements = []
        self.active = 0
        self.bg_color = (0,0,0)


    def add_UI_element(self, element):
        self.UI_elements.append(element)

    def populate_UI(self):
        for i in self.UI_elements:
            i.draw(Game().screen)

    def change_ative(self, is_active):
        self.active = is_active

    def update_screen(self):
        if self.active:
            self.populate_UI