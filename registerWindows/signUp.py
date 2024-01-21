import customtkinter
from tkinter import (
    messagebox as tkmb,
)
from PIL import Image
import os, hashlib, re, sqlite3


class SignUpWindow(customtkinter.CTk):
    width = 300
    height = 400

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.title("Log In Window")
        self.geometry(f"{600}x{400}")
        self.resizable(False, False)

        currentPath = os.path.dirname(os.path.realpath(__file__))

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
        )
        self.signInButton.pack(anchor="w", pady=(20, 0), padx=(25, 0))

    # * Sign Up Function
    # TODO Sign Up Functio - Same with loginProcess function
    def signupProcess(self):
        email = self.userEmailEntry.get()
        password = self.userPasswordEntry.get()
        hashedPassword = super().hashPassword(password)
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


"""
    def openLogInWindow(self):
        self.destroy()
        loginwindow = LogInWindow()
        loginwindow.mainloop()
"""

if __name__ == "__main__":
    master = SignUpWindow()
    master.mainloop()
