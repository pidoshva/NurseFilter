import tkinter as tk
import logging
from views.view_constants import ViewStyles

class MainView:
    """
    The initial (main) window with 4 buttons:
      - Read Excel File 1
      - Read Excel File 2
      - Combine Data
      - Load Existing File
    """

    def __init__(self, root, controller):
        self.root: tk.Tk = root
        self.controller = controller
        self.root.title("Excel Combiner (MVC)")
        self.create_widgets()
        logging.info("MainView initialized.")

    def create_widgets(self):
        self.root.geometry(f"{ViewStyles.MV_WINDOW_WIDTH}x{ViewStyles.MV_WINDOW_HEIGHT}")
        self.root.minsize(ViewStyles.MV_WINDOW_WIDTH, ViewStyles.MV_WINDOW_HEIGHT)
        self.root.configure(bg=ViewStyles.WINDOW_COLOR)

        button_frame = tk.Frame(self.root, padx=20, pady=20, bg=ViewStyles.WINDOW_FRAME_COLOR)
        button_frame.pack(expand=True)

        read_button1 = tk.Button(button_frame, text="Read Excel File 1",
                                 command=self.controller.read_excel_file,
                                 width=30, height=2, bg=ViewStyles.WINDOW_BUTTON_COLOR)
        read_button1.pack(pady=10)

        read_button2 = tk.Button(button_frame, text="Read Excel File 2",
                                 command=self.controller.read_excel_file,
                                 width=30, height=2, bg=ViewStyles.WINDOW_BUTTON_COLOR)
        read_button2.pack(pady=10)

        combine_button = tk.Button(button_frame, text="Combine Data",
                                   command=self.controller.combine_data,
                                   width=30, height=2,  bg=ViewStyles.WINDOW_BUTTON_COLOR)
        combine_button.pack(pady=10)

        upload_existing_button = tk.Button(button_frame, text="Load Existing File",
                                           command=self.controller.load_combined_data,
                                           width=30, height=2, bg=ViewStyles.WINDOW_BUTTON_COLOR)
        upload_existing_button.pack(pady=10)

        logging.info("MainView widgets created.")
