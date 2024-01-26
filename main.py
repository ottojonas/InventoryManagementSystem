# main.py
# * Standard Library Imports
import csv
import os
import sqlite3
from datetime import datetime, timedelta
from sqlite3 import Error
from tkinter import messagebox as tkmb

# * Local Application/Library Specific Imports
import customtkinter
import matplotlib.pyplot as plt
from CTkTable import CTkTable
from customtkinter import StringVar
from dateutil.relativedelta import relativedelta
from icecream import ic
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.dates import date2num
from matplotlib.figure import Figure

# * Related Third Party Imports
from PIL import Image
from tkcalendar import DateEntry
from windows_toasts import Toast, WindowsToaster


# * Application State Management Classes
# The `ApplicationState` class represents the state of an application and contains various state
# variables.
class ApplicationState:
    def __init__(self, SQLiteWrapper):
        # * State Variables
        self.databaseWrapper = SQLiteWrapper(
            "database/inventoryDatabase.db",
            "database/loginInfoDatabase.db",
            "database/remindersDatabase.db",
            "database/inventoryDatabaseUpdated.db",
        )
        self.currentUser = None
        self.currentOrder = None
        self.currentProduct = None
        self.currentInventory = None
        self.currentStaff = None
        self.currentTransfer = None
        self.currentSale = None

    def login(self, email, password):
        """
        The `login` function takes an email and password as input, retrieves the user from the database,
        sets the current user if found, and returns a boolean indicating whether the login was successful.

        :param email: The email parameter is the email address entered by the user during the login process
        :param password: The `password` parameter is the password entered by the user during the login
        process
        :return: The login method returns a boolean value. If the user is successfully logged in, it returns
        True. If the login fails, it returns False.
        """
        user = self.databaseWrapper.get_user(email, password)
        if user is not None:
            self.currentUser = user
            print(f"Logged in as {user.firstName} {user.lastName}.")
            return True
        else:
            return False

    def getCurrentUser(self):
        return self.currentUser


class ImageWrapper:
    ICONDICT = {
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
        "downloadIcon": "images/downloadIcon.png",
        "emailIcon": "images/emailIcon.png",
        "passwordIcon": "images/passwordIcon.png",
        "presentationIcon": "images/presentation.png",
    }

    @staticmethod
    def loadImage(iconName, size=None):
        """
        The `loadImage` function loads an image file based on the given `iconName` and resizes it if a
        `size` is provided.

        :param iconName: The `iconName` parameter is a string that represents the name of the icon. It is
        used to look up the path of the image file in the `ICONDICT` dictionary
        :param size: The `size` parameter is an optional argument that specifies the desired size of the
        image. It is a tuple of two integers representing the width and height of the image. If provided,
        the image will be resized to the specified size using the `resize()` method of the `Image` class. If
        :return: The method `loadImage` returns a `customtkinter.CTkImage` object.
        """
        iconName = str(iconName)
        if iconName not in ImageWrapper.ICONDICT:
            raise ValueError(
                f"Invalid iconName: {iconName}. Must be a key in the ICONDICT."
            )
        iconPath = ImageWrapper.ICONDICT.get(iconName)
        if iconPath is not None:
            image = Image.open(iconPath)
            if size is not None:
                image = image.resize(size)
            return customtkinter.CTkImage(image)
        else:
            raise ValueError(f"No image found for name: {iconName}")


# The `SQLiteWrapper` class is a wrapper for interacting with SQLite databases, providing methods for
# querying and manipulating data.
class SQLiteWrapper:
    def __init__(
        self,
        inventoryDatabase,
        inventoryDatabaseUpdated,
        loginInfoDatabase,
        remindersDatabase,
    ):
        with sqlite3.connect("database/inventoryDatabase.db") as self.db:
            self.myCursor = self.db.cursor()
        with sqlite3.connect("database/loginInfoDatabase.db") as self.logindb:
            self.loginCursor = self.logindb.cursor()
        with sqlite3.connect("database/remindersDatabase.db") as self.remindersdb:
            self.remindersCursor = self.remindersdb.cursor()
        with sqlite3.connect("database/inventoryDatabaseUpdated.db") as self.updateddb:
            self.updatedCursor = self.updateddb.cursor()

    def getNumberOfItems(self):
        query = "SELECT COUNT(*) FROM Items"
        self.myCursor.execute(query)
        numberOfRows = self.myCursor.fetchone()[0]
        return numberOfRows

    def searchDatabase(self, tableName, columnName, searchText):
        query = f"SELECT * FROM {tableName} WHERE {columnName} LIKE ?"
        searchText = "%" + searchText + "%"
        self.myCursor.execute(query, (searchText,))
        searchResults = self.myCursor.fetchall()
        return searchResults

    def fetchOrders(self):
        self.myCursor.execute("SELECT * FROM (Sales, OnlineSales)")
        self.sales = self.myCursor.fetchall()
        return self.sales

    def fetchPurchaseOrderNumber(self):
        self.myCursor.execute("SELECT MAX(purchaseOrderNumber) FROM PurchaseOrder")
        fetchedID = self.myCursor.fetchone()
        if fetchedID is not None and fetchedID[0] is not None:
            return fetchedID[0] + 1
        else:
            return 1

    def fetchUniqueItemNames(self):
        self.myCursor.execute("SELECT DISTINCT itemName from Items")
        return [row[0] for row in self.myCursor.fetchall()]

    def fetchTransferNumber(self):
        self.myCursor.execute("SELECT MAX(transferNumber) from Transfers")
        fetchedID = self.myCursor.fetchone()
        if fetchedID is not None and fetchedID[0] is not None:
            return fetchedID[0] + 1
        else:
            return 1

    def fetchUniqueLocationNames(self):
        self.myCursor.execute("SELECT DISTINCT locationName from Retail")
        return [row[0] for row in self.myCursor.fetchall()]

    def fetchUniqueCategoryNames(self):
        self.myCursor.execute("SELECT DISTINCT categoryName from Categories")
        return [row[0] for row in self.myCursor.fetchall()]

    def fetchUniquePurchaseOrderNumbers(self):
        self.myCursor.execute("SELECT DISTINCT purchaseOrderNumber FROM PurchaseOrder")
        return [row[0] for row in self.myCursor.fetchall()]

    def executeDatabaseQuery(self, query, params):
        self.myCursor.execute(query, params)
        results = self.myCursor.fetchall()
        return results

    def executeLogInQuery(self, query, params):
        self.loginCursor.execute(query, params)
        loginResults = self.loginCursor.fetchall()
        return loginResults

    def executeRemindersQuery(self, query, params):
        self.remindersCursor.execute(query, params)
        remindersResult = self.remindersCursor.fetchall()
        return remindersResult

    def commit(self):
        self.db.commit()

    def loginCommit(self):
        self.logindb.commit()

    def remindersCommit(self):
        self.remindersdb.commit()


# * Design Pattern Classes
class Factory:
    pass


class Observer:
    pass


class Subject:
    pass


customtkinter.set_appearance_mode("light")


def adaptDatetime(ts):
    """
    The function `adaptDatetime` takes a datetime object `ts` and returns a formatted string
    representation of the datetime in the format "YYYY-MM-DD_HH-MM-SS.ssssss".

    :param ts: The parameter "ts" is expected to be a datetime object
    :return: a formatted string representation of the input datetime object.
    """
    return ts.strftime("%Y-%m-%d_%H-%M-%S.%f")


def convertDatetime(ts):
    """
    The function `convertDatetime` takes a timestamp string in the format "YYYY-MM-DD_HH-MM-SS.&f" and
    converts it to a datetime object.

    :param ts: The parameter "ts" is a string representing a timestamp in the format
    "YYYY-MM-DD_HH-MM-SS.&f"
    :return: a datetime object.
    """
    return datetime.strptime(ts, "%Y-%m-%d_%H-%M-%S.&f")


sqlite3.register_adapter(datetime, adaptDatetime)
sqlite3.register_converter("datetime", convertDatetime)


