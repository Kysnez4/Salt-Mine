
import tkinter as tk
from tkinter import filedialog, messagebox # For masters task
from typing import Callable, Union, Optional
from support_functions import *
from model import *
from constants import *

""" ############ HELPER FUNCTIONS ############ """

def has_buy_price(buy_price) -> bool:
    """ Returns True if item has a buy price, and False otherwise """
    if buy_price == "N/A":
        return False
    else: return True

def set_text(name: str, amount: int, sell_price: int, buy_price: int) -> str:
    """ Returns the text used in the ItemViews formatted apropriately """
    
    text = f"{name}: {amount} \n \
Sell price: ${sell_price} \n \
Buy price: ${buy_price}"

    return text

""" ############ CONTROLLER ############ """

class FarmGame(object):
    """ Controller object to handle Viewer/Model interactions """
    
    _width = INVENTORY_WIDTH + FARM_WIDTH
    
    def __init__(self, master: tk.Tk, map_file: str, cave_map_file: str, model: 'FarmModel' = None) -> None:
        """ Instantiate and initialize all necessary objects and variables """
        
        ### Window title, Key presses and Instantiate Model object ###
        master.title('Farm Game')
        master.bind("<KeyPress>", self.handle_keypress)
        if model:
            self._model = model
        else:
            self._model = FarmModel(map_file, cave_map_file)
        
        ### Instantiate Banner Image ###
        self._cache = {}
        self._banner_img = get_image('images/header.png',
                                 (self._width, BANNER_HEIGHT), self._cache)
        self._banner = tk.Label(master,
                                image = self._banner_img).pack(side=tk.TOP)

        ### Instantiate FarmViewer & ItemViewersFrame Frame ###
        self._farm_and_inventory = tk.Frame(master)
        self._farm_and_inventory.pack(side = tk.TOP, expand=True, fill=tk.BOTH)
    
            ### Instantiate FarmViewer ###
        self.farm_view = FarmView(self._farm_and_inventory,
                                  self._model.get_dimensions(),
                                  (FARM_WIDTH, FARM_WIDTH))
        self.farm_view.pack(side=tk.LEFT)

            ### Instantiate ItemViewersFrame ###
        self._inventory = tk. Frame(self._farm_and_inventory)
        self._inventory.pack(side=tk.TOP, expand=True, fill=tk.BOTH)

                ### Instantiate ItemViews ###
        self._item_views = {}
        for item in ITEMS:
            
            """ Setup ItemViews to reflect player inventory """
            item_name = item
            if item_name not in self._model.get_player().get_inventory():
                item_amount = 0
            else:
                item_amount = self._model.get_player().\
                                 get_inventory()[item_name]
                
            """ Functions below handle callbacks in ItemViewers  """
            item_select = lambda event, item = item_name: self.select_item(item)
            item_sell = lambda item = item_name: self.sell_item(item)
            item_buy = lambda item = item_name: self.buy_item(item)

            """ Instantiate and pack ItemView """
            self._item_views[item] = ItemView(self._inventory,
                                              item_name,
                                              item_amount,
                                              item_select,
                                              item_sell,
                                              item_buy)
            self._item_views[item].pack(side=tk.TOP,
                                        expand=True,
                                        fill=tk.BOTH)
            
        ### Instantiate next day button ###
        self.next_day_button =  tk.Button(master,
                                text = "Next day",
                                command = lambda: self.handle_next_day_press()
                                ).pack(side=tk.BOTTOM)
        
        ### Instantiate InfoBar Viewer ###
        self.info_bar = InfoBar(master)
        self.info_bar.pack(side=tk.BOTTOM)


        self.menu_button = tk.Button(master, text="Управление", command=self.toggle_menu)
        self.menu_button.pack(side=tk.BOTTOM)

        self.menu_frame = tk.Frame(master, bg="lightgray")
        self.menu_frame.pack_forget()

        self.menu_label = tk.Label(self.menu_frame, text=self.get_menu_text(), justify="left", wraplength=300)
        self.menu_label.pack(pady=10)

        self.save_button = tk.Button(master, text="Сохранить игру", command=self.save_game)
        self.save_button.pack(side=tk.BOTTOM)

        self.load_button = tk.Button(master, text="Загрузить игру", command=self.load_game)
        self.load_button.pack(side=tk.BOTTOM)

        self.redraw()

    def save_game(self):
        self._model.save_game()

    def load_game(self):
        loaded_model = FarmModel.load_game()
        if loaded_model:
            self._model = loaded_model
            self.redraw()
        else:
            messagebox.showerror("Ошибка", "Не удалось загрузить игру")

    def get_menu_text(self) -> str:
        return """
        **Управление:**
        - W, A, S, D: Перемещение
        - P: Посадка растений (нужно выбрать семечко в инвентаре)
        - H: Сбор урожая
        - T: Вспашка земли
        - U: Откапывание земли
        - R: Удаление растения
        - E: Вход в пещеру / Выход из пещеры
        - B: Разрушение жеоды (в пещере)
        """

    def toggle_menu(self):
        if self.menu_frame.winfo_ismapped():
            self.menu_frame.pack_forget()
        else:
            self.menu_frame.pack(pady=5)
            # self.menu_frame.pack(pady=5, padx=5)

    def redraw(self, message=None) -> None:
        """ Method redraws InforBar Viewer and FarmView """
        
        self.info_bar.redraw(self._model.get_days_elapsed(),
                             self._model.get_player().get_money(),
                             self._model.get_player().get_energy()
                             )

        if self._model.get_is_in_cave():
            self.farm_view.redraw(self._model.get_cave_map(),
                                  self._model.get_geodes(),
                                  self._model.get_player_position(),
                                  self._model.get_player_direction(),
                                  True, message
                                  )
        else:
            self.farm_view.redraw(self._model.get_map(),
                                  self._model.get_plants(),
                                  self._model.get_player_position(),
                                  self._model.get_player_direction()
                                  )

    def handle_keypress(self, event: tk.Event) -> None:
        """ Method handles keypress actions """
        
        ### Move the Player ###
        if event.keysym == UP:
            self._model.move_player(UP)
            self.redraw()
        elif event.keysym == DOWN:
            self._model.move_player(DOWN)
            self.redraw()
        elif event.keysym == LEFT:
            self._model.move_player(LEFT)
            self.redraw()
        elif event.keysym == RIGHT:
            self._model.move_player(RIGHT)
            self.redraw()

        ### Till and Untill Soil ###
        elif event.keysym == 't':
            self._model.till_soil(self._model.get_player_position())
            self.redraw()
        elif event.keysym == 'u':
            self._model.untill_soil(self._model.get_player_position())
            self.redraw()
        ### Break geode
        elif event.keysym == 'b' and self._model.get_is_in_cave():
            message = None
            harvest_result = self._model.break_geode(self._model.get_player_position())
            if harvest_result:
                self._model.get_player().add_item((harvest_result, 1))
                self._item_views[harvest_result].update(1, self._item_views[harvest_result].get_is_selected())
                message = "Жеода сломалась! Вы получили кристалл!"
            else:
                message = "Жеода сломалась!"

            self.redraw(message)

        ### Plant ###
        elif event.keysym == 'p':
            if self._model.get_player().get_selected_item() != None \
               and self._item_views[self._model.get_player().\
                                get_selected_item()]._amount != 0:
                
                # Determine the selected plant seed
                if self._model.get_player().get_selected_item() == 'Ruby crystal':
                    plant = KalePlant()
                if self._model.get_player().get_selected_item() == 'Emerald crystal':
                    plant = PotatoPlant()
                if self._model.get_player().get_selected_item() == 'Salt crystal':
                    plant = BerryPlant()
    
                # Update the plant seed viewer
                self._model.add_plant(self._model.get_player_position(), plant)
                self._item_views[self._model.get_player().get_selected_item()].\
                                                                update(-1, True)
                self.redraw()
                
        ### Remove plant ###
        elif event.keysym == 'r' and not self._model.get_is_in_cave():
            self._model.remove_plant(self._model.get_player_position())
            self.redraw()

        ### Harvest Plant ###
        elif event.keysym == 'h' and not self._model.get_is_in_cave():
            successful_harvest = \
                    self._model.harvest_plant(self._model.get_player_position())
            if successful_harvest != None:
                self._model.get_player().add_item(successful_harvest)
                self._item_views[successful_harvest[0]].update(
                    successful_harvest[1],
                    self._item_views[successful_harvest[0]].get_is_selected()
                    )
                
                self.redraw()
            else: pass

        ### Cave Entrance ###
        elif event.keysym == 'e':
            current_position = self._model.get_player_position()
            if self._model.get_is_in_cave() == False:
                if self._model.get_map()[current_position[0]][current_position[1]] == CAVE_ENTRANCE:
                    self._model.set_is_in_cave(True)
                    self._model.get_player().set_position((1, 1))
                    self.redraw()

            elif self._model.get_is_in_cave() == True:
                if self._model.get_cave_map()[current_position[0]][current_position[1]] == STAIRS:
                    self._model.set_is_in_cave(False)
                    self._model.get_player().set_position((0, 1))
                    self.redraw()

        else:
            pass

    def select_item(self, item_name: str) -> None:
        """ Select item on ItemViewer press """
        
        try:
            ### Deselect Current Selection ###
            currently_selected = self._model.get_player().get_selected_item()
            self._item_views[currently_selected].update(0, False)
            
            ### Select New Selection ###
            self._model.get_player().select_item(item_name)
            self._item_views[item_name].update(0, True)
            
        except KeyError or TypeError:
            ### Select New Selection ###
            self._model.get_player().select_item(item_name)
            self._item_views[item_name].update(0, True)

    def buy_item(self, item_name: str) -> None:
        """ Methods buys item on 'buy' click, if possible """
        
        if self._model.get_player().get_money() >= BUY_PRICES[item_name]:
            # Buy in module
            self._model.get_player().buy(item_name, BUY_PRICES[item_name])
            self._item_views[item_name].\
                    update(1, self._item_views[item_name].get_is_selected())

            self.redraw()

    def sell_item(self, item_name: str) -> None:
        """ Methods sells item on 'sell' click, if possible """
        
        if item_name in self._model.get_player()._inventory.keys():
            self._model.get_player().sell(item_name, SELL_PRICES[item_name])
            self._item_views[item_name].update(-1, self._item_views[item_name].\
                                                               get_is_selected())
            # Redraw info bar
            self.redraw()
  
    def handle_next_day_press(self) -> None:
        """ Handles next day button command """
        
        self._model.new_day()
        self.redraw()

