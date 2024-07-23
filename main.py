import csv

# https://www.geeksforgeeks.org/load-csv-data-into-list-and-dictionary-using-python/

CUSTOMERS_FILE = "customers.csv"
STOCK_FILE = "stock.csv"


pastCustomerOrders = {}
with open(CUSTOMERS_FILE,'r') as data:

    for order in csv.reader(data):
        print(order)
        pastCustomerOrders[order[0]]["recieptIDs"] = order[1]
        pastCustomerOrders[order[0]]["itemsCurrentlyRented"] = order[2]

class Customers:
    def __init__(self, name, ID, items, amounts):
        self.name = name
        self.recieptID = ID
        self.items = items
        self.amounts = amounts

        self.updateStock()
        self.storeDetails()

    def updateStock(self):
