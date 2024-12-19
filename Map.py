class Map:
    def __init__(self, screen, w, h, tile_size=32, tile_images=None):
        self.screen = screen
        self.tile_size = tile_size
        self.tile_images = tile_images # Dictionary: {tile_type: image}  e.g., {"grass": grass_image, "plantable": plantable_image}
        self.map_data = []  # 2D array to represent the map

        #Example map initialization. This will create a 20x15 map filled with grass tiles
        width = w
        height = h
        self.map_data = [["grass"] * width for _ in range(height)]


    def draw(self):
        for y, row in enumerate(self.map_data):
            for x, tile_type in enumerate(row):
                if tile_type in self.tile_images:
                    tile_image = self.tile_images[tile_type]
                    self.screen.blit(tile_image, (x * self.tile_size, y * self.tile_size))
                else:
                    print(f"Warning: Tile type '{tile_type}' not found in tile_images.")


    def use_tile(self, x, y, new_tile_type):
        """Changes the tile at the given coordinates to a new tile type. """
        map_x = x // self.tile_size
        map_y = y // self.tile_size

        if 0 <= map_x < len(self.map_data[0]) and 0 <= map_y < len(self.map_data):
            self.map_data[map_y][map_x] = new_tile_type
        else:
            print("Coordinates are outside the map bounds.")

'''
#Example usage (remember to initialize pygame and load your tile images):

pygame.init()
screen = pygame.display.set_mode((640, 480)) #Example screen size. Adjust as needed

tile_images={"grass": loadim("rамень.png"), "plantable": loadim("земля.png")}

game_map = Map(screen, tile_size=32, tile_images=tile_images)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        


    screen.fill((0, 0, 0))
    game_map.draw()
    pygame.display.flip()

pygame.quit()

'''