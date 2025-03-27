import tkinter as tk
from tkinter import ttk
import logging
from views.tooltip import add_tooltip

class InitialView(ttk.Frame):
    """
    Initial view of the application that allows users to load Excel files and combine data.
    """
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.files_loaded = 0  # Track number of files loaded
        logging.info("MainView initialized.")
        
        # Configure style
        self.style = ttk.Style()
        self._configure_styles()

    def _configure_styles(self):
        """Configure custom styles for widgets"""
        # Button styles
        self.style.configure("Action.TButton", 
                            font=("Arial", 12),
                            padding=10)
                            
        self.style.configure("Combine.TButton", 
                            font=("Arial", 12, "bold"),
                            padding=10)
                            
        # Progress frame style
        self.style.configure("Progress.TFrame", 
                            background="#f0f0f0",
                            relief="groove")

    def create_widgets(self):
        """Create and place widgets in the view."""
        # Main container with padding and background
        main_frame = ttk.Frame(self, padding="50 40 50 60")  # Increased bottom padding from 40 to 60
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title with icon-like prefix
        title_frame = ttk.Frame(main_frame)
        title_frame.pack(fill=tk.X, pady=(0, 25))
        
        # Diamond icon as a visual element
        title_icon = ttk.Label(title_frame, text="◆", font=("Arial", 20), foreground="#ff3b30")
        title_icon.pack(side=tk.LEFT, padx=(0, 10))
        
        title_label = ttk.Label(title_frame, text="Data Loading Center", font=("Arial", 18, "bold"))
        title_label.pack(side=tk.LEFT)
        
        # Separator
        sep = ttk.Separator(main_frame, orient="horizontal")
        sep.pack(fill=tk.X, pady=(0, 25))
        
        # File status frame - styled as a progress indicator
        status_frame = ttk.Frame(main_frame, style="Progress.TFrame", padding=15)
        status_frame.pack(fill=tk.X, pady=(0, 25))
        
        # File counter with visual indicator
        counter_frame = ttk.Frame(status_frame)
        counter_frame.pack(fill=tk.X)
        
        counter_label = ttk.Label(counter_frame, text="Files Ready:", font=("Arial", 12))
        counter_label.pack(side=tk.LEFT, padx=(0, 10))
        
        self.file_status = tk.StringVar(value="0/2")
        status_label = ttk.Label(counter_frame, textvariable=self.file_status, 
                               font=("Arial", 14, "bold"), foreground="#4a86e8")
        status_label.pack(side=tk.LEFT)
        
        # Add clear button next to file counter
        clear_files_btn = ttk.Button(counter_frame, text="✕", width=3, 
                                   command=self.clear_loaded_files)
        clear_files_btn.pack(side=tk.LEFT, padx=(5, 0))
        add_tooltip(clear_files_btn, "Clear all loaded files and start over")
        
        # Progress indicators
        indicator_frame = ttk.Frame(status_frame)
        indicator_frame.pack(fill=tk.X, pady=(10, 0))
        
        # Database file indicator
        self.db_indicator = ttk.Label(indicator_frame, text="○", font=("Arial", 16), foreground="#cccccc")
        self.db_indicator.pack(side=tk.LEFT, padx=(0, 5))
        db_label = ttk.Label(indicator_frame, text="Database", font=("Arial", 11))
        db_label.pack(side=tk.LEFT, padx=(0, 20))
        
        # Medicaid file indicator
        self.med_indicator = ttk.Label(indicator_frame, text="○", font=("Arial", 16), foreground="#cccccc")
        self.med_indicator.pack(side=tk.LEFT, padx=(0, 5))
        med_label = ttk.Label(indicator_frame, text="Medicaid", font=("Arial", 11))
        med_label.pack(side=tk.LEFT)
        
        # Button frame
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=(0, 15))
        
        # Load file button with custom style
        load_btn = ttk.Button(button_frame, text="Load Excel File", 
                             command=self.load_file, style="Action.TButton")
        load_btn.pack(fill=tk.X, pady=(0, 15), ipady=5)
        add_tooltip(load_btn, "Click to select and load an Excel file (database or Medicaid)")
        
        # Combine data button (initially disabled) with custom style
        self.combine_btn = ttk.Button(button_frame, text="Combine Data", 
                                     command=self.combine_data, 
                                     state="disabled",
                                     style="Combine.TButton")
        self.combine_btn.pack(fill=tk.X, pady=(0, 15), ipady=5)
        add_tooltip(self.combine_btn, "Merge the database and Medicaid data")
        
        # Load existing file button
        load_existing_btn = ttk.Button(button_frame, text="Load Existing Combined File", 
                                      command=self.load_existing_file,
                                      style="Action.TButton")
        load_existing_btn.pack(fill=tk.X, ipady=5)
        add_tooltip(load_existing_btn, "Load a previously combined data file")
        
        # Instructions panel
        instruction_frame = ttk.Frame(main_frame, padding="15 15 15 25")  # Increased bottom padding from 15 to 25
        instruction_frame.pack(fill=tk.X, pady=(15, 0))
        
        instruction_title = ttk.Label(instruction_frame, text="Instructions:", 
                                    font=("Arial", 12, "bold"))
        instruction_title.pack(anchor="w", pady=(0, 5))
        
        instructions = ttk.Label(instruction_frame, 
                               text="1. Load the database Excel file first\n" +
                                    "2. Load the Medicaid Excel file next\n" +
                                    "3. Click 'Combine Data' when both files are loaded\n\n" +
                                    "Or use 'Load Existing Combined File' if you have\n" +
                                    "previously combined data to work with.",
                               font=("Arial", 11),
                               justify="left",
                               wraplength=450)  # Added wraplength to ensure text doesn't get cut off
        instructions.pack(anchor="w", pady=(0, 10))  # Added bottom padding to the label itself
        
        logging.info("MainView widgets created.")
        return self
        
    def load_file(self):
        """Handle the load file button click."""
        # Call the controller to read the Excel file
        result = self.controller.read_excel_file()
        
        # Update file counter if file was successfully loaded
        if hasattr(self.controller.model, 'data_frames') and len(self.controller.model.data_frames) > self.files_loaded:
            self.files_loaded = len(self.controller.model.data_frames)
            self.file_status.set(f"{self.files_loaded}/2")
            
            # Update indicators based on file types
            if hasattr(self.controller.model, 'file_types'):
                # Reset indicators
                self.db_indicator.config(text="○", foreground="#cccccc")
                self.med_indicator.config(text="○", foreground="#cccccc")
                
                # Mark appropriate indicators based on loaded file types
                for file_type in self.controller.model.file_types:
                    if file_type == "Database":
                        self.db_indicator.config(text="●", foreground="#4CAF50")  # Green filled circle
                    elif file_type == "Medicaid":
                        self.med_indicator.config(text="●", foreground="#4CAF50")  # Green filled circle
                
                # Enable combine button if both types loaded
                if "Database" in self.controller.model.file_types and "Medicaid" in self.controller.model.file_types:
                    self.combine_btn.config(state="normal")
            # Fallback to old behavior if file_types not available
            else:
                if self.files_loaded >= 1:
                    self.db_indicator.config(text="●", foreground="#4CAF50")  # Green filled circle
                    
                if self.files_loaded >= 2:
                    self.med_indicator.config(text="●", foreground="#4CAF50")  # Green filled circle
                    self.combine_btn.config(state="normal")
        
    def combine_data(self):
        """Handle the combine data button click."""
        self.controller.combine_data()
        
    def load_existing_file(self):
        """Handle the load existing file button click."""
        self.controller.load_existing_combined_data()

    def clear_loaded_files(self):
        """Clear all loaded files and reset indicators."""
        # Ask the controller to clear data frames
        self.controller.clear_loaded_files()
        
        # Reset UI elements
        self.files_loaded = 0
        self.file_status.set("0/2")
        
        # Reset indicators
        self.db_indicator.config(text="○", foreground="#cccccc")
        self.med_indicator.config(text="○", foreground="#cccccc")
        
        # Disable combine button
        self.combine_btn.config(state="disabled")

