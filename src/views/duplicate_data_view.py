import tkinter as tk
from tkinter import ttk, messagebox
from views.view_constants import ViewStyles

class DuplicateDataView:
    """
    View class for displaying duplicate data in a Treeview.
    """
    def __init__(self, root, controller, duplicate_data):
        self.root = root
        self.controller = controller
        self.duplicate_data = duplicate_data

        self.create_view()

    def create_view(self):
        self.window = tk.Toplevel(self.root, bg=ViewStyles.WINDOW_COLOR)
        self.window.title("Duplicate Data")
        self.window.geometry(f"{ViewStyles.DD_WINDOW_WIDTH}x{ViewStyles.DD_WINDOW_HEIGHT}")

        columns = list(self.duplicate_data.columns)

        self.tree = ttk.Treeview(self.window, columns=columns, show='headings')
        self.tree.pack(fill=tk.BOTH, expand=True)

        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="center", width=150)

        for _, row in self.duplicate_data.iterrows():
            values = [row[col] for col in columns]
            self.tree.insert("", "end", values=values)

        tk.Button(self.window, text="Close", command=self.window.destroy, bg=ViewStyles.WINDOW_BUTTON_COLOR).pack(pady=10)
