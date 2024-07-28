"""to read and write csv files"""
import csv
from ast import literal_eval
from typing import (
    Union,
    Callable,
    List,
)  # to use FloatSpinbox from the customtkinter tutorial
import customtkinter  # a more modern tkinter
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
    "Napkin Rings"
]

ITEM_IMAGES = [f"images/{ITEM_NAME}.png" for ITEM_NAME in ITEM_NAMES]

def load_past_customer_orders():
    """Needed to load past customer orders from file, used in App.show_orders()"""
    past_customer_orders = []
    with open(CUSTOMERS_FILE, "r", encoding="utf-8") as data:
        for order in csv.reader(data):

            if len(order) == 3:
                # create a new Customer object for each order
                past_customer_orders.append(Customer(order[0], order[1], literal_eval(order[2])))

    return past_customer_orders


def load_stock():
    """Needed to load stock from file, used when 
    the user inputs a new order with too many items"""
    initial_stock = {}
    with open(STOCK_FILE, "r", encoding="utf-8") as data:
        for item in csv.reader(data):
            stock[item[0]] = int(item[1])
    return initial_stock


stock = load_stock()


def reset_stock():
    """for testing or for on an admin page if I added that
    https://www.w3schools.com/python/python_file_write.asp"""
    with open(STOCK_FILE, "w", encoding="utf-8") as file:
        file.writelines(
            [
                "Chairs,100\n",
                "Tables,100\n",
                "Cutlery Sets,100\n",
                "BBQs,100\n",
                "Table Cloths,100\n",
                "Napkin Rings,100\n",
            ]
        )


class Customer:
    """customer class to store order details"""
    # initialise a customers order
    def __init__(self, name, order_id, items):
        # store order details to object
        self.name = name
        self.reciept_id = order_id
        self.items = items

        self.update_stock()
        self.store_details()

    def update_stock(self):
        """update the stock file"""
        with open(STOCK_FILE, "r", encoding="utf-8") as file:
            lines = file.readlines()

        # go through each item in the order check if it is in each line of the stock file
        for item, amount in self.items.items():
            for i, line in enumerate(lines):
                if item in line:
                    # simple string manipulation
                    line_parts = line.split(",")
                    # simple indexing to omit the newline character
                    line_parts[1] = str(int(line_parts[1][:-1]) - amount)
                    lines[i] = ",".join(line_parts)
                    lines[i] += "\n"

        # write the updated stock file
        with open(STOCK_FILE, "w", encoding="utf-8") as file:
            file.writelines(lines)

    def store_details(self):
        """store customer details to file"""
        # more string manipulation, using str() on a dict to convert it to a string
        # this is quite interesting as I have never done this before
        order = f"\n{self.name}, {str(self.reciept_id)}, {str(self.items)}"

        with open(CUSTOMERS_FILE, "a", encoding="utf-8") as file:
            file.write(order)


# https://customtkinter.tomschimansky.com/tutorial/spinbox


# I changed a few things in the customtkinter tutorial code
# to suit my needs, I have added comments where I have done so
# ---------Start of code used from customtkinter tutorial--------
class WidgetName(customtkinter.CTkFrame):
    """Custom widget name"""
    def __init__(self, *args, width: int = 100, height: int = 32, **kwargs):
        super().__init__(*args, width=width, height=height, **kwargs)


class FloatSpinbox(customtkinter.CTkFrame):
    """Custom float spinbox widget"""
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
        """increment value"""
        if self.command is not None:
            self.command()
        try:
            value = int(self.entry.get()) + self.step_size
            self.entry.delete(0, "end")
            self.entry.insert(0, value)
        except ValueError:
            return

    def subtract_button_callback(self):
        """increment value"""
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
        """get value"""
        try:
            return int(self.entry.get())
        except ValueError:
            return None

    def set(self, value: int):
        """set value"""
        self.entry.delete(0, "end")
        self.entry.insert(0, str(int(value)))


# -----------------------End of code used from customtkinter tutorial-------------------------------

# Using customtkinter format conventions from:
# https://customtkinter.tomschimansky.com/tutorial/frames

# create list to store customers and only customers
customers: List[Customer] = load_past_customer_orders()


