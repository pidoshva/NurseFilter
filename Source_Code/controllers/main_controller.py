# controllers/main_controller.py

import tkinter as tk
from tkinter import filedialog, messagebox
import logging
import os
from models.data_model import DataModel
from views.main_view import MainView
from views.combined_data_view import CombinedDataView
from app_crypto import Crypto
from controllers.combined_data_controller import CombinedDataController

class MainController:
    """
    Controller class that connects the main view and the data model.
    """
    def __init__(self, root):
        self.root = root
        self.model = DataModel()
        self.view = MainView(root, self)
        logging.info("MainController initialized.")

        if not os.path.exists("key.txt"):
            logging.info("Encryption key does not exist. Generating new key.")
            try:
                self.model.generate_encryption_key()
                logging.info("Successfully generated new encryption key.")
            except:
                messagebox.showwarning("Warning!", "Error generating encryption key.")

    def on_closing(self):
        logging.info("Closing application.")
        filepath = 'combined_matched_data.xlsx'
        # Encrypt combined data files
        if self.model.combined_data is not None:
            logging.info("Encrypting combined data before exiting.")
            key = Crypto.loadKey()
            Crypto.encrypt_file(filepath, key)
        self.root.destroy()

    def read_excel_file(self):
        """
        Handle reading an Excel file chosen by the user.
        """
        logging.info("Selecting file to read.")
        filepath = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx *.xls")])

        if not filepath:
            logging.error("No file selected.")
            messagebox.showerror("Error", "No file selected.")
            return

        # Decrypt files if encrypted
        logging.info(f"Checking if file '{filepath}' is encrypted.")
        if Crypto.is_encrypted(filepath):
            logging.info("File is encrypted. Starting decryption.")
            try:
                key = Crypto.loadKey()
                Crypto.decrypt_file(filepath, key)
                logging.info("File successfully decrypted.")
            except:
                logging.error("Error decrypting file.")
                messagebox.showerror("Error", "Error decrypting file. Encryption key may be incorrect.")
                return
        else:
            logging.info("File is not encrypted.")

        data_frame = self.model.read_excel_file(filepath)
        if data_frame is not None:
            logging.info(f"Data from '{filepath}' successfully read and added to data frames.")
        else:
            logging.warning("No data frame returned from the file read.")

        # Re-encrypt files
        try:
            key = Crypto.loadKey()
            Crypto.encrypt_file(filepath, key)
            logging.info("File re-encrypted successfully.")
        except Exception as e:
            logging.error(f"Error re-encrypting file: {e}")
            messagebox.showwarning("Warning", f"Error re-encrypting file: {e}")

    def combine_data(self):
        """
        Combine data from the two Excel files read by the user and display it.
        """
        logging.info("Initiating data combination.")
        if len(self.model.data_frames) >= 2:
            logging.info("Attempting to combine data from two Excel files.")
            combined_data = self.model.combine_data()

            if combined_data is not None:
                logging.info("Data combined successfully. Displaying combined data.")
                # Display the combined data
                combined_data_controller = CombinedDataController(self.root, self.model)
                combined_data_controller.show_combined_data()
            else:
                logging.error("Failed to combine data.")
        else:
            messagebox.showwarning("Warning", "Please read two Excel files first.")
            logging.warning("Attempted to combine data with less than two files.")

    def load_combined_data(self):
        """
        Load existing combined data and display it.
        """
        logging.info("Loading existing combined data.")
        combined_data = self.model.load_combined_data()
        if combined_data is not None:
            logging.info("Combined data loaded successfully. Displaying combined data.")
            combined_data_controller = CombinedDataController(self.root, self.model)
            combined_data_controller.show_combined_data()