class BasePage:
    HOVERCOLOR = "grey"
    FGCOLOR = "white"
    FONT = ("Aptos", 15, "bold")
    LABELFONT = ("Aptos", 24, "bold")
    safeTimeString = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    def __init__(self, mainWindow, mainFrame, imageWrapper, mainApplicationClass):
        self.basePageFrame = mainFrame
        ic("BasePage Initialized")
        self.basePageFrame = customtkinter.CTkFrame(mainWindow)
        self.basePageFrame.pack_propagate(False)
        self.basePageFrame.pack(fill="both", expand=True)

        self.topBarFrame = customtkinter.CTkFrame(
            self.basePageFrame,
            fg_color=self.FGCOLOR,
            width=mainWindow.winfo_width(),
            height=70,
        )
        self.topBarFrame.pack_propagate(False)
        self.topBarFrame.pack(side="top")

        sideBarIcon = imageWrapper.loadImage("sideBarIcon")
        notificationBellIcon = imageWrapper.loadImage("notificationBellIcon")
        profileIcon = imageWrapper.loadImage("profileIcon")

        self.topBarButton = customtkinter.CTkButton(
            self.topBarFrame,
            image=sideBarIcon,
            text="",
            hover=False,
            fg_color="transparent",
            width=50,
            height=50,
            command=self.toggleSideBar,
        )
        self.topBarButton.place(x=5, y=10)

        self.oliverBrownLabel = customtkinter.CTkLabel(
            master=self.topBarFrame,
            text="Oliver Brown",
            text_color="black",
            anchor="w",
            justify="left",
            font=("Aptos", 15, "bold"),
        )
        self.oliverBrownLabel.place(x=55, y=22)

        self.notificationButton = customtkinter.CTkButton(
            self.topBarFrame,
            image=notificationBellIcon,
            text="",
            hover=False,
            fg_color="transparent",
            width=50,
            height=50,
        )
        self.notificationButton.place(x=1810, y=10)

        self.profileButton = customtkinter.CTkButton(
            self.topBarFrame,
            image=profileIcon,
            text="",
            hover=False,
            fg_color="transparent",
            width=50,
            height=50,
        )
        self.profileButton.place(x=1860, y=10)

        self.widgetFrame = customtkinter.CTkFrame(
            self.basePageFrame,
            width=self.basePageFrame.winfo_width(),
            height=self.basePageFrame.winfo_height() - self.topBarFrame.winfo_height(),
        )
        self.widgetFrame.pack_propagate(False)
        self.widgetFrame.pack(side="top", fill="both", expand=True)

        self.sideBarFrame = customtkinter.CTkFrame(
            self.basePageFrame,
            fg_color=self.FGCOLOR,
            width=300,
            height=mainWindow.winfo_height(),
            corner_radius=0,
        )
        self.sideBarFrame.pack_propagate(False)
        self.sideBarFrame.place(x=0, y=-self.sideBarFrame.winfo_height())
        self.sideBarFrame.place_forget()

        homeIcon = imageWrapper.loadImage("homeIcon")
        shoppingCartIcon = imageWrapper.loadImage("shoppingCartIcon")
        inventoryIcon = imageWrapper.loadImage("inventoryIcon")
        stockControlIcon = imageWrapper.loadImage("stockControlIcon")
        orderIcon = imageWrapper.loadImage("orderIcon")
        customerIcon = imageWrapper.loadImage("customerIcon")
        reportsIcon = imageWrapper.loadImage("presentationIcon")
        settingsIcon = imageWrapper.loadImage("settingsIcon")

        self.sideBarButton = customtkinter.CTkButton(
            self.sideBarFrame,
            image=sideBarIcon,
            text="",
            hover=False,
            fg_color="transparent",
            width=50,
            height=50,
            command=self.toggleSideBar,
        )
        self.sideBarButton.pack(anchor="w", padx=(10, 10), pady=(10, 10))
        self.homeButton = customtkinter.CTkButton(
            master=self.sideBarFrame,
            image=homeIcon,
            text="Home",
            text_color="black",
            fg_color="transparent",
            hover_color=self.HOVERCOLOR,
            width=300,
            height=50,
            font=self.FONT,
            compound="left",
            command=mainApplicationClass.openHomePage,
        )
        self.homeButton.pack(
            anchor="w",
            side="top",
            padx=(20, 20),
            pady=(10, 10),
        )

        self.sellButton = customtkinter.CTkButton(
            master=self.sideBarFrame,
            image=shoppingCartIcon,
            text="Sales",
            text_color="black",
            fg_color="transparent",
            hover_color=self.HOVERCOLOR,
            width=300,
            height=50,
            font=self.FONT,
            compound="left",
        )
        self.sellButton.pack(
            anchor="w",
            side="top",
            padx=(20, 20),
            pady=(10, 10),
        )

        self.inventoryButton = customtkinter.CTkButton(
            master=self.sideBarFrame,
            image=inventoryIcon,
            text="Inventory",
            text_color="black",
            fg_color="transparent",
            hover_color=self.HOVERCOLOR,
            width=300,
            height=50,
            font=self.FONT,
            compound="left",
        )
        self.inventoryButton.pack(
            anchor="w",
            side="top",
            padx=(20, 20),
            pady=(10, 10),
        )

        self.stockControlButton = customtkinter.CTkButton(
            master=self.sideBarFrame,
            image=stockControlIcon,
            text="Stock Control",
            text_color="black",
            fg_color="transparent",
            hover_color=self.HOVERCOLOR,
            width=300,
            height=50,
            font=self.FONT,
            compound="left",
        )
        self.stockControlButton.pack(
            anchor="w",
            side="top",
            padx=(20, 20),
            pady=(10, 10),
        )

        self.stockMovementButton = customtkinter.CTkButton(
            master=self.sideBarFrame,
            image=orderIcon,
            text="Stock Movement",
            text_color="black",
            fg_color="transparent",
            hover_color=self.HOVERCOLOR,
            width=300,
            height=50,
            font=self.FONT,
            compound="left",
        )
        self.stockMovementButton.pack(
            anchor="w",
            side="top",
            padx=(20, 20),
            pady=(10, 10),
        )

        # * Hover in and out functions for StockMovementHoverFrame
        def showHoverFrame(event):
            """
            The function `showHoverFrame` is used to display a hover frame next to a button and cancel any
            previous hide timer.

            :param event: The `event` parameter is an object that represents the event that triggered the
            function. It contains information about the event, such as the type of event, the widget that
            triggered the event, and any additional data associated with the event. In this case, the `event`
            parameter is used to determine
            """
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
            """
            The function hideHoverFrame hides the stockMovementHoverFrame if the event widget is not a child of
            it.

            :param event: The event parameter is an object that represents the event that triggered the
            function. It contains information about the event, such as the widget that triggered it and any
            additional data associated with the event
            """
            if event.widget in self.stockMovementHoverFrame.winfo_children():
                return
            self.stockMovementHoverFrame.place_forget()

        # * Hover Frame for stockMovementButton
        self.stockMovementHoverFrame = customtkinter.CTkFrame(
            master=self.basePageFrame,
            fg_color=self.FGCOLOR,
            width=300,
            height=300,
        )
        self.stockMovementHoverFrame.pack_propagate(True)
        self.stockMovementButton.bind("<Enter>", showHoverFrame)

        self.browseStockMovementPageButton = customtkinter.CTkButton(
            self.stockMovementHoverFrame,
            text="Browse Stock Movement",
            text_color="black",
            fg_color="transparent",
            hover_color=self.HOVERCOLOR,
            width=300,
            height=50,
            font=self.FONT,
            compound="left",
            command=mainApplicationClass.openPurchaseOrderListPage,
        )
        self.browseStockMovementPageButton.pack(
            anchor="w",
            side="top",
            padx=(20, 20),
            pady=(10, 10),
        )

        self.purchaseOrderButton = customtkinter.CTkButton(
            master=self.stockMovementHoverFrame,
            text="Create a Purchase Order",
            text_color="black",
            fg_color="transparent",
            hover_color=self.HOVERCOLOR,
            width=300,
            height=50,
            font=self.FONT,
            compound="left",
            command=mainApplicationClass.openPurchaseOrderPage,
        )
        self.purchaseOrderButton.pack(
            anchor="w",
            side="top",
            padx=(20, 20),
            pady=(10, 10),
        )

        self.stockTransferButton = customtkinter.CTkButton(
            master=self.stockMovementHoverFrame,
            text="Create a Transfer",
            text_color="black",
            fg_color="transparent",
            hover_color=self.HOVERCOLOR,
            width=300,
            height=50,
            font=self.FONT,
            compound="left",
            command=mainApplicationClass.openTransfersPage,
        )
        self.stockTransferButton.pack(
            anchor="w",
            side="top",
            padx=(20, 20),
            pady=(10, 10),
        )

        self.customersButton = customtkinter.CTkButton(
            master=self.sideBarFrame,
            image=customerIcon,
            text="Customers",
            text_color="black",
            fg_color="transparent",
            hover_color=self.HOVERCOLOR,
            width=300,
            height=50,
            font=self.FONT,
            compound="left",
        )
        self.customersButton.pack(
            anchor="w",
            side="top",
            padx=(20, 20),
            pady=(10, 10),
        )

        self.reportsButton = customtkinter.CTkButton(
            master=self.sideBarFrame,
            image=reportsIcon,
            text="Reports",
            text_color="black",
            fg_color="transparent",
            hover_color=self.HOVERCOLOR,
            width=300,
            height=50,
            font=self.FONT,
            compound="left",
            command=mainApplicationClass.openReportsPage,
        )
        self.reportsButton.pack(
            anchor="w",
            side="top",
            padx=(20, 20),
            pady=(10, 10),
        )

        self.hireButton = customtkinter.CTkButton(
            master=self.sideBarFrame,
            text="Hire",
            text_color="black",
            fg_color="transparent",
            hover_color=self.HOVERCOLOR,
            width=300,
            height=50,
            font=self.FONT,
            compound="left",
        )
        self.hireButton.pack(
            anchor="w",
            side="top",
            padx=(20, 20),
            pady=(20, 20),
        )

        self.settingsButton = customtkinter.CTkButton(
            master=self.sideBarFrame,
            image=settingsIcon,
            text="Settings",
            text_color="black",
            fg_color="transparent",
            hover_color=self.HOVERCOLOR,
            width=300,
            height=50,
            font=self.FONT,
            compound="left",
        )
        self.settingsButton.pack(
            anchor="w",
            side="bottom",
            padx=(20, 20),
            pady=(10, 20),
        )

    def toggleSideBar(self):
        """
        The function `toggleSideBar` toggles the visibility of the `sideBarFrame` by either forgetting it or
        animating it.
        """
        if self.sideBarFrame is not None:
            if self.sideBarFrame.winfo_viewable():
                self.sideBarFrame.place_forget()
            else:
                self.animateSideBar()

    def animateSideBar(self):
        """
        The `animateSideBar` function animates the sidebar by either hiding it or showing it with a sliding
        effect.
        """
        if self.sideBarFrame.winfo_viewable():
            for _ in range(
                0,
                -self.sideBarFrame.winfo_height(),
                -10,
            ):
                self.sideBarFrame.place_forget()
        else:
            for _ in range(
                -self.sideBarFrame.winfo_height(),
                0,
                10,
            ):
                self.sideBarFrame.place(x=0, y=0)
                self.sideBarFrame.update()
                self.basePageFrame.update()


# The RegisterBasePage class is a page for registering users, with various graphical elements such as
# frames and labels.
class RegisterBasePage:
    HOVERCOLOR = "#5e6963"
    FGCOLOR = "#37443d"
    FONT = ("Aptos", 15, "bold")
    LABELFONT = ("Aptos", 24, "bold")

    def __init__(self, mainWindow, mainFrame):
        self.registerPageFrame = mainFrame
        ic("RegisterBasePage Initialized")
        self.registerPageFrame = customtkinter.CTkFrame(mainWindow)
        self.registerPageFrame.pack_propagate(False)
        self.registerPageFrame.pack(fill="both", expand=True)

        self.userEntryFrame = customtkinter.CTkFrame(
            self.registerPageFrame, fg_color="white", width=500, height=500
        )
        self.userEntryFrame.pack_propagate(False)
        self.userEntryFrame.pack(anchor="center")

        self.welcomeLabel = customtkinter.CTkLabel(
            self.userEntryFrame, text="Welcome", text_color="black", font=self.LABELFONT
        )
        self.welcomeLabel.pack(anchor="center")


# The code defines two classes, `InventoryManagementSystemApplication` and `RegisterPages`, which are
# initialized with certain parameters.
class InventoryManagementSystemApplication(BasePage):
    def __init__(self, mainWindow, mainFrame, imageWrapper, mainApplicationClass):
        BasePage.__init__(
            self, mainWindow, mainFrame, imageWrapper, mainApplicationClass
        )
        ic("InventoryManagementSystemApplication Initialized")


class RegisterPages(RegisterBasePage):
    def __init__(self, mainWindow, mainFrame):
        RegisterBasePage.__init__(self, mainWindow, mainFrame)
        ic("RegisterPages Initialized")


