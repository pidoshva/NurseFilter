import unittest
from unittest.mock import MagicMock, patch
from initial_controller import InitialController
from tkinter import Tk
from tkinter import filedialog, messagebox

class TestInitialController(unittest.TestCase):

    @patch('initial_controller.InitialView')
    @patch('initial_controller.messagebox')
    @patch('initial_controller.filedialog')
    @patch('initial_controller.logging')
    def setUp(self, mock_logging, mock_filedialog, mock_messagebox, MockInitialView):
        self.mock_root = Tk()
        self.mock_model = MagicMock()
        self.mock_main_controller = MagicMock()
        self.mock_view = MagicMock()
        MockInitialView.return_value = self.mock_view
        self.controller = InitialController(self.mock_root, self.mock_model, self.mock_main_controller)
        mock_filedialog.askopenfilename.return_value = "dummy_file.xlsx"

    def test_show_initial_view(self):
        view = self.controller.show_initial_view()
        self.mock_main_controller.add_tab.assert_called_once_with(self.mock_view, "Data Loader")
        self.assertEqual(view, self.mock_view)

    @patch('initial_controller.pd.read_excel')
    def test_read_excel_file(self, mock_read_excel):
        self.controller.read_excel_file()
        self.mock_model.read_excel_file.assert_called_once_with("dummy_file.xlsx")
        
        self.mock_model.is_file_encrypted.return_value = True
        self.mock_model.decrypt_file.return_value = True
        self.controller.read_excel_file()
        self.mock_model.decrypt_file.assert_called_once_with("dummy_file.xlsx")
        
        self.mock_model.decrypt_file.return_value = False
        self.controller.read_excel_file()
        mock_messagebox.showwarning.assert_called_once_with("Warning", "Error re-encrypting file.")
        
        self.mock_model.encrypt_file.side_effect = None
        self.controller.read_excel_file()
        self.mock_model.encrypt_file.assert_called_once_with("dummy_file.xlsx")
        
        self.mock_model.encrypt_file.side_effect = Exception("Encryption Error")
        self.controller.read_excel_file()
        mock_messagebox.showwarning.assert_called_with("Warning", "Error re-encrypting file.")

    def test_combine_data(self):
        self.mock_model.combine_data.return_value = True
        self.controller.combine_data()
        self.mock_model.load_combined_data.assert_called_once()

        self.mock_model.combine_data.return_value = False
        self.controller.combine_data()
        self.mock_model.load_combined_data.assert_not_called()

    def test_load_combined_data(self):
        self.mock_model.load_combined_data.return_value = True
        self.controller.load_combined_data()
        self.mock_main_controller.show_combined_data.assert_called_once()

        self.mock_model.load_combined_data.return_value = False
        self.controller.load_combined_data()
        self.mock_main_controller.show_combined_data.assert_not_called()

if __name__ == '__main__':
    unittest.main()
