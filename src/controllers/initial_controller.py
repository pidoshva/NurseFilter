import logging
import tkinter as tk
from tkinter import messagebox, filedialog
from views.initial_view import InitialView
import os


class InitialController:
    """
    The main controller for the application.
    Wires up the Model (DataModel) and the Views (InitialView, CombinedDataView, ProfileView, etc.).
    """

    def __init__(self, root, model, main_controller):
        self.root = root
        self.model = model 
        self.main_controller = main_controller
        self.view = None
        logging.info("InitialController initialized.")

    def show_initial_view(self):
        view = InitialView(self.root, self).create_widgets()
        self.main_controller.add_tab(view, "Data Loader")
        self.view = view
        return view

    # 1. Reading Excel Files
    def read_excel_file(self):
        logging.info("Selecting Excel file...")
        filepath = filedialog.askopenfilename(
            initialdir=os.getcwd(),
            filetypes=[("Excel files", "*.xlsx *.xls")]
        )
        if not filepath:
            return
        # Decrypt if needed
        if self.model.is_file_encrypted(filepath):
            if not self.model.decrypt_file(filepath):
                return
        self.model.read_excel_file(filepath)
        # Re-encrypt
        try:
            self.model.encrypt_file(filepath)
        except Exception as e:
            logging.warning(f"Error re-encrypting file: {e}")
            messagebox.showwarning("Warning", "Error re-encrypting file.")

    # 2. Combining Data
    def combine_data(self):
        if self.model.combine_data():
            logging.info("Data combined successfully.")
            self.load_combined_data()
            # We don't need to remove the tab here, it's already removed in load_combined_data()
            # This prevents trying to remove the same tab twice

    def load_combined_data(self):
        if self.model.load_combined_data():
            logging.info("Combined data loaded successfully.")
            self.main_controller.show_combined_data()
            try:
                # Add error handling here
                if self.view and self.view.winfo_exists():
                    self.main_controller.remove_tab(self.view)
                    self.view = None  # Set to None after removal to avoid multiple attempts
            except Exception as e:
                logging.warning(f"Error removing tab: {e}")
