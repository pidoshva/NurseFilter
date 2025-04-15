from controllers.combined_data_controller import CombinedDataController
from controllers.profile_controller import ProfileController
from controllers.initial_controller import InitialController
from controllers.nurse_controller import NurseController
from controllers.login_controller import LoginController
from controllers.tabs_controller import TabsController
from models.data_model import DataModel
import os
from tkinter import messagebox
import platform
import logging



class MainController:
    '''Controller responsible for managing inter-controller communication.'''
    def __init__(self, root):
        self.app_root = root  # The main Tkinter window
        self.tabs = self._get_tabs_controller(root)
        self.root = self.tabs.get_tabs_root()
        self.model = DataModel()
        self.login()

    def login(self):
        self._get_login_controller()

    def _get_login_controller(self):
        return LoginController(self.root, self)
    
    def _get_initial_controller(self):
        return InitialController(self.root, self.model, self)

    def _get_combined_data_controller(self):
        return CombinedDataController(self.root, self.model, self)
    
    def _get_profile_controller(self, child_data, update_callback):
        return ProfileController(self.root, child_data, self.model, self, update_callback)
    
    def _get_nurse_controller(self):
        return NurseController(self.root, self.model, self)
    
    def _get_tabs_controller(self, root):
        return TabsController(root)
    
    def add_tab(self, tab_view, tab_name):
        self.tabs.add_tab(tab_view, tab_name)
        logging.info(f"Added tab: {tab_name}")

    def remove_tab(self, tab_view):
        self.tabs.remove_tab(tab_view)
    
    def show_initial_view(self):
        controller = self._get_initial_controller()
        return controller.show_initial_view()

    def show_combined_data(self):
        controller = self._get_combined_data_controller()
        return controller.show_combined_data()

    def show_unmatched_data(self):
        controller = self._get_combined_data_controller()
        return controller.view_unmatched_data()
    
    def show_duplicate_data(self):
        controller = self._get_combined_data_controller()
        return controller.view_duplicate_data()

    def show_profile(self, child_data, update_callback):
        controller = self._get_profile_controller(child_data, update_callback)
        return controller.show_profile()

    def show_nurse_statistics(self):
        controller = self._get_nurse_controller()
        return controller.show_nurse_statistics()

    def batch_assign_nurses(self, update_callback):
        controller = self._get_nurse_controller()
        return controller.batch_assign_nurses(update_callback)

    def assign_nurse(self, child_data, update_callback):
        controller = self._get_nurse_controller()
        return controller.assign_nurse(child_data, update_callback)

    def generate_report(self):
        controller = self._get_nurse_controller()
        return controller.generate_report()
    
    def load_existing_combined_data(self):
        if self.model.load_combined_data():
            controller = self._get_combined_data_controller()
            return controller.refresh_view()
        else:
            messagebox.showerror("Error", "Failed to load existing combined data.")

    def display_in_excel(self, filepath):
        '''
        Open the specified Excel file using the default application.
        '''
        if not os.path.exists(filepath):
            messagebox.showerror("Error", f"{filepath} does not exist.")
            return
        try:
            if platform.system() == "Darwin":  # macOS
                os.system(f"open {filepath}")
            elif platform.system() == "Windows":
                os.startfile(filepath)
            else:  # Linux
                os.system(f"xdg-open {filepath}")
        except Exception as e:
            messagebox.showerror("Error", f"Error opening Excel file: {e}")

    def on_closing(self):
            """
            Called when the user closes the main window.
            Optionally encrypt 'combined_matched_data.xlsx' or do cleanup.
            """
            logging.info("Closing App")
            filepath = 'combined_matched_data.xlsx'
            self.model.encrypt_file(filepath)
            self.app_root.destroy()