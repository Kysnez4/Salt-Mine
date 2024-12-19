from player import Player
from settings import *

class SceneManager:
    def __init__(self, screen):
        self.screen = screen
        self.scenes = {}
        self.current_scene = None
        self.player = None
        self.all_sprites = pygame.sprite.Group() # Manage all sprites centrally
        self.crystal_group = pygame.sprite.Group() # Group for crystals

    def add_scene(self, scene_name, scene):
        self.scenes[scene_name] = scene

    def set_scene(self, scene_name):
        if scene_name in self.scenes:
            if self.current_scene:
                self.current_scene.on_exit()

            self.current_scene = self.scenes[scene_name]
            if self.player:
                self.current_scene.on_enter(self.player)
            else:
                if scene_name != 'menu':
                  self.create_player(scene_name)

        else:
            print(f"Error: Scene '{scene_name}' not found.")

    def update(self, dt):
        if self.current_scene:
            self.current_scene.update(dt)
            self.all_sprites.update() # Update all sprites

    def draw(self):
        if self.current_scene:
            self.current_scene.draw(self.screen)
            self.all_sprites.draw(self.screen) # Draw all sprites

    def handle_input(self, event):
        if self.current_scene:
            self.current_scene.handle_input(event)

    def create_player(self, scene_name):
        self.player = Player(self, self.scenes[scene_name])
        self.all_sprites.add(self.player) # Add to central sprite group


#Example Scene Class
class Scene:
    def __init__(self):
        pass

    def on_enter(self):
        pass #Initialize scene elements

    def update(self,dt):
        pass  #Game logic for the scene

    def draw(self, screen):
        pass #Draw scene elements

    def handle_input(self, event):
        pass #Handle inputs for the scene

    def entrance_coords(self):
        # Set player starting position
        return (100, 100)