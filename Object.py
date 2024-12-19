import random
from settings import *

class Object:
    def __init__(self, x, y, image):
        self.x = x
        self.y = y
        self.image = image
        self.rect = self.image.get_rect(topleft=(x, y))  # Add a rect for collision detection

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

    def collides_with(self, other):  # Method for collision detection
        return self.rect.colliderect(other.rect)


class Item(Object):  # Inherits from Object to include drawing and collision
    def __init__(self, x, y, image, name):
        super().__init__(x, y, image)  # Call Object's __init__
        self.name = name

    def get_name(self):
        return self.name


class CrystalPile(Object):
    def __init__(self, x, y, image, planted_object_type, growth_speed, product_quantity, max_growth=3):
        super().__init__(x, y, image)
        self.planted_object_type = planted_object_type
        self.growth_speed = growth_speed
        self.product_quantity = product_quantity
        self.growth_stage = 0
        self.max_growth = max_growth
        self.images = [image]  # List to hold images for different growth stages. Add images here.

    def next_day(self):
        self.growth_stage += self.growth_speed
        if self.growth_stage >= self.max_growth:
            self.growth_stage = self.max_growth
        self.image = self.images[min(self.growth_stage, len(self.images) - 1)]  # Change image based on growth stage
        self.rect = self.image.get_rect(topleft=(self.x, self.y))

    def harvest(self):
        # This could create the 'planted_object_type' objects.  Requires more detail on what 'planted_object_type' represents
        # For now, it just returns a count.
        harvested_amount = self.planted_object_type * self.product_quantity
        self.kill()  # Remove from any sprite groups.  You'll need to add this to a group for this to work.
        return harvested_amount


class Crystal(Item):
    def __init__(self, x, y, image, aspects = None, price_per_aspect = 25):
        super().__init__(x, y, image, "Crystal")  # Call Item's __init__
        self.aspects = aspects
        self.price = len(self.aspects) * price_per_aspect  # Note: aspects are assumed to have equal value

class Entrance(Object):
    def __init__(self, x, y, image, cave):
        super().__init__(x, y, image)
        self.cave = cave

    def use(self, player):
        player.x, player.y = self.cave.entrance_coords #Teleport player

class Cobblestone(Object):
    def __init__(self, x, y, image, loot_table):
        super().__init__(x, y, image)
        self.loot_table = loot_table

    def destroy(self):
        if random.random() < 0.05:  # 5% chance
            loot_level = random.randint(1, 60) # Assuming 60 loot levels
            for level, loot in self.loot_table.items():
                if loot_level >= level[0] and loot_level <= level[1]:
                    for _ in range(loot[1]): #loot[1] is the number of crystals
                        #Create and add the crystal to the game world
                        pass #Implementation needed here

