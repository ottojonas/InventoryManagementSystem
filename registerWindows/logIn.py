import customtkinter
from tkinter import (
    messagebox as tkmb,
)
from PIL import Image
import os, hashlib, re, sqlite3


class LogInWindow(customtkinter.CTk):
    width = 300
    height = 400

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.title('Log In Window')
        self.geometry(f"{600}x{400}")
        self.resizable(False, False)

        currentPath = os.path.dirname(os.path.realpath(__file__))

        # * Image Loading
        # * Side Image
        self.sideImage = customtkinter.CTkImage(
            Image.open('images/sideImage.png'),
            size=(self.width, self.height),
        )
        # * Email Icon
        self.emailIcon = customtkinter.CTkImage(
            Image.open('images/emailIcon.png'),
            size=(17, 17),
        )
        # * Password Icon
        self.passwordIcon = customtkinter.CTkImage(
            Image.open('images/passwordIcon.png'),
            size=(20, 20),
        )

        # * Side Frame
        self.sideFrameLabel = customtkinter.CTkLabel(
            master=self,
            image=self.sideImage,
            text='',
        )
        self.sideFrameLabel.pack(expand=True, side='left')

        # * Main Frame
        self.userEntryFrame = customtkinter.CTkFrame(
            master=self, width=300, height=480, fg_color='#fff'
        )
        self.userEntryFrame.pack_propagate(False)
        self.userEntryFrame.pack(expand=True, side='right')

        # * Welcome Back Label
        self.welcomeLabel = customtkinter.CTkLabel(
            master=self.userEntryFrame,
            text='Welcome Back',
            text_color='#601e88',
            anchor='w',
            justify='left',
            font=('Aptos', 24, 'bold'),
        )
        self.welcomeLabel.pack(anchor='w', pady=(50, 5), padx=(25, 0))

        # * Sign In Label
        self.signInLabel = customtkinter.CTkLabel(
            master=self.userEntryFrame,
            text='Sign Into Your Account',
            text_color='#7e7e7e',
            anchor='w',
            justify='left',
            font=('Aptos', 12, 'bold'),
        )
        self.signInLabel.pack(anchor='w', padx=(25, 0))

        # * Email Label
        self.emailEntryLabel = customtkinter.CTkLabel(
            master=self.userEntryFrame,
            text='    Email',
            text_color='#601e88',
            anchor='w',
            justify='left',
            font=('Aptos', 14, 'bold'),
            image=self.emailIcon,
            compound='left',
        )
        self.emailEntryLabel.pack(anchor='w', pady=(38, 0), padx=(25, 0))

        # * Email Entry Point
        self.userEmailEntry = customtkinter.CTkEntry(
            master=self.userEntryFrame,
            width=225,
            fg_color='#eee',
            border_color='#601e88',
            border_width=1,
            text_color='#000',
        )
        self.userEmailEntry.pack(anchor='w', padx=(25, 0))

        # * Password Label
        self.passwordEntryLabel = customtkinter.CTkLabel(
            master=self.userEntryFrame,
            text='    Password',
            text_color='#601e88',
            anchor='w',
            justify='left',
            font=('Aptos', 14, 'bold'),
            image=self.passwordIcon,
            compound='left',
        )
        self.passwordEntryLabel.pack(anchor='w', pady=(21, 0), padx=(25, 0))

        # * Password Entry Point
        self.userPasswordEntry = customtkinter.CTkEntry(
            master=self.userEntryFrame,
            width=225,
            fg_color='#eee',
            border_color='#601e88',
            border_width=1,
            text_color='#000',
            show='*',
        )
        self.userPasswordEntry.pack(anchor='w', padx=(25, 0))

        # * Log In Button
        self.loginButton = customtkinter.CTkButton(
            master=self.userEntryFrame,
            text='Log In',
            fg_color='#601e88',
            hover_color='#e44982',
            font=('Aptos', 12, 'bold'),
            text_color='#fff',
            width=225,
        )
        self.loginButton.pack(anchor='w', pady=(40, 0), padx=(25, 0))

        # * Sign Up Password Button
        self.signupButton = customtkinter.CTkButton(
            master=self.userEntryFrame,
            text="Don't Have An Account? Sign Up",
            fg_color='#eee',
            hover_color='#eee',
            font=('Aptos', 12, 'bold'),
            text_color='#601e88',
            width=225,
        )
        self.signupButton.pack(anchor='w', pady=(20, 0), padx=(25, 0))

    # * Logging In Function
    # TODO loginProcess function - Need database and all of that
    def loginProcess(self):
        email = self.userEmailEntry.get()
        password = self.userPasswordEntry.get()
        hashedPassword = self.hashPassword(password)
        with sqlite3.connect('database/loginInfoDatabase.db') as db:
            myCursor = db.cursor()
            myCursor.execute(
                'SELECT * FROM userLogInInfo WHERE email = ? AND password = ?',
                (email, hashedPassword),
            )
            user = myCursor.fetchone()
            if user is None:
                tkmb.showerror(
                    title='Error',
                    message='Invalid details, please try again or Sign Up',
                )
            else:
                tkmb.showinfo(
                    title='Success', message='You have logged in successfully'
                )
                quit()

    # * Hashing Password Function
    def hashPassword(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    # * Checking if email is valid format function
    def emailFormatChecker(self, email):
        pattern = r'^[a-zA-Z0-9._%+_]+@[a-zA-Z0-9.-]+\.[a-zA-Z](2,)$'
        if re.match(pattern, email):
            return False
        return True

    # * Confirming there was an email entry function
    def emailEntryConfirm(self, email):
        email = self.userEmailEntry.get()
        if email == '':
            tkmb.showerror(title='Error', message='Enter an email before continuing')
            return False
        if not self.emailFormatChecker(email):
            tkmb.showerror(
                title='Error', message='Email format invalid, please try again'
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
        if password == '':
            tkmb.showerror(title='Error', message='Enter a password before continuing')
            return False
        if not self.passwordFormatChecker(password):
            tkmb.showerror(
                title='Error', message='Password format invalid, please try again'
            )


if __name__ == '__main__':
    master = LogInWindow()
    master.mainloop()
