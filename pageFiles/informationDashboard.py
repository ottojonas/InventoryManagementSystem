import datetime
import sqlite3

import customtkinter
import matplotlib.pyplot as plt
import numpy as np
from CTkTable import CTkTable
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from PIL import Image
from windows_toasts import Toast, ToastDisplayImage, WindowsToaster

customtkinter.set_appearance_mode("system")


class InformationPageDashboard(customtkinter.CTk):
    HOVERCOLOR = "#5e6963"
    FGCOLOR = "#37443d"
    FONT = ("Aptos", 15, "bold")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("Dashboard Front Page")
        self.geometry(
            "{}x{}".format(
                self.winfo_screenwidth(),
                self.winfo_screenheight(),
            )
        )
        self.resizable(True, True)
        self.numberOfRows = 0

        self.iconDictionary = {
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
        for iconName, iconPath in self.iconDictionary.items():
            setattr(self, iconName, customtkinter.CTkImage(Image.open(iconPath)))

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

        # * Sidebar Image Label for Top Bar Frame
        self.topBarButton = customtkinter.CTkButton(
            master=self.topBarFrame,
            image=self.sideBarIcon,
            text="",
            hover=False,
            fg_color="transparent",
            width=50,
            height=50,
            command=self.toggleSideBar,
        )
        self.topBarButton.pack(
            anchor="center",
            side="left",
            padx=(5, 0),
            pady=(0, 0),
        )
        self.topBarButton.place(x=5, y=10)

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

        # * Profile Button
        self.profileButton = customtkinter.CTkButton(
            master=self.topBarFrame,
            image=self.profileIcon,
            text="",
            hover=False,
            fg_color="transparent",
            width=50,
            height=50,
        )
        self.profileButton.pack(
            anchor="center",
            fill="both",
            side="right",
            padx=(0, 5),
            pady=(0, 0),
        )
        self.profileButton.place(x=1860, y=10)

        # * Notification Button
        self.notificationButton = customtkinter.CTkButton(
            master=self.topBarFrame,
            image=self.notificationBellIcon,
            text="",
            hover=False,
            fg_color="transparent",
            width=50,
            height=50,
        )
        self.notificationButton.pack(
            anchor="center",
            fill="both",
            side="right",
            padx=(0, 5),
            pady=(0, 0),
        )
        self.notificationButton.place(x=1810, y=10)

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

        # * Sidebar Button for Side Bar Frame
        self.sideBarButton = customtkinter.CTkButton(
            master=self.sideBarFrame,
            image=self.sideBarIcon,
            text="",
            hover=False,
            fg_color="transparent",
            width=50,
            height=50,
            command=self.toggleSideBar,
        )
        self.sideBarButton.pack(
            anchor="w",
            side="top",
            padx=(5, 0),
            pady=(5, 0),
        )

        # * Company Label for Side Bar Frame
        self.companyLabelSideFrame = customtkinter.CTkLabel(
            master=self.sideBarFrame,
            text="Oliver Brown",
            text_color="black",
            anchor="w",
            justify="left",
            font=self.FONT,
        )
        self.companyLabelSideFrame.pack(
            side="top",
            padx=(10, 0),
            pady=(0, 0),
        )
        # * Buttons on side frame
        self.homeButton = customtkinter.CTkButton(
            master=self.sideBarFrame,
            image=self.homeIcon,
            text="Home",
            text_color="black",
            fg_color="transparent",
            width=300,
            height=50,
            font=self.FONT,
            compound="left",
        )
        self.homeButton.pack(
            anchor="w",
            side="top",
            padx=(20, 20),
            pady=(10, 10),
        )

        # * Sell Button
        self.sellButton = customtkinter.CTkButton(
            master=self.sideBarFrame,
            image=self.shoppingCartIcon,
            text="Sell",
            text_color="black",
            fg_color="transparent",
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

        # * Inventory Button
        self.inventoryButton = customtkinter.CTkButton(
            master=self.sideBarFrame,
            image=self.inventoryIcon,
            text="Inventory",
            text_color="black",
            fg_color="transparent",
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

        # * Stock Control Button
        self.stockControlButton = customtkinter.CTkButton(
            master=self.sideBarFrame,
            image=self.stockControlIcon,
            text="Stock Control",
            text_color="black",
            fg_color="transparent",
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

        # * Orders and Transfers Button
        self.stockMovementButton = customtkinter.CTkButton(
            master=self.sideBarFrame,
            image=self.orderIcon,
            text="Stock Movement",
            text_color="black",
            fg_color="transparent",
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

        # * Customers Button
        self.customersButton = customtkinter.CTkButton(
            master=self.sideBarFrame,
            image=self.customerIcon,
            text="Customers",
            text_color="black",
            fg_color="transparent",
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

        # * Reports Button
        self.reportsButton = customtkinter.CTkButton(
            master=self.sideBarFrame,
            image=self.reportsIcon,
            text="Reports",
            text_color="black",
            fg_color="transparent",
            width=300,
            height=50,
            font=self.FONT,
            compound="left",
        )
        self.reportsButton.pack(
            anchor="w",
            side="top",
            padx=(20, 20),
            pady=(10, 10),
        )

        # * Chat Button
        self.chatButton = customtkinter.CTkButton(
            master=self.sideBarFrame,
            text="Chat",
            text_color="black",
            fg_color="transparent",
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

        # * Settings Button
        self.settingsButton = customtkinter.CTkButton(
            master=self.sideBarFrame,
            image=self.settingsIcon,
            text="Settings",
            text_color="black",
            fg_color="transparent",
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

        # * Reminders Frame
        self.remindersFrame = customtkinter.CTkFrame(
            master=self,
            fg_color="white",
            width=790,
            height=500,
        )
        self.remindersFrame.grid_propagate(False)
        self.remindersFrame.place(
            x=self.sideBarFrame.winfo_width() + 10,
            y=80,
        )

        # * Reminders List Table Frame
        self.remindersList = customtkinter.CTkScrollableFrame(
            master=self.remindersFrame,
            fg_color="transparent",
            width=750,
            height=400,
        )
        self.remindersList.grid(
            row=0,
            column=0,
            padx=(10, 10),
            pady=(10, 10),
            sticky="nsew",
        )

        # * Reminders userEntry
        self.userReminderEntry = customtkinter.CTkEntry(
            master=self.remindersFrame,
            placeholder_text="Add a task / reminder",
            fg_color="#becaee",
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
        for reminder in self.reminders:
            self.reminderLabel = customtkinter.CTkLabel(
                master=self.remindersList,
                text=reminder,
            )
            self.reminderLabel.grid_propagate(False)
            self.reminderLabel.grid()

        # * Reminders Table
        self.remindersTable = CTkTable(
            master=self.remindersList,
            values=self.reminders if self.reminders else [["", ""]],
            colors=["#becaee", "#cbd4f1"],
            hover_color="#a4b4e7",
            text_color="black",
            header_color=False,
            width=250,
        )
        self.remindersTable.edit_row(
            0,
            text_color="black",
            hover_color="#a4b4e7",
        )
        self.remindersTable.pack_propagate(False)
        self.remindersTable.grid(sticky="ew")
        self.remindersTable.bind("<<CTableClick>>", self.deleteRow)

        # * Shopify Orders Frame
        self.shopifyOrdersFrame = customtkinter.CTkFrame(
            master=self,
            fg_color="white",
            width=1100,
            height=500,
        )
        self.shopifyOrdersFrame.pack_propagate(False)
        self.shopifyOrdersFrame.place(
            x=self.remindersFrame.winfo_width() + 10,
            y=80,
        )

        # * Label Row for Shopify Order Info Frame
        self.labelRowFrame = customtkinter.CTkFrame(
            master=self.shopifyOrdersFrame,
            fg_color="transparent",
            width=1000,
            height=50,
        )
        self.labelRowFrame.grid_propagate(False)
        self.labelRowFrame.grid(row=0, column=0)

        # * Shopify Order Frame Label Row Labels
        self.orderNumberLabel = customtkinter.CTkLabel(
            master=self.labelRowFrame,
            text="Order Number",
            text_color="black",
            anchor="w",
            justify="center",
            font=self.FONT,
        )
        self.orderNumberLabel.grid(
            row=0,
            column=1,
            sticky="w",
            padx=(40, 40),
            pady=(10, 10),
        )

        self.customerNameLabel = customtkinter.CTkLabel(
            master=self.labelRowFrame,
            text="Customer Name",
            text_color="black",
            anchor="w",
            justify="center",
            font=self.FONT,
        )
        self.customerNameLabel.grid(
            row=0,
            column=2,
            sticky="w",
            padx=(40, 40),
            pady=(10, 10),
        )

        self.totalPriceLabel = customtkinter.CTkLabel(
            master=self.labelRowFrame,
            text="Price",
            text_color="black",
            anchor="w",
            justify="center",
            font=self.FONT,
        )
        self.totalPriceLabel.grid(
            row=0,
            column=3,
            sticky="w",
            padx=(50, 50),
            pady=(10, 10),
        )

        self.fulfilmentStatusLabel = customtkinter.CTkLabel(
            master=self.labelRowFrame,
            text="Fulfilment Status",
            text_color="black",
            anchor="w",
            justify="center",
            font=self.FONT,
        )
        self.fulfilmentStatusLabel.grid(
            row=0,
            column=4,
            sticky="w",
            padx=(40, 40),
            pady=(10, 10),
        )

        self.deliveryMethodLabel = customtkinter.CTkLabel(
            master=self.labelRowFrame,
            text="Delivery Method",
            text_color="black",
            anchor="w",
            justify="center",
            font=self.FONT,
        )
        self.deliveryMethodLabel.grid(
            row=0,
            column=5,
            sticky="w",
            padx=(40, 40),
            pady=(10, 10),
        )

        self.tagsLabel = customtkinter.CTkLabel(
            master=self.labelRowFrame,
            text="TAGS",
            text_color="black",
            anchor="w",
            justify="center",
            font=self.FONT,
        )
        self.tagsLabel.grid(
            row=0,
            column=6,
            sticky="w",
            padx=(60, 60),
            pady=(10, 10),
        )

        # * Test Data for Table
        self.testTableData = [
            ["3833", "Alice", "£23", "Confirmed", "Shipping", "Order"],
            ["3833", "Alice", "£23", "Confirmed", "Shipping", "Order"],
            ["3833", "Alice", "£23", "Confirmed", "Shipping", "Order"],
            ["3833", "Alice", "£23", "Confirmed", "Shipping", "Order"],
            ["3833", "Alice", "£23", "Confirmed", "Shipping", "Order"],
            ["3833", "Alice", "£23", "Confirmed", "Shipping", "Order"],
            ["3833", "Alice", "£23", "Confirmed", "Shipping", "Order"],
            ["3833", "Alice", "£23", "Confirmed", "Shipping", "Order"],
            ["3833", "Alice", "£23", "Confirmed", "Shipping", "Order"],
            ["3833", "Alice", "£23", "Confirmed", "Shipping", "Order"],
            ["3833", "Alice", "£23", "Confirmed", "Shipping", "Order"],
            ["3833", "Alice", "£23", "Confirmed", "Shipping", "Order"],
            ["3833", "Alice", "£23", "Confirmed", "Shipping", "Order"],
            ["3833", "Alice", "£23", "Confirmed", "Shipping", "Order"],
            ["3833", "Alice", "£23", "Confirmed", "Shipping", "Order"],
            ["3833", "Alice", "£23", "Confirmed", "Shipping", "Order"],
            ["3833", "Alice", "£23", "Confirmed", "Shipping", "Order"],
            ["3833", "Alice", "£23", "Confirmed", "Shipping", "Order"],
            ["3833", "Alice", "£23", "Confirmed", "Shipping", "Order"],
            ["3833", "Alice", "£23", "Confirmed", "Shipping", "Order"],
            ["3833", "Alice", "£23", "Confirmed", "Shipping", "Order"],
            ["3833", "Alice", "£23", "Confirmed", "Shipping", "Order"],
            ["3833", "Alice", "£23", "Confirmed", "Shipping", "Order"],
            ["3833", "Alice", "£23", "Confirmed", "Shipping", "Order"],
            ["3833", "Alice", "£23", "Confirmed", "Shipping", "Order"],
            ["3833", "Alice", "£23", "Confirmed", "Shipping", "Order"],
            ["3833", "Alice", "£23", "Confirmed", "Shipping", "Order"],
            ["3833", "Alice", "£23", "Confirmed", "Shipping", "Order"],
        ]

        # * Table Frame
        self.shopifyOrdersTableFrame = customtkinter.CTkScrollableFrame(
            master=self.shopifyOrdersFrame,
            fg_color="transparent",
            width=1070,
            height=416,
        )
        self.shopifyOrdersTableFrame.grid(
            row=2,
            column=0,
            padx=(10, 0),
            pady=(10, 10),
        )

        # * Shopify Orders Table
        self.shopifyOrdersTable = CTkTable(
            master=self.shopifyOrdersTableFrame,
            values=self.testTableData,
            colors=["#becaee", "#cbd4f1"],
            hover_color="#a4b4e7",
            text_color="black",
            header_color=False,
            width=170,
        )
        self.shopifyOrdersTable.edit_row(
            0,
            text_color="black",
            hover_color="#a4b4e7",
        )
        self.shopifyOrdersTable.pack_propagate(False)
        self.shopifyOrdersTable.grid(sticky="nsew")

        # * Graph of Data Frame
        self.dataGraphFrame = customtkinter.CTkFrame(
            master=self,
            fg_color="white",
            width=1900,
            height=450,
        )
        self.dataGraphFrame.pack_propagate(False)
        self.dataGraphFrame.place(
            x=self.sideBarFrame.winfo_width() + 10,
            y=590,
        )

        # * Frame for graph to be placed in
        self.plotDataGraphFrame = customtkinter.CTkFrame(
            master=self.dataGraphFrame,
            fg_color="#cbd4f1",
            width=1880,
            height=430,
        )
        self.plotDataGraphFrame.pack_propagate(False)
        self.plotDataGraphFrame.pack(
            anchor="center",
            padx=(10, 10),
            pady=(10, 10),
        )

    # * Random data for Data Graph Frame
    def generateRandomData(self):
        x = np.linspace(0, 2 * np.pi, 100)
        y = np.sin(x) + np.random.random(100) - 0.5
        return x, y

    # * Draw Graph Using generateRandomData()
    def drawGraph(self):
        x, y = self.generateRandomData()
        fig = plt.Figure(figsize=(5, 6), dpi=100)
        fig.add_subplot(111).plot(x, y, color="#58689b")
        canvas = FigureCanvasTkAgg(fig, master=self.plotDataGraphFrame)
        canvas.draw()
        canvas.get_tk_widget().pack(
            side="top",
            expand=True,
            fill="both",
        )

    # * Fetching Reminders from Reminders Database
    def fetchReminders(self):
        with sqlite3.connect("database/remindersDatabase.db") as db:
            myCursor = db.cursor()
            myCursor.execute("SELECT * FROM Reminders")
            reminders = myCursor.fetchall()
            return reminders

    # * Add reminder to Database function
    def addReminder(self, reminder):
        with sqlite3.connect("database/remindersDatabase.db") as db:
            myCursor = db.cursor()
            myCursor.execute(
                "INSERT INTO Reminders (reminderTask, createdAt) VALUES (?, datetime('now'))",
                (reminder,),
            )
            db.commit()

    # * Function to Update the Reminders Table every time a new reminder is added
    def updateRemindersTable(self):
        self.numberOfColumns = 3
        for row in range(self.numberOfRows):
            for column in range(self.numberOfColumns):
                self.remindersTable.delete(row, column)
        self.numberOfRows = 0
        self.reminders = [reminder for reminder in self.fetchReminders()]
        self.remindersTable.values = self.reminders
        for i, reminder in enumerate(self.reminders):
            self.remindersTable.add_row(i)
            for j, value in enumerate(reminder):
                self.remindersTable.insert(i, j, value)
            self.numberOfRows += 1
            self.checkReminder(reminder)

    # * Adding Reminder to Database from Entry Point
    def addReminderFromEntry(self):
        reminder = self.userReminderEntry.get()
        self.addReminder(reminder)
        self.userReminderEntry.delete(0, "end")
        self.numberOfRows += 1
        self.updateRemindersTable()

    # * Delete Row function
    def deleteRow(self, event):
        row = event.widget.index(event.x, event.y)[0]
        event.widget.delete_row(row)
        self.numberOfRows -= 1

    # * Function to check reminders and send notifications - changes bell icon to be "active" when there is notification
    def checkReminder(self, reminder):
        toaster = WindowsToaster("Reminders")
        for reminder in self.reminders:
            if reminder[1]:
                reminderDate = datetime.datetime.strptime(
                    reminder[2], "%Y-%m-%d %H:%M:%S"
                )
                timeDiff = datetime.datetime.now() - reminderDate
                if timeDiff.days >= 1:
                    toast = Toast()
                    toast.text_fields = [
                        "You have tasks that have been due for over a day"
                    ]
                    toaster.show_toast(toast)
                    self.notificationButton.configure(
                        image=self.activeNotificationBellIcon,
                    )
                    break

        # * Toggle Side Bar called to default sidebar as closed
        self.after(
            1000,
            self.toggleSideBar,
        )

    # * Sidebar Toggle Function
    def toggleSideBar(self):
        if self.sideBarFrame.winfo_viewable():
            self.sideBarFrame.place_forget()
            self.remindersFrame.place(x=10, y=80)
            self.shopifyOrdersFrame.place(
                x=self.remindersFrame.winfo_width() + 20,
                y=80,
            )
            self.dataGraphFrame.place(
                x=10,
                y=590,
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
                self.remindersFrame.place(
                    x=self.sideBarFrame.winfo_width() + 10,
                    y=80,
                )
                self.shopifyOrdersFrame.place(
                    x=self.remindersFrame.winfo_width()
                    + self.sideBarFrame.winfo_width()
                    + 20,
                    y=80,
                )
                self.dataGraphFrame.place(
                    x=self.sideBarFrame.winfo_width() + 10,
                    y=590,
                )
                self.update()


if __name__ == "__main__":
    master = InformationPageDashboard()
    master.drawGraph()
    reminder = {
        "active": True,
        "createdAt": datetime.datetime.now() - datetime.timedelta(days=2),
    }
    master.checkReminder(reminder)
    master.mainloop()
