import csv
import math
import customtkinter
from typing import Union
from typing import Callable

# https://www.geeksforgeeks.org/load-csv-data-into-list-and-dictionary-using-python/

CUSTOMERS_FILE = "customers.csv"
STOCK_FILE = "stock.csv"


# load past customer orders
pastCustomerOrders = {}
with open(CUSTOMERS_FILE, "r") as data:
    for order in csv.reader(data):
        if order[0] not in pastCustomerOrders:
            pastCustomerOrders[order[0]] = {
                "recieptIDs": [],
                "itemsCurrentlyRented": {},
            }
        pastCustomerOrders[order[0]]["recieptIDs"].append(order[1])
        itemsCurrentlyRented = {
            key: int(value) for key, value in eval(order[2]).items()
        }
        for item, amount in itemsCurrentlyRented.items():
            if item in pastCustomerOrders[order[0]]["itemsCurrentlyRented"]:
                pastCustomerOrders[order[0]]["itemsCurrentlyRented"][item] += amount
            else:
                pastCustomerOrders[order[0]]["itemsCurrentlyRented"][item] = amount


def resetStock():
    # https://www.w3schools.com/python/python_file_write.asp
    with open(STOCK_FILE, "w") as file:
        file.write("test1,100\n")
        file.write("test2,100\n")
        file.write("test3,100\n")
        file.write("test4,100\n")
        file.write("test5,100\n")


class Customers:
    def __init__(self, name, ID, items):
        self.name = name
        self.recieptID = ID
        self.items = items

        self.updateStock()
        self.storeDetails()

    def updateStock(self):
        with open(STOCK_FILE, "r") as file:
            lines = file.readlines()

        for item, amount in self.items.items():
            for i, line in enumerate(lines):
                if item in line:
                    lineParts = line.split(",")
                    lineParts[1] = str(int(lineParts[1]) - amount)
                    lines[i] = ",".join(lineParts)
                    lines[i] += "\n"

        with open(STOCK_FILE, "w") as file:
            file.writelines(lines)

    def storeDetails(self):
        order = f"\n{self.name}, {str(self.recieptID)}, {str(self.items)}"
        print(order)
        with open(CUSTOMERS_FILE, "a") as file:
            file.write(order)


# https://customtkinter.tomschimansky.com/tutorial/spinbox

class WidgetName(customtkinter.CTkFrame):
    def __init__(self, *args,
                 width: int = 100,
                 height: int = 32,
                 **kwargs):
        super().__init__(*args, width=width, height=height, **kwargs)

class FloatSpinbox(customtkinter.CTkFrame):
    def __init__(self, *args,
                 width: int = 100,
                 height: int = 32,
                 step_size: Union[int, float] = 1,
                 command: Callable = None,
                 **kwargs):
        super().__init__(*args, width=width, height=height, **kwargs)

        self.step_size = step_size
        self.command = command

        self.configure(fg_color=("gray78", "gray28"))  # set frame color

        self.grid_columnconfigure((0, 2), weight=0)  # buttons don't expand
        self.grid_columnconfigure(1, weight=1)  # entry expands

        self.subtract_button = customtkinter.CTkButton(self, text="-", width=height-6, height=height-6,
                                                       command=self.subtract_button_callback)
        self.subtract_button.grid(row=0, column=0, padx=(3, 0), pady=3)

        self.entry = customtkinter.CTkEntry(self, width=width-(2*height), height=height-6, border_width=0)
        self.entry.grid(row=0, column=1, columnspan=1, padx=3, pady=3, sticky="ew")

        self.add_button = customtkinter.CTkButton(self, text="+", width=height-6, height=height-6,
                                                  command=self.add_button_callback)
        self.add_button.grid(row=0, column=2, padx=(0, 3), pady=3)

        # default value
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
            value = int(self.entry.get()) - self.step_size if int(self.entry.get()) > 0 else 0
            self.entry.delete(0, "end")
            self.entry.insert(0, value)
        except ValueError:
            return

    def get(self) -> Union[float, None]:
        try:
            return float(self.entry.get())
        except ValueError:
            return None

    def set(self, value: float):
        self.entry.delete(0, "end")
        self.entry.insert(0, str(float(value)))


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title("my app")
        self.geometry("400x400")
        # self.grid_columnconfigure(3, weight=1)
        # self.grid_rowconfigure((0, 0), weight=1)

        self.items = [FloatSpinbox(self, width=150, step_size=1) for i in range(6)]

        for i, item in enumerate(self.items):
            item.grid(row=i//3, column=i%3, padx=20, pady=20)

    def submitNewOrder(name, ID, items):
        customer = Customers(name, ID, items)


    

    # button = customtkinter.CTkButton(
    #     app, text="Submit", command=submitNewOrder(name, ID, items)
    # )
    # button.grid(row=0, column=0, padx=20, pady=20)

    # app.mainloop()


app = App()
app.mainloop()