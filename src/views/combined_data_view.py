import tkinter as tk
import pandas as pd
import logging
from tkinter import ttk, messagebox
from views.tooltip import add_tooltip

class CombinedDataView:
    """
    View class for displaying the combined data in a Treeview,
    plus search, sort by DOB, nurse stats, batch assign, unmatched, etc.
    """

    def __init__(self, root, controller, combined_data, unmatched_count=0, duplicate_count=0):
        self.root = root
        self.controller = controller

        self.combined_data = combined_data.copy()
        self.filtered_data = combined_data.copy()

        self.sort_ascending = True
        self.unmatched_count = unmatched_count
        self.duplicate_count = duplicate_count

        logging.info("CombinedDataView initialized.")


    def create_widgets(self):
        self.combined_window = tk.Frame(self.root, width=1000, height=600)

        # Top frame: search, sort, nurse stats
        top_frame = tk.Frame(self.combined_window)
        top_frame.pack(fill=tk.X, padx=5, pady=5)

        # Create a frame for the search bar and clear button
        search_frame = tk.Frame(top_frame)
        search_frame.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)

        # Search components container
        search_components = tk.Frame(search_frame)
        search_components.pack(side=tk.LEFT, fill=tk.X, expand=True)

        self.search_var = tk.StringVar()
        search_entry = tk.Entry(search_components, textvariable=self.search_var, width=40)
        search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        # Add binding to search when Enter key is pressed
        search_entry.bind('<Return>', lambda event: self.search_data())

        # Add clear button (X) within the search bar area
        clear_button = tk.Button(search_components, text="✕", command=self.clear_search, width=2)
        clear_button.pack(side=tk.LEFT)
        add_tooltip(search_entry, "Search by name, ID, date of birth, or nurse name")

        # Move search button into the search frame
        search_button = tk.Button(search_components, text="Search", command=self.search_data)
        search_button.pack(side=tk.LEFT, padx=5)
        add_tooltip(search_button, "Search for specific records based on your search terms")

        # Sort by DOB
        self.sort_button = tk.Button(top_frame, text="Sort by DOB ▲", command=self.sort_by_dob)
        self.sort_button.pack(side=tk.LEFT, padx=5)
        add_tooltip(self.sort_button, "Sort the list by date of birth (toggle ascending/descending)")

        # Nurse Statistics
        nurse_stats_button = tk.Button(
            top_frame, 
            text="Nurse Statistics",
            command=self.controller.show_nurse_statistics
        )
        nurse_stats_button.pack(side=tk.LEFT, padx=5)
        add_tooltip(nurse_stats_button, "View statistics about nurse assignments and caseloads")

        # Treeview
        columns = ("Mother_ID", "First_Name", "Last_Name", "Date_of_Birth","City_db","Zip","Phone_#","Street_address", "Assigned_Nurse")
        self.treeview = ttk.Treeview(self.combined_window, columns=columns, show='headings')
        add_tooltip(self.treeview, "Double-click on a record to view or edit a child's detailed profile")

        # Set column headings with proper labels
        column_headers = {
            "Mother_ID": "Mother ID",
            "First_Name": "First Name",
            "Last_Name": "Last Name", 
            "Date_of_Birth": "Date of Birth",
            "City_db":"City_db",
            "Zip":"Zip",
            "Phone_#":"Phone_#",
            "Street_address":"Street_address",
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

        # Add Data from Previous Session Button
        add_button = tk.Button(bottom_frame, text="Add Data",
                            command=self.controller.add_previous_combined_data)
        add_button.pack(side=tk.LEFT, padx=10)
        add_tooltip(add_button, "Append previous combined data to the current session")

        excel_btn = tk.Button(bottom_frame, text="Display in Excel",
                              command=self.controller.display_in_excel)
        excel_btn.pack(side=tk.LEFT, padx=10)
        add_tooltip(excel_btn, "Open the current data in Excel for additional viewing or editing")

        batch_btn = tk.Button(bottom_frame, text="Batch Assign Nurses",
                              command=self.controller.batch_assign_nurses)
        batch_btn.pack(side=tk.LEFT, padx=10)
        add_tooltip(batch_btn, "Assign nurses to multiple children at once using criteria")

        report_btn = tk.Button(bottom_frame, text="Generate Report",
                               command=self.controller.generate_report)
        report_btn.pack(side=tk.LEFT, padx=10)
        add_tooltip(report_btn, "Generate a statistical report of the current data")

        # If there are unmatched rows, show a button w/ a red badge
        if self.unmatched_count > 0:
            unmatched_button = tk.Button(bottom_frame, text="View Unmatched Data",
                                         command=self.controller.view_unmatched_data)
            unmatched_button.pack(side=tk.LEFT, padx=10)
            add_tooltip(unmatched_button, f"View {self.unmatched_count} records that couldn't be matched between datasets")
            # Badge
            count_label = tk.Label(unmatched_button, text=str(self.unmatched_count),
                                   bg="red", fg="white", font=("Arial", 10, "bold"))
            count_label.place(relx=1.0, rely=0.0, anchor="ne")

        # If there are duplicate rows, show a button with a blue badge
        if self.duplicate_count > 0:
            duplicate_button = tk.Button(bottom_frame, text="View Duplicate Data", command=self.controller.view_duplicate_data)
            duplicate_button.pack(side=tk.LEFT, padx=10)
            # Badge
            duplicate_count = int((len(self.controller.model.duplicate_data))/2)
            add_tooltip(duplicate_button, f"View {duplicate_count} potentially duplicate records that need review")
            dup_count_label = tk.Label(duplicate_button, text=str(duplicate_count),
                                    bg="blue", fg="white", font=("Arial", 10, "bold"))
            dup_count_label.place(relx=1.0, rely=0.0, anchor="ne")
        return self.combined_window
        
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
                row.get('City_db',''),
                row.get('Zip',''),
                row.get('Phone_#',''),
                row.get('Street_address',''),

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
                mother_id, child_first_name, child_last_name, dob, City, Zip,Phone,Street, nurse = vals
                
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

    # Add a new method to clear the search
    def clear_search(self):
        self.search_var.set("")
        self.filtered_data = self.combined_data.copy()
        self.update_treeview(self.filtered_data)
