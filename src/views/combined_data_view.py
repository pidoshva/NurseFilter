import tkinter as tk
import pandas as pd
import logging
from tkinter import ttk, messagebox

class CombinedDataView:
    """
    View class for displaying the combined data in a Treeview,
    plus search, sort by DOB, nurse stats, batch assign, unmatched, etc.
    """

    def __init__(self, root, controller, combined_data, unmatched_count=0):
        self.root = root
        self.controller = controller

        self.combined_data = combined_data.copy()
        self.filtered_data = combined_data.copy()

        self.sort_ascending = True
        self.unmatched_count = unmatched_count

        self.create_view()
        logging.info("CombinedDataView initialized.")

    def get_combined_window(self):
        return self.combined_window

    def create_view(self):
        self.combined_window = tk.Frame(self.root, width=1000, height=600)

        # Top frame: search, sort, nurse stats
        top_frame = tk.Frame(self.combined_window)
        top_frame.pack(fill=tk.X, padx=5, pady=5)

        self.search_var = tk.StringVar()
        search_entry = tk.Entry(top_frame, textvariable=self.search_var)
        search_entry.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)

        search_button = tk.Button(top_frame, text="Search", command=self.search_data)
        search_button.pack(side=tk.LEFT, padx=5)

        # Sort by DOB
        self.sort_button = tk.Button(top_frame, text="Sort by DOB ▲", command=self.sort_by_dob)
        self.sort_button.pack(side=tk.LEFT, padx=5)

        # Nurse Statistics
        nurse_stats_button = tk.Button(
            top_frame, 
            text="Nurse Statistics",
            command=self.controller.show_nurse_statistics
        )
        nurse_stats_button.pack(side=tk.LEFT, padx=5)

        # Treeview
        columns = ("Mother_ID", "First_Name", "Last_Name", "Date_of_Birth", "Assigned_Nurse")
        self.treeview = ttk.Treeview(self.combined_window, columns=columns, show='headings')

        # Set column headings with proper labels
        column_headers = {
            "Mother_ID": "Mother ID",
            "First_Name": "First Name",
            "Last_Name": "Last Name", 
            "Date_of_Birth": "Date of Birth",
            "Assigned_Nurse": "Assigned Nurse"
        }
        
        for col in columns:
            self.treeview.heading(col, text=column_headers[col])
            self.treeview.column(col, anchor="center", width=150)

        scrollbar = ttk.Scrollbar(self.combined_window, orient="vertical", command=self.treeview.yview)
        self.treeview.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side='right', fill='y')

        self.treeview.pack(fill=tk.BOTH, expand=True)

        # Double-click => show child profile
        self.treeview.bind("<Double-1>", lambda e: self.controller.show_child_profile(self))

        # Populate
        self.update_treeview(self.filtered_data)

        # Bottom frame: display in excel, batch assign, generate report, unmatched
        bottom_frame = tk.Frame(self.combined_window)
        bottom_frame.pack(fill=tk.X, pady=5)

        excel_btn = tk.Button(bottom_frame, text="Display in Excel",
                              command=self.controller.display_in_excel)
        excel_btn.pack(side=tk.LEFT, padx=10)

        batch_btn = tk.Button(bottom_frame, text="Batch Assign Nurses",
                              command=self.controller.batch_assign_nurses)
        batch_btn.pack(side=tk.LEFT, padx=10)

        report_btn = tk.Button(bottom_frame, text="Generate Report",
                               command=self.controller.generate_report)
        report_btn.pack(side=tk.LEFT, padx=10)

        # If there are unmatched rows, show a button w/ a red badge
        if self.unmatched_count > 0:
            unmatched_button = tk.Button(bottom_frame, text="View Unmatched Data",
                                         command=self.controller.view_unmatched_data)
            unmatched_button.pack(side=tk.LEFT, padx=10)
            # Badge
            count_label = tk.Label(unmatched_button, text=str(self.unmatched_count),
                                   bg="red", fg="white", font=("Arial", 10, "bold"))
            count_label.place(relx=1.0, rely=0.0, anchor="ne")

        # If there are duplicate rows, show a button with a blue badge
        if self.controller.model.duplicate_data is not None and not self.controller.model.duplicate_data.empty:
            duplicate_button = tk.Button(bottom_frame, text="View Duplicate Data", command=self.controller.view_duplicate_data)
            duplicate_button.pack(side=tk.LEFT, padx=10)
            # Badge
            duplicate_count = int((len(self.controller.model.duplicate_data))/2)
            dup_count_label = tk.Label(duplicate_button, text=str(duplicate_count),
                                    bg="blue", fg="white", font=("Arial", 10, "bold"))
            dup_count_label.place(relx=1.0, rely=0.0, anchor="ne")
        


    def update_treeview(self, data):
        """Update treeview with fresh data."""
        # Clear existing items
        self.clear_treeview()
        
        # Insert fresh data
        for _, row in data.iterrows():
            values = [
                str(row.get('Mother_ID', '')),  # Ensure Mother_ID is string
                row.get('Child_First_Name', ''),
                row.get('Child_Last_Name', ''),
                row.get('Child_Date_of_Birth', ''),
                row.get('Assigned_Nurse', 'None')  # Ensure 'None' is displayed if no nurse
            ]
            self.treeview.insert('', 'end', values=values)
        
        # Force update
        self.treeview.update_idletasks()
        logging.info("Treeview updated with fresh data")

    def clear_treeview(self):
        """Clear all items from treeview"""
        for item in self.treeview.get_children():
            self.treeview.delete(item)

    def get_selected_child_data(self):
        """Get data for selected child in treeview."""
        selection = self.treeview.selection()
        if selection:
            try:
                vals = self.treeview.item(selection[0])['values']
                # Update unpacking to match actual columns (Mother_ID, First, Last, DOB, Nurse)
                mother_id, child_first_name, child_last_name, dob, nurse = vals
                
                # Locate the child's data in the combined DataFrame
                child_data = self.controller.model.combined_data[
                    (self.controller.model.combined_data['Mother_ID'].astype(str) == str(mother_id)) &
                    (self.controller.model.combined_data['Child_First_Name'].str.lower() == child_first_name.lower()) &
                    (self.controller.model.combined_data['Child_Last_Name'].str.lower() == child_last_name.lower()) &
                    (self.controller.model.combined_data['Child_Date_of_Birth'] == dob)
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
        return None

    def search_data(self):
        s = self.search_var.get().lower().strip()
        if not s:
            self.filtered_data = self.combined_data.copy()
        else:
            def row_matches(r):
                if s in str(r.get('Mother_ID','')).lower():
                    return True
                cname = f"{r.get('Child_First_Name','')} {r.get('Child_Last_Name','')}".lower()
                if s in cname:
                    return True
                if s in str(r.get('Child_Date_of_Birth','')).lower():
                    return True
                if s in str(r.get('Assigned_Nurse','')).lower():
                    return True
                return False

            self.filtered_data = self.combined_data[self.combined_data.apply(row_matches, axis=1)]

        self.update_treeview(self.filtered_data)

    def sort_by_dob(self):
        self.sort_ascending = not self.sort_ascending
        arrow = "▲" if self.sort_ascending else "▼"
        self.sort_button.config(text=f"Sort by DOB {arrow}")

        df = self.filtered_data.copy()
        df['dob_temp'] = pd.to_datetime(df['Child_Date_of_Birth'], errors='coerce')
        df.sort_values(by='dob_temp', ascending=self.sort_ascending, inplace=True)
        df.drop(columns=['dob_temp'], inplace=True)

        self.filtered_data = df
        self.update_treeview(self.filtered_data)
