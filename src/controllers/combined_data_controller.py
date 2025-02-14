# controllers/combined_data_controller.py

import tkinter as tk
import logging
from views.combined_data_view import CombinedDataView
from controllers.profile_controller import ProfileController
from tkinter import messagebox
import pandas as pd
import os
import platform

from views.unmatched_data_view import UnmatchedDataView
from views.duplicate_data_view import DuplicateDataView

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

    def show_child_profile(self, event, view):
        """
        Display the profile for the selected child
        
        Args:
            event: The event that triggered this method
            view: The view instance that contains the selected child data
        """
        selected_data = view.get_selected_child_data()
        if selected_data is not None:
            from controllers.profile_controller import ProfileController
            profile_controller = ProfileController(self.root, selected_data, self.model)
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

    def after_nurse_assignment(self):
        if hasattr(self.root, 'combined_data_controller'):
            self.root.combined_data_controller.refresh_view()

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
        df = self.model.combined_data
        if df is None or df.empty:
            messagebox.showinfo("No Data", "No nurse assignment data to display.")
            return
        if 'Assigned_Nurse' not in df.columns:
            messagebox.showinfo("No Data", "No 'Assigned_Nurse' column in the data.")
            return

        assigned = df[df['Assigned_Nurse'].notna() & (df['Assigned_Nurse'] != 'None')]
        if assigned.empty:
            messagebox.showinfo("No Data", "No nurse assignments found.")
            return

        counts = assigned['Assigned_Nurse'].value_counts()
        stats = tk.Toplevel(self.root)
        stats.title("Nurse Statistics")
        stats.geometry("400x400")

        most_assigned = counts.idxmax()
        least_assigned = counts.idxmin()
        tk.Label(stats, text=f"Most Assigned Nurse: {most_assigned} ({counts.max()})", font=("Arial",12)).pack(pady=5)
        tk.Label(stats, text=f"Least Assigned Nurse: {least_assigned} ({counts.min()})", font=("Arial",12)).pack(pady=5)

        tk.Label(stats, text="Assignments by Nurse:", font=("Arial",12,"bold")).pack(pady=5)
        for nurse, count in counts.items():
            tk.Label(stats, text=f"{nurse}: {count} assignment(s)", fg="blue").pack(anchor='w', padx=10)

        logging.info("Displayed nurse statistics window")

    def display_in_excel(self):
        """Display the combined data in Excel"""
        filepath = 'combined_matched_data.xlsx'
        if not os.path.exists(filepath):
            messagebox.showerror("Error", "The combined data file does not exist.")
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

    def batch_assign_nurses(self):
        """Handle batch nurse assignment"""
        if self.model.combined_data is None or self.model.combined_data.empty:
            messagebox.showerror("Error", "No data available for batch assignment.")
            return

        window = tk.Toplevel(self.root)
        window.title("Batch Assign Nurses")
        window.geometry("400x400")  # Made window taller to ensure buttons are visible

        # Create main frame to hold everything
        main_frame = tk.Frame(window)
        main_frame.pack(expand=True, fill='both', padx=20, pady=20)

        # Filter entries
        tk.Label(main_frame, text="Filter by City:").pack(pady=5)
        city_var = tk.StringVar()
        tk.Entry(main_frame, textvariable=city_var).pack(pady=5)

        tk.Label(main_frame, text="Filter by State:").pack(pady=5)
        state_var = tk.StringVar()
        tk.Entry(main_frame, textvariable=state_var).pack(pady=5)

        tk.Label(main_frame, text="Filter by ZIP Code:").pack(pady=5)
        zip_var = tk.StringVar()
        tk.Entry(main_frame, textvariable=zip_var).pack(pady=5)

        tk.Label(main_frame, text="Nurse Name:").pack(pady=5)
        nurse_var = tk.StringVar()
        tk.Entry(main_frame, textvariable=nurse_var).pack(pady=5)

        # Create a frame for buttons at the bottom
        button_frame = tk.Frame(main_frame)
        button_frame.pack(side='bottom', pady=20)

        def save():
            nurse_name = nurse_var.get().strip()
            if not nurse_name:
                messagebox.showerror("Error", "Nurse name is required.")
                return
            city = city_var.get().strip()
            state = state_var.get().strip()
            zipcode = zip_var.get().strip()
            count = self.model.batch_update_nurses(nurse_name, city, state, zipcode)
            if count > 0:
                messagebox.showinfo("Success", f"Nurse '{nurse_name}' assigned to {count} children.")
                self.refresh_view()  # Refresh the view after batch assignment
                window.destroy()
            else:
                messagebox.showinfo("No Matches", "No records matched the filters.")

        # Add both Save and Cancel buttons
        tk.Button(button_frame, text="Save", command=save, width=10).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Cancel", command=window.destroy, width=10).pack(side=tk.LEFT, padx=5)

    def generate_report(self):
        """Generate and display statistical report"""
        df = self.model.combined_data
        if df is None or df.empty:
            messagebox.showerror("Error", "No data available to generate a report.")
            return

        report_win = tk.Toplevel(self.root)
        report_win.title("Statistical Report")
        report_win.geometry("600x500")

        total = len(df)
        unassigned = len(df[df['Assigned_Nurse'] == 'None'])
        tk.Label(report_win, text=f"Total Children: {total}", font=("Arial",12)).pack(pady=5)
        tk.Label(report_win, text=f"Unassigned Children: {unassigned}", font=("Arial",12)).pack(pady=5)

        # Add more report details as needed...
        logging.info("Generated statistical report")

    def view_duplicate_data(self):
        """
        Display duplicate data in a separate window.
        """
        logging.info("Attempting to display duplicate data.")

        if self.model.duplicate_data is None or self.model.duplicate_data.empty:
            messagebox.showinfo("No Data", "No duplicate data found.")
            return

        DuplicateDataView(self.root, self, self.model.duplicate_data)
