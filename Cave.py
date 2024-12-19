import random
from player import Player
from scene import Scene



class CaveScene(Scene): #Inherits from Scene class
    def __init__(self, screen, scene_manager, tile_size=32, tile_images=None, num_levels=60):
        super().__init__()
        self.screen = screen
        self.scene_manager = scene_manager
        self.tile_size = tile_size
        self.tile_images = tile_images
        self.num_levels = num_levels
        self.current_level = 1
        self.unusable_tile = "wall"
        self.map_data = []  # Initialize map data
        self.player = Player(self, self.screen) # Initialize player object (add it when loading the scene)
        self.generate_level()

    def generate_level(self):
        # Adjust dimensions as needed:
        width = 20
        height = 15

        # Generate the map data for this level.  Replace with your room generation logic.
        self.map_data = [["grass"] * width for _ in range(height)] #Initial grass floor
        self.generate_walls()
        self.generate_cobblestones(20) # Generate 20 cobblestones.

        #Set player starting position
        self.player.x, self.player.y = self.tile_size, self.tile_size

    def generate_walls(self):
        width = len(self.map_data[0])
        height = len(self.map_data)
        for x in range(width):
            self.map_data[0][x] = self.unusable_tile
            self.map_data[height - 1][x] = self.unusable_tile
        for y in range(height):
            self.map_data[y][0] = self.unusable_tile
            self.map_data[y][width - 1] = self.unusable_tile

    def generate_cobblestones(self, num_cobblestones):
        width = len(self.map_data[0])
        height = len(self.map_data)
        for _ in range(num_cobblestones):
            x = random.randint(1, width - 2)
            y = random.randint(1, height - 2)
            if self.map_data[y][x] != self.unusable_tile:
                self.map_data[y][x] = "cobblestone"

    def draw(self, screen):
        for y, row in enumerate(self.map_data):
            for x, tile_type in enumerate(row):
                if tile_type in self.tile_images:
                    tile_image = self.tile_images[tile_type]
                    screen.blit(tile_image, (x * self.tile_size, y * self.tile_size))
                else:
                    print(f"Warning: Tile type '{tile_type}' not found in tile_images.")

        if self.player: # Draw the player only if it exists
            self.player.draw(screen)


    def handle_input(self, event):
        if self.player:
            self.player.handle_input(event) #Pass events to the player for handling

    def update(self, dt):
        if self.player:
            self.player.update(dt)  # Update the player's animation and position

    def on_enter(self):

        self.player = Player(self, self.screen, self.tile_images) # Pass necessary data to initialize Player
