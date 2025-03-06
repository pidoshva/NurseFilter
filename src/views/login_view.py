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
        self.root = tk.Toplevel(root)
        self.controller = controller
        self.root.title("Excel Combiner (MVC)")
        self.create_widgets()
        logging.info("LoginView initialized.")

    def login_button(self):
        username = self.entry_username.get()
        password = self.entry_password.get()

        self.controller.login(username, password)

    def create_widgets(self):
        self.root.geometry("300x300")

        label_username = tk.Label(self.root, text="Username:")
        label_username.pack(pady=5)

        self.entry_username = tk.Entry(self.root)
        self.entry_username.pack(pady=5)

        label_password = tk.Label(self.root, text="Password:")
        label_password.pack(pady=5)

        self.entry_password = tk.Entry(self.root, show="*")
        self.entry_password.pack(pady=5)

        login_button = tk.Button(self.root, text="Login", command=self.login_button)
        login_button.pack(pady=10)

    def close(self):
        self.root.destroy()
    
