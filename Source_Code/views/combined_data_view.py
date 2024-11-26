# views/combined_data_view.py

import tkinter as tk
from tkinter import ttk
import logging

class CombinedDataView:
    """
    View class for displaying combined data.
    """
    def __init__(self, root, controller, combined_data):
        self.root = root
        self.controller = controller
        self.combined_data = combined_data
        self.filtered_data = combined_data  # Initialize filtered data
        self.create_view()
        logging.info("CombinedDataView initialized.")

    def create_view(self):
        logging.info("Creating combined data view.")
        self.combined_names_window = tk.Toplevel(self.root)
        self.combined_names_window.title("Combined Data")
        self.combined_names_window.geometry("1000x600")
        self.combined_names_window.minsize(800, 400)
        self.combined_names_window.resizable(True, True)

        # Search Frame
        search_frame = tk.Frame(self.combined_names_window)
        search_frame.pack(fill=tk.X, pady=5)

        self.search_var = tk.StringVar()
        search_entry = tk.Entry(search_frame, textvariable=self.search_var)
        search_entry.pack(side=tk.LEFT, padx=10, fill=tk.X, expand=True)

        search_button = tk.Button(search_frame, text="Search", command=self.search_combined_names)
        search_button.pack(side=tk.RIGHT, padx=10)

        # Treeview to display data
        columns = ("Mother_ID", "Child_Name", "Child_Date_of_Birth", "Assigned_Nurse")
        self.treeview = ttk.Treeview(self.combined_names_window, columns=columns, show='headings')

        # Define headings
        for col in columns:
            self.treeview.heading(col, text=col)
            self.treeview.column(col, anchor="center", width=150)

        # Add vertical scrollbar
        scrollbar = ttk.Scrollbar(self.combined_names_window, orient="vertical", command=self.treeview.yview)
        self.treeview.configure(yscroll=scrollbar.set)
        scrollbar.pack(side='right', fill='y')

        self.treeview.pack(fill=tk.BOTH, expand=True)
        self.treeview.bind('<Double-1>', self.controller.show_child_profile)

        # Populate Treeview with data
        self.populate_treeview()
        logging.info("Combined data view created and displayed.")

    def populate_treeview(self):
        logging.info("Populating Treeview with combined data.")
        self.clear_treeview()
        for index, row in self.filtered_data.iterrows():
            child_name = f"{row.get('Child_First_Name', '')} {row.get('Child_Last_Name', '')}"
            assigned_nurse = row.get('Assigned_Nurse', 'None')
            self.treeview.insert("", "end", values=(
                row.get('Mother_ID', ''),
                child_name,
                row.get('Child_Date_of_Birth', ''),
                assigned_nurse
            ))
        logging.info("Treeview populated.")

    def clear_treeview(self):
        logging.info("Clearing Treeview.")
        for item in self.treeview.get_children():
            self.treeview.delete(item)
        logging.info("Treeview cleared.")

    def update_treeview(self):
        logging.info("Updating Treeview with filtered data.")
        self.populate_treeview()

    def search_combined_names(self):
        logging.info("Search initiated.")
        search_text = self.search_var.get().strip().lower()
        logging.info(f"Search text: '{search_text}'")
        if search_text == '':
            self.filtered_data = self.combined_data
        else:
            # Filter the combined_data DataFrame based on the search text
            self.filtered_data = self.combined_data[
                self.combined_data.apply(
                    lambda row: search_text in str(row.get('Mother_ID', '')).lower() or
                                search_text in str(row.get('Child_First_Name', '')).lower() or
                                search_text in str(row.get('Child_Last_Name', '')).lower() or
                                search_text in (str(row.get('Child_First_Name', '')).lower() + ' ' + str(row.get('Child_Last_Name', '')).lower()) or
                                search_text in str(row.get('Child_Date_of_Birth', '')).lower() or
                                search_text in str(row.get('Assigned_Nurse', '')).lower(),
                    axis=1
                )
            ]
        self.update_treeview()
        logging.info("Search completed and Treeview updated.")

    def get_selected_child_data(self):
        selected_item = self.treeview.selection()
        if not selected_item:
            logging.warning("No item selected in Treeview.")
            return None

        selected_values = self.treeview.item(selected_item, 'values')
        logging.info(f"Selected values: {selected_values}")

        mother_id = selected_values[0]
        child_name = selected_values[1].split()
        child_first_name = child_name[0] if len(child_name) > 0 else ''
        child_last_name = child_name[1] if len(child_name) > 1 else ''
        child_dob = selected_values[2]

        # Find the row in combined_data that matches the selected item
        child_data = self.combined_data[
            (self.combined_data['Mother_ID'].astype(str) == str(mother_id)) &
            (self.combined_data['Child_First_Name'].str.lower() == child_first_name.lower()) &
            (self.combined_data['Child_Last_Name'].str.lower() == child_last_name.lower()) &
            (self.combined_data['Child_Date_of_Birth'] == child_dob)
        ]

        if not child_data.empty:
            logging.info("Child data found for selected item.")
            return child_data.iloc[0]
        else:
            logging.error("Child data not found for selected item.")
            return None
