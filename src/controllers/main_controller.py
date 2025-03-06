from controllers.combined_data_controller import CombinedDataController
from controllers.profile_controller import ProfileController
from controllers.initial_controller import InitialController
from controllers.nurse_controller import NurseController
from controllers.login_controller import LoginController
from models.data_model import DataModel
import os
from tkinter import messagebox
import platform
import logging



class MainController:
    def __init__(self, root):
        self.root = root
        self.root.withdraw() # hack for now to hide when logging in and unhides when logged in
        self.model = DataModel()
        self.login()

    def login(self):
        self._get_login_controller()

    def _get_login_controller(self):
        return LoginController(self.root, self)
    
    def _get_initial_controller(self):
        self.root.deiconify()
        return InitialController(self.root, self.model, self)

    def _get_combined_data_controller(self):
        return CombinedDataController(self.root, self.model, self)
    
    def _get_profile_controller(self, child_data, update_callback):
        return ProfileController(self.root, child_data, self.model, self, update_callback)
    
    def _get_nurse_controller(self):
        return NurseController(self.root, self.model, self)
    
    def show_initial_view(self):
        controller = self._get_initial_controller()
        controller.show_initial_view()
    
    def show_combined_data(self):
        controller = self._get_combined_data_controller()
        controller.show_combined_data()

    def show_unmatched_data(self):
        controller = self._get_combined_data_controller()
        controller.view_unmatched_data()

    def show_profile(self, child_data, update_callback):
        controller = self._get_profile_controller(child_data, update_callback)
        controller.show_profile()

    def show_nurse_statistics(self):
        controller = self._get_nurse_controller()
        controller.show_nurse_statistics()

    def batch_assign_nurses(self, refresh_view_callback):
        controller = self._get_nurse_controller()
        controller.batch_assign_nurses(refresh_view_callback)

    def assign_nurse(self, child_data, update_callback):
        controller = self._get_nurse_controller()
        controller.assign_nurse(child_data, update_callback)

    def generate_report(self):
        controller = self._get_nurse_controller()
        controller.generate_report()

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
            self.root.destroy()