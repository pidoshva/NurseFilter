import sqlite3
import bcrypt
import logging
from tkinter import messagebox
from views.login_view import LoginView


class LoginController:
    def __init__(self, root, main_controller):
        self.root = root
        self.main_controller = main_controller
        self.initialize_db()
        self.view = self.show_login_view()
        self.upon_success = self.main_controller.show_initial_view

    def show_login_view(self):
        view = LoginView(self.root, self)
        self.main_controller.add_tab(view.get_view(), "Login")
        return view.get_view()


    def initialize_db(self):
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        
        c.execute('''CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT UNIQUE,
                        password TEXT)''')
        
        c.execute("SELECT * FROM users WHERE username=?", ('admin',))
        result = c.fetchone()

        if not result:
            admin_username = 'admin'
            admin_password = 'admin123'
            hashed_password = bcrypt.hashpw(admin_password.encode('utf-8'), bcrypt.gensalt())

            c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (admin_username, hashed_password))
            conn.commit()

        conn.close()

    def register_user(username, password):

        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        conn = sqlite3.connect('users.db')
        c = conn.cursor()

        try:
            c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_password))
            conn.commit()
            #registration success
        except sqlite3.IntegrityError:
            #username already exists
            pass
        
        conn.close()

    def login_user(self, username, password):

        conn = sqlite3.connect('users.db')
        c = conn.cursor()

        c.execute("SELECT password FROM users WHERE username=?", (username,))
        result = c.fetchone()

        if result:
            stored_password = result[0]
            if bcrypt.checkpw(password.encode('utf-8'), stored_password):
                conn.close()
                return True
            else:
                conn.close()
                return False
        else:
            conn.close()
            return None

    def login(self, username, password):
        """
        Handles login logic.
        If the username and password are correct, it shows a success message.
        Otherwise, it shows an error.
        """
        login_result = self.login_user(username, password)

        if login_result is True:
            logging.info(f"Login Success: {username}")
            self.upon_success()
            self.main_controller.remove_tab(self.view)
            return True
        elif login_result is False:
            logging.error(f"Login failed: Invalid password for {username}")
            messagebox.showerror("Login Failed", "Invalid username or password")
            return False
        elif login_result is None:
            logging.error(f"Login failed: Username '{username}' not found")
            messagebox.showerror("Login Failed", "Username not found")
            return False
        else:
            logging.error("Login failed: Unknown error")
            messagebox.showerror("Login Failed", "Unknown error occurred")
            return False
            
    

