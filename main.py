import csv  # to read and write csv files
import random  # to generate random reciept IDs
import customtkinter  # a more modern tkinter
from typing import (
    Union,
    Callable,
    List,
)  # to use FloatSpinbox from the customtkinter tutorial
from PIL import Image  # to load images

# https://www.geeksforgeeks.org/load-csv-data-into-list-and-dictionary-using-python/

# constants
CUSTOMERS_FILE = "customers.csv"
STOCK_FILE = "stock.csv"

ITEM_NAMES = [
    "Chairs",
    "Tables",
    "Cutlery Sets",
    "BBQs",
    "Table Cloths",
    "Napkin Rings",
]

ITEM_IMAGES = [f"images/{ITEM_NAME}.png" for ITEM_NAME in ITEM_NAMES]


def loadPastCustomerOrders():
    pastCustomerOrders = {}
    with open(CUSTOMERS_FILE, "r") as data:
        for order in csv.reader(data):
            # initialise new customer if not in dict
            # order[0] is customer name
            if order[0] not in pastCustomerOrders:
                pastCustomerOrders[order[0]] = {
                    "recieptIDs": [],
                    "itemsCurrentlyRented": {},
                }

            # order[1] is reciept ID
            pastCustomerOrders[order[0]]["recieptIDs"].append(order[1])

            itemsCurrentlyRented = {
                # using eval to convert string from csv to dict
                # key is item name, value is amount, order[2] is itemsCurrentlyRented as string
                key: int(value)
                for key, value in eval(order[2]).items()
            }

            # increment amount or add new item
            for item, amount in itemsCurrentlyRented.items():
                if item in pastCustomerOrders[order[0]]["itemsCurrentlyRented"]:
                    pastCustomerOrders[order[0]]["itemsCurrentlyRented"][item] += amount
                else:
                    pastCustomerOrders[order[0]]["itemsCurrentlyRented"][item] = amount

    return pastCustomerOrders

def loadStock():
    stock = {}
    with open(STOCK_FILE, "r") as data:
        for item in csv.reader(data):
            stock[item[0]] = int(item[1])
    return stock

stock = loadStock()


# for testing or for on an admin page if I added that
def resetStock():
    # https://www.w3schools.com/python/python_file_write.asp
    with open(STOCK_FILE, "w") as file:
        file.writelines(
            [
                "Chairs,100\n",
                "Tables,100\n",
                "Cutlery Sets,100\n",
                "BBQs,100\n",
                "Table Cloths,100\n",
                "Napkin Rings,100",
            ]
        )


# customer class to store order details
class Customer:
    # initialise a customers order
    def __init__(self, name, ID, items):
        # store details to object
        self.name = name
        self.recieptID = ID
        self.items = items

        self.updateStock()
        self.storeDetails()

    # update the stock file
    def updateStock(self):
        with open(STOCK_FILE, "r") as file:
            lines = file.readlines()

        # go through each item in the order check if it is in each line of the stock file
        for item, amount in self.items.items():
            for i, line in enumerate(lines):
                if item in line:
                    # simple string manipulation
                    lineParts = line.split(",")
                    # simple indexing to omit the newline character
                    lineParts[1] = str(int(lineParts[1][:-1]) - amount)
                    lines[i] = ",".join(lineParts)
                    lines[i] += "\n"

        # write the updated stock file
        with open(STOCK_FILE, "w") as file:
            file.writelines(lines)

    def storeDetails(self):
        # more string manipulation, using str() on a dict to convert it to a string, quite interesting as I have never done this before
        order = f"\n{self.name}, {str(self.recieptID)}, {str(self.items)}"

        with open(CUSTOMERS_FILE, "a") as file:
            file.write(order)


# https://customtkinter.tomschimansky.com/tutorial/spinbox


# I changed a few things in the customtkinter tutorial code to suit my needs, I have added comments where I have done so
# -----------------------Start of code used from customtkinter tutorial-------------------------------
class WidgetName(customtkinter.CTkFrame):
    def __init__(self, *args, width: int = 100, height: int = 32, **kwargs):
        super().__init__(*args, width=width, height=height, **kwargs)


