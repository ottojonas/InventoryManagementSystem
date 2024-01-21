# purchase order page class code
# * Standard Library Imports
import datetime
import sqlite3

# * Related Third Party Imports
from PIL import Image
from tkinter import messagebox as tkmb
from tkcalendar import DateEntry
from customtkinter import StringVar

# * Local Application/Library Specific Imports
import customtkinter

customtkinter.set_appearance_mode("dark")


# * Convert python datetime object to string format for SQLite
def adaptDatetime(ts):
    return ts.strftime("%Y-%m-%d %H:%M:%S.%f")


# * Convert SQLite string format to Python datetime object
def convertDatetime(ts):
    return datetime.datetime.strptime(ts, "%Y-%m-%d %H:%M:%S.%f")


# * Register the adapters and converters for Python datetime to SQLite
sqlite3.register_adapter(datetime.datetime, adaptDatetime)
sqlite3.register_converter("datetime", convertDatetime)


def fetchPurchaseOrderNumber():
    with sqlite3.connect("database/inventoryDatabase.db") as db:
        myCursor = db.cursor()
        myCursor.execute("SELECT MAX(purchaseOrderNumber) FROM PurchaseOrders")
        fetchedID = myCursor.fetchone()
        if fetchedID is not None and fetchedID[0] is not None:
            return fetchedID[0] + 1
        else:
            return 1


def fetchUniqueItemNames():
    with sqlite3.connect("database/inventoryDatabase.db") as db:
        myCursor = db.cursor()
        myCursor.execute("SELECT DISTINCT itemName FROM Items")
        return [row[0] for row in myCursor.fetchall()]


def executeDatabaseQuery(query, params):
    with sqlite3.connect("database/inventoryDatabase.db") as db:
        myCursor = db.cursor()
        myCursor.execute(query, params)
        results = myCursor.fetchall()
        return results, db


