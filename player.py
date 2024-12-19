import pygame.transform

from settings import *

class Inventory:
    def __init__(self, rows, cols, x, y, image):
        self.rows = rows
        self.cols = cols
        self.slots = [[None for _ in range(cols)] for _ in range(rows)]  # 2D array for slots
        self.x = x
        self.y = y
        self.image = image
        self.slot_size = image.get_width() // cols  # Assuming square slots
        self.active_slot = (0, 0)  # Row, column tuple
        self.dragging_item = None
        self.inventory_open = False #Flag to track inventory state.

    def add_item(self, item):
        for r in range(self.rows):
            for c in range(self.cols):
                if self.slots[r][c] is None:
                    self.slots[r][c] = item
                    return

    def draw(self, screen):
        if self.inventory_open: # Only draw if open
            screen.blit(self.image, (self.x, self.y))
            for r in range(self.rows):
                for c in range(self.cols):
                    item = self.slots[r][c]
                    if item:
                        item.draw(screen, self.x + c * self.slot_size, self.y + r * self.slot_size)

    def open_inventory(self):
        self.inventory_open = not (self.inventory_open)

    def open_chest(self, chest):
        print(f"Chest opened. Contains: {chest.contents}") # Placeholder - needs chest implementation


    def drag_and_drop(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_x, mouse_y = event.pos
            grid_x = (mouse_x - self.x) // self.slot_size
            grid_y = (mouse_y - self.y) // self.slot_size

            if 0 <= grid_x < self.cols and 0 <= grid_y < self.rows and self.inventory_open:
                item = self.slots[grid_y][grid_x]
                if item:
                    self.dragging_item = item
                    self.slots[grid_y][grid_x] = None

        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if self.dragging_item:
                mouse_x, mouse_y = event.pos
                grid_x = (mouse_x - self.x) // self.slot_size
                grid_y = (mouse_y - self.y) // self.slot_size

                if 0 <= grid_x < self.cols and 0 <= grid_y < self.rows and self.inventory_open:
                    if self.slots[grid_y][grid_x] is None:
                        self.slots[grid_y][grid_x] = self.dragging_item
                    else:
                        temp = self.slots[grid_y][grid_x]
                        self.slots[grid_y][grid_x] = self.dragging_item
                        self.dragging_item = temp
                self.dragging_item = None


class Hotbar:
    def __init__(self, inventory, x, y, image):
        self.inventory = inventory
        self.x = x
        self.y = y
        self.image = image
        self.active_slot = 0
        self.slot_size = image.get_width() // 12 # Assuming 12 slots

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))
        for i in range(12):
            item = self.inventory.slots[0][i]
            if item:
                item.draw(screen, self.x + i * self.slot_size, self.y)

    def update(self, event):
        if event.type == pygame.MOUSEWHEEL:
            self.active_slot = (self.active_slot + event.y) % 12