class FloatSpinbox(customtkinter.CTkFrame):
    def __init__(
        self,
        *args,
        width: int = 100,
        height: int = 32,
        step_size: Union[int, float] = 1,
        command: Callable = None,
        **kwargs,
    ):
        super().__init__(*args, width=width, height=height, **kwargs)

        self.step_size = step_size
        self.command = command

        self.configure(fg_color=("gray78", "gray28"))  # set frame color

        self.grid_columnconfigure((0, 2), weight=0)  # buttons don't expand
        self.grid_columnconfigure(1, weight=1)  # entry expands

        self.subtract_button = customtkinter.CTkButton(
            self,
            text="-",
            width=height - 6,
            height=height - 6,
            command=self.subtract_button_callback,
        )
        self.subtract_button.grid(row=0, column=0, padx=(3, 0), pady=3)

        self.entry = customtkinter.CTkEntry(
            self, width=width - (2 * height), height=height - 6, border_width=0
        )
        self.entry.grid(row=0, column=1, columnspan=1, padx=3, pady=3, sticky="ew")

        self.add_button = customtkinter.CTkButton(
            self,
            text="+",
            width=height - 6,
            height=height - 6,
            command=self.add_button_callback,
        )
        self.add_button.grid(row=0, column=2, padx=(0, 3), pady=3)

        # default value changed to 0 from 35
        self.entry.insert(0, "0")

    def add_button_callback(self):
        if self.command is not None:
            self.command()
        try:
            value = int(self.entry.get()) + self.step_size
            self.entry.delete(0, "end")
            self.entry.insert(0, value)
        except ValueError:
            return

    def subtract_button_callback(self):
        if self.command is not None:
            self.command()
        try:
            value = (
                # changed from float to int
                int(self.entry.get()) - self.step_size
                # added an if statement to make sure the value is not less than 0
                if int(self.entry.get()) > 0
                else 0
            )
            self.entry.delete(0, "end")
            self.entry.insert(0, value)
        except ValueError:
            return

    def get(self) -> Union[int, None]:
        try:
            return int(self.entry.get())
        except ValueError:
            return None

    def set(self, value: int):
        self.entry.delete(0, "end")
        self.entry.insert(0, str(int(value)))


# -----------------------End of code used from customtkinter tutorial-------------------------------

# Using customtkinter format conventions from https://customtkinter.tomschimansky.com/tutorial/frames

# create list to store customers and only customers
customers: List[Customer] = []


