import logging
import tkinter as tk
from tkinter import messagebox, filedialog
from views.initial_view import InitialView


class InitialController:
    """
    The main controller for the application.
    Wires up the Model (DataModel) and the Views (InitialView, CombinedDataView, ProfileView, etc.).
    """

    def __init__(self, root, model, main_controller):
        self.root = root
        self.model = model 
        self.main_controller = main_controller
        logging.info("InitialController initialized.")

    def show_initial_view(self):
        view = InitialView(self.root, self).create_widgets()
        self.main_controller.add_tab(view, "Data Loader")
        return view

    # 1. Reading Excel Files
    def read_excel_file(self):
        logging.info("Selecting Excel file...")
        filepath = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx *.xls")])
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


    def load_combined_data(self):
        if self.model.load_combined_data():
            logging.info("Combined data loaded successfully.")
            self.main_controller.show_combined_data()
