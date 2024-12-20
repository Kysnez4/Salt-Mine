# Farm Game - Python  
Farm Game is a lightweight farming simulation game where players can plant, harvest, and manage crops. The game involves managing resources like seeds, energy, and inventory space, providing players with a fun and engaging experience. With a grid-based map and interactive player movements, this game offers a small yet strategic simulation of farm management.

## Key Features  
- **Grid-Based Farm Map:**  
  The farm is represented on a grid where players can move around, till soil, plant seeds, harvest crops, and remove plants.

- **Inventory System:**  
  Players can manage seeds and harvested crops through an inventory with a visual representation.

- **Energy Management:**  
  Actions like planting, harvesting, and moving cost energy, requiring players to make strategic decisions.

- **Seed Variety:**  
  Players can plant several types of seeds (e.g., Potato, Kale, Berry) and manage their growth to harvest the final crops.

- **Store Mechanics:**  
  Buy and sell items through an in-game store. Items have different buy and sell prices, adding an economic strategy element.

## Technology Stack  
- **Language:** Python  
- **Game Interface:** Tkinter (for UI elements and graphics)  
- **Storage:** In-memory dictionaries and constants for managing game data  
- **Modular Code Design:** Organized into distinct Python files for better readability and maintenance:
  - **farm_game.py:** Main game logic and interface.
  - **support_functions.py:** Helper functions for repetitive actions.
  - **model.py:** Core game models, including player and inventory management.
  - **constants.py:** Predefined constants for colors, prices, seeds, and UI dimensions.

## Usage Workflow  
1. **Game Start:**  
   - Players begin with a small set of seeds and energy points. The game displays the farm map, inventory, and energy bar.

2. **Player Movement:**  
   - Use **W/A/S/D** keys to move the player around the farm grid. Each movement costs 1 energy point.

3. **Planting and Harvesting:**  
   - Till the soil, plant seeds, and wait for crops to grow. Harvest mature crops to store them in the inventory.

4. **Managing Inventory:**  
   - Use the inventory to select seeds or crops. Items in the inventory are color-coded to indicate their status.

5. **In-Game Store:**  
   - Visit the store to buy seeds or sell harvested crops. Prices are predefined in the constants.

## Setup & Installation  
1. **Install Dependencies:**  
   Ensure you have Python installed on your machine. This project primarily uses Tkinter, which comes pre-installed with most Python distributions.

2. **Run the Game:**  
   To start the game, run the following command in your terminal:  
   ```bash
   python farm_game.py

## Controls
- **W**: Move Up
- **A:** Move Left
- **S:** Move Down
- **D:** Move Right
- **T:** Till the soil
- **P:** Plant seeds
- **H:** Harvest crops
- **R:** Remove plants
- **Q:** Quit the game

### Action Keys:
The appropriate action is triggered based on the player’s context on the farm grid (e.g., Plant when standing on tilled soil).