# The `MainApplicationClass` is a Python class that represents the main application for an inventory
# management system, with various methods for opening different pages within the application.
class MainApplicationClass(InventoryManagementSystemApplication, RegisterPages):
    def __init__(self):
        self.mainWindow = customtkinter.CTk()
        self.mainWindow.attributes("-fullscreen", True)
        self.mainFrame = customtkinter.CTkFrame(self.mainWindow)
        self.mainFrame.pack_propagate(False)
        self.mainFrame.pack(anchor="center")

        self.imageWrapper = ImageWrapper()
        InventoryManagementSystemApplication.__init__(
            self, self.mainWindow, self.mainFrame, self.imageWrapper, self
        )
        RegisterPages.__init__(self, self.mainWindow, self.mainFrame)
        ic("MainApplicationClass Initialized")

        self.openSignUpPage()

    def loadImage(self, iconName, size=None):
        return self.imageWrapper.loadImage(iconName, size)

    def clearMainWindow(self):
        for widget in self.mainWindow.winfo_children():
            widget.destroy()

    def openSignUpPage(self):
        self.clearMainWindow()
        self.currentPage = SignUpPage(self.mainWindow, self.mainFrame, self)
        return self.currentPage

    def openLogInPage(self):
        self.clearMainWindow()
        self.currentPage = LogInPage(self.mainWindow, self.mainFrame, self)
        return self.currentPage

    def openOpeningPage(self):
        self.clearMainWindow()
        self.currentPage = OpeningPage(
            self.mainWindow, self.mainFrame, self.imageWrapper, self
        )
        return self.currentPage

    def openHomePage(self):
        self.clearMainWindow()
        self.currentPage = HomePage(
            self.mainWindow, self.mainFrame, self.imageWrapper, self
        )
        self.currentPage.drawGraph()
        self.currentPage.fetchReminders()
        return self.currentPage

    def openPurchaseOrderListPage(self):
        self.clearMainWindow()
        self.currentPage = BrowseStockMovementsPage(
            self.mainWindow, self.mainFrame, self.imageWrapper, self
        )
        return self.currentPage

    def openPurchaseOrderPage(self):
        self.clearMainWindow()
        self.currentPage = PurchaseOrderPage(
            self.mainWindow, self.mainFrame, self.imageWrapper, self
        )
        return self.currentPage

    def openTransfersPage(self, cellValue=None):
        self.clearMainWindow()
        self.currentPage = TransfersPage(
            self.mainWindow, self.mainFrame, self.imageWrapper, self, cellValue
        )
        return self.currentPage

    def openPurchaseOrderAndTransferEditingPage(self, cellValue):
        self.clearMainWindow()
        self.currentPage = PurchaseOrderAndTransferEditingPage(
            self.mainWindow, self.mainFrame, self.imageWrapper, self, cellValue
        )
        return self.currentPage

    def openReportsPage(self):
        self.clearMainWindow()
        self.currentPage = ReportsPage(
            self.mainWindow, self.mainFrame, self.imageWrapper, self
        )
        self.currentPage.drawGraph()
        self.currentPage.drawPieChart()
        return self.currentPage


class SignUpPage(RegisterBasePage):
    def __init__(self, mainWindow, mainFrame, mainApplicationClass):
        super().__init__(mainWindow, mainFrame)
        ic("SignUpPage Initialized")

        self.signUpPageLabel = customtkinter.CTkLabel(
            self.userEntryFrame, text="Sign Up Page", text_color="black"
        )
        self.signUpPageLabel.pack(anchor="center")
        self.confirmSignUpButton = customtkinter.CTkButton(
            self.userEntryFrame,
            text="Sign Up",
            text_color="white",
            fg_color="black",
            hover_color=self.HOVERCOLOR,
            width=225,
            font=self.FONT,
            command=mainApplicationClass.openOpeningPage,
        )
        self.confirmSignUpButton.pack(anchor="center", padx=(10, 10), pady=(10, 10))

        self.openLogInPageButton = customtkinter.CTkButton(
            self.userEntryFrame,
            text="Log In Here",
            text_color="white",
            fg_color="black",
            hover_color=self.HOVERCOLOR,
            width=225,
            font=self.FONT,
            command=mainApplicationClass.openLogInPage,
        )
        self.openLogInPageButton.pack(anchor="center", padx=(10, 10), pady=(20, 20))


class LogInPage(RegisterBasePage):
    def __init__(self, mainWindow, mainFrame, mainApplicationClass):
        super().__init__(mainWindow, mainFrame)

        self.logInPageLabel = customtkinter.CTkLabel(
            self.userEntryFrame, text="Log In Page", text_color="black"
        )
        self.logInPageLabel.pack(anchor="center")

        self.confirmLogInButton = customtkinter.CTkButton(
            self.userEntryFrame,
            text="Log In",
            text_color="white",
            fg_color="black",
            hover_color=self.HOVERCOLOR,
            width=225,
            font=self.FONT,
            command=mainApplicationClass.openOpeningPage,
        )
        self.confirmLogInButton.pack(anchor="center", padx=(10, 10), pady=(10, 10))

        self.openSignUpPageButton = customtkinter.CTkButton(
            self.userEntryFrame,
            text="Sign Up here",
            text_color="white",
            fg_color="black",
            hover_color=self.HOVERCOLOR,
            width=225,
            font=self.FONT,
            command=mainApplicationClass.openSignUpPage,
        )
        self.openSignUpPageButton.pack(anchor="center", padx=(10, 10), pady=(20, 20))


class OpeningPage(BasePage):
    def __init__(self, mainWindow, mainFrame, imageWrapper, mainApplicationClass):
        super().__init__(mainWindow, mainFrame, imageWrapper, mainApplicationClass)
        ic("OpeningPage Initialized")

        self.backgroundImage = customtkinter.CTkImage(
            Image.open("images/oliverBrownLogoNoBG.png"), size=(450, 87.5)
        )

        self.backgroundImageLabel = customtkinter.CTkLabel(
            master=self.widgetFrame,
            image=self.backgroundImage,
            text="",
        )
        self.backgroundImageLabel.place(x=700, y=500)


class HomePage(BasePage):
    def __init__(self, mainWindow, mainFrame, imageWrapper, mainApplicationClass):
        super().__init__(mainWindow, mainFrame, imageWrapper, mainApplicationClass)
        self.db = SQLiteWrapper(
            "database/inventoryDatabase.db",
            "database/loginInfoDatabase.db",
            "database/remindersDatabase.db",
            "database/inventoryDatabaseUpdated.db",
        )

        ic("HomePage Initialized")

        self.remindersFrame = customtkinter.CTkFrame(
            self.widgetFrame, fg_color="white", width=790, height=500
        )
        self.remindersFrame.grid_propagate(False)
        self.remindersFrame.place(x=10, y=10)

        self.remindersListFrame = customtkinter.CTkScrollableFrame(
            self.remindersFrame,
            fg_color="transparent",
            width=750,
            height=400,
        )
        self.remindersListFrame.grid(
            row=0, column=0, padx=(10, 10), pady=(10, 10), sticky="nsew"
        )

        self.userReminderEntry = customtkinter.CTkEntry(
            master=self.remindersFrame,
            placeholder_text="Add a task / reminder",
            fg_color=self.FGCOLOR,
            font=self.FONT,
            border_color="white",
            placeholder_text_color="black",
            text_color="black",
            width=750,
            height=40,
        )
        self.userReminderEntry.grid(
            row=1,
            column=0,
            padx=(10, 10),
            pady=(0, 10),
        )
        self.userReminderEntry.bind("<Return>", lambda _: self.addReminderFromEntry())
        self.reminders = [reminder for reminder in self.fetchReminders()]

        self.remindersTable = CTkTable(
            master=self.remindersListFrame,
            values=self.reminders if self.reminders else [["", ""]],
            colors=["#ffffff", "#ffffff"],
            hover_color="grey",
            text_color="black",
            header_color=False,
            corner_radius=0,
            font=self.FONT,
        )
        self.remindersTable.edit_row(
            0,
            text_color="black",
            hover_color="grey",
        )
        self.remindersTable.grid_propagate(False)
        self.remindersTable.grid(sticky="nsew")

        self.salesFrame = customtkinter.CTkFrame(
            master=self.widgetFrame,
            fg_color="white",
            width=1100,
            height=500,
        )
        self.salesFrame.pack_propagate(False)
        self.salesFrame.place(
            x=self.remindersFrame.winfo_width() + 20,
            y=10,
        )

        self.labelRowFrame = customtkinter.CTkFrame(
            master=self.salesFrame,
            fg_color="transparent",
            width=1100,
            height=50,
        )
        self.labelRowFrame.grid_propagate(False)
        self.labelRowFrame.grid(row=0, column=0)

        self.orderNumberLabel = customtkinter.CTkLabel(
            self.labelRowFrame,
            text="Order Number",
            text_color="black",
            anchor="w",
            justify="left",
        )
        self.orderNumberLabel.grid(row=0, column=0, padx=(110, 40), pady=(10, 10))

        self.orderLocationLabel = customtkinter.CTkLabel(
            self.labelRowFrame,
            text="Sale Location",
            text_color="black",
            anchor="w",
            justify="left",
        )
        self.orderLocationLabel.grid(row=0, column=1, padx=(150, 40), pady=(10, 10))

        self.dateOfSaleLabel = customtkinter.CTkLabel(
            self.labelRowFrame,
            text="Date of Sale",
            text_color="black",
            anchor="w",
            justify="left",
        )
        self.dateOfSaleLabel.grid(row=0, column=2, padx=(160, 40), pady=(10, 10))

        self.priceOfSaleLabel = customtkinter.CTkLabel(
            self.labelRowFrame,
            text="Price of Sale",
            text_color="black",
            anchor="w",
            justify="left",
        )
        self.priceOfSaleLabel.grid(row=0, column=3, padx=(160, 40), pady=(10, 10))

        self.salesTableFrame = customtkinter.CTkScrollableFrame(
            master=self.salesFrame,
            fg_color="transparent",
            width=1070,
            height=416,
        )
        self.salesTableFrame.grid(
            row=2,
            column=0,
            padx=(10, 0),
            pady=(10, 10),
        )

        self.sales = [sale for sale in self.fetchSales()]
        if not self.sales:
            self.sales = [["" for _ in range(5)]]

        self.salesTable = CTkTable(
            master=self.salesTableFrame,
            values=self.sales,
            colors=["#ffffff", "#ffffff"],
            hover_color="grey",
            text_color="black",
            header_color=False,
            corner_radius=0,
        )
        self.salesTable.edit_row(
            0,
            text_color="black",
            hover_color="grey",
        )
        self.salesTable.grid_propagate(False)
        self.salesTable.grid(sticky="nsew")
        self.salesTable.pack(fill="both", expand=True)

        self.dataGraphFrame = customtkinter.CTkFrame(
            master=self.widgetFrame,
            fg_color="white",
            width=1900,
            height=450,
        )
        self.dataGraphFrame.pack_propagate(False)
        self.dataGraphFrame.place(
            x=10,
            y=530,
        )

        self.plotDataGraphFrame = customtkinter.CTkFrame(
            master=self.dataGraphFrame,
            fg_color="transparent",
            width=1880,
            height=430,
        )
        self.plotDataGraphFrame.pack_propagate(False)
        self.plotDataGraphFrame.pack(
            anchor="center",
            padx=(10, 10),
            pady=(10, 10),
        )

        self.activeNotificationBellIcon = imageWrapper.loadImage(
            "activeNotificationBellIcon"
        )
        self.numberOfRows = 0
        self.numberOfColumns = 0
        self.updateRemindersTable()

    def drawGraph(self):
        """
        The `drawGraph` function retrieves data from a database, converts the dates to a numerical format,
        and plots the data on a graph using matplotlib.
        """
        self.db.myCursor.execute(
            "SELECT DATE(dateOfSale), COUNT(*) FROM Sales GROUP BY DATE(dateOfSale)"
        )
        data = self.db.myCursor.fetchall()
        dates = [date2num(datetime.strptime(row[0], "%Y-%m-%d")) for row in data]
        sales = [row[1] for row in data]
        ic(f"data: {data}, dates: {dates}, sales: {sales}")
        fig = Figure(figsize=(5, 6), dpi=100)
        a = fig.add_subplot(111)
        a.plot_date(dates, sales, "-")
        canvas = FigureCanvasTkAgg(fig, master=self.plotDataGraphFrame)
        canvas.draw()
        canvas.get_tk_widget().pack(side="top", fill="both", expand=True)

    def fetchSales(self):
        """
        The `fetchSales` function retrieves sales data from a database table and returns it as a list of
        tuples.
        :return: The `fetchSales` method is returning a list of sales data. Each item in the list is a tuple
        containing the order number, location of sale, date of sale, and price of sale.
        """
        self.db.myCursor.execute(
            "SELECT orderNumber, locationOfSale, dateOfSale, priceOfSale FROM Sales"
        )
        sales = self.db.myCursor.fetchall()
        ic(f"sales: {sales}")
        return sales

    def updateSalesTable(self):
        """
        The `updateSalesTable` function updates the sales table by fetching new sales data, creating a new
        table with the updated data, and displaying it on the screen.
        """
        self.salesTable.grid_forget()
        self.sales = [sale for sale in self.fetchSales()]
        ic(f"self.sales: {self.sales}")
        self.salesTable = CTkTable(
            self.salesTableFrame,
            values=self.sales,
            colors=["#ffffff", "#ffffff"],
            hover_color="grey",
            text_color="black",
            header_color=False,
            corner_radius=0,
            font=self.FONT,
        )
        self.salesTable.edit_row(
            0,
            text_color="black",
            hover_color="grey",
        )
        self.salesTable.pack_propagate(False)
        self.salesTable.grid(sticky="nsew")
        self.salesTable.pack(expand=True, fill="both")
        self.fetchSales(self.sales)

    def fetchReminders(self):
        """
        The function fetchReminders retrieves all reminders from a SQLite database.
        :return: The function fetchReminders is returning a list of reminders fetched from the Reminders
        table in the remindersDatabase.db SQLite database.
        """
        with sqlite3.connect("database/remindersDatabase.db") as db:
            myCursor = db.cursor()
            myCursor.execute("SELECT reminderTask, createdAt FROM Reminders")
            reminders = myCursor.fetchall()
            return reminders

    def addReminder(self, reminder):
        """
        The `addReminder` function inserts a new reminder task into a SQLite database with the current
        timestamp.
        """
        with sqlite3.connect("database/remindersDatabase.db") as db:
            myCursor = db.cursor()
            myCursor.execute(
                "INSERT INTO Reminders (reminderTask, createdAt) VALUES (?, strftime('%d-%m-%Y', 'now'))",
                (reminder,),
            )
            db.commit()

    def updateRemindersTable(self):
        """
        The function updates a reminders table by forgetting the existing table, fetching new
        reminders, and adding them to the table
        """
        self.remindersTable.grid_forget()
        self.reminders = [reminder for reminder in self.fetchReminders()]
        ic(f"self.remindes: {self.reminders}")
        self.remindersTable = CTkTable(
            self.remindersListFrame,
            values=self.reminders,
            colors=["#ffffff", "#ffffff"],
            hover_color="grey",
            text_color="black",
            header_color=False,
            corner_radius=0,
            font=self.FONT,
        )
        self.remindersTable.edit_row(
            0,
            text_color="black",
            hover_color="grey",
        )
        self.remindersTable.grid_propagate(False)
        self.remindersTable.grid(sticky="nsew")
        self.remindersTable.bind("<Button-1>", self.completeReminderTask)
        self.reminderNotifications()

    def addReminderFromEntry(self):
        """
        The function `addReminderFromEntry` adds a reminder from the user's input, updates the reminders
        table, and clears the user input field.
        """
        reminder = self.userReminderEntry.get()
        self.addReminder(reminder)
        self.userReminderEntry.delete(0, "end")
        self.numberOfRows += 1
        self.updateRemindersTable()

    def reminderNotifications(self):
        """
        The function sends reminder notifications for tasks that have been overdue for more than a day.
        """
        toaster = WindowsToaster("Reminders")
        for reminder in self.reminders:
            if reminder[1]:
                reminderDate = datetime.strptime(reminder[1], "%d-%m-%Y")
                if datetime.now() - reminderDate > timedelta(days=1):
                    toast = Toast()
                    toast.text_fields = [
                        "You have tasks that have been due for over a day"
                    ]
                    toaster.show_toast(toast)
                    self.notificationButton.configure(
                        image=self.activeNotificationBellIcon
                    )

    def completeReminderTask(self, event):
        """
        The `completeReminderTask` function deletes a selected reminder task from the database and updates
        the reminders table.

        :param event: The `event` parameter is likely an event object that is passed to the
        `completeReminderTask` method. This object may contain information about the event that triggered
        the method, such as the user's interaction with a button or a timer event. The specific details of
        the `event` object would depend
        """
        selectedTask = self.remindersTable.get_selected_row()
        ic(f"selectedTask: {selectedTask}")
        reminderTask = selectedTask["values"][0]
        self.db.remindersCursor.execute(
            "DELETE FROM Reminders WHERE reminderTask = ?", (reminderTask,)
        )
        self.db.remindersCommit()
        self.updateRemindersTable()


