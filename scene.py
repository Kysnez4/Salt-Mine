class SceneManager:
    def __init__(self, screen):
        self.screen = screen
        self.scenes = {}  # Dictionary to store scenes: {scene_name: Scene object}
        self.current_scene = None  # Currently active scene

    def add_scene(self, scene_name, scene_object):
        self.scenes[scene_name] = scene_object

    def set_scene(self, scene_name):
        if scene_name in self.scenes:
            self.current_scene = self.scenes[scene_name]
            self.current_scene.on_enter() #Optional: Call on_enter method for scene setup
        else:
            print(f"Error: Scene '{scene_name}' not found.")

    def update(self, dt):
        if self.current_scene:
            self.current_scene.update(dt)

    def draw(self):
        if self.current_scene:
            self.current_scene.draw(self.screen)

    def handle_input(self, event):
        if self.current_scene:
            self.current_scene.handle_input(event)


#Example Scene Class
class Scene:
    def __init__(self):
        pass #Add scene-specific initialization

    def on_enter(self):
        pass #Initialize scene elements

    def update(self,dt):
        pass  #Game logic for the scene

    def draw(self, screen):
        pass #Draw scene elements

    def handle_input(self, event):
        pass #Handle inputs for the scene