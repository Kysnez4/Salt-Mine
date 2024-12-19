import random
from settings import *

class Object(pygame.sprite.Sprite): # Inherits from pygame.sprite.Sprite
    def __init__(self, x, y, image):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)



class Item(Object):
    def __init__(self, x, y, image, name):
        super().__init__(x, y, image)
        self.name = name


class CrystalPile(Object):
    def __init__(self, x, y, images, planted_object_type, growth_speed, product_quantity, max_growth=3):
        super().__init__(x, y, images[0]) # Start with the first image
        self.planted_object_type = planted_object_type
        self.growth_speed = growth_speed
        self.product_quantity = product_quantity
        self.growth_stage = 0
        self.max_growth = max_growth
        self.images = images # List of images for growth stages

    def next_day(self):
        self.growth_stage += self.growth_speed
        self.growth_stage = min(self.growth_stage, self.max_growth) #Clamp growth stage
        self.image = self.images[self.growth_stage]
        self.rect = self.image.get_rect(topleft=(self.x, self.y))

    def harvest(self, all_sprites, crystal_group):
        harvested_crystals = []
        for _ in range(self.product_quantity):
            #Create a crystal.  You'll need to define how crystals are created.
            new_crystal = self.planted_object_type(self.rect.centerx, self.rect.centery,  #Position near the pile
                                                    pygame.image.load("crystal.png"), #Replace with your crystal image
                                                    aspects=["aspect1", "aspect2"]) #Example aspects

            all_sprites.add(new_crystal)
            crystal_group.add(new_crystal)
            harvested_crystals.append(new_crystal)

        self.kill() #Remove from sprite groups
        return harvested_crystals


class Crystal(Item):
    def __init__(self, x, y, image, aspects=None, price_per_aspect=25):
        super().__init__(x, y, image)
        self.name = "Crystal"
        self.aspects = aspects or [] # Handle case where aspects is None
        self.price = len(self.aspects) * price_per_aspect

class Entrance(Object):
    def __init__(self, x, y, image, scene): # scene instead of cave
        super().__init__(x, y, image)
        self.scene = scene

    def use(self, player):
        #Get the entrance coordinates from the target scene.
        entrance_coords = self.scene.get_entrance_coords()
        player.rect.topleft = entrance_coords

class Cobblestone(Object):
    def __init__(self, x, y, image, loot_table):
        super().__init__(x, y, image)
        self.loot_table = loot_table

    def destroy(self, all_sprites, crystal_group): # Needs sprite groups
        if random.random() < 0.05:
            loot_level = random.randint(1, 60)
            for (min_level, max_level), (crystal_type, quantity) in self.loot_table.items():
                if min_level <= loot_level <= max_level:
                    for _ in range(quantity):
                        #Create and add the crystal to the game world
                        new_crystal = crystal_type(self.rect.centerx, self.rect.centery,
                                                   pygame.image.load("crystal.png"), #Replace with image
                                                   aspects=["aspect1", "aspect2"])
                        all_sprites.add(new_crystal)
                        crystal_group.add(new_crystal)
        self.kill()