import tkinter as tk
from tkinter import ttk, messagebox
from views.combined_data_view import CombinedDataView
from controllers.combined_data_controller import CombinedDataController
from views.duplicate_data_view import DuplicateDataView



from controllers.combined_data_controller import CombinedDataController

class MainApplication(tk.Toplevel):
    
    def __init__(self, root, combined_data, duplicate_data):
        super().__init__(root)
        self.title("Data Viewer")
        self.geometry("1200x700")
       

        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        # ✅ Pass notebook to MainController
        from controllers.main_controller import MainController
        self.main_controller = MainController(self, self.notebook)

        # ✅ Call create_tabs() to add tabs
        self.create_tabs(combined_data, duplicate_data)

    def create_tabs(self, combined_data, duplicate_data):
        """ ✅ Create and add tabs to the Notebook """

        self.combined_data_view = CombinedDataView(self.notebook, self.main_controller.combined_data_controller, combined_data)
        self.notebook.add(self.combined_data_view.frame, text="Combined Data")

        if not duplicate_data.empty:
            self.duplicate_data_view = DuplicateDataView(self.notebook, self.main_controller.combined_data_controller, duplicate_data)
            self.notebook.add(self.duplicate_data_view.frame, text="Duplicate Data")

    # ✅ Print debug info to check if tabs are created
        print("📌 Notebook Tabs Exist:", self.notebook.tabs())

    # ✅ Switch to the first tab
        if self.notebook.tabs():  
            self.notebook.select(self.notebook.tabs()[0])  # Select the first tab






    def go_to_duplicate_tab(self):
        """Switch to the Duplicate Data tab."""
        if hasattr(self, 'duplicate_data_view'):
            self.notebook.select(self.duplicate_data_view.frame)  # ✅ Switch to Duplicate Data tab

    def back_to_main(self):
        """Closes the tabbed UI and returns to MainView."""
        self.destroy()
        self.master.deiconify()
