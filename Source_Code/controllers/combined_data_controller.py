# controllers/combined_data_controller.py

import tkinter as tk
import logging
from views.combined_data_view import CombinedDataView
from controllers.profile_controller import ProfileController
from tkinter import messagebox

class CombinedDataController:
    """
    Controller class for combined data view.
    """
    def __init__(self, root, model):
        self.root = root
        self.model = model
        self.view = None
        logging.info("CombinedDataController initialized.")

    def show_combined_data(self):
        logging.info("Displaying combined data view.")
        self.view = CombinedDataView(self.root, self, self.model.combined_data)

    def search_combined_names(self):
        # Implement search functionality
        logging.info("Searching combined names.")
        pass

    def show_child_profile(self, event):
        selected_item = self.view.treeview.selection()
        if not selected_item:
            logging.warning("No profile selected for viewing.")
            return

        # Get selected entry values
        selected_values = self.view.treeview.item(selected_item, 'values')

        # Extract data and show profile
        child_data = self.get_child_data(selected_values)
        if child_data is not None:
            logging.info(f"Opening profile for child: {child_data['Child_First_Name']} {child_data['Child_Last_Name']}")
            profile_controller = ProfileController(self.root, child_data)
            profile_controller.show_profile()

    def get_child_data(self, selected_values):
        # Implement method to extract child data from the model
        logging.info("Retrieving child data for profile display.")
        try:
            mother_id = selected_values[0]
            child_name = selected_values[1].split()
            child_first_name = child_name[0]
            child_last_name = child_name[1]
            child_dob = selected_values[2]

            # Locate the child's data in the combined DataFrame
            child_data = self.model.combined_data[
                (self.model.combined_data['Mother_ID'].astype(str) == str(mother_id)) &
                (self.model.combined_data['Child_First_Name'].str.lower() == child_first_name.lower()) &
                (self.model.combined_data['Child_Last_Name'].str.lower() == child_last_name.lower()) &
                (self.model.combined_data['Child_Date_of_Birth'] == child_dob)
            ]

            if not child_data.empty:
                logging.info("Child data found.")
                return child_data.iloc[0]
            else:
                logging.error("Child data not found.")
                messagebox.showerror("Error", "Child data not found.")
                return None
        except Exception as e:
            logging.error(f"Error retrieving child data: {e}")
            messagebox.showerror("Error", f"Error retrieving child data: {e}")
            return None
