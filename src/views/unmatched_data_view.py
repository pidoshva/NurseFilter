import tkinter as tk
import logging
import os
from tkinter import ttk, messagebox

class UnmatchedDataView:
    """
    View class for displaying unmatched data in a collapsible Treeview.
    """

    def __init__(self, root, controller, unmatched_data):
        self.root = root
        self.controller = controller
        self.unmatched_data = unmatched_data

        logging.info("Opening unmatched data window.")
        self.create_view()

    def create_view(self):
        self.window = tk.Toplevel(self.root)
        self.window.title("Unmatched Data")
        self.window.geometry("900x500")

        # Define primary columns to display initially
        primary_columns = ["Source", "Child_ID", "Mother_First_Name", "Mother_Last_Name"]
        all_columns = list(self.unmatched_data.columns)

        # Create Treeview widget
        self.tree = ttk.Treeview(self.window, columns=primary_columns, show="headings")
        self.tree.pack(fill=tk.BOTH, expand=True)

        # Configure column headings
        for col in primary_columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="center", width=150)

        expanded_rows = {}

        # Insert unmatched data with expand/collapse feature
        for index, row in self.unmatched_data.iterrows():
            main_values = [row.get(col, "") for col in primary_columns]
            row_id = self.tree.insert("", "end", values=main_values, open=False)
            
            # Store additional details for expansion
            additional_info = [f"{col}: {row.get(col, '')}" for col in all_columns if col not in primary_columns]
            expanded_rows[row_id] = {"expanded": False, "details": additional_info}

        # Function to expand/collapse rows
        def toggle_expand(event):
            selected_item = self.tree.selection()
            if not selected_item:
                return
            
            row_data = expanded_rows.get(selected_item[0], {})
            is_expanded = row_data.get("expanded", False)

            if not is_expanded:
                detail_items = []
                for detail in row_data["details"]:
                    detail_item = self.tree.insert(selected_item[0], "end", values=[detail], tags=("additional",))
                    detail_items.append(detail_item)
                row_data["expanded"] = True
                row_data["detail_items"] = detail_items
            else:
                for child in row_data.get("detail_items", []):
                    self.tree.delete(child)
                row_data["expanded"] = False
                row_data["detail_items"] = []

            expanded_rows[selected_item[0]] = row_data

        self.tree.bind("<Double-1>", toggle_expand)
        self.tree.tag_configure("additional", background="#962f2f", font=("Arial", 10, "italic"))

        tk.Button(self.window, text="View in Excel", command=self.controller.display_in_excel).pack(pady=10)

        logging.info("Unmatched data window loaded successfully.")
