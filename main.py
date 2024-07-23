import csv

# https://www.geeksforgeeks.org/load-csv-data-into-list-and-dictionary-using-python/

CUSTOMERS_FILE = "customers.csv"
STOCK_FILE = "stock.csv"


pastCustomerOrders = {}
with open(CUSTOMERS_FILE, "r") as data:
    for order in csv.reader(data):
        if order[0] not in pastCustomerOrders:
            pastCustomerOrders[order[0]] = {
                "recieptIDs": [],
                "itemsCurrentlyRented": {}
            }
        pastCustomerOrders[order[0]]["recieptIDs"].append(order[1])
        items_currently_rented = {key: int(value) for key, value in eval(order[2]).items()}
        for item, amount in items_currently_rented.items():
            if item in pastCustomerOrders[order[0]]["itemsCurrentlyRented"]:
                pastCustomerOrders[order[0]]["itemsCurrentlyRented"][item] += amount
            else:
                pastCustomerOrders[order[0]]["itemsCurrentlyRented"][item] = amount

print(pastCustomerOrders)


class Customers:
    def __init__(self, name, ID, items, amounts):
        self.name = name
        self.recieptID = ID
        self.items = items
        self.amounts = amounts

        self.updateStock()
        self.storeDetails()

    def updateStock(self):
        pass
