from scene import Scene
from settings import *

class MenuScene(Scene):
    def __init__(self, scene_manager):
        super().__init__()
        self.scene_manager = scene_manager  # Keep a reference to the scene manager
        self.font = pygame.font.Font(None, 36)  # Default font for menu text
        self.buttons = self.create_buttons()
        self.image = loadim("Фон меню.png")
        self.background_image = pygame.transform.scale( self.image , (800,800))



    def create_buttons(self):
        button_width = 200
        button_height = 50
        button_spacing = 20

        new_game_button = Button(300, 400, button_width, button_height, "New Game", self.start_new_game)
        continue_button = Button(300, 400 + button_height + button_spacing, button_width, button_height, "Continue",
                                 self.continue_game)
        exit_button = Button(300, 400 + 2 * (button_height + button_spacing), button_width, button_height, "Exit",
                             self.exit_game)
        return [new_game_button, continue_button, exit_button]

    def draw(self, screen):
        screen.blit(self.background_image, (0, 0))  # Draw background image

        for button in self.buttons:
            button.draw(screen)

        title_text = self.font.render("Salt Mine", True, (255, 255, 255))
        title_rect = title_text.get_rect(center=(screen.get_width() // 2, 100))
        screen.blit(title_text, title_rect)

    def handle_input(self, event):
        for button in self.buttons:
            button.handle_event(event)

    def start_new_game(self):
        # Initialize game data, create game objects, etc.
        # Example:
        self.scene_manager.set_scene("game")

    def continue_game(self):
        # Load game data from save file
        self.scene_manager.set_scene("game")  # Replace with your game scene loading logic

    def exit_game(self):
        pygame.quit()
        quit()

    def on_enter(self):
        pass  # You could add some initializations if needed here

    def on_exit(self):
        pass


# Example button class (you might already have one defined)
class Button:
    def __init__(self, x, y, width, height, text, onclick_function, color=(255, 255, 255), text_color=(0, 0, 0)):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.onclick_function = onclick_function
        self.color = color
        self.text_color = text_color
        self.font = pygame.font.Font(None, 36)  # Default menu font
        self.hovering = False

    def draw(self, screen):
        color = (150, 150, 150) if self.hovering else self.color  # Hover effect
        pygame.draw.rect(screen, color, self.rect)
        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.hovering = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.onclick_function()