from menu import MenuScene
from farmerfield import FarmerField
from scene import SceneManager
from Cave import CaveScene
from settings import *

# Example Usage:
pygame.init()
screen = pygame.display.set_mode((800, 800))

scene_manager = SceneManager(screen)

# Create and add scenes. Replace with your actual scenes
game_scene = FarmerField(screen, scene_manager)
menu_scene = MenuScene(scene_manager)
cave_scene = CaveScene(screen, scene_manager, tile_images={"grass": loadim("Map/rамень.png"), "plantable": loadim("Map/земля.png")})

scene_manager.add_scene("menu", menu_scene)
scene_manager.add_scene("game", game_scene)
scene_manager.add_scene("cave", cave_scene)

scene_manager.set_scene("menu") # Start with the menu scene

running = True
clock = pygame.time.Clock()
while running:
    dt = clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        scene_manager.handle_input(event)
    scene_manager.update(dt)
    scene_manager.draw()
    pygame.display.flip()

pygame.quit()