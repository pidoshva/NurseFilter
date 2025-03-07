import tkinter as tk
import logging

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
        self.create_widgets()
        logging.info("LoginView initialized.")

    def login_button(self):
        username = self.entry_username.get()
        password = self.entry_password.get()

        self.controller.login(username, password)

    def create_widgets(self):
        label_username = tk.Label(self.view, text="Username:")
        label_username.pack(pady=5)

        self.entry_username = tk.Entry(self.view)
        self.entry_username.pack(pady=5)

        label_password = tk.Label(self.view, text="Password:")
        label_password.pack(pady=5)

        self.entry_password = tk.Entry(self.view, show="*")
        self.entry_password.pack(pady=5)

        login_button = tk.Button(self.view, text="Login", command=self.login_button)
        login_button.pack(pady=10)

    def get_view(self):
        return self.view
    
