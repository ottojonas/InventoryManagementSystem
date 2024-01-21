import datetime
import hashlib
import re
import sqlite3
from tkinter import messagebox as tkmb

import customtkinter
from customtkinter import StringVar
from PIL import Image

customtkinter.set_appearance_mode("system")


class SignUpWindow(customtkinter.CTk):
    width = 300
    height = 400

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.title("Log In Window")
        self.geometry(f"{600}x{400}")
        self.resizable(False, False)

        # * Image Loading
        # * Side Image
        self.sideImage = customtkinter.CTkImage(
            Image.open("images/sideImage.png"), size=(self.width, self.height)
        )

        # * Email Icon
        self.emailIcon = customtkinter.CTkImage(
            Image.open("images/emailIcon.png"),
            size=(17, 17),
        )

        # * Password Icon
        self.passwordIcon = customtkinter.CTkImage(
            Image.open("images/passwordIcon.png"),
            size=(20, 20),
        )

        # * Side Frame
        self.sideFrameLabel = customtkinter.CTkLabel(
            master=self,
            image=self.sideImage,
            text="",
        )
        self.sideFrameLabel.pack(expand=True, side="left")

        # * Main Frame
        self.userEntryFrame = customtkinter.CTkFrame(
            master=self, width=300, height=480, fg_color="#fff"
        )
        self.userEntryFrame.pack_propagate(False)
        self.userEntryFrame.pack(expand=True, side="right")

        # * Welcome! Label
        self.welcomeLabel = customtkinter.CTkLabel(
            master=self.userEntryFrame,
            text="Welcome!",
            text_color="#601e88",
            anchor="w",
            justify="left",
            font=("Aptos", 24, "bold"),
        )
        self.welcomeLabel.pack(anchor="w", pady=(50, 5), padx=(25, 0))

        # * Sign Up Label
        self.signInLabel = customtkinter.CTkLabel(
            master=self.userEntryFrame,
            text="Sign Up For An Account",
            text_color="#7e7e7e",
            anchor="w",
            justify="left",
            font=("Aptos", 12, "bold"),
        )
        self.signInLabel.pack(anchor="w", padx=(25, 0))

        # * Email Label
        self.emailEntryLabel = customtkinter.CTkLabel(
            master=self.userEntryFrame,
            text="    Email",
            text_color="#601e88",
            anchor="w",
            justify="left",
            font=("Aptos", 14, "bold"),
            image=self.emailIcon,
            compound="left",
        )
        self.emailEntryLabel.pack(anchor="w", pady=(38, 0), padx=(25, 0))

        # * Email Entry Point
        self.userEmailEntry = customtkinter.CTkEntry(
            master=self.userEntryFrame,
            width=225,
            fg_color="#eee",
            border_color="#601e88",
            border_width=1,
            text_color="#000",
        )
        self.userEmailEntry.pack(anchor="w", padx=(25, 0))

        # * Password Label
        self.passwordEntryLabel = customtkinter.CTkLabel(
            master=self.userEntryFrame,
            text="    Password",
            text_color="#601e88",
            anchor="w",
            justify="left",
            font=("Aptos", 14, "bold"),
            image=self.passwordIcon,
            compound="left",
        )
        self.passwordEntryLabel.pack(anchor="w", pady=(21, 0), padx=(25, 0))

        # * Password Entry Point
        self.userPasswordEntry = customtkinter.CTkEntry(
            master=self.userEntryFrame,
            width=225,
            fg_color="#eee",
            border_color="#601e88",
            border_width=1,
            text_color="#000",
            show="*",
        )
        self.userPasswordEntry.pack(anchor="w", padx=(25, 0))

        # * Sign Up Button
        self.signUpBtton = customtkinter.CTkButton(
            master=self.userEntryFrame,
            text="Sign Up",
            fg_color="#601e88",
            hover_color="#e44982",
            font=("Aptos", 12, "bold"),
            text_color="#fff",
            width=225,
            command=self.signupProcess,
        )
        self.signUpBtton.pack(anchor="w", pady=(40, 0), padx=(25, 0))

        # * Sign In Password Button
        self.signInButton = customtkinter.CTkButton(
            master=self.userEntryFrame,
            text="Have An Account. Sign In",
            fg_color="#eee",
            hover_color="#eee",
            font=("Aptos", 12, "bold"),
            text_color="#601e88",
            width=225,
            command=self.openLogInWindow,
        )
        self.signInButton.pack(anchor="w", pady=(20, 0), padx=(25, 0))

    # * Sign Up Function
    # TODO Sign Up Function - Same with loginProcess function
    def signupProcess(self):
        email = self.userEmailEntry.get()
        password = self.userPasswordEntry.get()
        hashedPassword = self.hashPassword(password)
        if self.emailFormatChecker(email) and self.passwordFormatChecker(password):
            with sqlite3.connect("database/loginInfoDatabase.db") as db:
                myCursor = db.cursor
                try:
                    myCursor.execute(
                        "INSERT INTO userLogInInfo(email, password) VALUES(?, ?)",
                        (email, hashedPassword),
                    )
                    db.commit()
                    tkmb.showinfo(
                        title="Sign Up Successful",
                        message="Your account has been created",
                    )
                    quit()
                except sqlite3.IntegrityError:
                    tkmb.showerror(
                        title="Error",
                        message="Account exists, please use a different email, or sign in",
                    )

    # * Hashing Password Function
    def hashPassword(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    # * Checking if email is valid format function
    def emailFormatChecker(self, email):
        pattern = r"^[a-zA-Z0-9._%+_]+@[a-zA-Z0-9.-]+\.[a-zA-Z](2,)$"
        if re.match(pattern, email):
            return False
        return True

    # * Confirming there was an email entry function
    def emailEntryConfirm(self, email):
        email = self.userEmailEntry.get()
        if email == "":
            tkmb.showerror(title="Error", message="Enter an email before continuing")
            return False
        if not self.emailFormatChecker(email):
            tkmb.showerror(
                title="Error", message="Email format invalid, please try again"
            )
            return False
        return True

    # * Checking if password is valid format
    def passwordFormatChecker(self, password):
        if len(password) < 8:
            return False
        upperCaseChar = False
        lowerCaseChar = False
        digitChar = False
        for char in password:
            if char.isupper():
                upperCaseChar = True
            if char.islower():
                lowerCaseChar = True
            if char.isdigit():
                digitChar = True
                if not (upperCaseChar and lowerCaseChar and digitChar):
                    return False
                return True

    # * Confirming there was an password entry function
    def passwordEntryConfirm(self, password):
        password = self.userPasswordEntry.get()
        if password == "":
            tkmb.showerror(title="Error", message="Enter a password before continuing")
            return False
        if not self.passwordFormatChecker(password):
            tkmb.showerror(
                title="Error", message="Password format invalid, please try again"
            )

    # * Function to close Sign Up Window and open Log In Window
    def openLogInWindow(self):
        self.destroy()
        loginwindow = LogInWindow()
        loginwindow.mainloop()


class LogInWindow(customtkinter.CTk):
    width = 300
    height = 400

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.title("Log In Window")
        self.geometry(f"{600}x{400}")
        self.resizable(False, False)

        # * Image Loading
        # * Side Image
        self.sideImage = customtkinter.CTkImage(
            Image.open("images/sideImage.png"),
            size=(self.width, self.height),
        )
        # * Email Icon
        self.emailIcon = customtkinter.CTkImage(
            Image.open("images/emailIcon.png"),
            size=(17, 17),
        )
        # * Password Icon
        self.passwordIcon = customtkinter.CTkImage(
            Image.open("images/passwordIcon.png"),
            size=(20, 20),
        )

        # * Side Frame
        self.sideFrameLabel = customtkinter.CTkLabel(
            master=self,
            image=self.sideImage,
            text="",
        )
        self.sideFrameLabel.pack(expand=True, side="left")

        # * Main Frame
        self.userEntryFrame = customtkinter.CTkFrame(
            master=self, width=300, height=480, fg_color="#fff"
        )
        self.userEntryFrame.pack_propagate(False)
        self.userEntryFrame.pack(expand=True, side="right")

        # * Welcome Back Label
        self.welcomeLabel = customtkinter.CTkLabel(
            master=self.userEntryFrame,
            text="Welcome Back",
            text_color="#601e88",
            anchor="w",
            justify="left",
            font=("Aptos", 24, "bold"),
        )
        self.welcomeLabel.pack(anchor="w", pady=(50, 5), padx=(25, 0))

        # * Sign In Label
        self.signInLabel = customtkinter.CTkLabel(
            master=self.userEntryFrame,
            text="Sign Into Your Account",
            text_color="#7e7e7e",
            anchor="w",
            justify="left",
            font=("Aptos", 12, "bold"),
        )
        self.signInLabel.pack(anchor="w", padx=(25, 0))

        # * Email Label
        self.emailEntryLabel = customtkinter.CTkLabel(
            master=self.userEntryFrame,
            text="    Email",
            text_color="#601e88",
            anchor="w",
            justify="left",
            font=("Aptos", 14, "bold"),
            image=self.emailIcon,
            compound="left",
        )
        self.emailEntryLabel.pack(anchor="w", pady=(38, 0), padx=(25, 0))

        # * Email Entry Point
        self.userEmailEntry = customtkinter.CTkEntry(
            master=self.userEntryFrame,
            width=225,
            fg_color="#eee",
            border_color="#601e88",
            border_width=1,
            text_color="#000",
        )
        self.userEmailEntry.pack(anchor="w", padx=(25, 0))

        # * Password Label
        self.passwordEntryLabel = customtkinter.CTkLabel(
            master=self.userEntryFrame,
            text="    Password",
            text_color="#601e88",
            anchor="w",
            justify="left",
            font=("Aptos", 14, "bold"),
            image=self.passwordIcon,
            compound="left",
        )
        self.passwordEntryLabel.pack(anchor="w", pady=(21, 0), padx=(25, 0))

        # * Password Entry Point
        self.userPasswordEntry = customtkinter.CTkEntry(
            master=self.userEntryFrame,
            width=225,
            fg_color="#eee",
            border_color="#601e88",
            border_width=1,
            text_color="#000",
            show="*",
        )
        self.userPasswordEntry.pack(anchor="w", padx=(25, 0))

        # * Log In Button
        self.loginButton = customtkinter.CTkButton(
            master=self.userEntryFrame,
            text="Log In",
            fg_color="#601e88",
            hover_color="#e44982",
            font=("Aptos", 12, "bold"),
            text_color="#fff",
            width=225,
            command=self.loginProcess,
        )
        self.loginButton.pack(anchor="w", pady=(40, 0), padx=(25, 0))

        # * Sign Up Password Button
        self.signupButton = customtkinter.CTkButton(
            master=self.userEntryFrame,
            text="Don't Have An Account? Sign Up",
            fg_color="#eee",
            hover_color="#eee",
            font=("Aptos", 12, "bold"),
            text_color="#601e88",
            width=225,
            command=self.openSignUpWindow,
        )
        self.signupButton.pack(anchor="w", pady=(20, 0), padx=(25, 0))

    # * Logging In Function
    # TODO loginProcess function - Need database and all of that
    def loginProcess(self):
        email = self.userEmailEntry.get()
        password = self.userPasswordEntry.get()
        hashedPassword = self.hashPassword(password)
        with sqlite3.connect("database/loginInfoDatabase.db") as db:
            myCursor = db.cursor()
            myCursor.execute(
                "SELECT * FROM userLogInInfo WHERE email = ? AND password = ?",
                (email, hashedPassword),
            )
            user = myCursor.fetchone()
            if user is None:
                tkmb.showerror(
                    title="Error",
                    message="Invalid details, please try again or Sign Up",
                )
            else:
                tkmb.showinfo(
                    title="Success", message="You have logged in successfully"
                )
                self.openOpeningPage()

    # * Hashing Password Function
    def hashPassword(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    # * Checking if email is valid format function
    def emailFormatChecker(self, email):
        pattern = r"^[a-zA-Z0-9._%+_]+@[a-zA-Z0-9.-]+\.[a-zA-Z](2,)$"
        if re.match(pattern, email):
            return False
        return True

    # * Confirming there was an email entry function
    def emailEntryConfirm(self, email):
        email = self.userEmailEntry.get()
        if email == "":
            tkmb.showerror(title="Error", message="Enter an email before continuing")
            return False
        if not self.emailFormatChecker(email):
            tkmb.showerror(
                title="Error", message="Email format invalid, please try again"
            )
            return False
        return True

    # * Checking if password is valid format
    def passwordFormatChecker(self, password):
        if len(password) < 8:
            return False
        upperCaseChar = False
        lowerCaseChar = False
        digitChar = False
        for char in password:
            if char.isupper():
                upperCaseChar = True
            if char.islower():
                lowerCaseChar = True
            if char.isdigit():
                digitChar = True
                if not (upperCaseChar and lowerCaseChar and digitChar):
                    return False
                return True

    # * Confirming there was an password entry function
    def passwordEntryConfirm(self, password):
        password = self.userPasswordEntry.get()
        if password == "":
            tkmb.showerror(title="Error", message="Enter a password before continuing")
            return False
        if not self.passwordFormatChecker(password):
            tkmb.showerror(
                title="Error", message="Password format invalid, please try again"
            )

    # * Function to close Log In Window and open Sign Up Window
    def openSignUpWindow(self):
        self.destroy()
        signupwindow = SignUpWindow()
        signupwindow.mainloop()

    # * Function to open Opening Page Window
    def openOpeningPage(self):
        self.destroy()
        OpeningPage()


# * Initialising the Class
class OpeningPage(customtkinter.CTk):
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

        # * Background image of the users companys Logo
        self.backgroundImage = customtkinter.CTkImage(
            Image.open("images/oliverBrownLogoNoBG.png"),
            size=(450, 87.5),
        )
        self.backgroundImageLabel = customtkinter.CTkLabel(
            master=self,
            image=self.backgroundImage,
            text="",
        )
        self.backgroundImageLabel.place(
            anchor="center",
            x=self.winfo_screenwidth() / 2,
            y=self.winfo_screenheight() / 2,
        )

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
            hover_color=self.HOVERCOLOR,
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
            hover_color=self.HOVERCOLOR,
            width=300,
            height=50,
            font=("Aptos", 15, "bold"),
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

        # * Stock Control Button
        self.stockControlButton = customtkinter.CTkButton(
            master=self.sideBarFrame,
            image=self.stockControlIcon,
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

        # * Orders and Transfers Button
        self.stockMovementButton = customtkinter.CTkButton(
            master=self.sideBarFrame,
            image=self.orderIcon,
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
            command=self.openPurchaseOrderPage,
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

        # * Customers Button
        self.customersButton = customtkinter.CTkButton(
            master=self.sideBarFrame,
            image=self.customerIcon,
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

        # * Reports Button
        self.reportsButton = customtkinter.CTkButton(
            master=self.sideBarFrame,
            image=self.reportsIcon,
            text="Reports",
            text_color="black",
            fg_color="transparent",
            hover_color=self.HOVERCOLOR,
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

        # * Settings Button
        self.settingsButton = customtkinter.CTkButton(
            master=self.sideBarFrame,
            image=self.settingsIcon,
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

        # * Toggle Side Bar called to default sidebar as closed
        self.after(
            100,
            self.toggleSideBar,
        )

    # * Function to open the PurchaseOrderPage
    def openPurchaseOrderPage(self):
        for frame in self.winfo_children():
            frame.pack_forget()
        if not hasattr(self, "purchaseOrderPage"):
            self.purchaseOrderPage = PurchaseOrderPage(master=self)
        self.purchaseOrderPage.pack()
        self.toggleSideBar()

    # * Sidebar Toggle Function
    def toggleSideBar(self):
        if self.sideBarFrame.winfo_viewable():
            self.sideBarFrame.place_forget()
        else:
            self.animateSideBar()

    # * Sidebar toggle animation
    def animateSideBar(self):
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
                self.update()


class PurchaseOrderPage(customtkinter.CTkFrame):
    HOVERCOLOR = "#5e6963"
    FGCOLOR = "#37443d"
    FONT = ("Aptos", 15, "bold")
    LABELFONT = ("Aptos", 20, "bold")

    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        print("PurchaseOrderPage created")
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

        # *  Image
        self.purchaseOrderImage = customtkinter.CTkImage(
            Image.open("images/obfcLogoBG.JPG"), size=(274, 366)
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
            hover_color=self.HOVERCOLOR,
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
            hover_color=self.HOVERCOLOR,
            width=300,
            height=50,
            font=("Aptos", 15, "bold"),
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

        # * Stock Control Button
        self.stockControlButton = customtkinter.CTkButton(
            master=self.sideBarFrame,
            image=self.stockControlIcon,
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

        # * Orders and Transfers Button
        self.stockMovementButton = customtkinter.CTkButton(
            master=self.sideBarFrame,
            image=self.orderIcon,
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

        # * Customers Button
        self.customersButton = customtkinter.CTkButton(
            master=self.sideBarFrame,
            image=self.customerIcon,
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

        # * Reports Button
        self.reportsButton = customtkinter.CTkButton(
            master=self.sideBarFrame,
            image=self.reportsIcon,
            text="Reports",
            text_color="black",
            fg_color="transparent",
            hover_color=self.HOVERCOLOR,
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

        # * Settings Button
        self.settingsButton = customtkinter.CTkButton(
            master=self.sideBarFrame,
            image=self.settingsIcon,
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

        # * Item Information Frame
        self.itemInformationFrame = customtkinter.CTkFrame(
            master=self,
            fg_color=self.FGCOLOR,
            width=965,
            height=900,
        )
        self.itemInformationFrame.pack_propagate(False),
        self.itemInformationFrame.place(x=self.sideBarFrame.winfo_width() + 10, y=80)
        # * Fetching and creating purchase order number
        purchaseOrderNumber = "Not Saved"
        with sqlite3.connect("database/inventoryDatabase.db") as db:
            myCursor = db.cursor()
            myCursor.execute("SELECT purchaseOrderNumber FROM PurchaseOrders")
            fetchedID = myCursor.fetchone()
            if fetchedID is not None:
                purchaseOrderNumber = fetchedID[0] + 1
            myCursor.execute("SELECT DISTINCT itemName FROM Items")
            uniqueOptions = [row[0] for row in myCursor.fetchall()]
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

        # * Function to fetch and calculate total price
        def calculateTotalPrice():
            self.totalPrice = 0
            with sqlite3.connect("database/inventoryDatabase.db") as db:
                myCursor = db.cursor()
                item = self.itemOptionMenu.get()
                myCursor.execute("SELECT price FROM Items WHERE itemName = ?", (item,))
                row = myCursor.fetchone()
                if row is not None:
                    price = row[0].replace("£", "")
                    for sizeEntry in self.sizeEntries.values():
                        quantity = sizeEntry.get()
                        if quantity.isdigit():
                            self.totalPrice += float(price) * int(quantity)
            return self.totalPrice

        # * Function to update the priceLabel each time sizeEntries is updated
        def updateTotalPrice(event):
            self.totalPrice = calculateTotalPrice()
            self.priceLabel.configure(text=f"Total Price: £{self.totalPrice: .2f}")

        # * Function to clear the listOfItemsFrame each time a new item is chosen
        def clearListOfItemsFrame():
            for widget in self.listOfItemsFrame.winfo_children():
                widget.destroy()

        # * Function to create labels and entry points in the listOfItemsFrame
        def onItemSelect(event):
            self.priceLabel.configure(text="Total Price: £0.00")
            clearListOfItemsFrame()
            self.selectedItem = self.itemOptionMenu.get()
            with sqlite3.connect("database/inventoryDatabase.db") as db:
                myCursor = db.cursor()
                myCursor.execute(
                    "SELECT sizes FROM Items WHERE itemName = ? ", (self.selectedItem,)
                )
                itemSizes = myCursor.fetchall()
            self.sizeEntries = {}
            for self.itemSize in itemSizes:
                self.sizeLabel = customtkinter.CTkLabel(
                    master=self.listOfItemsFrame,
                    text=f"Size: {self.itemSize[0]}",
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
                self.sizeEntries[self.itemSize[0]] = customtkinter.CTkEntry(
                    master=self.listOfItemsFrame,
                    text_color="black",
                    fg_color="white",
                    font=self.FONT,
                )
                self.sizeEntries[self.itemSize[0]].pack(
                    anchor="center",
                    padx=(10, 10),
                    pady=(10, 10),
                )
                self.sizeEntries[self.itemSize[0]].bind("<Key>", updateTotalPrice)

        # * Item Option Drop Down Menu
        self.itemOptionMenu = customtkinter.CTkOptionMenu(
            master=self.itemInformationFrame,
            fg_color=self.FGCOLOR,
            button_color=self.FGCOLOR,
            button_hover_color=self.HOVERCOLOR,
            text_color="black",
            variable=self.selectedOption,
            values=uniqueOptions,
            command=onItemSelect,
        )
        self.itemOptionMenu.pack(
            anchor="center",
            padx=(10, 10),
            pady=(10, 10),
        )

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

        # * Updating the itemLabel with the chosen item
        def updateLabel(*args):
            with sqlite3.connect("database/inventoryDatabase.db") as db:
                myCursor = db.cursor()
                myCursor.execute(
                    "SELECT sku FROM Items WHERE itemName = ?",
                    (self.selectedOption.get(),),
                )
                self.sku = myCursor.fetchone()
                if self.sku is not None:
                    self.itemLabel.configure(
                        text=f"{self.selectedOption.get()}, (SKU: {self.sku[0]})"
                    )
                else:
                    self.itemLabel.configure(
                        text=f"{self.selectedOption.get()}, (SKU: Not Found)"
                    )

        self.selectedOption.trace("w", updateLabel)
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

        # * Fetching supplier from database to display
        def updateSupplierLable(*args):
            with sqlite3.connect("database/inventoryDatabase.db") as db:
                myCursor = db.cursor()
                item = self.itemOptionMenu.get()
                myCursor.execute(
                    "SELECT manufacturerID FROM Items WHERE itemName = ?", (item,)
                )
                result = myCursor.fetchone()
                if result is not None:
                    self.supplierID = result[0]
                    myCursor.execute(
                        "SELECT manufacturerName FROM Manufacturers WHERE manufacturerID = ?",
                        (self.supplierID,),
                    )
                    supplier = myCursor.fetchone()[0]
                    self.supplierLabel.configure(text=f"Supplier: {supplier}")
                else:
                    self.supplierLabel.configure(text="Supplier not found")

        self.selectedOption.trace("w", updateSupplierLable)

        # * Supplier Label
        self.supplierLabel = customtkinter.CTkLabel(
            master=self.itemInformationFrame,
            text="Supplier: ",
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
        self.deliveryDate = customtkinter.CTkEntry(
            master=self.itemInformationFrame,
            text_color="black",
            font=self.LABELFONT,
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
            height=80,
        )
        self.priceFrame.pack_propagate(False)
        self.priceFrame.grid(
            row=1,
            column=0,
        )

        # * Price label
        self.priceLabel = customtkinter.CTkLabel(
            master=self.priceFrame,
            text=f"Total Price: £{calculateTotalPrice()}",
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

    # * Update date
    def updateDate(self):
        now = datetime.datetime.now()
        dateString = now.strftime("%d.%m.%Y")
        self.createdInformationLabel.configure(
            text=f"Created by: Otto Jonas on {dateString}"
        )

    # * Function to save purchase order to database
    def saveToDatabase(self):
        with sqlite3.connect("database/inventoryDatabase.db") as db:
            myCursor = db.cursor()
            itemName = self.selectedItem
            supplier = self.supplierID
            sku = self.sku[0]
            price = self.totalPrice
            createdBy = "Otto Jonas"
            createdAt = self.updateDate()
            sizes = list(self.sizeEntries.keys())
            deliveryDate = self.deliveryDate.get()
            quantity = self.sizeEntries[self.itemSize[0]].get()
            items = [{"size": size} for size in sizes]
            myCursor.execute("SELECT MAX(purchaseOrderNumber)FROM PurchaseOrders")
            result = myCursor.fetchone()
            purchaseOrderNumber = result[0] + 1 if result[0] is not None else 1
            for item in items:
                myCursor.execute(
                    "INSERT INTO PurchaseOrders (itemID, manufacturerID, sku, price, createdBy, createdAt, sizes, deliveryDate, quantity, purchaseOrderNumber) VALUES(?, ?, ?,?, ?, ?, ?, ?, ?, ?)",
                    (
                        itemName,
                        supplier,
                        sku,
                        price,
                        createdBy,
                        createdAt,
                        item["size"],
                        deliveryDate,
                        quantity,
                        purchaseOrderNumber,
                    ),
                )
                purchaseOrderID = myCursor.lastrowid
                item["purchaseOrderID"] = purchaseOrderID
            db.commit()

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
    master = OpeningPage()
    master.mainloop()
