from tkinter import ttk
import tkinter as tk


class TabsView:
    def __init__(self, root):
        self.root = root
        self.tab_count = 0
        self.notebook = None

    def create_widgets(self):
        self.root.deiconify()
        self.root.title("Data Viewer")
        self.root.geometry("1200x700")
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill=tk.BOTH, expand=True)
        self.notebook = notebook
        return notebook

    def add_tab(self, tab_view, tab_name):
        """Add a new tab to the Notebook."""
        self.notebook.add(tab_view, text=tab_name)
        self.notebook.select(self.notebook.tabs()[self.tab_count])  # Select the new tab
        self.tab_count += 1

    def remove_tab(self, tab_view):
        """Remove a tab from the Notebook."""
        self.notebook.forget(tab_view)
        tab_view.destroy()
        self.tab_count -= 1