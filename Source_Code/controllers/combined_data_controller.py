# controllers/combined_data_controller.py

import tkinter as tk
import logging
from views.combined_data_view import CombinedDataView
from controllers.profile_controller import ProfileController
from tkinter import messagebox
import pandas as pd

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
        if self.model.combined_data is not None and not self.model.combined_data.empty:
            logging.info(f"Combined data has {len(self.model.combined_data)} records.")
            self.view = CombinedDataView(self.root, self, self.model.combined_data)
        else:
            logging.error("No combined data available to display.")
            messagebox.showerror("Error", "No combined data available to display.")

    def search_combined_names(self, query):
        logging.info(f"Searching combined names for query: {query}")
        if self.model.combined_data is not None and not self.model.combined_data.empty:
            results = self.model.combined_data[
                self.model.combined_data['Child_First_Name'].str.contains(query, case=False, na=False)
            ]
            if self.view:
                self.view.update_table(results)
        else:
            logging.warning("No combined data to search.")

    def show_child_profile(self, event):
        logging.info("Show child profile requested.")
        child_data = self.view.get_selected_child_data()
        if child_data is not None:
            logging.info(f"Opening profile for child: {child_data['Child_First_Name']} {child_data['Child_Last_Name']}")
            profile_controller = ProfileController(self.root, child_data, self.model)
            profile_controller.show_profile()
        else:
            logging.warning("No child data found for selected item.")

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

    def refresh_view(self):
        """Refresh the CombinedDataView TreeView with the latest combined data."""
        if self.view:
            # Reload fresh data from Excel
            try:
                fresh_data = pd.read_excel('combined_matched_data.xlsx')
                self.model.combined_data = fresh_data
                self.view.update_treeview(fresh_data)
                logging.info("Combined data view refreshed with latest data")
            except Exception as e:
                logging.error(f"Error refreshing combined data view: {e}")

    def after_nurse_assignment(self):
        if hasattr(self.root, 'combined_data_controller'):
            self.root.combined_data_controller.refresh_view()
