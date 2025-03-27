import tkinter as tk
import logging
from views.tooltip import add_tooltip

class InitialView:
  """
  The initial (main) window with 4 buttons:
    - Read Excel File 1
    - Read Excel File 2
    - Combine Data
    - Load Existing File
  """

  def __init__(self, root, controller):
      self.root = tk.Frame(root, width=500, height=600)
      self.controller = controller
      logging.info("MainView initialized.")

  def create_widgets(self):
      button_frame = tk.Frame(self.root, padx=20, pady=20)
      button_frame.pack(expand=True)

      read_button1 = tk.Button(button_frame, text="Read Excel File 1",
                                command=self.controller.read_excel_file,
                                width=30, height=2)
      read_button1.pack(pady=10)
      add_tooltip(read_button1, "Import the first Excel file (database data)")

      read_button2 = tk.Button(button_frame, text="Read Excel File 2",
                                command=self.controller.read_excel_file,
                                width=30, height=2)
      read_button2.pack(pady=10)
      add_tooltip(read_button2, "Import the second Excel file (Medicaid data)")

      combine_button = tk.Button(button_frame, text="Combine Data",
                                  command=self.controller.combine_data,
                                  width=30, height=2)
      combine_button.pack(pady=10)
      add_tooltip(combine_button, "Merge the two imported Excel files into a combined dataset")

      upload_existing_button = tk.Button(button_frame, text="Load Existing File",
                                          command=self.controller.load_combined_data,
                                          width=30, height=2)
      upload_existing_button.pack(pady=10)
      add_tooltip(upload_existing_button, "Load a previously combined and saved data file")

      logging.info("MainView widgets created.")
      return self.root

