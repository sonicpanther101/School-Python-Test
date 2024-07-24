import csv
import math

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
                "itemsCurrentlyRented": {}
            }
        pastCustomerOrders[order[0]]["recieptIDs"].append(order[1])
        itemsCurrentlyRented = {key: int(value) for key, value in eval(order[2]).items()}
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
                    lines[i]+="\n"

        with open(STOCK_FILE, "w") as file:
            file.writelines(lines)

    def storeDetails(self):
        order = f"\n{self.name}, {str(self.recieptID)}, {str(self.items)}"
        print(order)
        with open(CUSTOMERS_FILE, "a") as file:
            file.write(order)


customers = Customers("name", 1567654356, {"test1":50})