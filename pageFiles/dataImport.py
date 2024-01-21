import csv
import sqlite3

with sqlite3.connect("database/inventoryDatabase.db") as db:
    myCursor = db.cursor()


with open("Sales.csv") as salesCSV:
    csvReader = csv.reader(salesCSV, delimiter=",")
    for row in csvReader:
        insert = "INSERT INTO Sales(salesID, orderNumber, staffID, itemID, locationOfSale, dateOfSale, quantity, priceOfSale)VALUES(?,?,?,?,?,?,?,?)"
        myCursor.execute(
            insert,
            [
                (row[0]),
                (row[1]),
                (row[2]),
                (row[3]),
                (row[4]),
                (row[5]),
                (row[6]),
                (row[7]),
            ],
        )
        db.commit()
"""
with open("csvTestData/Items.csv") as csvFile:
    csvReader = csv.reader(csvFile, delimiter=",")
    for row in csvReader:
        insert = "INSERT INTO Items(itemName, sku, price, quantity, numberSold, createdBy, updatedBy, createdAt, updatedAt, sizes) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
        myCursor.execute(
            insert,
            [
                (row[1]),
                (row[5]),
                (row[7]),
                (row[8]),
                (row[9]),
                (row[10]),
                (row[11]),
                (row[12]),
                (row[13]),
                (row[15]),
            ],
        )
        db.commit()

with open("Manufacturers.csv") as csvFile:
    csvReader = csv.reader(csvFile, delimiter=",")
    for row in csvReader:
        insert = (
            "INSERT INTO Manufacturers(manufacturerName, countryOfOrigin) VALUES(?, ?)"
        )
        myCursor.execute(
            insert,
            [
                (row[1]),
                (row[2]),
            ],
        )
        db.commit()

with open("csvTestData/OnlineSales.csv") as csvFile:
    csvReader = csv.reader(csvFile, delimiter=",")
    for row in csvReader:
        insert = "INSERT INTO OnlineSales(customterName, totalPrice, fulfilmentStatus, deliveryMethod, itemID) VALUES(?, ?, ?, ?, ?)"
        myCursor.execute(
            insert,
            [
                (row[1]),
                (row[2]),
                (row[3]),
                (row[4]),
                (row[6]),
            ],
        )
        db.commit()

with open("csvTestData/Categories.csv") as csvFile:
    csvReader = csv.reader(csvFile, delimiter=",")
    for row in csvReader:
        insert = "INSERT INTO Categories(catagoryName) VALUES(?)"
        myCursor.execute(
            insert,
            [
                (row[1]),
            ],
        )
        db.commit()


with open("csvTestData/Retail.csv") as csvFile:
    csvReader = csv.reader(csvFile, delimiter=",")
    for row in csvReader:
        insert = "INSERT INTO Retail(locationName)VALUES(?)"
        myCursor.execute(insert, [(row[1])])
        db.commit()
"""
