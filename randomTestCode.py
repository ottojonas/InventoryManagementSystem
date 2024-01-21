import csv
import datetime
VALUES = None
db = None
yearly = None
radioButton = None
items = []
collectioData = {}
# Transfer logic
def transferLogic(self):
    # ! Collect data to input into database
    results = self.db.executeDatabaseQuery(
        "SELECT MAX(transferNumber) FROM Transfers", ()
    )
    transferNumber = results[0][0] + 1 if results[0][0] is not None else 1
    for item in items:
        results = self.db.executeDatabaseQuery(
            "INSERT INTO Transfers(DATA) VALUES(?)",
            (collectionData,),
        )
        transferID = self.db.myCursor.lastrowid
        item["transferID"] = transferID
    self.db.commit()
    self.resetAttributes


# export logic
tables = ["OnlineSales", "Sales"]
now = datetime.datetime.now()
safeTimeString = now.strftime("%Y-%m-%d_%H-%M-%S")
with open(f"{safeTimeString}.csv", "w") as file: 
    csvPen = csv.writer(file, delimiter = ",")
    if radioButton == yearly: 
        for table in tables: 
            db.myCursor.execute(f"SELECT * FROM {table} WHERE (dateOfSale)", VALUES(?))
            rows = db.myCursor.fetchall()
            if rows: 
                csvPen.writerow([i[0] for i in db.myCursor.description])
                csvPen.writerows(rows)
