import tkinter as tk
import logging

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
      self.create_widgets()
      logging.info("MainView initialized.")

  def create_widgets(self):
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

  def get_view(self):
    return self.root