class BrowseStockMovementsPage(BasePage):
    def __init__(self, mainWindow, mainFrame, imageWrapper, mainApplicationClass):
        super().__init__(mainWindow, mainFrame, imageWrapper, mainApplicationClass)
        self.db = SQLiteWrapper(
            "database/inventoryDatabase.db",
            "database/loginInfoDatabase.db",
            "database/remindersDatabase.db",
            "database/inventoryDatabaseUpdated.db",
        )
        ic("PurchaseOrderListPage Initialized")

        defaultTableValues = self.db.fetchUniquePurchaseOrderNumbers()
        tableValues = [[number] for number in defaultTableValues]

        self.pageSearchContainer = customtkinter.CTkFrame(
            self.widgetFrame,
            fg_color="transparent",
            width=1900,
            height=50,
        )
        self.pageSearchContainer.pack_propagate(False)
        self.pageSearchContainer.pack(anchor="center", padx=(10, 10), pady=(10, 10))

        self.userSearchEntry = customtkinter.CTkEntry(
            self.pageSearchContainer,
            fg_color="transparent",
            width=1400,
            height=40,
            placeholder_text="Enter a Number or Item",
            placeholder_text_color="black",
            text_color="black",
            border_color="black",
            border_width=2,
        )
        self.userSearchEntry.grid(row=0, column=0, padx=(10, 10), pady=(10, 10))

        self.searchButton = customtkinter.CTkButton(
            self.pageSearchContainer,
            fg_color="transparent",
            text="Search",
            text_color="black",
            hover_color="white",
            width=200,
            height=50,
            command=self.search,
        )
        self.searchButton.grid(row=0, column=1, padx=(10, 10), pady=(10, 10))

        self.movementOptionMenuStringVar = StringVar()
        self.movementOptionMenu = customtkinter.CTkOptionMenu(
            self.pageSearchContainer,
            fg_color=self.FGCOLOR,
            button_color=self.FGCOLOR,
            button_hover_color=self.HOVERCOLOR,
            text_color="black",
            variable=self.movementOptionMenuStringVar,
            values=["Purchase Orders", "Transfers"],
        )
        self.movementOptionMenu.grid(row=0, column=2, padx=(10, 10), pady=(10, 10))

        self.itemTableScrollFrame = customtkinter.CTkScrollableFrame(
            self.widgetFrame,
            fg_color="white",
            width=1900,
            height=900,
        )
        self.itemTableScrollFrame.pack_propagate(False)
        self.itemTableScrollFrame.pack(anchor="center", padx=(10, 10), pady=(10, 10))

        self.tableOfContents = CTkTable(
            self.itemTableScrollFrame,
            values=tableValues,
            colors=["#ffffff", "#ffffff"],
            hover_color="grey",
            text_color="black",
            header_color=False,
            justify="center",
            corner_radius=0,
            font=self.FONT,
            command=mainApplicationClass.openPurchaseOrderAndTransferEditingPage,
        )
        self.tableOfContents.grid_propagate(False)
        self.tableOfContents.grid(sticky="nsew")

    def search(self):
        """
        The `search` function takes a search term, queries a database for purchase order and transfer
        numbers matching the search term, and displays the results in a table.
        """
        searchTerm = self.userSearchEntry.get()
        purchaseOrderNumbersDatabase = self.db.searchDatabase(
            "PurchaseOrder", "purchaseOrderNumber", searchTerm
        )
        transferNumberDatabase = self.db.searchDatabase(
            "Transfers", "transferNumber", searchTerm
        )
        purchaseOrderValues = [
            [purchaseOrderNumber for purchaseOrderNumber in row]
            for row in purchaseOrderNumbersDatabase
        ]
        transferValues = [
            [transferNumber for transferNumber in row] for row in transferNumberDatabase
        ]
        if not purchaseOrderNumbersDatabase:
            ic("No Purchase Orders Found")
        else:
            ic(f"Purchase Order Numbers: {purchaseOrderValues}")
        if not transferValues:
            ic("No Transfer Numbers Found")
        else:
            ic(f"Transfer Numbers: {transferValues}")
        stockMovementToSearch = self.movementOptionMenu.get()
        self.tableOfContents.grid_forget()
        addedPurchaseOrderNumbers = set()
        addedTransferNumbers = set()
        purchaseOrderValues = []
        transferValues = []
        if stockMovementToSearch == "Purchase Orders":
            for purchaseOrder in purchaseOrderNumbersDatabase:
                ic(f"PurchaseOrderNumbers: {purchaseOrder}")
                purchaseOrderNumber = str(purchaseOrder[1]).lower()
                if (
                    searchTerm.lower() in purchaseOrderNumber
                    and purchaseOrderNumber not in addedPurchaseOrderNumbers
                ):
                    purchaseOrderValues.append([purchaseOrder[1]])
                    addedPurchaseOrderNumbers.add(purchaseOrderNumber)
            self.tableOfContents = CTkTable(
                self.itemTableScrollFrame,
                values=purchaseOrderValues,
                colors=["#ffffff", "#ffffff"],
                hover_color="grey",
                text_color="black",
                header_color=False,
                justify="center",
                corner_radius=0,
                font=self.FONT,
                command=mainApplicationClass.openPurchaseOrderAndTransferEditingPage,
            )
            self.tableOfContents.pack_propagate(False)
            self.tableOfContents.grid(sticky="nsew")

        elif stockMovementToSearch == "Transfers":
            for transfer in transferNumberDatabase:
                ic(f"TransferNumbers: {transfer}")
                transferNumber = str(transfer[1]).lower()
                if (
                    searchTerm.lower() in transferNumber
                    and transferNumber not in addedTransferNumbers
                ):
                    transferValues.append([transfer[1]])
                    addedTransferNumbers.add(transferNumber)
            self.tableOfContents = CTkTable(
                self.itemTableScrollFrame,
                values=transferValues,
                colors=["#ffffff", "#ffffff"],
                hover_color="grey",
                text_color="black",
                header_color=False,
                justify="center",
                corner_radius=0,
                font=self.FONT,
                command=mainApplicationClass.openPurchaseOrderAndTransferEditingPage,
            )
            self.tableOfContents.pack_propagate(False)
            self.tableOfContents.grid(sticky="nsew")

    def getOptionMovement(self):
        """
        The function `getOptionMovement` returns the selected option from a menu.
        :return: The method `getOptionMovement` is returning the value of `self.movementOptionMenu`.
        """
        return self.movementOptionMenu.get()


