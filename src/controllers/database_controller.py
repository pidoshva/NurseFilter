import sqlite3
import bcrypt

class DatabaseController:
    def __init__(self):
        self.initialize_db()

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
                return True
            else:
                return False
        else:
            return None

        conn.close()
