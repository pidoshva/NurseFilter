import tkinter as tk
import logging
from tkinter import ttk
from pandas import DataFrame
from views.view import View

class DuplicateDataView(View):
    """
    View class for displaying duplicate data in a Treeview.
    """

    WINDOW_TITLE = "Duplicate Data"
    WINDOW_WIDTH = 900
    WINDOW_HEIGHT = 500


    def __init__(self, root, controller, duplicate_data: DataFrame):
        super().__init__(root, controller)
        self.duplicate_data = duplicate_data

        self.create_view()
        logging.info("DuplicateDataView initialized.")


    def create_view(self):
        self.window = tk.Toplevel(self.root)
        self.window.title(DuplicateDataView.WINDOW_TITLE)
        self.window.geometry(f"{DuplicateDataView.WINDOW_WIDTH}x{DuplicateDataView.WINDOW_HEIGHT}")

        columns = list(self.duplicate_data.columns)

        self.tree = ttk.Treeview(self.window, columns=columns, show='headings')
        self.tree.pack(fill=tk.BOTH, expand=True)

        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="center", width=150)

        for _, row in self.duplicate_data.iterrows():
            values = [row[col] for col in columns]
            self.tree.insert("", "end", values=values)

        tk.Button(self.window, text="Close", command=self.window.destroy).pack(pady=10)
