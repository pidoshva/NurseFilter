from views.duplicate_data_view import DuplicateDataView
from tkinter import messagebox

class DuplicateDataController:
    """
    Controller for displaying duplicate data view.
    """
    def __init__(self, root, model, main_controller):
        self.root = root
        self.model = model
        self.main_controller = main_controller
        self.view = None

    def show_duplicate_data(self):
        """
        Display the duplicate data view in a new tab.
        """
        if self.model.duplicate_data is not None and not self.model.duplicate_data.empty:
            self.view = DuplicateDataView(self.root, self, self.model.duplicate_data, self.main_controller)
            frame = self.view.create_widgets()
            self.main_controller.add_tab(frame, "Duplicate Records")
            return frame
        else:
            messagebox.showinfo("Info", "No duplicate data to display.")

    def close_duplicate(self):
        """
        Close the duplicate data tab.
        """
        if self.view:
            self.main_controller.remove_tab(self.view.get_frame())
            self.view = None

    def display_in_excel(self):
        self.main_controller.display_in_excel("duplicate_names.xlsx")
