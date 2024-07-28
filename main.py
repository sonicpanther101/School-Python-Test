"""to read and write csv files"""

import csv
from ast import literal_eval
from typing import (
    Union,
    Callable,
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
    "Napkin Rings",
]

ITEM_IMAGES = [f"images/{ITEM_NAME}.png" for ITEM_NAME in ITEM_NAMES]


def load_past_customer_orders():
    """Needed to load past customer orders from file, used in App.show_orders_page()"""
    past_customer_orders = []
    # open file and read each line
    with open(CUSTOMERS_FILE, "r", encoding="utf-8") as data:
        for order in csv.reader(data):
            # if the order has at least 3 items (a valid order)
            if len(order) >= 3:
                # create a new Customer object for each order with some funky indexing
                past_customer_orders.append(
                    Customer(
                        order[0], order[1], literal_eval(",".join(order[2:])), "init"
                    )
                )

    # reverse the list so the most recent order is at the top
    return past_customer_orders[::-1]


def load_stock():
    """Needed to load stock from file, used when
    the user inputs a new order with too many items"""
    initial_stock = {}
    # open file and read each line
    with open(STOCK_FILE, "r", encoding="utf-8") as data1:
        for item in csv.reader(data1):
            # write the stock to a dictionary
            initial_stock[item[0]] = int(item[1])
    return initial_stock


def reset_stock():
    """for testing or for on an admin page if I added that
    https://www.w3schools.com/python/python_file_write.asp"""

    # open file and write each line to the default stock
    with open(STOCK_FILE, "w", encoding="utf-8") as file:
        file.writelines(
            [
                "Chairs,500\n",
                "Tables,500\n",
                "Cutlery Sets,500\n",
                "BBQs,500\n",
                "Table Cloths,500\n",
                "Napkin Rings,500\n",
            ]
        )


# if the stock file is empty, reset it

# with open(STOCK_FILE, "r", encoding="utf-8") as data2:
#     for item1 in csv.reader(data2):
#         if int(item1[1]) == 0:
#             reset_stock()


class Customer:
    """customer class to store order details"""

    # initialise a customers order
    def __init__(self, name, order_id, items, mode="normal"):
        # store order details to object
        self.name = name
        self.receipt_id = order_id
        self.items = items

        # use this to avoid updating the stock upon addingpast orders from the file
        # this caused serious issues before I added it
        # it would recursively update the stock and cause an infinite loop
        # it made the cusomers file 2.5gb, which is not ideal
        if mode != "init":
            self.update_stock()
            self.store_details()

    def update_stock(self):
        """update the stock file"""

        # open file and read each line
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
        order = f"\n{self.name}, {str(self.receipt_id)}, {str(self.items)}"

        # open file and write new line
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
customers = load_past_customer_orders()

# create dictionary to store stock in a item:quantity format
stock = load_stock()


class OrdersFrame(customtkinter.CTkScrollableFrame):
    """Orders Frame"""

    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.orders = []
        self.order_remove_buttons = []

    def update_orders(self):
        """update orders"""

        # create orders widget
        self.orders = [
            customtkinter.CTkLabel(
                self,
                # use of \ to make a new line in the code not the output
                text=f"Receipt:\n\
Full Name: {customer.name}\n\
Receipt ID: {customer.receipt_id}\n\
Items: \n{format_items(customer.items)}",
                width=300,
                justify="left",
            )
            for customer in customers
        ]

        # add orders to grid
        for i, item in enumerate(self.orders):
            item.grid(row=i, column=0, padx=0, pady=10)

        # create remove buttons
        self.order_remove_buttons = [
            customtkinter.CTkButton(
                self,
                text="",
                command=lambda i=i: app.remove_order(i),
                width=40,
            )
            for i in range(len(self.orders))
        ]

        # add remove buttons to grid
        for i, item in enumerate(self.order_remove_buttons):
            item.grid(row=i, column=1, padx=0, pady=0)


