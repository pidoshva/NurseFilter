import unittest
from unittest.mock import MagicMock, patch
from login_controller import LoginController
from tkinter import Tk, messagebox
import sqlite3
import bcrypt

class TestLoginController(unittest.TestCase):

    @patch('login_controller.LoginView')
    @patch('tkinter.messagebox')
    @patch('login_controller.logging')
    def setUp(self, mock_logging, mock_messagebox, MockLoginView):
        self.mock_root = Tk()
        self.mock_main_controller = MagicMock()
        self.mock_view = MagicMock()
        MockLoginView.return_value = self.mock_view
        self.controller = LoginController(self.mock_root, self.mock_main_controller)

    @patch('login_controller.sqlite3.connect')
    def test_initialize_db(self, mock_connect):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_connect.return_value = mock_conn

        self.controller.initialize_db()

        mock_cursor.execute.assert_called_with("SELECT * FROM users WHERE username=?", ('admin',))
        mock_cursor.execute.assert_called_with("INSERT INTO users (username, password) VALUES (?, ?)", ('admin', 'hashed_password'))

    @patch('login_sqlite3.connect')
    @patch('login_bcrypt.checkpw')
    def test_login_success(self, mock_checkpw, mock_connect):
        mock_checkpw.return_value = True
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_connect.return_value = mock_conn
        self.controller._login_user = MagicMock(return_value=True)

        result = self.controller.login('admin', 'admin123')

        self.assertTrue(result)
        self.mock_main_controller.show_initial_view.assert_called_once()

    @patch('login_sqlite3.connect')
    @patch('login_controller.bcrypt.checkpw')
    def test_login_invalid_password(self, mock_checkpw, mock_connect):
        mock_checkpw.return_value = False
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_connect.return_value = mock_conn
        self.controller._login_user = MagicMock(return_value=False)

        result = self.controller.login('admin', 'wrongpassword')

        self.assertFalse(result)
        mock_messagebox.showerror.assert_called_with("Login Failed", "Invalid username or password")

    @patch('login_controller.sqlite3.connect')
    @patch('login_controller.bcrypt.checkpw')
    def test_login_username_not_found(self, mock_checkpw, mock_connect):
        mock_checkpw.return_value = False
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_connect.return_value = mock_conn
        self.controller._login_user = MagicMock(return_value=None)

        result = self.controller.login('nonexistentuser', 'password')

        self.assertFalse(result)
        mock_messagebox.showerror.assert_called_with("Login Failed", "Username not found")

    @patch('login_controller.sqlite3.connect')
    def test_register_user(self, mock_connect):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_connect.return_value = mock_conn

        self.controller.register_user('newuser', 'newpassword')

        mock_cursor.execute.assert_called_with("INSERT INTO users (username, password) VALUES (?, ?)", ('newuser', 'hashed_password'))

if __name__ == '__main__':
    unittest.main()
