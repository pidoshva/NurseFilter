import unittest
from unittest.mock import MagicMock, patch
from main_controller import MainController
from tkinter import Tk, messagebox
import os

class TestMainController(unittest.TestCase):

    @patch('main_controller.TabsController')
    @patch('main_controller.DataModel')
    def setUp(self, MockDataModel, MockTabsController):
        self.mock_root = Tk()
        self.mock_tabs_controller = MagicMock()
        self.mock_model = MagicMock()
        MockTabsController.return_value = self.mock_tabs_controller
        self.controller = MainController(self.mock_root)

    @patch('main_controller.LoginController')
    def test_login(self, MockLoginController):
        mock_login_controller = MagicMock()
        MockLoginController.return_value = mock_login_controller
        self.controller.login()
        MockLoginController.assert_called_once_with(self.controller.root, self.controller)

    @patch('main_controller.InitialController')
    def test_show_initial_view(self, MockInitialController):
        mock_initial_controller = MagicMock()
        MockInitialController.return_value = mock_initial_controller
        self.controller.show_initial_view()
        MockInitialController.assert_called_once_with(self.controller.root, self.controller.model, self.controller)

    @patch('main_controller.CombinedDataController')
    def test_show_combined_data(self, MockCombinedDataController):
        mock_combined_data_controller = MagicMock()
        MockCombinedDataController.return_value = mock_combined_data_controller
        self.controller.show_combined_data()
        MockCombinedDataController.assert_called_once_with(self.controller.root, self.controller.model, self.controller)

    @patch('main_controller.CombinedDataController')
    def test_show_unmatched_data(self, MockCombinedDataController):
        mock_combined_data_controller = MagicMock()
        MockCombinedDataController.return_value = mock_combined_data_controller
        self.controller.show_unmatched_data()
        MockCombinedDataController.assert_called_once_with(self.controller.root, self.controller.model, self.controller)

    @patch('main_controller.CombinedDataController')
    def test_show_duplicate_data(self, MockCombinedDataController):
        mock_combined_data_controller = MagicMock()
        MockCombinedDataController.return_value = mock_combined_data_controller
        self.controller.show_duplicate_data()
        MockCombinedDataController.assert_called_once_with(self.controller.root, self.controller.model, self.controller)

    @patch('main_controller.ProfileController')
    def test_show_profile(self, MockProfileController):
        mock_profile_controller = MagicMock()
        MockProfileController.return_value = mock_profile_controller
        self.controller.show_profile('child_data', 'update_callback')
        MockProfileController.assert_called_once_with(self.controller.root, 'child_data', self.controller.model, self.controller, 'update_callback')

    @patch('main_controller.NurseController')
    def test_show_nurse_statistics(self, MockNurseController):
        mock_nurse_controller = MagicMock()
        MockNurseController.return_value = mock_nurse_controller
        self.controller.show_nurse_statistics()
        MockNurseController.assert_called_once_with(self.controller.root, self.controller.model, self.controller)

    @patch('main_controller.NurseController')
    def test_batch_assign_nurses(self, MockNurseController):
        mock_nurse_controller = MagicMock()
        MockNurseController.return_value = mock_nurse_controller
        self.controller.batch_assign_nurses('update_callback')
        MockNurseController.assert_called_once_with(self.controller.root, self.controller.model, self.controller)

    @patch('main_controller.NurseController')
    def test_assign_nurse(self, MockNurseController):
        mock_nurse_controller = MagicMock()
        MockNurseController.return_value = mock_nurse_controller
        self.controller.assign_nurse('child_data', 'update_callback')
        MockNurseController.assert_called_once_with(self.controller.root, self.controller.model, self.controller)

    @patch('main_controller.NurseController')
    def test_generate_report(self, MockNurseController):
        mock_nurse_controller = MagicMock()
        MockNurseController.return_value = mock_nurse_controller
        self.controller.generate_report()
        MockNurseController.assert_called_once_with(self.controller.root, self.controller.model, self.controller)

    @patch('main_controller.messagebox')
    @patch('main_controller.platform.system')
    def test_display_in_excel(self, mock_platform_system, mock_messagebox):
        mock_platform_system.return_value = "Windows"
        self
