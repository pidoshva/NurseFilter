import unittest
from unittest.mock import MagicMock
import pandas as pd
from tkinter import Tk, messagebox
from nurse_controller import NurseController
from models.data_model import DataModel
from views.statistical_view import StatisticalView
from views.nurse_statistics_view import NursesStatisticalView
from views.batch_assign_view import BatchAssignView
from views.assign_nurse_view import AssignNurseView

class TestNurseController(unittest.TestCase):

    def setUp(self):
        self.root = Tk()
        self.model = MagicMock(spec=DataModel)
        self.main_controller = MagicMock()
        self.controller = NurseController(self.root, self.model, self.main_controller)

    def test_generate_report_no_data(self):
        self.model.combined_data = None
        with self.assertRaises(Exception):
            self.controller.generate_report()

    def test_generate_report_no_assigned_nurse_column(self):
        self.model.combined_data = pd.DataFrame({'some_column': [1, 2, 3]})
        with self.assertRaises(Exception):
            self.controller.generate_report()

    def test_generate_report_success(self):
        self.model.combined_data = pd.DataFrame({
            'Assigned_Nurse': ['None', 'Nurse A', 'None'],
            'Child_First_Name': ['John', 'Jane', 'Jim'],
            'Child_Last_Name': ['Doe', 'Doe', 'Smith'],
            'Child_Date_of_Birth': ['2010-01-01', '2011-01-01', '2012-01-01']
        })
        frame = self.controller.generate_report()
        self.assertIsNotNone(frame)

    def test_export_report_to_pdf_no_data(self):
        df = pd.DataFrame({'Assigned_Nurse': ['None', 'Nurse A', 'None']})
        self.controller.export_report_to_pdf(df)
        messagebox.showinfo.assert_called_with("Success", "Report saved at ")

    def test_export_report_to_pdf_no_assigned_nurse(self):
        df = pd.DataFrame({'Assigned_Nurse': ['None', 'None', 'None']})
        self.controller.export_report_to_pdf(df)
        messagebox.showinfo.assert_called_with("Success", "Report saved at ")

    def test_show_nurse_statistics_no_data(self):
        self.model.combined_data = None
        frame = self.controller.show_nurse_statistics()
        self.assertIsNone(frame)

    def test_show_nurse_statistics_no_assigned_nurse_column(self):
        self.model.combined_data = pd.DataFrame({'some_column': [1, 2, 3]})
        frame = self.controller.show_nurse_statistics()
        self.assertIsNone(frame)

    def test_show_nurse_statistics_success(self):
        self.model.combined_data = pd.DataFrame({
            'Assigned_Nurse': ['Nurse A', 'Nurse B'],
            'Child_First_Name': ['John', 'Jane'],
            'Child_Last_Name': ['Doe', 'Doe'],
            'Child_Date_of_Birth': ['2010-01-01', '2011-01-01']
        })
        frame = self.controller.show_nurse_statistics()
        self.assertIsNotNone(frame)

    def test_batch_assign_nurses_no_data(self):
        self.model.combined_data = None
        frame = self.controller.batch_assign_nurses(None)
        self.assertIsNone(frame)

    def test_batch_assign_nurses_success(self):
        self.model.combined_data = pd.DataFrame({
            'Assigned_Nurse': ['None', 'None'],
            'Child_First_Name': ['John', 'Jane'],
            'Child_Last_Name': ['Doe', 'Doe'],
            'Child_Date_of_Birth': ['2010-01-01', '2011-01-01']
        })
        frame = self.controller.batch_assign_nurses(None)
        self.assertIsNotNone(frame)

    def test_assign_nurse_success(self):
        child_data = {'Mother_ID': 1, 'Child_First_Name': 'John', 'Child_Last_Name': 'Doe', 'Child_Date_of_Birth': '2010-01-01'}
        frame = self.controller.assign_nurse(child_data, None)
        self.assertIsNotNone(frame)

    def test_save_nurse_success(self):
        self.model.combined_data = pd.DataFrame({
            'Mother_ID': [1],
            'Child_First_Name': ['John'],
            'Child_Last_Name': ['Doe'],
            'Child_Date_of_Birth': ['2010-01-01'],
            'Assigned_Nurse': ['None']
        })
        update_callback = MagicMock()
        close_callback = MagicMock()
        self.controller.save_nurse('Nurse A', {'Mother_ID': 1, 'Child_First_Name': 'John', 'Child_Last_Name': 'Doe', 'Child_Date_of_Birth': '2010-01-01'}, update_callback, close_callback)
        update_callback.assert_called_once_with("Name: Nurse A")
        close_callback.assert_called_once()

    def test_save_nurse_no_matching_record(self):
        self.model.combined_data = pd.DataFrame({
            'Mother_ID': [1],
            'Child_First_Name': ['Jane'],
            'Child_Last_Name': ['Doe'],
            'Child_Date_of_Birth': ['2010-01-01'],
            'Assigned_Nurse': ['None']
        })
        update_callback = MagicMock()
        close_callback = MagicMock()
        self.controller.save_nurse('Nurse A', {'Mother_ID': 2, 'Child_First_Name': 'John', 'Child_Last_Name': 'Doe', 'Child_Date_of_Birth': '2010-01-01'}, update_callback, close_callback)
        messagebox.showerror.assert_called_with("Error", "Failed to assign nurse.")

    def test_save_nurse_empty_name(self):
        update_callback = MagicMock()
        close_callback = MagicMock()
        self.controller.save_nurse('', {'Mother_ID': 1, 'Child_First_Name': 'John', 'Child_Last_Name': 'Doe', 'Child_Date_of_Birth': '2010-01-01'}, update_callback, close_callback)
        messagebox.showerror.assert_called_with("Error", "Nurse name cannot be empty.")

    def test_close_report(self):
        self.controller.report_view = MagicMock()
        self.controller.close_report()
        self.main_controller.remove_tab.assert_called_once_with(self.controller.report_view)

    def test_close_nurse_stats(self):
        self.controller.nurse_stats_view = MagicMock()
        self.controller.close_nurse_stats()
        self.main_controller.remove_tab.assert_called_once_with(self.controller.nurse_stats_view)

    def test_close_batch_assign(self):
        self.controller.batch_assign_view = MagicMock()
        self.controller.close_batch_assign()
        self.main_controller.remove_tab.assert_called_once_with(self.controller.batch_assign_view)

    def test_close_assign_nurse(self):
        self.controller.assign_nurse_view = MagicMock()
        self.controller.close_assign_nurse()
        self.main_controller.remove_tab.assert_called_once_with(self.controller.assign_nurse_view)

if __name__ == '__main__':
    unittest.main()