class PurchaseOrderPage(customtkinter.CTk):
    # * Dictionaries
    HOVERCOLOR = "#5e6963"
    FGCOLOR = "#37443d"
    FONT = ("Aptos", 15, "bold")
    LABELFONT = ("Aptos", 20, "bold")
    ICONDICTIONARY = {
        "notificationBellIcon": "images/notificationBellIcon.png",
        "activeNotificationBellIcon": "images/activeNotificationIcon.png",
        "sideBarIcon": "images/listIcon.png",
        "profileIcon": "images/profileIcon.png",
        "homeIcon": "images/homeIcon.png",
        "shoppingCartIcon": "images/shoppingCartIcon.png",
        "customerIcon": "images/customerIcon.png",
        "inventoryIcon": "images/inventoryIcon.png",
        "orderIcon": "images/orderIcon.png",
        "reportsIcon": "images/reportsIcon.png",
        "stockControlIcon": "images/stockControlIcon.png",
        "settingsIcon": "images/settingsIcon.png",
    }

    @staticmethod
    def loadImage(path, size=None):
        image = Image.open(path)
        return (
            customtkinter.CTkImage(image, size=size)
            if size
            else customtkinter.CTkImage(image)
        )

    def createTopBarButton(self, master, image, x, y, command=None):
        button = customtkinter.CTkButton(
            master=master,
            image=image,
            text="",
            hover=False,
            fg_color="transparent",
            width=50,
            height=50,
            command=command,
        )
        button.pack(
            anchor="center",
            fill="both",
            side="right",
            padx=(0, 5),
            pady=(0, 0),
        )
        button.place(x=x, y=y)
        return button

    def createSideBarButton(
        self,
        master,
        image,
        text,
        width,
        height,
        font,
        compound,
        anchor="w",
        side="top",
        padx=(20, 20),
        pady=(20, 20),
        fg_color="transparent",
        hover_color=None,
        text_color="black",
    ):
        button = customtkinter.CTkButton(
            master=master,
            image=image,
            text=text,
            text_color=text_color,
            fg_color=fg_color,
            hover_color=hover_color,
            width=width,
            height=height,
            font=font,
            compound=compound,
        )
        button.pack(anchor=anchor, side=side, padx=padx, pady=pady)
        return button

    def createLabel(
        self,
        master,
        text,
        font,
        side="top",
        padx=(10, 0),
        pady=(10, 0),
        text_color="black",
        anchor="w",
        justify="left",
    ):
        label = customtkinter.CTkLabel(
            master=master,
            text=text,
            text_color=text_color,
            anchor=anchor,
            justify=justify,
            font=font,
        )
        label.pack(
            side=side,
            padx=padx,
            pady=pady,
        )
        return label

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("Dashboard Front Page")
        self.geometry(f"{self.winfo_screenwidth()}x{self.winfo_screenheight()}")
        self.resizable(True, True)

        # * Load Icons
        for iconName, iconPath in self.ICONDICTIONARY.items():
            setattr(self, iconName, self.loadImage(iconPath))

        # * Load Image
        self.purchaseOrderImage = self.loadImage(
            "images/obfcLogoBG.JPG",
            size=(274, 366),
        )

        # * Top Bar Frame
        self.topBarFrame = customtkinter.CTkFrame(
            master=self,
            fg_color=self.FGCOLOR,
            width=self.winfo_screenwidth(),
            height=70,
        )
        self.topBarFrame.pack_propagate(False)
        self.topBarFrame.pack(
            pady=(0, 0),
            padx=(0, 0),
        )

        self.topBarButton = self.createTopBarButton(
            self.topBarFrame, self.sideBarIcon, 5, 10, self.toggleSideBar
        )
        # * Company Label
        self.companyLabelTopFrame = customtkinter.CTkLabel(
            master=self.topBarFrame,
            text="Oliver Brown",
            text_color="black",
            anchor="w",
            justify="left",
            font=self.FONT,
        )
        self.companyLabelTopFrame.pack(
            anchor="w",
            padx=(10, 0),
            pady=(0, 0),
        )
        self.companyLabelTopFrame.place(x=55, y=22)
        self.profileButton = self.createTopBarButton(
            self.topBarFrame, self.profileIcon, 1860, 10
        )
        self.notificationButton = self.createTopBarButton(
            self.topBarFrame, self.notificationBellIcon, 1810, 10
        )

        # * Side Bar Frame
        self.sideBarFrame = customtkinter.CTkFrame(
            master=self,
            fg_color=self.FGCOLOR,
            width=300,
            height=self.winfo_screenheight(),
            corner_radius=0,
        )
        self.sideBarFrame.pack_propagate(False)
        self.sideBarFrame.place(
            x=0,
            y=-self.sideBarFrame.winfo_height(),
        )

        self.sideBarButton = self.createTopBarButton(
            self.sideBarFrame, self.sideBarIcon, 5, 10, self.toggleSideBar
        )

        self.companyLabelSideFrame = self.createLabel(
            self.sideBarFrame, "Oliver Brown", self.FONT
        )

        self.homeButton = self.createSideBarButton(
            self.sideBarFrame,
            self.homeIcon,
            "Home",
            300,
            50,
            self.FONT,
            "left",
            hover_color=self.HOVERCOLOR,
        )

        self.sellButton = self.createSideBarButton(
            self.sideBarFrame,
            self.shoppingCartIcon,
            "Sell",
            300,
            50,
            self.FONT,
            "left",
            hover_color=self.HOVERCOLOR,
        )

        self.inventoryButton = self.createSideBarButton(
            self.sideBarFrame,
            self.inventoryIcon,
            "Inventory",
            300,
            50,
            self.FONT,
            "left",
            hover_color=self.HOVERCOLOR,
        )

        self.stockControlButton = self.createSideBarButton(
            self.sideBarFrame,
            self.stockControlIcon,
            "Stock Control",
            300,
            50,
            self.FONT,
            "left",
            hover_color=self.HOVERCOLOR,
        )

        self.stockMovementButton = self.createSideBarButton(
            self.sideBarFrame,
            self.orderIcon,
            "Stock Movement",
            300,
            50,
            self.FONT,
            "left",
            hover_color=self.HOVERCOLOR,
        )

        # * Hover in and out functions for StockMovementHoverFrame
        def showHoverFrame(event):
            buttonXAxis = self.stockMovementButton.winfo_x()
            buttonYAxis = self.stockMovementButton.winfo_y()
            frameWidth = self.sideBarFrame.winfo_width()
            self.stockMovementHoverFrame.place(
                x=buttonXAxis + frameWidth, y=buttonYAxis
            )
            self.stockMovementHoverFrame.lift()
            if hasattr(self, "hideID"):
                self.stockMovementHoverFrame.after_cancel(self.hideID)

        def hideHoverFrame(event):
            if event.widget in self.stockMovementHoverFrame.winfo_children():
                return
            self.stockMovementHoverFrame.place_forget()

        # * Hover Frame for stockMovementButton
        self.stockMovementHoverFrame = customtkinter.CTkFrame(
            master=self,
            fg_color=self.FGCOLOR,
            width=300,
            height=200,
        )
        self.stockMovementHoverFrame.pack_propagate(False)
        self.stockMovementButton.bind("<Enter>", showHoverFrame)
        self.stockMovementHoverFrame.bind("<Leave>", hideHoverFrame)

        # * Purchase Order Button
        self.purchaseOrderButton = customtkinter.CTkButton(
            master=self.stockMovementHoverFrame,
            text="Purchase Orders",
            text_color="black",
            fg_color="transparent",
            hover_color=self.HOVERCOLOR,
            width=300,
            height=50,
            font=self.FONT,
            compound="left",
        )
        self.purchaseOrderButton.pack(
            anchor="w",
            side="top",
            padx=(20, 20),
            pady=(10, 10),
        )

        # * Transfers Button
        self.stockTransferButton = customtkinter.CTkButton(
            master=self.stockMovementHoverFrame,
            text="Transfers",
            text_color="black",
            fg_color="transparent",
            hover_color=self.HOVERCOLOR,
            width=300,
            height=50,
            font=self.FONT,
            compound="left",
        )
        self.stockTransferButton.pack(
            anchor="w",
            side="top",
            padx=(20, 20),
            pady=(10, 10),
        )

        self.customersButton = self.createSideBarButton(
            self.sideBarFrame,
            self.customerIcon,
            "Customers",
            300,
            50,
            self.FONT,
            "left",
            hover_color=self.HOVERCOLOR,
        )

        self.reportsButton = self.createSideBarButton(
            self.sideBarFrame,
            self.reportsIcon,
            "Reports",
            300,
            50,
            self.FONT,
            "left",
            hover_color=self.HOVERCOLOR,
        )

        # * Chat Button
        self.chatButton = customtkinter.CTkButton(
            master=self.sideBarFrame,
            text="Chat",
            text_color="black",
            fg_color="transparent",
            hover_color=self.HOVERCOLOR,
            width=300,
            height=50,
            font=self.FONT,
            compound="left",
        )
        self.chatButton.pack(
            anchor="w",
            side="top",
            padx=(20, 20),
            pady=(10, 10),
        )

        self.settingsButton = self.createSideBarButton(
            self.sideBarFrame,
            self.settingsIcon,
            "Settings",
            300,
            50,
            self.FONT,
            "left",
            hover_color=self.HOVERCOLOR,
        )

        # * Item Information Frame
        self.itemInformationFrame = customtkinter.CTkFrame(
            master=self,
            fg_color=self.FGCOLOR,
            width=965,
            height=900,
        )
        self.itemInformationFrame.pack_propagate(False),
        self.itemInformationFrame.place(x=self.sideBarFrame.winfo_width() + 10, y=80)
        purchaseOrderNumber = fetchPurchaseOrderNumber()
        uniqueOptions = fetchUniqueItemNames()
        with sqlite3.connect("database/inventoryDatabase.db") as db:
            myCursor = db.cursor()
            for item in uniqueOptions:
                myCursor.execute(
                    "UPDATE Items SET purchaseOrderNumber = ? WHERE itemName = ?",
                    (purchaseOrderNumber, item),
                )

        # * Purchase order number label
        self.purchaseOrderLabel = customtkinter.CTkLabel(
            master=self.itemInformationFrame,
            text=f"Purchase Order Number = {purchaseOrderNumber}",
            text_color="black",
            font=self.LABELFONT,
        )
        self.purchaseOrderLabel.pack(
            anchor="center",
            padx=(10, 10),
            pady=(10, 10),
        )
        # * Connecting to database and fetching data
        with sqlite3.connect("database/inventoryDatabase.db") as db:
            myCursor = db.cursor()
            myCursor.execute("SELECT itemName FROM Items")
            items = myCursor.fetchall()
            options = [item for t in items for item in t]
            uniqueOptions = list(set(options))
            self.selectedOption = StringVar()

        # * Item Option Drop Down Menu
        self.itemOptionMenu = customtkinter.CTkOptionMenu(
            master=self.itemInformationFrame,
            fg_color=self.FGCOLOR,
            button_color=self.FGCOLOR,
            button_hover_color=self.HOVERCOLOR,
            text_color="black",
            variable=self.selectedOption,
            values=uniqueOptions,
            command=self.onItemSelect,
        )
        self.itemOptionMenu.pack(
            anchor="center",
            padx=(10, 10),
            pady=(10, 10),
        )
        self.selectedOption.trace("w", self.updateSupplierLabel)
        self.selectedOption.trace("w", self.updateLabel)

        # * Item Label
        self.itemLabel = customtkinter.CTkLabel(
            master=self.itemInformationFrame,
            text="",
            text_color="black",
            anchor="w",
            justify="left",
            font=self.LABELFONT,
        )
        self.itemLabel.pack(
            anchor="center",
            padx=(10, 10),
            pady=(10, 10),
        )

        # * Example Image Label
        self.imageLabel = customtkinter.CTkLabel(
            master=self.itemInformationFrame,
            image=self.purchaseOrderImage,
            text="",
        )
        self.imageLabel.pack(
            anchor="center",
            padx=(10, 10),
            pady=(10, 10),
        )

        # * Supplier Label
        self.supplierLabel = customtkinter.CTkLabel(
            master=self.itemInformationFrame,
            text=f"Supplier:",
            text_color="black",
            anchor="w",
            justify="left",
            font=self.LABELFONT,
        )
        self.supplierLabel.pack(
            anchor="center",
            padx=(10, 10),
            pady=(10, 10),
        )

        # * Created At and Created By Label
        self.createdInformationLabel = customtkinter.CTkLabel(
            master=self.itemInformationFrame,
            text="Created by: Otto Jonas",
            text_color="black",
            anchor="w",
            justify="left",
            font=self.LABELFONT,
        )
        self.createdInformationLabel.pack(
            anchor="center",
            padx=(10, 10),
            pady=(10, 10),
        )

        # * Desired Delivery Date Label
        self.deliveryDateLabel = customtkinter.CTkLabel(
            master=self.itemInformationFrame,
            text="Delivery Date: ",
            text_color="black",
            anchor="w",
            justify="left",
            font=self.LABELFONT,
        )
        self.deliveryDateLabel.pack(
            anchor="center",
            padx=(10, 10),
            pady=(10, 10),
        )

        # * Desired Delivery Date Entry
        self.deliveryDate = DateEntry(
            master=self.itemInformationFrame,
            width=12,
            background="darkblue",
            foreground="white",
            borderwidth=2,
        )
        self.deliveryDate.pack(
            anchor="center",
            padx=(10, 10),
            pady=(10, 10),
        )

        # * Create Button
        self.confirmButton = customtkinter.CTkButton(
            master=self.itemInformationFrame,
            text="Confirm",
            text_color="black",
            fg_color="transparent",
            hover_color=self.HOVERCOLOR,
            width=300,
            height=50,
            font=self.FONT,
            command=self.saveToDatabase,
        )
        self.confirmButton.pack(
            anchor="w",
            side="left",
            padx=(10, 10),
            pady=(10, 10),
        )

        # * Cancel Button
        self.cancelButton = customtkinter.CTkButton(
            master=self.itemInformationFrame,
            text="Cancel",
            text_color="black",
            fg_color="transparent",
            hover_color=self.HOVERCOLOR,
            width=300,
            height=50,
            font=self.FONT,
        )
        self.cancelButton.pack(
            anchor="e",
            side="right",
            padx=(10, 10),
            pady=(10, 10),
        )
        # * Varient and Sizes Frame
        self.orderFrame = customtkinter.CTkFrame(
            master=self,
            fg_color=self.FGCOLOR,
            width=900,
            height=900,
        )
        self.orderFrame.pack_propagate(False)
        self.orderFrame.place(
            x=self.itemInformationFrame.winfo_width() + 10,
            y=80,
        )

        # * List of Items Frame
        self.listOfItemsFrame = customtkinter.CTkScrollableFrame(
            master=self.orderFrame,
            fg_color="white",
            width=900,
            height=800,
        )
        self.listOfItemsFrame.grid(row=0, column=0)

        # * Price Frame
        self.priceFrame = customtkinter.CTkFrame(
            master=self.orderFrame,
            fg_color="transparent",
            width=920,
            height=90,
        )
        self.priceFrame.pack_propagate(False)
        self.priceFrame.grid(
            row=1,
            column=0,
        )

        # * Price label
        totalPrice = self.calculateTotalPrice()
        self.priceLabel = customtkinter.CTkLabel(
            master=self.priceFrame,
            text=f"Total Price: £{totalPrice}",
            text_color="black",
            anchor="w",
            justify="left",
            font=self.LABELFONT,
        )
        self.priceLabel.pack(
            anchor="center",
            padx=(10, 10),
            pady=(10, 10),
        )

        # * Toggle Side Bar called to default sidebar as closed
        self.after(
            100,
            self.toggleSideBar,
        )
        self.after(
            1000,
            self.updateDate,
        )

    # * Function to clear the listOfItemsFrame each time a new item is chosen
    def clearListOfItemsFrame(self):
        # ! Clear the list of items frame each time a new item is chosen.
        for widget in self.listOfItemsFrame.winfo_children():
            widget.destroy()

    # * Function to create labels and entry points in the listOfItemsFrame
    def onItemSelect(self, event):
        # ! Create labels and entry points in the list of items frame when an item is selected.
        self.priceLabel.configure(text="Total Price: £0.00")
        self.clearListOfItemsFrame()
        self.selectedItem = self.itemOptionMenu.get()
        itemSize, db = executeDatabaseQuery(
            "SELECT sizes FROM Items WHERE itemName = ?", (self.selectedItem,)
        )
        self.sizeEntries = {}
        for self.size in itemSize:
            self.sizeLabel = customtkinter.CTkLabel(
                master=self.listOfItemsFrame,
                text=f"Size: {self.size[0]}",
                text_color="black",
                fg_color="white",
                anchor="w",
                justify="left",
                font=self.FONT,
            )
            self.sizeLabel.pack_propagate(False)
            self.sizeLabel.pack(
                anchor="center",
                padx=(10, 10),
                pady=(10, 10),
            )
            self.sizeEntries[self.size[0]] = customtkinter.CTkEntry(
                master=self.listOfItemsFrame,
                text_color="black",
                fg_color="white",
                font=self.FONT,
            )
            self.sizeEntries[self.size[0]].pack(
                anchor="center",
                padx=(10, 10),
                pady=(10, 10),
            )
            self.sizeEntries[self.size[0]].bind("<Key>", self.updateTotalPrice)

    # * Function to fetch and calculate total price
    def calculateTotalPrice(self):
        # ! Calculate the total price of the order based on the selected items and their quantities.
        self.totalPrice = 0
        item = self.itemOptionMenu.get()
        rows, db = executeDatabaseQuery(
            "SELECT price FROM Items WHERE itemName = ?", (item,)
        )
        totalPrice = 0
        if rows and len(rows) > 0:
            price = rows[0][0].replace("£", "")
            for sizeEntry in self.sizeEntries.values():
                quantity = sizeEntry.get()
                if quantity.isdigit():
                    totalPrice += float(price) * int(quantity)
        return totalPrice

    # * Function to update the priceLabel each time sizeEntries is updated
    def updateTotalPrice(self, event):
        # ! Update the total price label each time the size entries are updated.
        self.totalPrice = self.calculateTotalPrice()
        self.priceLabel.configure(text=f"Total Price: £{self.totalPrice: .2f}")

    def updateSupplierLabel(self, *args):
        item = self.itemOptionMenu.get()
        results, db = executeDatabaseQuery(
            "SELECT manufacturerID FROM Items WHERE itemName = ?",
            (item,),
        )
        if results:
            self.supplierID = results[0][0]
            suppliers, db = executeDatabaseQuery(
                "SELECT manufacturerName FROM Manufacturers WHERE manufacturerID = ?",
                (self.supplierID),
            )
            if suppliers:
                self.supplier = suppliers[0]
                self.supplierLabel.configure(text=f"Supplier: {self.supplier}")
            else:
                self.supplierLabel.configure(text="Supplier Not Found")
        self.selectedOption = StringVar()
        self.selectedOption.trace("w", self.updateSupplierLabel)

    def updateLabel(self, *args):
        selectedOption = self.selectedOption.get()
        rows, db = executeDatabaseQuery(
            "SELECT sku FROM Items WHERE itemName = ?", (selectedOption,)
        )
        if rows:
            self.sku = rows[0]
            self.itemLabel.configure(
                text=f"{self.selectedOption.get()}, (SKU:{self.sku})"
            )
        else:
            self.itemLabel.configure(
                text=f"{self.selectedOption.get()}, (SKU: Not Found)"
            )

        self.selectedOption.trace("w", self.updateLabel)

    # * Update date
    def updateDate(self):
        # ! Update the date to be the present date.
        now = datetime.datetime.now()
        dateString = now.strftime("%d.%m.%Y")
        self.createdInformationLabel.configure(
            text=f"Created by: Otto Jonas on {dateString}"
        )

    # * Function to reset the attributes
    def resetAttributes(self):
        # ! Resetting the attributes each time there is a successful save.
        self.itemOptionMenu
        self.itemLabel.configure(text="")
        self.supplierLabel.configure(text="")
        self.priceLabel.configure(text="Total Price: £0.00")
        self.createdInformationLabel.configure(text="Created By: Otto Jonas")
        self.clearListOfItemsFrame()
        self.deliveryDate.set_date(datetime.datetime.now().date())

    def saveToDatabase(self):
        # * Collecting data from entry points
        currentDate = datetime.datetime.now().date()
        itemName = self.selectedItem
        supplier = self.supplierID
        sku = self.sku[0]
        price = self.totalPrice
        createdBy = "Otto Jonas"
        createdAt = currentDate
        sizes = list(self.sizeEntries.keys())
        deliveryDate = self.deliveryDate.get_date()
        quantity = self.sizeEntries[self.size[0]].get()
        items = [{"sizes": size} for size in sizes]

        # * Data Validation for Database Inputs
        if not deliveryDate:
            tkmb.showerror(title="Error", message="Delivery Date is required")
            raise ValueError("Delivery Date is required")
        if not quantity:
            tkmb.showerror(title="Error", message="Quanities are required")
            raise ValueError("Quantity is Required")
        try:
            quantity = int(quantity)
        except ValueError:
            tkmb.showerror(title="Error", message="Quantities must be a number")
            raise TypeError("Quantity must be an integer")
        if quantity < 0:
            tkmb.showerror(
                title="Error",
                message="Quantity must be greater than or equal to 0 ",
            )
            raise ValueError("Quantity must be 0 or larger")
        if deliveryDate <= currentDate:
            tkmb.showerror(title="Error", message="Delivery Date must be in the future")
            raise ValueError("Delivery Date must be in the future")

        results, db = executeDatabaseQuery(
            "SELECT MAX(purchaseOrderNumber)FROM PurchaseOrders", ()
        )
        purchaseOrderNumber = results[0][0] + 1 if results[0][0] is not None else 1
        for item in items:
            results, db = executeDatabaseQuery(
                "INSERT INTO PurchaseOrders (itemID, manufacturerID, sku, price, createdBy, createdAt, sizes, deliveryDate, quantity, purchaseOrderNumber) VALUES(?, ?, ?,?, ?, ?, ?, ?, ?, ?)",
                (
                    itemName,
                    supplier,
                    sku,
                    price,
                    createdBy,
                    currentDate,
                    item["sizes"],
                    deliveryDate,
                    quantity,
                    purchaseOrderNumber,
                ),
            )
            purchaseOrderID = db.cursor().lastrowid
            item["purchaseOrderID"] = purchaseOrderID
        db.commit()
        self.resetAttributes()

    # * Sidebar Toggle Function
    def toggleSideBar(self):
        if self.sideBarFrame.winfo_viewable():
            self.sideBarFrame.place_forget()
            self.itemInformationFrame.place(x=10, y=80)
            self.orderFrame.place(
                x=self.itemInformationFrame.winfo_width() + 20,
                y=80,
            )
        else:
            self.animateSideBar()

    # * Sidebar toggle animation
    def animateSideBar(self):
        if self.sideBarFrame.winfo_viewable():
            for y in range(
                0,
                -self.sideBarFrame.winfo_height(),
                -10,
            ):
                self.sideBarFrame.place_forget()
        else:
            for y in range(
                -self.sideBarFrame.winfo_height(),
                0,
                10,
            ):
                self.sideBarFrame.place(x=0, y=0)
                self.sideBarFrame.update()
                self.itemInformationFrame.place(
                    x=self.sideBarFrame.winfo_width() + 10,
                    y=80,
                )
                self.orderFrame.place(
                    x=self.itemInformationFrame.winfo_width()
                    + self.sideBarFrame.winfo_width()
                    + 20,
                    y=80,
                )
                self.update()


if __name__ == "__main__":
    main = PurchaseOrderPage()
    main.mainloop()
