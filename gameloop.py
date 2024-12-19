from menu import MenuScene
from scene import SceneManager
from cart import CaveScene
from Object import *

# Example Usage:
pygame.init()
screen = pygame.display.set_mode((800, 800))

scene_manager = SceneManager(screen)

menu_scene = MenuScene(scene_manager)
game_scene = CaveScene(screen, scene_manager, tile_images={"grass": loadim("Map/rамень.png"),
                                                           "plantable": loadim("Map/земля.png"),
                                                           "wall": loadim("Map/rамень.png")
                                                           })

cave_scene = CaveScene(screen, scene_manager, tile_images={"grass": loadim("Map/rамень.png"),
                                                           "plantable": loadim("Map/земля.png"),
                                                           "wall": loadim("Map/rамень.png")
                                                           })


scene_manager.add_scene("menu", menu_scene)
scene_manager.add_scene("game", game_scene)
scene_manager.add_scene("cave", cave_scene)

scene_manager.set_scene("menu")

clock = pygame.time.Clock()
running = True

while running:
    dt = clock.tick(60) / 1000.0  # Delta time in seconds

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        scene_manager.handle_input(event)
        if scene_manager.player:
            scene_manager.player.run(event)


    scene_manager.update(dt)
    scene_manager.draw()
    pygame.display.flip()

pygame.quit()
