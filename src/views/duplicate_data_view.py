import tkinter as tk
from tkinter import ttk

class DuplicateDataView:
    """
    View class for displaying duplicate data in a Treeview.
    """

    def __init__(self, root, controller, duplicate_data):
        self.root = root
        self.controller = controller
        self.duplicate_data = duplicate_data

    def create_widgets(self):
        view = tk.Frame(self.root, width=900, height=500)

        columns = list(self.duplicate_data.columns)

        self.tree = ttk.Treeview(view, columns=columns, show='headings')
        self.tree.pack(fill=tk.BOTH, expand=True)

        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="center", width=150)

        for _, row in self.duplicate_data.iterrows():
            values = [row[col] for col in columns]
            self.tree.insert("", "end", values=values)

        tk.Button(view, text="Close", command=self.controller.close_duplicate).pack(pady=10)
        view.pack()
        return view