class Player:
    # State consts
    IDLE_STATE = 0
    MOVING_STATE = 1
    USING_STATE = 2
    SWITCHING_STATE = 3
    PICKING_UP_STATE = 4

    WALK_SPEED = 3
    RUN_SPEED = 6

    NO_ITEM = -1
    ROCK_ITEM = 0
    WEED_ITEM = 1
    TURNIP_ITEM = 2

    DOWN = 0
    UP = 1
    LEFT = 2
    RIGHT = 3

    FRAME_SIZE = (100, 100)
    TOOL_FRAME_SIZE = (32, 32)
    ITEM_FRAME_SIZE = (32, 32)
    TOOL_OFFSET = (-40, -50)
    ITEM_OFFSET = (-18, -40)
    TILE_SIZE = 32

    # Tool consts
    HOE = 0
    WATERING_CAN = 1
    TURNIP_SEED = 5

    # Tool vars
    cur_tool = 0
    tools = [HOE, WATERING_CAN, TURNIP_SEED]
    tool_frame_rect = pygame.Rect(0, 0, TOOL_FRAME_SIZE[0], TOOL_FRAME_SIZE[1])
    tool_screen_rect = pygame.Rect(0, 0, TOOL_FRAME_SIZE[0], TOOL_FRAME_SIZE[1])

    # Item vars
    item_frame_rect = pygame.Rect(0, 0, ITEM_FRAME_SIZE[0], ITEM_FRAME_SIZE[1])
    item_screen_rect = pygame.Rect(0, 0, ITEM_FRAME_SIZE[0], ITEM_FRAME_SIZE[1])

    # Animations
    IDLE_ANIMATION = [(0, 60)]
    WALK_ANIMATION = [(1, 10), (0, 10), (2, 10), (0, 10)]
    RUN_ANIMATION = [(3, 8), (0, 8), (4, 8), (0, 8)]

    PICKUP_ANIMATION = [(5, 10)]
    HOLD_ANIMATION = [(6, 60)]
    HOLD_WALK_ANIMATION = [(6, 10), (7, 10), (6, 10), (8, 10)]
    HOLD_RUN_ANIMATION = [(6, 8), (9, 8), (6, 8), (10, 8)]

    TILLING_ANIMATION = [(12, 15), (13, 4), (14, 8), (15, 30)]
    WATER_ANIMATION = [(16, 15), (17, 30), (16, 7)]
    SOW_ANIMATION = [(18, 10), (19, 10), (20, 10), (21, 10), (22, 30)]
    TOOL_SWITCH_ANIMATION = [(11, 45)]

    TILLING_FRAME = 14
    WATERING_FRAME = 17
    SOWING_FRAME = 22

    # Variables
    screen = None
    game = None

    holding = False
    held_item = None

    pos_x = 100
    pos_y = 100

    current_state = IDLE_STATE
    current_direction = DOWN

    current_frame = 0
    current_animation = None

    frame_counter = 0
    current_duration = 0
    animation_index = 0

    tile_x = 0
    tile_y = 0
    reticle_x = 0
    reticle_y = 0

    running = False

    screen_rect = None
    frame_rect = None

    spritesheet = None
    tool_sheet = None
    item_sheet = None

    def __init__(self, g, s):
        self.game = g
        self.screen = s
        self.spritesheet = loadim("farmer-big.png").convert_alpha()
        self.frame_rect = pygame.Rect(0, 0, self.FRAME_SIZE[0], self.FRAME_SIZE[1])
        self.screen_rect = pygame.Rect(self.pos_x, self.pos_y, self.FRAME_SIZE[0], self.FRAME_SIZE[1])
        self.screen_rect.center = (self.pos_x, self.pos_y)
        self.set_animation(self.IDLE_ANIMATION)
        self.inventory = Inventory(3, 12, 10, 10, loadim("inventory.png"))
        self.hotbar = Hotbar(self.inventory, 10, 20, pygame.transform.scale(loadim("Хотбар. Увелич обводка.png"), (700, 200)))


    def set_frame(self, frame):
        self.current_frame = frame
        cur_row = self.current_direction
        cur_col = self.current_frame

        self.frame_rect.topleft = (cur_col * self.FRAME_SIZE[0], cur_row * self.FRAME_SIZE[1])

    def next_frame(self):
        self.current_frame = self.current_animation[self.animation_index][0]
        self.current_duration = self.current_animation[self.animation_index][1]
        self.on_frame()

    def set_animation(self, animation):
        self.current_animation = animation
        self.animation_index = 0

        self.frame_counter = 0
        self.next_frame()
        self.set_frame(self.current_frame)

    def update_animation(self):
        self.frame_counter += 1

        if self.frame_counter >= self.current_duration:
            self.frame_counter = 0
            self.animation_index += 1
            if self.animation_index >= len(self.current_animation):
                self.animation_index = 0
                self.on_animation_end()
            self.next_frame()
            self.set_frame(self.current_frame)

    def on_animation_end(self):
        if self.current_state == self.USING_STATE or self.current_state == self.SWITCHING_STATE:
            self.current_state = self.IDLE_STATE
            if self.holding:
                self.set_animation(self.HOLD_ANIMATION)
            else:
                self.set_animation(self.IDLE_ANIMATION)
            return
        elif self.current_animation == self.PICKUP_ANIMATION:
            self.holding = True
            self.update_held_item_rect()
            self.item_frame_rect.topleft = (self.held_item * self.ITEM_FRAME_SIZE[0], 0)

            self.set_animation(self.HOLD_ANIMATION)
            self.current_state = self.IDLE_STATE

    def use_item(self, item, screen):
        if item and hasattr(item, 'use'):  # Check if the item has a 'use' method
            item.use(screen)  # Call the item's use method

    def pick_up_item(self, item, distance_threshold=20):
        distance = ((self.x + self.rect.width // 2) - (item.x + item.rect.width // 2)) ** 2 + ((self.y + self.rect.height // 2) - (item.y + item.rect.height //2)) **2
        if distance <= distance_threshold**2:
            self.inventory.add_item(item)
            #Remove the item from the world (requires proper management of items in the game world)
            #item.kill() # Assuming item is part of a sprite group

    def move(self, direction):
        if self.current_state != self.IDLE_STATE and self.current_state != self.MOVING_STATE:
            return

        if self.current_state != self.MOVING_STATE:
            if self.running:
                if self.holding:
                    self.set_animation(self.HOLD_RUN_ANIMATION)
                else:
                    self.set_animation(self.RUN_ANIMATION)
            else:
                if self.holding:
                    self.set_animation(self.HOLD_WALK_ANIMATION)
                else:
                    self.set_animation(self.WALK_ANIMATION)
            self.current_state = self.MOVING_STATE

        if self.running == True:
            if direction == self.DOWN:
                self.pos_y += self.RUN_SPEED
                self.current_direction = self.DOWN
            if direction == self.UP:
                self.pos_y -= self.RUN_SPEED
                self.current_direction = self.UP
            if direction == self.LEFT:
                self.pos_x -= self.RUN_SPEED
                self.current_direction = self.LEFT
            if direction == self.RIGHT:
                self.pos_x += self.RUN_SPEED
                self.current_direction = self.RIGHT
        else:
            if direction == self.DOWN:
                self.pos_y += self.WALK_SPEED
                self.current_direction = self.DOWN
            if direction == self.UP:
                self.pos_y -= self.WALK_SPEED
                self.current_direction = self.UP
            if direction == self.LEFT:
                self.pos_x -= self.WALK_SPEED
                self.current_direction = self.LEFT
            if direction == self.RIGHT:
                self.pos_x += self.WALK_SPEED
                self.current_direction = self.RIGHT
        self.screen_rect.center = (self.pos_x, self.pos_y)

    def stop_move(self):
        if self.current_state == self.MOVING_STATE:
            self.current_state = self.IDLE_STATE
            if self.holding:
                self.set_animation(self.HOLD_ANIMATION)
            else:
                self.set_animation(self.IDLE_ANIMATION)

    def start_running(self):
        if self.current_state == self.USING_STATE:
            return
        self.running = True
        if self.current_animation != self.RUN_ANIMATION:
            self.set_animation(self.RUN_ANIMATION)

    def stop_running(self):
        if self.current_state == self.USING_STATE:
            return
        self.running = False
        if self.current_state == self.MOVING_STATE:
            self.set_animation(self.WALK_ANIMATION)

    def on_frame(self):
        if self.current_frame == self.TILLING_FRAME:
            self.game.till_tile(self.reticle_x, self.reticle_y)
        elif self.current_frame == self.SOWING_FRAME:
            self.game.sow_tile(self.tile_x, self.tile_y)
        elif self.current_frame == self.WATERING_FRAME:
            self.game.water_tile(self.reticle_x, self.reticle_y)

    def update_held_item_rect(self):
        self.item_screen_rect.topleft = (self.pos_x + self.ITEM_OFFSET[0], self.pos_y + self.ITEM_OFFSET[1])

    def update(self):
        self.update_animation()

    def run(self, event):
        self.hotbar.update(event)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LSHIFT or event.key == pygame.K_RSHIFT:
                self.start_running()
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LSHIFT or event.key == pygame.K_RSHIFT:
                self.stop_running()

    def draw(self):
        self.inventory.draw(self.screen)
        self.hotbar.draw(self.screen)
        self.screen.blit(self.spritesheet, self.screen_rect, self.frame_rect)

        if self.current_state == self.SWITCHING_STATE:
            self.screen.blit(self.tool_sheet, self.tool_screen_rect, self.tool_frame_rect)

        if self.holding:
            self.screen.blit(self.item_sheet, self.item_screen_rect, self.item_frame_rect)


