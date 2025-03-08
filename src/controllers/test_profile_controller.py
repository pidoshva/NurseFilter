import unittest
from unittest.mock import MagicMock
from tkinter import Tk, messagebox
from profile_controller import ProfileController
from views.profile_view import ProfileView
import tempfile
import os

class TestProfileController(unittest.TestCase):

    def setUp(self):
        self.root = Tk()
        self.child_data = {'Mother_ID': 1, 'Child_First_Name': 'John', 'Child_Last_Name': 'Doe', 'Child_Date_of_Birth': '2010-01-01'}
        self.model = MagicMock()
        self.main_controller = MagicMock()
        self.update_callback = MagicMock()
        self.controller = ProfileController(self.root, self.child_data, self.model, self.main_controller, self.update_callback)

    def test_show_profile(self):
        frame = self.controller.show_profile()
        self.assertIsNotNone(frame)

    def test_assign_nurse(self):
        child_data = {'Mother_ID': 1, 'Child_First_Name': 'John', 'Child_Last_Name': 'Doe', 'Child_Date_of_Birth': '2010-01-01'}
        frame = self.controller.assign_nurse(child_data, self.update_callback)
        self.main_controller.assign_nurse.assert_called_once_with(child_data, MagicMock())

    def test_copy_to_clipboard(self):
        self.controller.view = MagicMock(spec=ProfileView)
        self.controller.view.get_mother_info_text.return_value = "Mother Info"
        self.controller.view.get_child_info_text.return_value = "Child Info"
        self.controller.view.get_address_info_text.return_value = "Address Info"
        self.controller.view.get_nurse_info_text.return_value = "Nurse Info"
        
        self.controller.copy_to_clipboard()
        self.root.clipboard_clear.assert_called_once()
        self.root.clipboard_append.assert_called_once()
        messagebox.showinfo.assert_called_with("Copied", "Profile info copied to clipboard.")

    def test_export_profile_to_pdf(self):
        self.controller.view = MagicMock(spec=ProfileView)
        self.controller.view.get_mother_info_text.return_value = "Mother Info"
        self.controller.view.get_child_info_text.return_value = "Child Info"
        self.controller.view.get_address_info_text.return_value = "Address Info"
        self.controller.view.get_nurse_info_text.return_value = "Nurse Info"

        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_pdf:
            self.controller.export_profile_to_pdf()
            self.assertTrue(os.path.exists(tmp_pdf.name))

    def test_export_profile_to_pdf_error(self):
        self.controller.view = MagicMock(spec=ProfileView)
        self.controller.view.get_mother_info_text.return_value = "Mother Info"
        self.controller.view.get_child_info_text.return_value = "Child Info"
        self.controller.view.get_address_info_text.return_value = "Address Info"
        self.controller.view.get_nurse_info_text.return_value = "Nurse Info"
        
        with self.assertRaises(Exception):
            self.controller.export_profile_to_pdf()

    def test_close(self):
        self.controller.view = MagicMock()
        self.controller.view.get_frame.return_value = MagicMock()
        self.controller.close()
        self.main_controller.remove_tab.assert_called_once_with(self.controller.view.get_frame())

if __name__ == '__main__':
    unittest.main()
