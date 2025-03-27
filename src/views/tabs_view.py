from tkinter import ttk
import tkinter as tk
from PIL import Image, ImageTk
import os

import logging


class TabsView:
    def __init__(self, root):
        self.root = root
        self.tab_count = 0
        self.notebook = None

    def create_widgets(self):
        self.root.deiconify()
        self.root.title("NurseFilter")
        self.root.geometry("1200x700")
        
        # Set application icon - with improved quality
        try:
            icon_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets", "nursefilter_icon.png")
            
            # Load at larger size and with antialiasing for better quality
            original_image = Image.open(icon_path)
            
            # Create multiple sizes for different resolutions
            icons = []
            for size in (16, 32, 48, 64, 128):
                resized_img = original_image.resize((size, size), Image.Resampling.LANCZOS)
                icons.append(ImageTk.PhotoImage(resized_img))
            
            # Set all sizes as icon
            self.root.iconphoto(True, *icons)
            
            # Keep reference to prevent garbage collection
            self.icon_images = icons
            
        except Exception as e:
            print(f"Could not set icon: {e}")
            
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
        try:
            # Check if the tab is actually in the notebook
            if tab_view in self.notebook.winfo_children():
                self.notebook.forget(tab_view)
                tab_view.destroy()
                self.tab_count -= 1
            else:
                logging.warning(f"Tab not found in notebook when attempting to remove")
        except Exception as e:
            logging.warning(f"Error removing tab: {e}")
            # Still try to destroy the widget if possible
            try:
                if tab_view and tab_view.winfo_exists():
                    tab_view.destroy()
            except:
                pass