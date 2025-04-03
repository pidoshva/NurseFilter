import tkinter as tk
from tkinter import ttk
import threading
import logging
import time

class ProgressWindow:
    """
    A simple progress window that displays a progress bar during operations.
    """
    def __init__(self, parent, title="Operation in Progress"):
        """Initialize the progress window."""
        self.window = tk.Toplevel(parent)
        self.window.title(title)
        self.window.geometry("400x150")
        
        # Center the window
        self.window.update_idletasks()
        width = 400
        height = 150
        x = (self.window.winfo_screenwidth() // 2) - (width // 2)
        y = (self.window.winfo_screenheight() // 2) - (height // 2)
        self.window.geometry(f"{width}x{height}+{x}+{y}")
        
        # Make window stay on top
        self.window.attributes('-topmost', True)
        self.window.transient(parent)
        self.window.grab_set()
        
        # Variables
        self.progress_var = tk.DoubleVar(value=0)
        self.status_var = tk.StringVar(value="Processing...")
        
        # Create UI
        self._create_widgets()
        
        # Force update to ensure window is displayed
        self.window.update()
        
    def _create_widgets(self):
        """Create the UI components."""
        frame = ttk.Frame(self.window, padding="20")
        frame.pack(fill=tk.BOTH, expand=True)
        
        # Status label
        status_label = ttk.Label(frame, textvariable=self.status_var, font=("Arial", 12))
        status_label.pack(fill=tk.X, pady=(0, 15))
        
        # Progress bar
        self.progress_bar = ttk.Progressbar(
            frame, 
            orient="horizontal", 
            length=360,
            mode="determinate", 
            variable=self.progress_var
        )
        self.progress_bar.pack(fill=tk.X, pady=(0, 10))
    
    def update_progress(self, percent, message="Processing..."):
        """Update the progress display."""
        self.progress_var.set(percent)
        self.status_var.set(message)
        self.window.update_idletasks()
        self.window.update()
    
    def close(self):
        """Close the progress window."""
        if self.window:
            self.window.grab_release()
            self.window.destroy()

def show_progress_for_operation(parent, operation_func, title="Operation in Progress"):
    """
    Show a progress window while executing an operation.
    
    Args:
        parent: Parent window
        operation_func: Function that takes a progress callback
        title: Window title
        
    Returns:
        Result from the operation function
    """
    result = None
    progress_window = ProgressWindow(parent, title)
    
    def progress_callback(message, percent):
        """Callback for the operation to report progress."""
        # Only update if still open
        if progress_window and progress_window.window.winfo_exists():
            progress_window.update_progress(percent, message)
        return True  # Continue operation
    
    def run_operation():
        nonlocal result
        try:
            # Add slight delay to ensure window shows
            time.sleep(0.1)
            
            # Run the operation
            result = operation_func(progress_callback)
            
            # Set to 100% when done
            if progress_window and progress_window.window.winfo_exists():
                progress_window.update_progress(100, "Complete")
                time.sleep(0.5)  # Let user see completion
            
        except Exception as e:
            logging.error(f"Error during operation: {e}")
            if progress_window and progress_window.window.winfo_exists():
                progress_window.update_progress(100, "Error occurred")
                time.sleep(1)  # Let user see error state
        finally:
            # Close the window
            if progress_window and progress_window.window.winfo_exists():
                progress_window.window.after(0, progress_window.close)
    
    # Run operation in background thread
    thread = threading.Thread(target=run_operation)
    thread.daemon = True
    thread.start()
    
    # Wait for operation to complete (this is modal)
    parent.wait_window(progress_window.window)
    
    return result 