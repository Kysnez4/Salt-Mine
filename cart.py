import pygame
import random

from Object import Cobblestone


class CaveScene(pygame.sprite.Sprite):
    def __init__(self, screen, scene_manager, tile_size=32, tile_images=None, num_levels=60):
        super().__init__()
        self.screen = screen
        self.scene_manager = scene_manager
        self.tile_size = tile_size
        self.tile_images = tile_images or {}
        self.num_levels = num_levels
        self.current_level = 1
        self.unusable_tile = "wall"
        self.map_data = []
        self.player = None
        self.all_sprites = scene_manager.all_sprites  # Access SceneManager's sprite group
        self.crystal_group = scene_manager.crystal_group # Access SceneManager's crystal group
        self.generate_level()

    def generate_level(self):
        # Adjust dimensions as needed
        width = 20
        height = 15
        # Generate the map data for this level. Replace with your room generation logic.
        self.map_data = [["grass"] * width for _ in range(height)]  # Initial grass floor
        self.generate_walls()
        self.generate_cobblestones(20)  # Generate 20 cobblestones.

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
        # ... (draw remains largely the same, but see below) ...
        for y, row in enumerate(self.map_data):
            for x, tile_type in enumerate(row):
                if tile_type in self.tile_images:
                    tile_image = self.tile_images[tile_type]
                    screen.blit(tile_image, (x * self.tile_size, y * self.tile_size))
                else:
                    print(f"Warning: Tile type '{tile_type}' not found in tile_images.")

        # Draw all sprites in SceneManager's group
        self.all_sprites.draw(screen) #Removed self.sprites.draw


    def handle_input(self, event):
        if self.player:
            self.player.run(event) # Use the event handling from the player itself

    def update(self, dt):
        if self.player:
            self.player.update() # Removed dt,  The player's update doesn't need dt directly
        self.all_sprites.update() # Update all sprites from SceneManager

    def on_enter(self, player):
        self.player = player
        # The player is already added to all_sprites by the SceneManager

    def get_entrance_coords(self):
        return (self.tile_size * 1, self.tile_size * 1)

    def use_tile(self, x, y, new_tile_type):
        map_x = x // self.tile_size
        map_y = y // self.tile_size
        if 0 <= map_x < len(self.map_data[0]) and 0 <= map_y < len(self.map_data):
            self.map_data[map_y][map_x] = new_tile_type
        else:
            print("Coordinates are outside the map bounds.")

    def destroy_cobblestone(self, x, y):
        map_x = x // self.tile_size
        map_y = y // self.tile_size
        if 0 <= map_x < len(self.map_data[0]) and 0 <= map_y < len(self.map_data) and self.map_data[map_y][map_x] == "cobblestone":
            for sprite in self.all_sprites: # Iterate through sprites in SceneManager's group
                if isinstance(sprite, Cobblestone) and sprite.rect.topleft == (map_x * self.tile_size, map_y * self.tile_size):
                    sprite.destroy(self.all_sprites, self.crystal_group)
                    self.map_data[map_y][map_x] = "grass" #Update map data
                    break