""" ############ VIEWERS ############ """

class InfoBar(AbstractGrid):
    """ Viewer class for the Infobar """
    
    def __init__(self, master: tk.Tk | tk.Frame) -> None:
        """ Initialize viewer with dimensions """
        
        super().__init__(master,
                         dimensions = (2,3),
                         size = (700, INFO_BAR_HEIGHT))

    def redraw(self, day: int, money: int, energy: int) -> None:
        """ Method redraws Viewer """
        
        self.clear()

        self.annotate_position((0,0), "Day:", HEADING_FONT)
        self.annotate_position((1,0), day)
        self.annotate_position((0,1), "Money:", HEADING_FONT)
        self.annotate_position((1,1), f"${money}")
        self.annotate_position((0,2), "Energy:", HEADING_FONT)
        self.annotate_position((1,2), energy)

class FarmView(AbstractGrid):
    """ Viewer class for the Farm """
    
    def __init__(self, master: tk.Tk | tk.Frame, dimensions: tuple[int, int],
                 size: tuple[int, int], **kwargs) -> None:
        """ Initialize viewer with dimensions, and set a cache """

        super().__init__(master, dimensions, size)
        self._cache = {}
        
    def redraw(self, ground: list[str], objects: dict[tuple[int, int], 'Plant' ] or dict[tuple[int, int], 'Geode'],
               player_position: tuple[int, int], player_direction: str, is_cave=False, message=None) -> None:
        """ Method redraws Viewer """

        if message:
            self.create_text(self.get_midpoint(player_position), text=message, font=("Arial", 14, "bold"), fill="white",
                             anchor=tk.CENTER)
        self.clear()

        if not is_cave:

            grass_img = get_image( \
                'images/' + IMAGES[GRASS], self.get_cell_size(), self._cache)
            soil_img = get_image( \
                'images/'+ IMAGES[SOIL],  self.get_cell_size(), self._cache)
            untilled_img = get_image( \
                'images/' + IMAGES[UNTILLED], self.get_cell_size(), self._cache)
            cave_entrance_img = get_image( \
                'images/' + IMAGES[CAVE_ENTRANCE], self.get_cell_size(), self._cache)
            ### Read and assemble map ###
            for r, row in enumerate(ground):
                for c, letter in enumerate(row):
                    if letter == GRASS:
                        self.create_image(self.get_midpoint((r, c)),
                                          image = grass_img)
                    if letter == SOIL:
                        self.create_image(self.get_midpoint((r, c)),
                                          image = soil_img)
                    if letter == UNTILLED:
                        self.create_image(self.get_midpoint((r, c)),
                                          image = untilled_img)
                    if letter == CAVE_ENTRANCE:
                        self.create_image(self.get_midpoint((r, c)),
                                          image=cave_entrance_img)


            ### Construct the plant objects
            for position in objects:
                plant_img = \
                    get_image('images/' + get_plant_image_name(objects[position]),
                              self.get_cell_size(), self._cache)
                self.create_image(self.get_midpoint(position), image = plant_img)

            ### Construct the player ###
            player_img = get_image('images/' + IMAGES[player_direction],
                                   self.get_cell_size(), self._cache)
            self.create_image(self.get_midpoint(player_position),
                              image = player_img)
        else:
            cave_floor_img = get_image( \
                'images/' + IMAGES[CAVE_FLOOR], self.get_cell_size(), self._cache)
            stairs_img = get_image( \
                'images/' + IMAGES[STAIRS], self.get_cell_size(), self._cache)
            for r, row in enumerate(ground):
                for c, letter in enumerate(row):
                    if letter == CAVE_FLOOR:
                        self.create_image(self.get_midpoint((r, c)),
                                          image=cave_floor_img)
                    if letter == STAIRS:
                        self.create_image(self.get_midpoint((r, c)),
                                          image=stairs_img)
            for position in objects:
                geode_img = get_image('images/' + IMAGES[GEODE],
                                      self.get_cell_size(), self._cache)
                self.create_image(self.get_midpoint(position), image=geode_img)
            player_img = get_image('images/' + IMAGES[player_direction],
                                   self.get_cell_size(), self._cache)
            self.create_image(self.get_midpoint(player_position),
                              image=player_img)
            
