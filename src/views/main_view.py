import tkinter as tk
import logging
from views.view import View

class MainView(View):
  '''
  The initial (main) window with 4 buttons:
    - Read Excel File 1
    - Read Excel File 2
    - Combine Data
    - Load Existing File
  '''

  # Class Constants
  WINDOW_TITLE = "Excel Data Combiner"
  WINDOW_WIDTH = 500
  WINDOW_HEIGHT = 600

  def __init__(self, root, controller):
    super().__init__(root, controller)
    self.root.title(MainView.WINDOW_TITLE)
    self.create_view()
    logging.info("MainView initialized.")

  def create_view(self):
    self.root.geometry(f"{MainView.WINDOW_WIDTH}x{MainView.WINDOW_HEIGHT}")
    self.root.minsize(MainView.WINDOW_WIDTH, MainView.WINDOW_HEIGHT)

    button_frame = tk.Frame(self.root, padx=20, pady=20)
    button_frame.pack(expand=True)

    read_button1 = tk.Button(button_frame, text="Read Excel File 1",
                              command=self.controller.read_excel_file,
                              width=30, height=2)
    read_button1.pack(pady=10)

    read_button2 = tk.Button(button_frame, text="Read Excel File 2",
                              command=self.controller.read_excel_file,
                              width=30, height=2)
    read_button2.pack(pady=10)

    combine_button = tk.Button(button_frame, text="Combine Data",
                                command=self.controller.combine_data,
                                width=30, height=2)
    combine_button.pack(pady=10)

    upload_existing_button = tk.Button(button_frame, text="Load Existing File",
                                        command=self.controller.load_combined_data,
                                        width=30, height=2)
    upload_existing_button.pack(pady=10)

    logging.info("MainView widgets created.")