# define the App class
class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # configure window
        self.title("Julie's Party Hire Store")
        self.geometry("600x750")
        self.resizable(width=False, height=False)

        # create widgets
        # create name entry
        self.nameLabel = customtkinter.CTkLabel(self, text="Name:")
        self.nameLabel.grid(row=0, column=0, padx=20, pady=20)
        self.name = customtkinter.CTkEntry(self, width=150, height=30, border_width=0)
        self.name.grid(row=0, column=1, padx=20, pady=20)

        # create item entrys
        self.itemImageImports = [
            customtkinter.CTkImage(
                light_image=Image.open(ITEM_IMAGES[i]),
                dark_image=Image.open(ITEM_IMAGES[i]),
                size=(100, 100),
            )
            for i in range(6)
        ]
        self.itemImages = [
            customtkinter.CTkLabel(self, image=self.itemImageImports[i], text="")
            for i in range(6)
        ]
        self.itemNameLabels = [
            customtkinter.CTkLabel(self, text=ITEM_NAMES[i]) for i in range(6)
        ]
        self.items = [FloatSpinbox(self, width=150, step_size=1) for i in range(6)]

        topRowOffset = 3 * 1  # 3 rows, 1 empty row

        for i, item in enumerate(self.itemNameLabels):
            item.grid(
                # use topRowOffset so there is an empty row for the name
                # used i%3 to make sure there are 3 items in each column
                # used i//3 to make sure that every 3 items, it goes to a new row
                # used *3 to leave a space for the items and images in between
                row=((i + topRowOffset) // 3) * 3,
                column=i % 3,
                padx=20,
                pady=20,
            )
        for i, item in enumerate(self.itemImages):
            item.grid(
                # use topRowOffset so there is an empty row for the name
                # used i%3 to make sure there are 3 items in each column
                # used i//3 to make sure that every 3 items, it goes to a new row
                # used +1 for rows to offset item images from item names
                # used *3 to leave a space for the items and labels in between
                row=((i + topRowOffset) // 3) * 3 + 1,
                column=i % 3,
                padx=20,
                pady=20,
            )
        for i, item in enumerate(self.items):
            item.grid(
                # use topRowOffset so there is an empty row for the name
                # used i%3 to make sure there are 3 items in each column
                # used i//3 to make sure that every 3 items, it goes to a new row
                # used +2 for rows to offset items from item names and images
                # used *3 to leave a space for the item names and images in between
                row=((i + topRowOffset) // 3) * 3 + 2,
                column=i % 3,
                padx=20,
                pady=20,
            )

        # create submit button that calls submitNewOrder when pressed
        self.submitButton = customtkinter.CTkButton(
            self, text="Submit", command=self.submitNewOrder
        )
        self.submitButton.grid(row=10, column=1, padx=20, pady=20)

    # finish the transaction by storing the order in a file and showing the reciept
    def submitNewOrder(self):
        # check if order is valid
        if self.orderValidation():
            # use of global variable
            global customers
            name = self.name.get()
            ID = random.randint(1000, 9999)
            items = {}
            for i, item in enumerate(self.items):
                if item.get() is not None:
                    items[ITEM_NAMES[i]] = item.get()

            customers.append(Customer(name, ID, items))

            # use negative index to get the most recent customer
            self.showReciept(customers[-1])

    def orderValidation(self):
        # check if name is valid
        if self.name.get() == "":
            self.popup("Please enter a name")
            return False
        elif self.name.get().isnumeric():
            self.popup("Please enter a valid name")
            return False
        elif " " not in self.name.get():
            self.popup("Please enter your full name")
            return False

        # check if at least one item is has an amount more than 0
        validItems = False
        for item in self.items:
            # try to convert to int or return false
            try:
                if item.get() is not None and int(item.get()) > 0:
                    validItems = True
            except ValueError:
                self.popup("Please enter a valid\n amount for each item")
                return False

        if not validItems:
            self.popup("Please enter a valid\n amount for each item")
            return False
        
        # Check stock level
        for i, item in enumerate(self.items):
            amount = item.get()
            if int(amount) > stock[ITEM_NAMES[i]]:
                self.popup(f"Insufficient stock for {ITEM_NAMES[i].lower()}")
                return False

        return True

    def popup(self, message: str):
        popup = customtkinter.CTkToplevel(self)
        popup.geometry("200x100")
        popup.resizable(width=False, height=False)
        popup.title("Error")
        customtkinter.CTkLabel(popup, text=message).pack()
        customtkinter.CTkButton(popup, text="Ok", command=popup.destroy).pack()

    # show the reciept for the customer
    def showReciept(self, customer: Customer):
        # remove old widgets
        self.name.grid_forget()
        self.nameLabel.grid_forget()
        for item in self.itemNameLabels:
            item.grid_forget()
        for item in self.items:
            item.grid_forget()
        self.submitButton.grid_forget()

        # create reciept widget
        self.reciept = customtkinter.CTkLabel(
            self,
            # use of \ to make a new line in the code not the output
            text=f"Reciept:\n\
Full Name: {customer.name}\n\
Reciept ID: {customer.recieptID}\n\
Items: \n{self.formatItems(customer.items)}",
            width=300,
            justify="left",
        )
        self.reciept.grid(row=0, column=1, padx=20, pady=20)

        # create close button that calls closeWindow when pressed
        self.closeButton = customtkinter.CTkButton(
            self, text="Close", command=self.closeWindow
        )
        self.closeButton.grid(row=1, column=1, padx=20, pady=20)

    # format the items for the reciept
    def formatItems(self, items: dict):
        output = ""
        # iterating through dict
        for item, amount in items.items():
            if amount > 0:
                output += f"{item}: {amount}\n"
        return output

    def closeWindow(self):
        # destroy the window
        self.destroy()


# start the app
app = App()
app.mainloop()
