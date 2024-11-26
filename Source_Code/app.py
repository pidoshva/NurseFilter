# app.py
import sys
sys.dont_write_bytecode = True
import logging
import tkinter as tk
from controllers.main_controller import MainController

# Configure logging to output to the terminal
logging.basicConfig(
    level=logging.INFO,  # Use INFO or DEBUG level as needed
    format='%(asctime)s - %(levelname)s - %(message)s'
)

if __name__ == "__main__":
    root = tk.Tk()
    app = MainController(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()
