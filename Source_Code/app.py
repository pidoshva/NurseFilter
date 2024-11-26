import tkinter as tk
from controllers.main_controller import MainController

if __name__ == "__main__":
    root = tk.Tk()
    app = MainController(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()
