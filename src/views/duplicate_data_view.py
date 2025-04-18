import tkinter as tk
from tkinter import ttk

class DuplicateDataView:
    def __init__(self, root, controller, duplicate_data):
        self.root = root
        self.controller = controller
        self.duplicate_data = duplicate_data
        self.view = None

    def get_frame(self):
        return self.view

    def create_widgets(self):
        self.view = tk.Frame(self.root, width=900, height=500)

        columns = list(self.duplicate_data.columns)

        self.tree = ttk.Treeview(self.view, columns=columns, show='headings')
        self.tree.pack(fill=tk.BOTH, expand=True)

        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="center", width=150)

        for _, row in self.duplicate_data.iterrows():
            values = [row[col] for col in columns]
            self.tree.insert("", "end", values=values)

        tk.Button(self.view, text="View in Excel",
                  command=self.controller.display_in_excel).pack(pady=5)

        tk.Button(self.view, text="Close", command=self.controller.close_duplicate).pack(pady=10)

        self.view.pack()
        return self.view
