import logging
from tkinter import messagebox
from tkinter import filedialog
import pandas as pd

from views.combined_data_view import CombinedDataView
from views.unmatched_data_view import UnmatchedDataView
from views.duplicate_data_view import DuplicateDataView
from controllers.duplicate_data_controller import DuplicateDataController
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
        self.duplicate_data_view = None
        self.unmatched_data_view = None
        logging.info("CombinedDataController initialized.")

    def show_combined_data(self):
        logging.info("Displaying combined data view.")
        if self.model.combined_data is not None and not self.model.combined_data.empty:
            logging.info(f"Combined data has {len(self.model.combined_data)} records.")
            # Calculate unmatched count
            unmatched_count = len(self.model.unmatched_data) if self.model.unmatched_data is not None else 0
            duplicate_count = len(self.model.duplicate_data) if self.model.duplicate_data is not None else 0
            print (f"Unmatched Count: {unmatched_count}, Duplicate Count: {duplicate_count}")
            self.view = CombinedDataView(self.root, self, self.model.combined_data, unmatched_count, duplicate_count)
            frame = self.view.create_widgets()
            self.main_controller.add_tab(frame, "Combined Data")
        else:
            logging.error("No combined data available to display.")
            messagebox.showerror("Error", "No combined data available to display.")
        return frame
    

    def search_combined_names(self, query):
        logging.info(f"Searching combined names for query: {query}")
        if self.model.combined_data is not None and not self.model.combined_data.empty:
            # Convert everything to strings and search across all columns
            results = self.model.combined_data[
                self.model.combined_data.apply(
                    lambda row: row.astype(str).str.contains(query, case=False, na=False).any(), axis=1
                )
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
            profile = self.main_controller.show_profile(selected_data, self.refresh_view)
            return profile
        else:
            logging.warning("No child data found for selected item.")
        

    def refresh_view(self):
        """Refresh the CombinedDataView TreeView with the latest combined data."""
        if self.view:
            try:
                # Reload fresh data from Excel
                fresh_data = self.model.updated_data()
                
                if fresh_data is None or fresh_data.empty:
                    messagebox.showerror("Error", "No fresh data available to refresh the view.")
                    return
                
                # Update all data sources
                self.view.combined_data = fresh_data
                self.view.filtered_data = fresh_data
                
                # Clear and update the treeview
                self.view.clear_treeview()
                self.view.update_treeview(fresh_data)
                
                logging.info("Combined data view refreshed with latest data")
            except Exception as e:
                logging.error(f"Error refreshing combined data view: {e}")
                messagebox.showerror("Error", f"Failed to refresh view: {e}")

    def refresh_view(self):
        if self.model.combined_data is not None:
            self.view.update_treeview(self.model.combined_data)
            logging.info("Combined data view refreshed with loaded data.")
    
    def view_duplicate_data(self):
        """
        Display duplicate data in a separate window.
        """
        logging.info("Attempting to display duplicate data.")
        controller = DuplicateDataController(self.root, self.model, self.main_controller)
        controller.show_duplicate_data()


    def view_unmatched_data(self):
        """
        Display unmatched data in a separate window.
        """
        logging.info("Attempting to display unmatched data.")

        if self.model.unmatched_data is None or self.model.unmatched_data.empty:
            messagebox.showinfo("No Data", "No unmatched data available.")
            return

        # Open UnmatchedDataView instead of showing combined data
        unmatched_window = UnmatchedDataView(self.root, self, self.model.unmatched_data)
        self.unmatched_data_view = unmatched_window.create_widgets()
        self.main_controller.add_tab(self.unmatched_data_view, "Unmatched Data")
        return self.unmatched_data_view

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

    def close_combined(self):
        """Close the combined data view."""
        if self.view:
            self.main_controller.remove_tab(self.view)
            self.view = None

    def close_duplicate(self):
        """Close the duplicate data view."""
        if self.duplicate_data_view:
            self.main_controller.remove_tab(self.duplicate_data_view)
            self.duplicate_data_view = None
    
    def close_unmatched(self):
        """Close the unmatched data view."""
        if self.unmatched_data_view:
            self.main_controller.remove_tab(self.unmatched_data_view)
            self.unmatched_data_view = None

    def add_previous_combined_data(self):
        filepath = filedialog.askopenfilename(title="Select Combined Data Excel File", filetypes=[("Excel Files", "*.xlsx")])
        if not filepath:
            return

        try:
            new_data = pd.read_excel(filepath)

            # Standardize null nurse fields
            if 'Assigned_Nurse' in new_data.columns:
                new_data['Assigned_Nurse'] = new_data['Assigned_Nurse'].fillna('None')
            else:
                new_data['Assigned_Nurse'] = 'None'

            # Combine with existing data
            if self.model.combined_data is not None:
                combined = pd.concat([self.model.combined_data, new_data], ignore_index=True)
            else:
                combined = new_data.copy()

            self.model.combined_data = combined

            # Refresh view
            if self.view:
                self.view.update_treeview(combined)

            # Save to file
            combined.to_excel("combined_matched_data.xlsx", index=False)
            logging.info("Previous combined data added and saved successfully.")

            messagebox.showinfo("Success", "Data successfully loaded and added to combined dataset.")

        except Exception as e:
            logging.error(f"Error loading previous combined data: {e}")
            messagebox.showerror("Error", f"Failed to load data: {e}")
