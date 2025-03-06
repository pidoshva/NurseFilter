import logging
from tkinter import messagebox
import pandas as pd

from views.combined_data_view import CombinedDataView
from views.unmatched_data_view import UnmatchedDataView
from views.duplicate_data_view import DuplicateDataView
from models.data_model import DataModel

class CombinedDataController:
    """
    Controller class for combined data view.
    """
    def __init__(self, root, model: DataModel, main_controller):
        self.root = root
        self.model = model
        self.main_controller = main_controller
        self.view = None
        logging.info("CombinedDataController initialized.")

    def show_combined_data(self):
        logging.info("Displaying combined data view.")
        if self.model.combined_data is not None and not self.model.combined_data.empty:
            logging.info(f"Combined data has {len(self.model.combined_data)} records.")
            # Calculate unmatched count
            unmatched_count = len(self.model.unmatched_data) if self.model.unmatched_data is not None else 0
            self.view = CombinedDataView(self.root, self, self.model.combined_data, unmatched_count=unmatched_count)
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

    def show_child_profile(self, view):
        """
        Display the profile for the selected child
            view: The view instance that contains the selected child data
        """
        selected_data = view.get_selected_child_data()
        if selected_data is not None:
            self.main_controller.show_profile(selected_data, self.refresh_view)
        else:
            logging.warning("No child data found for selected item.")

    # def get_child_data(self, selected_values):
    #     # Implement method to extract child data from the model
    #     logging.info("Retrieving child data for profile display.")
    #     try:
    #         mother_id = selected_values[0]
    #         child_name = selected_values[1].split()
    #         child_first_name = child_name[0]
    #         child_last_name = child_name[1]
    #         child_dob = selected_values[2]

    #         # Locate the child's data in the combined DataFrame
    #         child_data = self.model.combined_data[
    #             (self.model.combined_data['Mother_ID'].astype(str) == str(mother_id)) &
    #             (self.model.combined_data['Child_First_Name'].str.lower() == child_first_name.lower()) &
    #             (self.model.combined_data['Child_Last_Name'].str.lower() == child_last_name.lower()) &
    #             (self.model.combined_data['Child_Date_of_Birth'] == child_dob)
    #         ]

    #         if not child_data.empty:
    #             logging.info("Child data found.")
    #             return child_data.iloc[0]
    #         else:
    #             logging.error("Child data not found.")
    #             messagebox.showerror("Error", "Child data not found.")
    #             return None
    #     except Exception as e:
    #         logging.error(f"Error retrieving child data: {e}")
    #         messagebox.showerror("Error", f"Error retrieving child data: {e}")
    #         return None

    def refresh_view(self):
        """Refresh the CombinedDataView TreeView with the latest combined data."""
        if self.view:
            try:
                # Reload fresh data from Excel
                fresh_data = pd.read_excel('combined_matched_data.xlsx')
                
                # Update all data sources
                self.model.combined_data = fresh_data
                self.view.combined_data = fresh_data
                self.view.filtered_data = fresh_data
                
                # Clear and update the treeview
                self.view.clear_treeview()
                self.view.update_treeview(fresh_data)
                
                logging.info("Combined data view refreshed with latest data")
            except Exception as e:
                logging.error(f"Error refreshing combined data view: {e}")
                messagebox.showerror("Error", f"Failed to refresh view: {e}")
    
    def view_duplicate_data(self):
        """
        Display duplicate data in a separate window.
        """
        logging.info("Attempting to display duplicate data.")

        if self.model.duplicate_data is None or self.model.duplicate_data.empty:
            messagebox.showinfo("No Data", "No duplicate data found.")
            return

        DuplicateDataView(self.root, self, self.model.duplicate_data)


    def view_unmatched_data(self):
        """
        Display unmatched data in a separate window.
        """
        logging.info("Attempting to display unmatched data.")

        if self.model.unmatched_data is None or self.model.unmatched_data.empty:
            messagebox.showinfo("No Data", "No unmatched data available.")
            return

        # Open UnmatchedDataView instead of showing combined data
        UnmatchedDataView(self.root, self, self.model.unmatched_data)

    def show_nurse_statistics(self):
        """
        Display nurse statistics window
        """
        self.main_controller.show_nurse_statistics()


    def batch_assign_nurses(self):
        """Handle batch nurse assignment"""
        if self.model.combined_data is None or self.model.combined_data.empty:
            messagebox.showerror("Error", "No data available for batch assignment.")
            return

        self.main_controller.batch_assign_nurses(self.refresh_view)
    
    def generate_report(self):
        """Generate and display statistical report"""
        self.main_controller.generate_report()

    def display_in_excel(self):
        """Open the combined matched data in Excel."""
        self.main_controller.display_in_excel('combined_matched_data.xlsx')