import unittest
import pandas as pd
from unittest.mock import MagicMock, patch
from combined_data_controller import CombinedDataController
from tkinter import Tk

class TestCombinedDataController(unittest.TestCase):
    
    @patch('combined_data_controller.CombinedDataView')
    @patch('combined_data_controller.UnmatchedDataView')
    @patch('combined_data_controller.DuplicateDataView')
    @patch('combined_data_controller.DataModel')
    @patch('combined_data_controller.messagebox')
    def setUp(self, mock_messagebox, MockDataModel, MockDuplicateDataView, MockUnmatchedDataView, MockCombinedDataView):
        self.mock_root = Tk()
        self.mock_main_controller = MagicMock()
        self.mock_model = MockDataModel()

        self.mock_model.combined_data = pd.DataFrame({'Child_First_Name': ['Alice', 'Bob']})
        self.mock_model.unmatched_data = pd.DataFrame({'Child_First_Name': ['Charlie']})
        self.mock_model.duplicate_data = pd.DataFrame({'Child_First_Name': ['Alice', 'Alice']})

        self.controller = CombinedDataController(self.mock_root, self.mock_model, self.mock_main_controller)
        
        self.mock_view = MagicMock()
        MockCombinedDataView.return_value = self.mock_view
        MockUnmatchedDataView.return_value = self.mock_view
        MockDuplicateDataView.return_value = self.mock_view
        self.mock_messagebox = mock_messagebox

    @patch('combined_data_controller.logging')
    def test_show_combined_data(self, mock_logging):
        frame = self.controller.show_combined_data()
        self.mock_main_controller.add_tab.assert_called_once()
        self.assertEqual(frame, self.mock_view.create_widgets())

        self.mock_model.combined_data = pd.DataFrame()
        self.controller.show_combined_data()
        self.mock_messagebox.showerror.assert_called_with("Error", "No combined data available to display.")

    @patch('combined_data_controller.logging')
    def test_search_combined_names(self, mock_logging):
        self.controller.search_combined_names('Alice')
        self.mock_view.update_table.assert_called()

        self.controller.search_combined_names('Eve')
        self.mock_view.update_table.assert_called()

        self.mock_model.combined_data = pd.DataFrame()
        self.controller.search_combined_names('Alice')
        mock_logging.warning.assert_called_with("No combined data to search.")

    def test_view_duplicate_data(self):
        self.controller.view_duplicate_data()
        self.mock_main_controller.add_tab.assert_called_once()

        self.mock_model.duplicate_data = pd.DataFrame()
        self.controller.view_duplicate_data()
        self.mock_messagebox.showinfo.assert_called_with("No Data", "No duplicate data found.")

    def test_view_unmatched_data(self):
        self.controller.view_unmatched_data()
        self.mock_main_controller.add_tab.assert_called_once()

        self.mock_model.unmatched_data = pd.DataFrame()
        self.controller.view_unmatched_data()
        self.mock_messagebox.showinfo.assert_called_with("No Data", "No unmatched data available.")

    def test_show_child_profile(self):
        view_mock = MagicMock()
        view_mock.get_selected_child_data.return_value = {'name': 'Alice', 'age': 10}
        
        result = self.controller.show_child_profile(view_mock)
        self.mock_main_controller.show_profile.assert_called()
        self.assertEqual(result, self.mock_main_controller.show_profile.return_value)

        view_mock.get_selected_child_data.return_value = None
        self.controller.show_child_profile(view_mock)
        self.mock_logging.warning.assert_called_with("No child data found for selected item.")

    def test_refresh_view(self):
        with patch('pandas.read_excel') as mock_read_excel:
            mock_read_excel.return_value = pd.DataFrame({'Child_First_Name': ['Alice', 'Bob']})
            self.controller.refresh_view()
            self.mock_view.clear_treeview.assert_called_once()
            self.mock_view.update_treeview.assert_called_once()

        with patch('pandas.read_excel', side_effect=Exception("Error")):
            self.controller.refresh_view()
            self.mock_messagebox.showerror.assert_called()

    def test_batch_assign_nurses(self):
        self.controller.batch_assign_nurses()
        self.mock_main_controller.batch_assign_nurses.assert_called_once()

        self.mock_model.combined_data = pd.DataFrame()
        self.controller.batch_assign_nurses()
        self.mock_messagebox.showerror.assert_called_with("Error", "No data available for batch assignment.")

    def test_generate_report(self):
        self.controller.generate_report()
        self.mock_main_controller.generate_report.assert_called_once()

    def test_display_in_excel(self):
        self.controller.display_in_excel()
        self.mock_main_controller.display_in_excel.assert_called_with('combined_matched_data.xlsx')

    def test_close_combined(self):
        self.controller.close_combined()
        self.mock_main_controller.remove_tab.assert_called_once()

    def test_close_duplicate(self):
        self.controller.close_duplicate()
        self.mock_main_controller.remove_tab.assert_called_once()

    def test_close_unmatched(self):
        self.controller.close_unmatched()
        self.mock_main_controller.remove_tab.assert_called_once()


if __name__ == '__main__':
    unittest.main()