# define the App class
class App(customtkinter.CTk):
    """main application"""

    def __init__(self):
        super().__init__()

        # configure window
        self.title("Julie's Party Hire Store")
        self.geometry("600x800")
        self.resizable(width=False, height=False)
        self.order_to_remove = None

        # create widgets, not adding them to the grid yet
        self.current_page = "add_order_page"

        # create stock list
        self.stock = customtkinter.CTkLabel(self, text="Stock:")

        # create close button that calls close_window when pressed
        self.close_button = customtkinter.CTkButton(
            self, text="Close", command=self.close_window
        )
        self.close_button.grid(row=0, column=2, padx=20, pady=20)

        # create swap page button that calls show_orders_page when pressed
        # by default and add_order_page when pressed once
        self.swap_page_button = customtkinter.CTkButton(
            self, text="Show Orders", command=self.swap_page
        )
        self.swap_page_button.grid(row=1, column=2, padx=20, pady=20)

        # create name entry
        self.name_label = customtkinter.CTkLabel(self, text="Full Name:")
        self.name = customtkinter.CTkEntry(self, width=150, height=30, border_width=0)

        # create receipt ID entry
        self.receipt_id_label = customtkinter.CTkLabel(self, text="Receipt ID:")
        self.receipt_id = customtkinter.CTkEntry(
            self, width=150, height=30, border_width=0
        )

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
        self.item_name_labels = [
            customtkinter.CTkLabel(self, text=ITEM_NAMES[i]) for i in range(6)
        ]
        self.items = [FloatSpinbox(self, width=150, step_size=1) for i in range(6)]

        # create submit button that calls submit_new_order when pressed
        self.submit_button = customtkinter.CTkButton(
            self, text="Add Order", command=self.submit_new_order
        )

        # create orders frame
        self.orders_frame = OrdersFrame(master=self, width=350, height=750)

        # add widgets to grid for the add order page
        self.add_order_page()

    def swap_page(self):
        """swaps the current page"""
        if self.current_page == "add_order_page":
            # change the text of the button
            self.swap_page_button.configure(text="Show Add Order Page")
            self.current_page = "show_orders_page"
            # call show_orders_page
            self.show_orders_page()
        elif self.current_page == "show_orders_page":
            # change the text of the button
            self.swap_page_button.configure(text="Show Orders")
            self.current_page = "add_order_page"
            # call add_order_page
            self.add_order_page()

    def add_order_page(self):
        """page to add an order"""

        # clear all items from other pages in the grid
        self.orders_frame.grid_forget()
        self.stock.grid_forget()

        # add widgets to grid for the add order page
        self.name_label.grid(row=0, column=0, padx=20, pady=20)
        self.name.grid(row=0, column=1, padx=20, pady=20)

        self.receipt_id_label.grid(row=1, column=0, padx=20, pady=20)
        self.receipt_id.grid(row=1, column=1, padx=20, pady=20)

        top_row_offset = 3 * 2  # 3 empty columns, 2 empty rows

        for i, item in enumerate(self.item_name_labels):
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

        self.submit_button.grid(row=13, column=1, padx=20, pady=20)

    # finish the transaction by storing the order in a file and showing the receipt
    def submit_new_order(self):
        """finish the transaction by checking the order and
        storing the order in a file and showing the past orders"""
        # check if order is valid
        if self.order_validation():
            # store the order details
            name = self.name.get()
            new_order_id = self.receipt_id.get()
            items = {}
            for i, item in enumerate(self.items):
                if item.get() is not None:
                    # nested dictionary
                    items[ITEM_NAMES[i]] = item.get()

            # use of global variable
            # using insert(0) so that the new order is at the top
            customers.insert(0, Customer(name, new_order_id, items))

            # show the past orders including the new order
            self.show_orders_page()

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

        # check if receipt ID is valid
        if self.receipt_id.get() == "":
            self.popup("Please enter a receipt ID")
            return False
        # better version of checking if receipt ID is numeric than try else
        if self.receipt_id.get().isnumeric() is False:
            self.popup("Please enter a valid receipt ID")
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

        # create new window
        popup = customtkinter.CTkToplevel(self)
        popup.geometry("200x100")
        popup.resizable(width=False, height=False)
        popup.title("Error")

        # set the popup message
        customtkinter.CTkLabel(popup, text=message).pack()
        customtkinter.CTkButton(popup, text="Ok", command=popup.destroy).pack()

    def show_orders_page(self):
        """show the orders for the customer"""
        # remove old widgets
        self.name.grid_forget()
        self.name_label.grid_forget()
        for item in self.item_name_labels:
            item.grid_forget()
        for item in self.items:
            item.grid_forget()
        for item in self.item_images:
            item.grid_forget()
        self.submit_button.grid_forget()
        self.receipt_id.grid_forget()
        self.receipt_id_label.grid_forget()

        # show the stock of each item
        self.stock.grid(row=2, column=2, padx=20, pady=20)

        self.stock.configure(text=f"Stock:\n{format_items(stock)}")

        # show orders
        self.orders_frame.update_orders()
        self.orders_frame.grid(row=0, column=0, padx=20, pady=20, rowspan=100)

    def remove_order(self, i: int):
        """remove the order"""
        # set the order to remove for later
        self.order_to_remove = i

        # ask for confirmation
        self.confirm_action(
            f"remove order{customers[i].receipt_id}", self.confirmed_remove_order
        )

    def confirmed_remove_order(self):
        """once confirmed, remove the order"""

        # check that the order exists
        if self.order_to_remove >= len(customers):
            self.popup("Order does not exist")
            return

        # update the stock file
        with open(STOCK_FILE, "r", encoding="utf-8") as file:
            lines = file.readlines()

        # go through each item in the order check if it is in each line of the stock file
        for item, amount in customers[self.order_to_remove].items.items():
            for i, line in enumerate(lines):
                if item in line:
                    # simple string manipulation
                    line_parts = line.split(",")
                    # simple indexing to omit the newline character
                    line_parts[1] = str(int(line_parts[1][:-1]) + amount)
                    lines[i] = ",".join(line_parts)
                    lines[i] += "\n"

        # write the updated stock file
        with open(STOCK_FILE, "w", encoding="utf-8") as file:
            file.writelines(lines)

        # update the customer file
        with open(CUSTOMERS_FILE, "r", encoding="utf-8") as file:
            lines = file.readlines()

        # remove the order from the customer file
        for i, line in enumerate(lines):
            if (
                str(customers[self.order_to_remove].receipt_id) in line
                and customers[self.order_to_remove].name in line
            ):
                lines.pop(i)

        # write the updated customer file
        with open(CUSTOMERS_FILE, "w", encoding="utf-8") as file:
            file.writelines(lines)

        # remove the customer from the list
        customers.pop(self.order_to_remove)
        self.order_to_remove = None

        # bad fix to reload the page after removing an order
        self.add_order_page()
        self.show_orders_page()

    def confirm_action(self, action: str, function: Callable):
        """confirm if the user wants to perform an action"""

        # create new window
        confirm = customtkinter.CTkToplevel(self)
        confirm.geometry("300x150")
        confirm.resizable(width=False, height=False)
        confirm.title("Confirm")

        # set the message
        customtkinter.CTkLabel(
            confirm, text=f"Are you sure you want to \n{action}?"
        ).pack()
        customtkinter.CTkButton(confirm, text="No", command=confirm.destroy).pack()
        # using blank label to leave gap between buttons
        customtkinter.CTkLabel(confirm, text="").pack()

        # cool passing 2 functions as argument using lambda
        customtkinter.CTkButton(
            confirm,
            text="Yes",
            command=lambda: [confirm.destroy(), function()],
        ).pack()

    def close_window(self):
        """closes the window"""
        # destroy the window
        self.destroy()


def format_items(items: dict):
    """format the items for the receipt"""
    output = ""
    # iterating through dict
    for item, amount in items.items():
        if amount > 0:
            output += f"{item}: {amount}\n"
    return output


# start the app
app = App()
app.mainloop()