# define the App class
class App(customtkinter.CTk):
    """main application"""
    def __init__(self):
        super().__init__()

        # configure window
        self.title("Julie's Party Hire Store")
        self.geometry("600x800")
        self.resizable(width=False, height=False)

        # create widgets
        self.reciept = customtkinter.CTkLabel(self)

        # create close button that calls close_window when pressed
        self.close_button = customtkinter.CTkButton(
            self, text="Close", command=self.close_window
        )
        self.close_button.grid(row=1, column=1, padx=20, pady=20)

        # create name entry
        self.name_label = customtkinter.CTkLabel(self, text="Name:")
        self.name_label.grid(row=0, column=0, padx=20, pady=20)
        self.name = customtkinter.CTkEntry(self, width=150, height=30, border_width=0)
        self.name.grid(row=0, column=1, padx=20, pady=20)

        # create reciept ID entry
        self.reciept_id_label = customtkinter.CTkLabel(self, text="Reciept ID:")
        self.reciept_id_label.grid(row=1, column=0, padx=20, pady=20)
        self.reciept_id = customtkinter.CTkEntry(
            self, width=150, height=30, border_width=0
        )
        self.reciept_id.grid(row=1, column=1, padx=20, pady=20)

        # create item entrys
        self.item_image_imports = [
            customtkinter.CTkImage(
                light_image=Image.open(ITEM_IMAGES[i]),
                dark_image=Image.open(ITEM_IMAGES[i]),
                size=(100, 100),
            )
            for i in range(6)
        ]
        self.item_images = [
            customtkinter.CTkLabel(self, image=self.item_image_imports[i], text="")
            for i in range(6)
        ]
        self.itemname_labels = [
            customtkinter.CTkLabel(self, text=ITEM_NAMES[i]) for i in range(6)
        ]
        self.items = [FloatSpinbox(self, width=150, step_size=1) for i in range(6)]

        top_row_offset = 3 * 2  # 3 empty columns, 2 empty rows

        for i, item in enumerate(self.itemname_labels):
            item.grid(
                # use top_row_offset so there is an empty row for the name
                # used i%3 to make sure there are 3 items in each column
                # used i//3 to make sure that every 3 items, it goes to a new row
                # used *3 to leave a space for the items and images in between
                row=((i + top_row_offset) // 3) * 3,
                column=i % 3,
                padx=20,
                pady=20,
            )
        for i, item in enumerate(self.item_images):
            item.grid(
                # use top_row_offset so there is an empty row for the name
                # used i%3 to make sure there are 3 items in each column
                # used i//3 to make sure that every 3 items, it goes to a new row
                # used +1 for rows to offset item images from item names
                # used *3 to leave a space for the items and labels in between
                row=((i + top_row_offset) // 3) * 3 + 1,
                column=i % 3,
                padx=20,
                pady=20,
            )
        for i, item in enumerate(self.items):
            item.grid(
                # use top_row_offset so there is an empty row for the name
                # used i%3 to make sure there are 3 items in each column
                # used i//3 to make sure that every 3 items, it goes to a new row
                # used +2 for rows to offset items from item names and images
                # used *3 to leave a space for the item names and images in between
                row=((i + top_row_offset) // 3) * 3 + 2,
                column=i % 3,
                padx=20,
                pady=20,
            )

        # create submit button that calls submit_new_order when pressed
        self.submit_button = customtkinter.CTkButton(
            self, text="Add Order", command=self.submit_new_order
        )
        self.submit_button.grid(row=13, column=1, padx=20, pady=20)

    # finish the transaction by storing the order in a file and showing the reciept
    def submit_new_order(self):
        """finish the transaction by checking the order and 
        storing the order in a file and showing the past orders"""
        # check if order is valid
        if self.order_validation():
            name = self.name.get()
            new_order_id = self.reciept_id.get()
            items = {}
            for i, item in enumerate(self.items):
                if item.get() is not None:
                    items[ITEM_NAMES[i]] = item.get()

            # use of global variable
            customers.append(Customer(name, new_order_id, items))

            # use negative index to get the most recent customer
            self.show_reciept(customers[-1])

    def order_validation(self):
        """check if order is valid"""
        # check if name is valid
        if self.name.get() == "":
            self.popup("Please enter a name")
            return False
        if self.name.get().isnumeric():
            self.popup("Please enter a valid name")
            return False
        if " " not in self.name.get():
            self.popup("Please enter your full name")
            return False

        # check if reciept ID is valid
        if self.reciept_id.get() == "":
            self.popup("Please enter a reciept ID")
            return False
        # better version of checking if reciept ID is numeric than try else
        if self.reciept_id.get().isnumeric() is False:
            self.popup("Please enter a valid reciept ID")
            return False

        # check if at least one item is has an amount more than 0
        valid_items = False
        for item in self.items:
            # try to convert to int or return false
            try:
                if item.get() is not None and int(item.get()) > 0:
                    valid_items = True
            except ValueError:
                self.popup("Please enter a valid\n amount for each item")
                return False

        if not valid_items:
            self.popup("Please add some items\n to your order")
            return False

        # Check stock level
        for i, item in enumerate(self.items):
            amount = item.get()
            if int(amount) > stock[ITEM_NAMES[i]]:
                self.popup(
                    f"Insufficient stock for {ITEM_NAMES[i].lower()}\n{stock[ITEM_NAMES[i]]} \
                    {ITEM_NAMES[i].lower()} available"
                )
                return False

        return True

    def popup(self, message: str):
        """show error popup"""
        popup = customtkinter.CTkToplevel(self)
        popup.geometry("200x100")
        popup.resizable(width=False, height=False)
        popup.title("Error")
        customtkinter.CTkLabel(popup, text=message).pack()
        customtkinter.CTkButton(popup, text="Ok", command=popup.destroy).pack()

    def show_reciept(self, customer: Customer):
        """show the reciept for the customer"""
        # remove old widgets
        self.name.grid_remove()
        self.name_label.grid_remove()
        for item in self.itemname_labels:
            item.grid_remove()
        for item in self.items:
            item.grid_remove()
        self.submit_button.grid_remove()

        # create reciept widget
        self.reciept = customtkinter.CTkLabel(
            self,
            # use of \ to make a new line in the code not the output
            text=f"Reciept:\n\
Full Name: {customer.name}\n\
Reciept ID: {customer.reciept_id}\n\
Items: \n{self.format_items(customer.items)}",
            width=300,
            justify="left",
        )
        self.reciept.grid(row=0, column=1, padx=20, pady=20)

    def format_items(self, items: dict):
        """format the items for the reciept"""
        output = ""
        # iterating through dict
        for item, amount in items.items():
            if amount > 0:
                output += f"{item}: {amount}\n"
        return output

    def close_window(self):
        """close the window"""
        # destroy the window
        self.destroy()


# start the app
app = App()
app.mainloop()
