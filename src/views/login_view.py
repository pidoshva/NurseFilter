import tkinter as tk
import logging
from views.tooltip import add_tooltip

class LoginView:
    """
    The login window with 2 text fields and 2 buttons:
      - Username
      - Password
      - Log In
      - Forgot Password
    """
    def __init__(self, root, controller):
        self.view = tk.Frame(root, width=300, height=300)
        self.controller = controller
        logging.info("LoginView initialized.")

    def login_button(self):
        username = self.entry_username.get()
        password = self.entry_password.get()

        self.controller.login(username, password)

    def create_widgets(self):
        label_username = tk.Label(self.view, text="Username:")
        label_username.pack(pady=5)
        add_tooltip(label_username, "Enter your assigned username")

        self.entry_username = tk.Entry(self.view)
        self.entry_username.pack(pady=5)
        add_tooltip(self.entry_username, "Enter your assigned username")

        label_password = tk.Label(self.view, text="Password:")
        label_password.pack(pady=5)
        add_tooltip(label_password, "Enter your secure password")

        self.entry_password = tk.Entry(self.view, show="*")
        self.entry_password.pack(pady=5)
        add_tooltip(self.entry_password, "Enter your secure password")

        login_button = tk.Button(self.view, text="Login", command=self.login_button)
        login_button.pack(pady=10)
        add_tooltip(login_button, "Click to log in with your credentials")

        return self.view