class PurchaseOrderAndTransferEditingPage(BasePage):
    def __init__(
        self, mainWindow, mainFrame, imageWrapper, mainApplicationClass, cellValue
    ):
        super().__init__(mainWindow, mainFrame, imageWrapper, mainApplicationClass)
        self.db = SQLiteWrapper(
            "database/inventoryDatabase.db",
            "database/loginInfoDatabase.db",
            "database/remindersDatabase.db",
            "database/inventoryDatabaseUpdated.db",
        )
        ic("PurchaseOrderAndTransferEditingPage Initialized")
        ic(f"cellValue: {cellValue}")

        self.db.myCursor.execute(
            "SELECT deliveryDate FROM PurchaseOrder where purchaseOrderNumber = ?",
            (cellValue["value"],),
        )
        deliveryDate = self.db.myCursor.fetchone()[0]
        self.db.myCursor.execute(
            "SELECT manufacturer FROM PurchaseOrder WHERE purchaseOrderNumber = ? ",
            (cellValue["value"],),
        )
        manufacturerID = self.db.myCursor.fetchone()[0]
        self.db.myCursor.execute(
            "SELECT manufacturerName FROM Manufacturers WHERE manufacturerID = ?",
            (manufacturerID,),
        )
        manufacturerName = self.db.myCursor.fetchone()[0]

        self.db.myCursor.execute(
            "SELECT price FROM PurchaseOrder WHERE purchaseOrderNumber = ?",
            (cellValue["value"],),
        )
        purchaseOrderPrice = self.db.myCursor.fetchone()[0]

        self.db.myCursor.execute(
            "SELECT purchaseOrderID FROM PurchaseOrder WHERE purchaseOrderNumber = ? ",
            (cellValue["value"],),
        )
        purchaseOrderID = self.db.myCursor.fetchone()[0]

        self.db.myCursor.execute(
            "SELECT itemID FROM PurchaseOrderInformation WHERE purchaseOrderID = ?",
            (purchaseOrderID,),
        )
        itemID = self.db.myCursor.fetchone()[0]

        self.db.myCursor.execute(
            "SELECT itemName FROM Items WHERE itemID = ?", (itemID,)
        )
        result = self.db.myCursor.fetchone()
        if result is not None:
            itemName = result[0]
        else:
            itemName = None

        self.informationFrame = customtkinter.CTkFrame(
            self.widgetFrame,
            fg_color="white",
            width=950,
            height=1000,
        )
        self.informationFrame.pack_propagate(False)
        self.informationFrame.pack(
            side="left", anchor="center", padx=(10, 10), pady=(10, 10)
        )

        self.stockMovementNumberLabel = customtkinter.CTkLabel(
            self.informationFrame,
            text=f"Stock Movement Number: {cellValue['value']}, Item: {itemName}",
            text_color="black",
            font=self.FONT,
        )
        self.stockMovementNumberLabel.pack(
            anchor="center", padx=(10, 10), pady=(10, 10)
        )

        self.expectedDeliveryDateLabel = customtkinter.CTkLabel(
            self.informationFrame,
            text=f"Expected Delivery Date: {deliveryDate}",
            text_color="black",
            font=self.FONT,
        )
        self.expectedDeliveryDateLabel.pack(
            anchor="center", padx=(10, 10), pady=(10, 10)
        )

        self.supplierLabel = customtkinter.CTkLabel(
            self.informationFrame,
            text=f"Supplier: {manufacturerName}",
            text_color="black",
            font=self.FONT,
        )
        self.supplierLabel.pack(anchor="center", padx=(10, 10), pady=(10, 10))

        self.priceLabel = customtkinter.CTkLabel(
            self.informationFrame,
            text=f"Price of Order: £{purchaseOrderPrice}",
            text_color="black",
            font=self.FONT,
            width=950,
        )
        self.priceLabel.pack(anchor="center", padx=(10, 10), pady=(10, 10))

        self.updateButton = customtkinter.CTkButton(
            self.informationFrame,
            fg_color="black",
            text="Update",
            text_color="white",
            font=self.FONT,
            command=lambda: self.updatingPurchaseOrderInformation(cellValue),
        )
        self.updateButton.pack(side="right")

        self.cancelButton = customtkinter.CTkButton(
            self.informationFrame,
            fg_color="black",
            text="Cancel",
            text_color="white",
            font=self.FONT,
        )
        self.cancelButton.pack(side="left")

        self.editingInformationFrame = customtkinter.CTkFrame(
            self.widgetFrame,
            fg_color="white",
            width=950,
            height=1000,
        )
        self.editingInformationFrame.pack_propagate(False)
        self.editingInformationFrame.pack(
            side="right", anchor="center", padx=(10, 10), pady=(10, 10)
        )

        self.editItemsLabel = customtkinter.CTkLabel(
            self.editingInformationFrame,
            text="Edit Quantity Here",
            text_color="black",
            font=self.FONT,
        )
        self.editItemsLabel.pack(anchor="center", padx=(10, 10), pady=(10, 10))

        self.displayItems(cellValue, self.movementOptionMenuStringVar.get())

    def retrievingItemsFromPurchaseOrder(self, cellValue):
        """
        The function retrieves item size and quantity information from the PurchaseOrderInformation table
        based on a given purchase order number.
        :param cellValue: The `cellValue` parameter is a dictionary that contains a key called "value". The
        value of this key is used in the SQL query to retrieve information from the database
        :return: The function `retrievingItemsFromStockMovement` returns the `informationResults`, which is
        a list of tuples containing the item size and quantity retrieved from the database.
        """
        self.db.myCursor.execute(
            """        
            SELECT PurchaseOrderInformation.itemSize, PurchaseOrderInformation.quantity 
            FROM PurchaseOrder 
            JOIN PurchaseOrderInformation ON PurchaseOrder.purchaseOrderID = PurchaseOrderInformation.purchaseOrderID 
            WHERE PurchaseOrder.purchaseOrderNumber = ?
            """,
            (cellValue["value"],),
        )
        self.purchaseOrderInformationResults = self.db.myCursor.fetchall()
        ic(f"purchaseOrderInformationResults: {self.purchaseOrderInformationResults}")
        return self.purchaseOrderInformationResults

    def retrievingItemsFromTransfer(self, cellValue):
        """
        The function retrieves item information from a database table based on a given transfer number.
        :param cellValue: The `cellValue` parameter is a dictionary that contains the value of a cell. It is
        used to retrieve items from a transfer based on the transfer number. The transfer number is obtained
        from the `cellValue["value"]` key in the dictionary
        """
        self.db.myCursor.execute(
            """
        SELECT itemName, itemSize, quantity 
        FROM Transfers
        WHERE transferNumber = ? 
        """,
            (cellValue["value"],),
        )
        self.transferInformationResults = self.db.myCursor.fetchall()
        ic(f"transferInformationResults: {self.transferInformationResults}")

    def displayItems(self, cellValue, movementType):
        """
        The `displayItems` function retrieves items from stock movement and displays them along with their
        size and quantity in a customtkinter GUI.
        :param cellValue: The parameter `cellValue` is the value of a cell in a spreadsheet or table. It is
        used as input to the `retrievingItemsFromStockMovement` method to retrieve a list of items
        """
        self.itemEntry = []
        if movementType == "Purchase Order":
            items = self.retrievingItemsFromPurchaseOrder(cellValue)
        else:
            items = self.retrievingItemsFromTransfer(cellValue)
        for item in items:
            self.itemSize, self.quantity = item
            ic(f"Item Size: {self.itemSize}, Quantity: {self.quantity}")
            self.itemLabel = customtkinter.CTkLabel(
                self.editingInformationFrame,
                text=f"Item Size: {self.itemSize}, Quantity: {self.quantity}",
                text_color="black",
                font=self.FONT,
            )
            self.itemLabel.pack(anchor="center", padx=(10, 10), pady=(10, 10))

            itemEntry = customtkinter.CTkEntry(
                self.editingInformationFrame,
                text_color="black",
                fg_color="white",
                font=self.FONT,
            )
            itemEntry.pack(anchor="center", padx=(10, 10), pady=(10, 10))
            self.itemEntry.append(itemEntry)

    def clearWidgets(self):
        """
        The 'clearWidget' function clears the widgets on the editingInformationFrame, it should be called
        when the user either saves or cancels their changes.
        """
        for widget in self.editingInformationFrame.winfo_children():
            widget.destroy()

    def updatingPurchaseOrderInformation(self, cellValue):
        """
        The 'updatingPurchaseOrderInformation' function retrieves the user input and updates the data in the
        database to the data inputted by the user.
        """
        items = self.retrievingItemsFromPurchaseOrder(cellValue)
        ic(f"items: {items}")
        for i, item in enumerate(items):
            self.itemSize, _ = item
            self.newQuantity = self.itemEntry[i].get()
            ic([entry.get() for entry in self.itemEntry])
            for _ in range(len(items)):
                if self.newQuantity:
                    self.db.myCursor.execute(
                        """
                        UPDATE PurchaseOrderInformation 
                        SET quantity = ? 
                        WHERE itemSize = ? AND purchaseOrderID IN (
                            SELECT purchaseOrderID
                            FROM PurchaseOrder
                            WHERE purchaseOrderNumber = ?
                        )
                        """,
                        (self.newQuantity, self.itemSize, cellValue["value"]),
                    )
                    self.db.commit()
            ic(f"newQuantity: {self.newQuantity}")
            ic(f"itemSize: {self.itemSize}")
        self.clearWidgets()