class ItemView(tk.Frame):
    """ Viewer class for the Inventory """
    
    def __init__(self, master: tk.Frame, item_name: str, amount: int,
                 select_command: Optional[Callable[[str], None]] = None,
                 sell_command: Optional[Callable[[str], None]] = None,
                 buy_command: Optional[Callable[[str], None]] = None) -> None:
        """ Initialize Viewer with necessary variables """

        ### Setup Frame Characteristics ###
        super().__init__(master,
                         highlightbackground = INVENTORY_OUTLINE_COLOUR,
                         highlightthickness = 1)

        ### Assign Variables ###
        self._item_name = item_name
        self._amount = amount
        self._sell_price = SELL_PRICES[self._item_name]       
        try:
            self._buy_price = BUY_PRICES[self._item_name]
        except KeyError:
            self._buy_price = "N/A"
        self._is_selected = False

        ### Assign callback functions ###
        self._select_command = select_command
        self._sell_command = sell_command
        self._buy_command = buy_command
        
        ### Setup Widgets ###
        self._item_details = tk.Label(self)
        self._item_details.pack(side=tk.LEFT)
        self._sell_button = tk.Button(self, text="Sell", command= \
                                      self._sell_command).pack(side=tk.LEFT)
        if has_buy_price(self._buy_price):              
            self._buy_button = tk.Button(self, text="Buy", command= \
                                      self._buy_command).pack(side=tk.LEFT)
        ### Bind widgets ###
        self.bind("<Button-1>", select_command)
        self._item_details.bind("<Button-1>", select_command)

        self.update(0, self.get_is_selected())

    def get_is_selected(self):
        """ Returns the selectred state of the object """
        
        return self._is_selected
        
    def update(self, amount: int, selected: bool = False) -> None:
        """ Redraws the individual Item View """

        self._is_selected = selected
        
        self._amount += amount
        if self._amount <= 0:
            self._amount = 0
            
        ### Reassign Label ###
        self._item_details.configure(text=set_text(self._item_name,
                                                   self._amount,
                                                   self._sell_price,
                                                   self._buy_price))
        ### Update Colours ###
        if self._amount == 0:
            self.configure(bg=INVENTORY_EMPTY_COLOUR)
            self._item_details.configure(bg=INVENTORY_EMPTY_COLOUR)
        elif self._amount != 0:
            self.configure(bg=INVENTORY_COLOUR)
            self._item_details.configure(bg=INVENTORY_COLOUR)
            if self._is_selected == True:
                self.configure(bg=INVENTORY_SELECTED_COLOUR)
                self._item_details.configure(bg=INVENTORY_SELECTED_COLOUR)

""" ############ MAIN ############ """

def play_game(root: tk.Tk, map_file: str, cave_map_file: str, loaded_model: FarmModel = None) -> None:
    if loaded_model == None:
        controller = FarmGame(root, map_file, cave_map_file)
    else:
        controller = FarmGame(root, map_file, cave_map_file, loaded_model)

    def remove_message():
        controller.redraw()

    controller.redraw()

    root.after(1500, remove_message)
    root.mainloop()

def main() -> None:
    """ Construct the root window, and setup the game with any map. """

    map_file = 'maps/map1.txt'
    cave_map_file = 'maps/cave.txt'
    root = tk.Tk()
    loaded_model = FarmModel.load_game()
    if loaded_model:
        play_game(root, map_file, cave_map_file, loaded_model)  # загрузка при старте игры
    else:
        play_game(root, map_file, cave_map_file)

if __name__ == '__main__':
    main()
