# * Related Third Party Imports
from PIL import Image

# * Local Application/Library Specific Imports
import customtkinter

customtkinter.set_appearance_mode("dark")


# * Initialising the Class
class openingPage(customtkinter.CTk):
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
        self.geometry(
            "{}x{}".format(
                self.winfo_screenwidth(),
                self.winfo_screenheight(),
            )
        )
        self.resizable(True, True)

        # * Load Icons
        for iconName, iconPath in self.ICONDICTIONARY.items():
            setattr(self, iconName, self.loadImage(iconPath))

        self.backgroundImage = self.loadImage(
            "images/oliverBrownLogoNoBG.png", size=(450, 87.5)
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

        # * Toggle Side Bar called to default sidebar as closed
        self.after(
            100,
            self.toggleSideBar,
        )

    # * Sidebar Toggle Function
    def toggleSideBar(self):
        if self.sideBarFrame.winfo_viewable():
            self.sideBarFrame.place_forget()
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
                self.update()


if __name__ == "__main__":
    main = openingPage()
    main.mainloop()