class PurchaseOrderPage(BasePage):
    def __init__(self, mainWindow, mainFrame, imageWrapper, mainApplicationClass):
        super().__init__(mainWindow, mainFrame, imageWrapper, mainApplicationClass)
        self.db = SQLiteWrapper(
            "database/inventoryDatabase.db",
            "database/loginInfoDatabase.db",
            "database/remindersDatabase.db",
            "database/inventoryDatabaseUpdated.db",
        )
        ic("PurchaseOrderPage Initialized")
        self.itemInformationFrame = customtkinter.CTkFrame(
            master=self.widgetFrame,
            fg_color=self.FGCOLOR,
            width=965,
            height=990,
        )
        (self.itemInformationFrame.pack_propagate(False),)
        self.itemInformationFrame.place(x=10, y=10)
        purchaseOrderNumber = self.db.fetchPurchaseOrderNumber()
        uniqueItems = self.db.fetchUniqueItemNames()
        with sqlite3.connect("database/inventoryDatabase.db") as db:
            myCursor = db.cursor()
            for item in uniqueItems:
                myCursor.execute(
                    """
                    UPDATE Items
                    SET purchaseOrderNumber = ? 
                    WHERE itemName = ?""",
                    (purchaseOrderNumber, item),
                )

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

        with sqlite3.connect("database/inventoryDatabase.db") as db:
            myCursor = db.cursor()
            myCursor.execute("SELECT itemName FROM Items")
            items = myCursor.fetchall()
            options = [item for itemElement in items for item in itemElement]
            uniqueItems = list(set(options))
            self.selectedItem = StringVar()

        self.itemOptionMenu = customtkinter.CTkOptionMenu(
            master=self.itemInformationFrame,
            fg_color=self.FGCOLOR,
            button_color=self.FGCOLOR,
            button_hover_color=self.HOVERCOLOR,
            text_color="black",
            variable=self.selectedItem,
            values=uniqueItems,
            command=self.onItemSelect,
        )
        self.itemOptionMenu.pack(
            anchor="center",
            padx=(10, 10),
            pady=(10, 10),
        )
        self.selectedItem.trace_add("write", self.updateSupplierLabel)
        self.selectedItem.trace_add("write", self.updateLabel)

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

        self.supplierLabel = customtkinter.CTkLabel(
            master=self.itemInformationFrame,
            text="Supplier:",
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

        self.confirmButton = customtkinter.CTkButton(
            master=self.itemInformationFrame,
            text="Confirm",
            text_color="black",
            fg_color="transparent",
            hover_color=self.HOVERCOLOR,
            width=300,
            height=50,
            font=self.FONT,
            command=self.savePurchaseOrder,
        )
        self.confirmButton.pack(
            anchor="w",
            side="left",
            padx=(10, 10),
            pady=(10, 10),
        )

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

        self.orderFrame = customtkinter.CTkFrame(
            master=self.widgetFrame,
            fg_color=self.FGCOLOR,
            width=900,
            height=990,
        )
        self.orderFrame.pack_propagate(False)
        self.orderFrame.place(
            x=self.itemInformationFrame.winfo_width() + 10,
            y=10,
        )

        self.listOfItemsFrame = customtkinter.CTkScrollableFrame(
            master=self.orderFrame,
            fg_color="white",
            width=900,
            height=890,
        )
        self.listOfItemsFrame.grid(row=0, column=0)

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

    def clearListOfItemsFrame(self):
        """
        The function clears all the widgets in the listOfItemsFrame.
        """
        for widget in self.listOfItemsFrame.winfo_children():
            widget.destroy()

    def onItemSelect(self, event):
        """
        The `onItemSelect` function updates the UI when an item is selected, including clearing the price
        label, clearing the list of items frame, retrieving the available sizes for the selected item from
        the database, and creating labels and entry fields for each size.

        :param event: The `event` parameter is the event object that triggered the `onItemSelect` function.
        It contains information about the event, such as the type of event and any additional data
        associated with it. In this case, it is not used in the function, so you can ignore it for now
        """
        self.priceLabel.configure(text="Total Price: £0.00")
        self.clearListOfItemsFrame()
        self.selectedItem = self.itemOptionMenu.get()
        itemSize = self.db.executeDatabaseQuery(
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

    def calculateTotalPrice(self):
        """
        The function calculates the total price of an item based on the selected item and quantity.
        :return: the total price of the selected item and quantities.
        """
        self.totalPrice = 0
        item = self.itemOptionMenu.get()
        rows = self.db.executeDatabaseQuery(
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

    def updateTotalPrice(self, event):
        """
        The function updates the total price and displays it on a label.

        :param event: The `event` parameter is an event object that is passed to the
        `updateTotalPrice` method when it is called. This parameter allows the method to access information
        about the event that triggered the method, such as the user's interaction with a GUI element
        """
        self.totalPrice = self.calculateTotalPrice()
        self.priceLabel.configure(text=f"Total Price: £{self.totalPrice: .2f}")

    def updateSupplierLabel(self, *args):
        """
        The `updateSupplierLabel` function retrieves the manufacturer ID of an item from the database, and
        then retrieves the manufacturer name associated with that ID, updating a label with the supplier
        information.
        """
        item = self.itemOptionMenu.get()
        results = self.db.executeDatabaseQuery(
            "SELECT manufacturerID FROM Items WHERE itemName = ?",
            (item,),
        )
        if results:
            self.supplierID = results[0][0]
            suppliers = self.db.executeDatabaseQuery(
                "SELECT manufacturerName FROM Manufacturers WHERE manufacturerID = ?",
                (self.supplierID,),
            )
            if suppliers:
                self.supplier = suppliers[0][0]
                self.supplierLabel.configure(text=f"Supplier: {self.supplier}")
            else:
                self.supplierLabel.configure(text="Supplier Not Found")
        self.selectedItem = StringVar()
        self.selectedItem.trace_add("write", self.updateSupplierLabel)

    def updateLabel(self, *args):
        """
        The `updateLabel` function updates a label with the selected item's name and SKU, based on the
        selected option from a dropdown menu.
        """
        selectedOption = self.selectedItem.get()
        rows = self.db.executeDatabaseQuery(
            "SELECT sku FROM Items WHERE itemName = ?", (selectedOption,)
        )
        if rows:
            self.sku = rows[0][0]
            self.itemLabel.configure(text=f"{self.selectedItem.get()}(SKU: {self.sku})")
        else:
            self.itemLabel.configure(
                text=f"{self.selectedItem.get()}, (SKU: Not Found)"
            )
        self.selectedItem.trace_add("write", self.updateLabel)

    def updateDate(self):
        """
        The `updateDate` function updates the text of a label widget to display the current date.
        """
        now = datetime.datetime.now()
        dateString = now.strftime("%d.%m.%Y")
        self.createdInformationLabel.configure(
            text=f"Created by: Otto Jonas on {dateString}"
        )

    def resetAttributes(self):
        """
        The function "resetAttributes" resets various attributes and labels to their default values.
        """
        self.itemOptionMenu
        self.itemLabel.configure(text="")
        self.supplierLabel.configure(text="")
        self.priceLabel.configure(text="Total Price: £0.00")
        self.createdInformationLabel.configure(text="Created By: Otto Jonas")
        self.clearListOfItemsFrame()
        self.deliveryDate.set_date(datetime.now().date())

    def savePurchaseOrder(self):
        """
        The `savePurchaseOrder` function saves a purchase order with the specified details and confirms the
        order with the user before committing it to the database.
        """
        currentDate = datetime.now().date()
        itemName = self.selectedItem
        supplier = self.supplierID
        price = self.totalPrice
        createdAt = currentDate
        sizes = list(self.sizeEntries.keys())
        deliveryDate = self.deliveryDate.get_date()
        quantity = self.sizeEntries[self.size[0]].get()
        items = [{"sizes": size} for size in sizes]
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
        itemIDResults = self.db.executeDatabaseQuery(
            "SELECT itemID FROM Items WHERE itemName = ?", (itemName,)
        )
        itemID = itemIDResults[0][0] if itemIDResults else None
        results = self.db.executeDatabaseQuery(
            "SELECT MAX(purchaseOrderNumber) FROM PurchaseOrder", ()
        )
        purchaseOrderNumber = results[0][0] + 1 if results[0][0] is not None else 1

        purchaseOrderInformation = f"""
        purchaseOrderNumber: {purchaseOrderNumber}
        Supplier: {self.supplier}
        Item Name: {itemName}
        Sizes: {sizes}
        Price: {price}
        Created At: {createdAt}
        Delivery Date: {deliveryDate}
        """
        userConfirmation = tkmb.askyesno(
            title="Confirm Purchase Order",
            message=f"Here is a breakdown of your purchase order:\n {purchaseOrderInformation} \nSelect 'YES' to proceed?",
        )
        if userConfirmation:
            for item in items:
                quantity = self.sizeEntries[item["sizes"]].get()
                results = self.db.executeDatabaseQuery(
                    "INSERT INTO PurchaseOrder (purchaseOrderNumber, manufacturer, price, createdAt, deliveryDate) VALUES(?, ?, ?, ?, ?)",
                    (
                        purchaseOrderNumber,
                        supplier,
                        price,
                        createdAt,
                        deliveryDate,
                    ),
                )
                purchaseOrderID = self.db.myCursor.lastrowid
                item["purchaseOrderID"] = purchaseOrderID
                self.db.executeDatabaseQuery(
                    "INSERT INTO PurchaseOrderInformation (purchaseOrderID, itemID, itemSize, quantity) VALUES(?, ?, ?, ?)",
                    (purchaseOrderID, itemID, item["sizes"], quantity),
                )
                self.db.executeDatabaseQuery(
                    "INSERT INTO ItemStock (itemID, itemSize, onOrder) VALUES(?, ?, ?)",
                    (itemID, item["sizes"], quantity),
                )
            self.db.commit()
            self.resetAttributes()
        else:
            return


class TransfersPage(BasePage):
    def __init__(
        self, mainWindow, mainFrame, imageWrapper, mainApplicationClass, cellValue
    ):
        super().__init__(mainWindow, mainFrame, imageWrapper, mainApplicationClass)
        self.db = SQLiteWrapper(
            "database/inventoryDatabase.db",
            "database/loginInfoDatabase.db",
            "database/remindersDatabase.db",
            "database/inventoryDatabaseUpdated.db",
        )
        ic("TransfersPage Initialized")
        transferNumber = self.db.fetchTransferNumber()
        self.uniqueItemNames = self.db.fetchUniqueItemNames()
        values = [[itemNames] for itemNames in self.uniqueItemNames]
        if not values:
            ic("No data retrieved from database")
            values = [[]]
        self.numberOfItems = self.db.getNumberOfItems()

        self.transferInformationFrame = customtkinter.CTkFrame(
            master=self.widgetFrame,
            fg_color=self.FGCOLOR,
            width=930,
            height=990,
        )
        (self.transferInformationFrame.pack_propagate(False),)
        self.transferInformationFrame.place(x=10, y=10)

        self.transferNumberLabel = customtkinter.CTkLabel(
            master=self.transferInformationFrame,
            text=f"Transfer Number: {transferNumber}",
            text_color="black",
            font=self.LABELFONT,
        )
        self.transferNumberLabel.pack(
            anchor="center",
            padx=(10, 10),
            pady=(10, 10),
        )
        with sqlite3.connect("database/inventoryDatabase.db") as db:
            myCursor = db.cursor()
            myCursor.execute("SELECT locationName from Retail")
            locations = myCursor.fetchall()
            options = [
                location
                for locationElement in locations
                for location in locationElement
            ]
            uniqueLocations = list(set(options))
            self.selectedLocationSending = StringVar()
            self.selectedLocationReceiving = StringVar()

        self.sendingStoreOptionMenu = customtkinter.CTkOptionMenu(
            master=self.transferInformationFrame,
            fg_color=self.FGCOLOR,
            button_color=self.FGCOLOR,
            button_hover_color=self.HOVERCOLOR,
            text_color="black",
            variable=self.selectedLocationSending,
            values=uniqueLocations,
        )
        self.sendingStoreOptionMenu.pack(
            anchor="center",
            padx=(10, 10),
            pady=(10, 10),
        )

        self.receivingStoreOptionMenu = customtkinter.CTkOptionMenu(
            master=self.transferInformationFrame,
            fg_color=self.FGCOLOR,
            button_color=self.FGCOLOR,
            button_hover_color=self.HOVERCOLOR,
            text_color="black",
            variable=self.selectedLocationReceiving,
            values=uniqueLocations,
        )
        self.receivingStoreOptionMenu.pack(
            anchor="center",
            padx=(10, 10),
            pady=(10, 10),
        )

        self.itemSearchContainer = customtkinter.CTkFrame(
            self.transferInformationFrame,
            fg_color=self.FGCOLOR,
            width=900,
            height=70,
        )
        self.itemSearchContainer.pack_propagate(False)
        self.itemSearchContainer.pack(anchor="center")

        self.itemSearchEntry = customtkinter.CTkEntry(
            self.itemSearchContainer,
            fg_color=self.FGCOLOR,
            width=600,
            height=50,
            placeholder_text="Enter item name",
            placeholder_text_color="black",
            text_color="black",
            border_color="black",
            border_width=1,
        )
        self.itemSearchEntry.grid(row=0, column=0, padx=(5, 5), pady=(10, 10))

        self.searchButton = customtkinter.CTkButton(
            self.itemSearchContainer,
            text="Search",
            text_color="black",
            fg_color=self.FGCOLOR,
            width=70,
            height=50,
            command=self.search,
            state="disabled",
        )
        self.searchButton.grid(row=0, column=1, padx=(5, 5), pady=(10, 10))

        self.searchedItemScrollFrame = customtkinter.CTkScrollableFrame(
            self.transferInformationFrame,
            fg_color="red",
            width=900,
            height=680,
        )
        self.searchedItemScrollFrame.pack_propagate(False)
        self.searchedItemScrollFrame.pack(anchor="center", padx=(10, 10), pady=(10, 10))

        self.itemListTable = CTkTable(
            self.searchedItemScrollFrame,
            values=values,
            colors=["#ffffff", "#ffffff"],
            hover_color="grey",
            text_color="black",
            header_color=False,
            corner_radius=0,
        )
        ic(f"itemListTable Created: {self.itemListTable}")
        self.itemListTable.edit_row(0, text_color="black", hover_color="grey")
        self.itemListTable.pack_propagate(False)
        self.itemListTable.pack(fill="both", expand=True)
        ic(f"itemListTable Packed: {self.itemListTable}")

        self.confirmButton = customtkinter.CTkButton(
            master=self.transferInformationFrame,
            text="Confirm and Send",
            text_color="black",
            fg_color="transparent",
            hover_color=self.HOVERCOLOR,
            width=300,
            height=50,
            font=self.FONT,
        )
        self.confirmButton.pack(
            anchor="w",
            side="left",
            padx=(10, 10),
            pady=(10, 10),
        )

        self.cancelButton = customtkinter.CTkButton(
            master=self.transferInformationFrame,
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
        self.searchButton.configure(state="normal")

        self.itemsFrame = customtkinter.CTkFrame(
            self.widgetFrame,
            fg_color="white",
            width=955,
            height=990,
        )
        self.itemsFrame.pack_propagate(False)
        self.itemsFrame.place(x=950, y=10)

        self.itemsScrollFrame = customtkinter.CTkScrollableFrame(
            self.itemsFrame,
            fg_color="white",
        )
        self.itemsScrollFrame.pack(fill="both", expand=True)

    def search(self):
        """
        The `search` function retrieves data from a database based on a search term, updates the UI with the
        search results, and displays them in a table.
        """
        searchTerm = self.itemSearchEntry.get()
        results = self.db.searchDatabase("Items", "itemName", searchTerm)
        values = []
        if not values:
            ic("No data retrieved from database")
        else:
            ic(f"Data retrieved from database: {values}")
        if hasattr(self, "itemListTable"):
            self.itemListTable.pack_forget()
            self.itemListTable.destroy()
        values = []
        for result in results:
            ic(f"Item: {result}")
            itemName = result[1].lower()
            itemSize = result[-2].split(",")
            if searchTerm.lower() in itemName:
                sizes = ", ".join([size.strip() for size in itemSize])
                values.append([f"{result[1]}: {sizes}"])
        self.itemListTable = CTkTable(
            self.searchedItemScrollFrame,
            values=values,
            colors=["#ffffff", "#ffffff"],
            hover_color="grey",
            text_color="black",
            header_color=False,
            corner_radius=0,
            command=self.onCellSelect,
        )
        ic(f"itemListTable Created:{self.itemListTable}")
        self.itemListTable.edit_row(0, text_color="black", hover_color="grey")
        self.itemListTable.pack_propagate(False)
        self.itemListTable.pack(expand=True, fill="both")
        ic(f"itemListTable Packed: {self.itemListTable}")

    def onCellSelect(self, cellValue):
        """
        The `onCellSelect` function takes a cell value as input, extracts the selected row values, converts
        them to a string, and creates a label with the selected row values.

        :param cellValue: The `cellValue` parameter is a dictionary that contains the value of the selected
        cell
        """
        self.selectedCell = cellValue["value"]
        ic(f"self.selectedCell: {cellValue}")

        selectedRowValues = cellValue.get("value", [])
        if not isinstance(selectedRowValues, list):
            selectedRowValues = [selectedRowValues]
        else:
            ic(f"selectedRowValues is not a list: {selectedRowValues}")

        selectedRowValuesString = ", ".join(map(str, selectedRowValues))
        ic(f"selectedRowValues: {selectedRowValues}")
        ic(f"selectedRowValuesString: {selectedRowValuesString}")

        self.itemLabel = customtkinter.CTkLabel(
            self.itemsScrollFrame,
            text=f"{selectedRowValuesString}",
            text_color="black",
            font=self.FONT,
        )
        self.itemLabel.pack(anchor="center", padx=(10, 10), pady=(10, 10))

        self.itemEntry = customtkinter.CTkEntry(
            self.itemsScrollFrame,
            text_color="black",
            fg_color="white",
            font=self.FONT,
        )
        self.itemEntry.pack(anchor="center", padx=(10, 10), pady=(10, 10))

    def transferingStock(self):
        pass

    def savingTransferToDatabase(self):
        pass


class ReportsPage(BasePage):
    def __init__(self, mainFrame, mainWindow, imageWrapper, mainApplicationClass):
        super().__init__(mainFrame, mainWindow, imageWrapper, mainApplicationClass)
        self.db = SQLiteWrapper(
            "database/inventoryDatabase.db",
            "database/loginInfoDatabase.db",
            "database/remindersDatabase.db",
            "database/inventoryDatabaseUpdated.db",
        )
        ic("ReportsPage Initialized")

        self.userReportGenerationFrame = customtkinter.CTkFrame(
            self.widgetFrame,
            fg_color=self.FGCOLOR,
            width=290,
            height=990,
        )
        self.userReportGenerationFrame.pack_propagate(False)
        self.userReportGenerationFrame.place(
            x=10, y=-self.userReportGenerationFrame.winfo_width() + 10
        )

        self.userReportGenerationLabel = customtkinter.CTkLabel(
            master=self.userReportGenerationFrame,
            text="User Report Generation",
            text_color="black",
            font=self.LABELFONT,
        )
        self.userReportGenerationLabel.pack(
            anchor="center",
            padx=(10, 10),
            pady=(10, 10),
        )

        self.reportTypeVariable = StringVar(value="daily")

        self.dailyRadioButton = customtkinter.CTkRadioButton(
            master=self.userReportGenerationFrame,
            text="Daily Report",
            variable=self.reportTypeVariable,
            value="daily",
            text_color="black",
            fg_color="white",
            font=self.FONT,
        )
        self.dailyRadioButton.pack(
            anchor="center",
            padx=(10, 10),
            pady=(10, 10),
        )
        self.weeklyRadioButton = customtkinter.CTkRadioButton(
            master=self.userReportGenerationFrame,
            text="Weekly Report",
            variable=self.reportTypeVariable,
            value="weekly",
            text_color="black",
            fg_color="white",
            font=self.FONT,
        )
        self.weeklyRadioButton.pack(
            anchor="center",
            padx=(10, 10),
            pady=(10, 10),
        )
        self.monthlyRadioButton = customtkinter.CTkRadioButton(
            master=self.userReportGenerationFrame,
            text="Monthly Report",
            variable=self.reportTypeVariable,
            value="monthly",
            text_color="black",
            fg_color="white",
            font=self.FONT,
        )
        self.monthlyRadioButton.pack(
            anchor="center",
            padx=(10, 10),
            pady=(10, 10),
        )
        self.yearlyRadioButton = customtkinter.CTkRadioButton(
            master=self.userReportGenerationFrame,
            text="Yearly Report",
            variable=self.reportTypeVariable,
            value="yearly",
            text_color="black",
            fg_color="white",
            font=self.FONT,
        )
        self.yearlyRadioButton.pack(
            anchor="center",
            padx=(10, 10),
            pady=(10, 10),
        )

        with sqlite3.connect("database/inventoryDatabase.db") as invdb:
            myCursor = invdb.cursor()
            myCursor.execute("SELECT categoryName from Categories")
            categories = myCursor.fetchall()
            options = [
                category
                for categoryElement in categories
                for category in categoryElement
            ]
            uniqueCategories = ["All"] + list(set(options))
            self.selectedItem = StringVar()

        self.catagoryOptionMenu = customtkinter.CTkOptionMenu(
            self.userReportGenerationFrame,
            fg_color=self.FGCOLOR,
            button_color=self.FGCOLOR,
            button_hover_color=self.FGCOLOR,
            text_color="black",
            variable=self.selectedItem,
            values=uniqueCategories,
        )
        self.catagoryOptionMenu.pack(anchor="center", padx=(10, 10), pady=(10, 10))

        self.exportReportButton = customtkinter.CTkButton(
            master=self.userReportGenerationFrame,
            text="Export Report",
            text_color="black",
            fg_color="transparent",
            width=300,
            height=50,
            font=self.FONT,
            command=self.exportReportFileFunction,
        )
        self.exportReportButton.pack(
            anchor="center",
            padx=(10, 10),
            pady=(10, 10),
        )

        self.pieChartFrame = customtkinter.CTkFrame(
            master=self.widgetFrame,
            fg_color="white",
            width=800,
            height=700,
        )
        self.pieChartFrame.pack_propagate(False)
        self.pieChartFrame.place(x=310, y=10)

        self.chartFrame = customtkinter.CTkFrame(
            master=self.widgetFrame,
            fg_color="white",
            width=800,
            height=280,
        )
        self.chartFrame.pack_propagate(False)
        self.chartFrame.place(x=310, y=720)

        self.activitiesFrame = customtkinter.CTkFrame(
            master=self.widgetFrame,
            fg_color=self.FGCOLOR,
            width=300,
            height=1010,
        )
        self.activitiesFrame.pack_propagate(False)
        self.activitiesFrame.pack(
            anchor="e",
            side="right",
            padx=(10, 10),
            pady=(10, 10),
        )

        self.activitiesFrameLabel = customtkinter.CTkLabel(
            self.activitiesFrame,
            text="Daily Activity",
            font=self.LABELFONT,
            text_color="black",
        )
        self.activitiesFrameLabel.pack(anchor="center", padx=(10, 10), pady=(10, 10))

        self.activitiesFrameInfo = customtkinter.CTkLabel(
            self.activitiesFrame,
            text="Information of activity in company each day",
            font=self.FONT,
            text_color="black",
        )
        self.activitiesFrameInfo.pack(anchor="center", padx=(10, 10), pady=(10, 10))

        self.chartCanvas = customtkinter.CTkFrame(
            self.chartFrame, fg_color="transparent", width=950, height=280
        )
        self.chartCanvas.pack_propagate(False)
        self.chartCanvas.pack(anchor="center", padx=(10, 10), pady=(10, 10))

    def exportReportFileFunction(self):
        """
        The function `exportReportFileFunction` exports a report file based on the selected report type and
        category.
        """
        reportType = self.reportTypeVariable.get()
        now = datetime.now()
        ic(f"now: {now}")
        safeTimeString = now.strftime("%Y-%m-%d_%H-%M-%S")
        selectedCategory = self.catagoryOptionMenu.get()
        startOfLastWeekRaw = now - timedelta(days=now.weekday() + 7)
        endOfLastWeekRaw = startOfLastWeekRaw + timedelta(days=6)
        startOfLastWeek = startOfLastWeekRaw.strftime("%Y-%m-%d")
        endOfLastWeek = endOfLastWeekRaw.strftime("%Y-%m-%d")
        startOfLastMonthRaw = now.replace(day=1) - relativedelta(months=1)
        endOfLastMonthRaw = now.replace(day=1) - relativedelta(days=1)
        startOfLastMonth = startOfLastMonthRaw.strftime("%Y-%m-%d")
        endOfLastMonth = endOfLastMonthRaw.strftime("%Y-%m-%d")
        startOfLastYearRaw = now.replace(year=now.year - 1, month=1, day=1)
        endOfLastYearRaw = now.replace(year=now.year - 1, month=12, day=31)
        startOfLastYear = startOfLastYearRaw.strftime("%Y-%m-%d")
        endOfLastYear = endOfLastYearRaw.strftime("%Y-%m-%d")
        try:
            with open(f"{safeTimeString}.csv", "w") as exportedFile:
                csvPen = csv.writer(exportedFile, delimiter=",")

                if reportType == "daily":
                    if selectedCategory == "All":
                        self.db.myCursor.execute(
                            """
                            SELECT Sales.orderNumber, Items.itemName, Sales.quantity, Sales.priceOfSale, Sales.dateOfSale 
                            FROM Sales 
                            JOIN Items 
                            ON Sales.itemID = Items.itemID 
                            JOIN 
                            Categories 
                            ON Items.categoryID = Categories.categoryID 
                            WHERE Sales.dateOfSale = CURRENT_DATE
                            """
                        )
                    else:
                        self.db.myCursor.execute(
                            f"""
                            SELECT Sales.orderNumber, Items.itemName, Sales.quantity, Sales.priceOfSale, Sales.dateOfSale 
                            FROM Sales 
                            JOIN Items 
                            ON Sales.itemID = Items.itemID 
                            JOIN Categories 
                            ON Items.categoryID = Categories.categoryID 
                            WHERE Categories.categoryName = '{selectedCategory}' 
                            AND Sales.dateOfSale = CURRENT_DATE
                            """
                        )

                elif reportType == "weekly":
                    if selectedCategory == "All":
                        self.db.myCursor.execute(
                            f"""
                            SELECT Sales.orderNumber, Items.itemName, Sales.quantity, Sales.priceOfSale, Sales.dateOfSale 
                            FROM Sales 
                            JOIN Items 
                            ON Sales.itemID = Items.itemID 
                            JOIN Categories 
                            ON Items.categoryID = Categories.categoryID 
                            WHERE Sales.dateOfSale 
                            BETWEEN '{startOfLastWeek}' 
                            AND '{endOfLastWeek}'
                            """
                        )
                    else:
                        self.db.myCursor.execute(
                            f"""
                            SELECT Sales.orderNumber, Items.itemName, Sales.quantity, Sales.priceOfSale, Sales.dateOfSale 
                            FROM Sales 
                            JOIN Items 
                            ON Sales.itemID = Items.itemID 
                            JOIN Categories ON Items.categoryID = Categories.categoryID 
                            WHERE Categories.categoryName = '{selectedCategory}' 
                            AND Sales.dateOfSale 
                            BETWEEN '{startOfLastWeek}' 
                            AND '{endOfLastWeek}'
                            """
                        )

                elif reportType == "monthly":
                    if selectedCategory == "All":
                        self.db.myCursor(
                            f"""
                            SELECT Sales.orderNumber, Items.itemName, Sales.quantity, Sales.priceOfSale, Sales.dateOfSale 
                            FROM Sales 
                            JOIN Items 
                            ON Sales.itemID = Items.itemID 
                            JOIN Categories 
                            ON Items.categoryID = Categories.categoryID 
                            WHERE Sales.dateOfSale 
                            BETWEEN '{startOfLastMonth}' 
                            AND '{endOfLastMonth}'
                            """
                        )
                    else:
                        self.db.myCursor.execute(
                            f"""
                            SELECT Sales.orderNumber, Items.itemName, Sales.quantity, Sales.priceOfSale, Sales.dateOfSale 
                            FROM Sales 
                            JOIN Items 
                            ON Sales.itemID = Items.itemID 
                            JOIN Categories 
                            ON Items.categoryID = Categories.categoryID 
                            WHERE Categories.categoryName = '{selectedCategory}' 
                            AND Sales.dateOfSale 
                            BETWEEN '{startOfLastMonth}' 
                            AND '{endOfLastMonth}'
                            """
                        )

                elif reportType == "yearly":
                    if selectedCategory == "All":
                        self.db.myCursor.execute(
                            f"""
                            SELECT Sales.orderNumber, Items.itemName, Sales.quantity, Sales.priceOfSale, Sales.dateOfSale 
                            FROM Sales 
                            JOIN Items 
                            ON Sales.itemID = Items.itemID 
                            JOIN Categories 
                            ON Items.categoryID = Categories.categoryID 
                            WHERE Sales.dateOfSale 
                            BETWEEN '{startOfLastYear}' 
                            AND '{endOfLastYear}'
                            """
                        )
                    else:
                        self.db.myCursor.execute(
                            f"""
                            SELECT Sales.orderNumber, Items.itemName, Sales.quantity, Sales.priceOfSale, Sales.dateOfSale 
                            FROM Sales 
                            JOIN Items 
                            ON Sales.itemID = Items.itemID 
                            JOIN Categories 
                            ON Items.categoryID = Categories.categoryID 
                            WHERE Categories.categoryName = '{selectedCategory}' 
                            AND Sales.dateOfSale 
                            BETWEEN '{startOfLastYear}' 
                            AND '{endOfLastYear}'
                            """
                        )
                rows = self.db.myCursor.fetchall()
                ic(f"ReportType: {reportType}")
                ic(f"Rows: {rows}")
                ic(f"EndOfLastWeek = {endOfLastWeek}")
                ic(f"StartOfLastWeek: {startOfLastWeek}")
                if rows:
                    csvPen.writerow(
                        [
                            descriptionElement[0]
                            for descriptionElement in self.db.myCursor.description
                        ]
                    )
                    csvPen.writerows(rows)
                    dirpath = os.getcwd() + r"\salesDateExported.csv"
                    ic("Data has been successfully export: {}".format(dirpath))
                    tkmb.showinfo(
                        title="Success",
                        message=f"Report has been successfully exported: {dirpath}",
                    )
                else:
                    ic("Could not export file")
                    tkmb.showerror(
                        title="Error", message="Could not export file, please try again"
                    )
        except Error as e:
            ic(f"File could not be exported: {e}")

    def drawPieChart(self):
        """
        The function `drawPieChart` retrieves data from a database, creates a pie chart using matplotlib,
        and displays it in a tkinter window.
        """
        self.db.myCursor.execute(
            """
            SELECT locationOfSale, 
            COUNT(*) 
            FROM Sales 
            GROUP BY locationOfSale
            """
        )
        locationOfSales = self.db.myCursor.fetchall()

        locations = [row[0] for row in locationOfSales]
        sales = [row[1] for row in locationOfSales]

        self.pieChart = plt.figure(figsize=(10, 7))
        canvas = FigureCanvasTkAgg(self.pieChart, master=self.pieChartFrame)
        pie = plt.pie(sales, labels=locations)
        plt.legend(pie[0], locations, bbox_to_anchor=(0.5, 1.05))
        canvas.get_tk_widget().pack(side="top", fill="both", expand=True)

    def drawGraph(self):
        """
        The `drawGraph` function retrieves data from a database, converts the dates to a numerical format,
        and then plots the data on a graph using matplotlib.
        """
        self.db.myCursor.execute(
            """
            SELECT DATE(dateOfSale), 
            COUNT(*) 
            FROM Sales 
            GROUP BY DATE(dateOfSale)
            """
        )
        data = self.db.myCursor.fetchall()
        dates = [date2num(datetime.strptime(row[0], "%Y-%m-%d")) for row in data]
        sales = [row[1] for row in data]
        fig = Figure(figsize=(5, 6), dpi=100)
        a = fig.add_subplot(111)
        a.plot_date(dates, sales, "-")
        canvas = FigureCanvasTkAgg(fig, master=self.chartCanvas)
        canvas.draw()
        canvas.get_tk_widget().pack(side="top", fill="both", expand=True)


# The below code is a Python script that creates an instance of the `MainApplicationClass` and runs
# its main window using the `mainloop()` method. The `if __name__ == "__main__":` condition ensures
# that the code inside it is only executed if the script is run directly and not imported as a module.
if __name__ == "__main__":
    mainApplicationClass = MainApplicationClass()
    mainApplicationClass.mainWindow.mainloop()
