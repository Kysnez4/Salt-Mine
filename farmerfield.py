from player import Player, Inventory
from Map import Map
from scene import Scene
from settings import *

class FarmerField(Scene):  # Inherits from Scene
    DOWN = 0
    UP = 1
    LEFT = 2
    RIGHT = 3

    def __init__(self, screen, scene_manager): #Pass scene_manager to the init method.
        super().__init__()
        self.scene_manager = scene_manager #Keep a reference to the scene manager
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.map = Map(self.screen, 25, 25, tile_size=32, tile_images={
            "grass": loadim('Map/rамень.png'),
            "plantable": loadim("Map/земля.png")})
        self.player = Player(self, self.screen)


    def update(self, dt): #update method takes delta time (dt) as a parameter.
        self.clock.tick(60)  #This should be done in the SceneManager, not here.
        key = pygame.key.get_pressed()
        if key[pygame.K_s]:
            self.player.move(self.DOWN)
        if key[pygame.K_w]:
            self.player.move(self.UP)
        if key[pygame.K_a]:
            self.player.move(self.LEFT)
        if key[pygame.K_d]:
            self.player.move(self.RIGHT)
        if key[pygame.K_e]:
            self.player.inventory.open_inventory()
        if not (key[pygame.K_s] or key[pygame.K_w] or key[pygame.K_a] or key[pygame.K_d]):
            self.player.stop_move()

        self.player.update()

    def draw(self, screen):
        self.update(screen) #Update is now part of draw
        self.screen.fill((0, 0, 0))
        self.map.draw()
        self.player.draw()
        pygame.display.flip()

    def handle_input(self, event):
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        self.player.inventory.drag_and_drop(event)
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                self.map.use_tile(*event.pos, "plantable")