import tkinter as tk
import logging

class MainView:
    """
    View class responsible for the main application window.
    """
    def __init__(self, root, controller):
        self.root = root
        self.controller = controller
        self.root.title("Excel Combiner")
        self.create_widgets()

    def create_widgets(self):
        self.root.geometry("500x600")
        self.root.minsize(500, 600)

        button_frame = tk.Frame(self.root, padx=20, pady=20)
        button_frame.pack(expand=True)

        self.read_button1 = tk.Button(button_frame, text="Read Excel File 1", command=self.controller.read_excel_file, width=30, height=2)
        self.read_button1.pack(pady=10)

        self.read_button2 = tk.Button(button_frame, text="Read Excel File 2", command=self.controller.read_excel_file, width=30, height=2)
        self.read_button2.pack(pady=10)

        self.combine_button = tk.Button(button_frame, text="Combine Data", command=self.controller.combine_data, width=30, height=2)
        self.combine_button.pack(pady=10)

        self.upload_existing_button = tk.Button(button_frame, text="Load Existing File", command=self.controller.load_combined_data, width=30, height=2)
        self.upload_existing_button.pack(pady=10)

        logging.info("UI widgets created.")
