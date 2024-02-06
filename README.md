# Inventory Management System

This system is designed to manage inventory in a warehouse or similar environment. It provides functionalities to track stock movement, display items along with their size and quantity, edit inventory information, and retrieve items from purchase orders.

## Features

- **Track Stock Movement**: The system keeps track of all stock movements, including incoming and outgoing items. It provides a detailed history of stock changes, which can be useful for auditing and inventory control.

- **Display Items**: The system can display a list of all items in the inventory, along with their size and quantity. This feature is useful for quickly checking the status of the inventory.

- **Edit Inventory Information**: The system allows users to edit the information of items in the inventory. This includes changing the size, quantity, and other details of an item.

- **Retrieve Items from Purchase Orders**: The system can retrieve items from purchase orders. This feature is useful for updating the inventory when a purchase order is received.

## Files

- `main.py`: This is the main file of the system. It contains the main logic for managing the inventory. It includes functions for tracking stock movement, displaying items, editing inventory information, and retrieving items from purchase orders.

## Usage

To use this system, run the `main.py` file. 

## Dependencies
This system uses the customtkinter library for the GUI. Make sure to install it before running the system.

python -m pip install customtkinter

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change. Please make sure to update tests as appropriate.

```bash
python main.py

```
ToDo Items From TODO file in project:
  Code: 
    ☐ Generate tests for system @high
    ☐ Data validation @high
    ☐ Debugging more in depth and more througout the system @low
    ☐ Fill in the design pattern functions. Need time to do this as well as will need to look at code and work out what can be implemented into the Factory and Observer Classes @low
  
  Testing: 
    ☐ Create unit tests @high
  
  Pages to Create: 
    ☐ Sales @high
    ☐ Inventory @critical
    ☐ Stock Control @high
    ☐ Checking in Transfers and Purchase Orders - Add this to the Editing page and add a button to check in ?  @critical
    ☐ Customers @high
    ☐ Hire @low
    ☐ Settings @low
  
  Home Page: 
    ☐ notificationButton not being updated when there are notifications @low
  
  Browse Stock Movement Page: 
    ☐ Utilise the movementOptionMenu @high / @low
      ☐ Need to make an instance of the origin page and then call it from there (subtask) @high
  
  Stock Movement Editing Page: 
    ☐ Create the method for retrieving data of transfer from data base @critical @est(1hour)
    ☐ Saving updated information to database, without changing data that the user has not changed or updated (Transfers) @critical @est(1hour)
    ☐ Label for which store is the sending and receiving store for transfers @critical @est(2hours)
    ☐  Not storing itemID in ItemStock table correctly, only stores the first ID of an item instead of each item @critical
  
  Purchase Order Page: 
    ☐ Not storing itemID in ItemStock table correctly, only stores the first ID of an item instead of each item @critical

