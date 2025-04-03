import logging
import tkinter as tk
from tkinter import messagebox, filedialog
from views.initial_view import InitialView
from views.progress_view import show_progress_for_operation
import os


class InitialController:
    """
    The main controller for the application.
    Wires up the Model (DataModel) and the Views (InitialView, CombinedDataView, ProfileView, etc.).
    """

    def __init__(self, root, model, main_controller):
        self.root = root
        self.model = model 
        self.main_controller = main_controller
        self.view = None
        logging.info("InitialController initialized.")

    def show_initial_view(self):
        view = InitialView(self.root, self).create_widgets()
        self.main_controller.add_tab(view, "Data Loader")
        self.view = view
        return view

    # 1. Reading Excel Files
    def read_excel_file(self):
        logging.info("Selecting Excel file...")
        
        filepath = filedialog.askopenfilename(
            initialdir=os.getcwd(),
            filetypes=[("Excel files", "*.xlsx *.xls")]
        )
        if not filepath:
            return None
            
        # Determine file type based on filename
        filename = os.path.basename(filepath).lower()
        
        # Check if filename contains medicaid or database
        is_medicaid = 'medicaid' in filename
        is_database = 'database' in filename
        
        # If neither is in the name, follow default order
        if not is_medicaid and not is_database:
            # Default assignment based on current loaded files
            if not self.model.data_frames or 'database' in self.model.data_frames:
                file_type = "Database"
            else:
                file_type = "Medicaid"
        else:
            # Explicit type based on filename
            file_type = "Medicaid" if is_medicaid else "Database"
        
        # Check which position this file is (1st or 2nd)
        file_num = len(self.model.data_frames) + 1
            
        # Define an operation that reports progress
        def file_loading_operation(progress_callback):
            # Start progress
            progress_callback(f"Loading {file_type} file ({file_num}/2)", 10)
            
            # Decrypt if needed
            if self.model.is_file_encrypted(filepath):
                progress_callback(f"Decrypting {file_type} file", 30)
                if not self.model.decrypt_file(filepath):
                    return None
                    
            # Read the file
            progress_callback(f"Reading {file_type} data", 50)
            result = self.model.read_excel_file(filepath, file_type=file_type)
            
            # Re-encrypt
            try:
                progress_callback(f"Securing {file_type} file", 90)
                self.model.encrypt_file(filepath)
            except Exception as e:
                logging.warning(f"Error re-encrypting file: {e}")
                messagebox.showwarning("Warning", "Error re-encrypting file.")
                
            progress_callback(f"{file_type} file loaded successfully", 100)
            return result
        
        # Show progress window while loading file
        result = show_progress_for_operation(self.root, file_loading_operation, f"Loading {file_type} File ({file_num}/2)")
        return result

    # 2. Combining Data
    def combine_data(self):
        # Define operation with progress updates
        def combination_operation(progress_callback):
            # Check if we have enough files
            if len(self.model.data_frames) < 2:
                progress_callback("Need both files to combine", 100)
                messagebox.showerror("Error", "Please load both database and Medicaid files before combining.")
                return False
                
            # Start progress
            progress_callback("Preparing to combine data", 10)
            progress_callback("Normalizing column names", 20)
            progress_callback("Processing dates and IDs", 30)
            progress_callback("Merging database and Medicaid data", 50)
            
            # Combine data
            success = self.model.combine_data()
            
            if success:
                progress_callback("Data combined successfully", 80)
                progress_callback("Checking for duplicates and unmatched records", 85)
                progress_callback("Processing combined data", 90)
                
                # Load combined data
                progress_callback("Loading combined data", 95)
                loaded = self.model.load_combined_data()
                
                if loaded:
                    # Show combined data view
                    progress_callback("Preparing data view", 98)
                    self.main_controller.show_combined_data()
                    
                    # Remove tab when done
                    try:
                        self.main_controller.remove_tab(self.view)
                    except Exception as e:
                        logging.error(f"Error removing tab: {e}")
                    
                progress_callback("Combination complete", 100)
                
            return success
            
        # Show progress window
        result = show_progress_for_operation(
            self.root, 
            combination_operation, 
            "Combining Database & Medicaid Data"
        )
        return result

    # Method to load existing combined data file
    def load_existing_combined_data(self):
        """Load an existing combined data file."""
        # Define operation with progress updates
        def loading_operation(progress_callback):
            # Start progress
            progress_callback("Checking for combined data file", 10)
            
            # Load combined data 
            progress_callback("Loading combined data", 40)
            success = self.model.load_combined_data()
            
            if success:
                progress_callback("Preparing data view", 80)
                
                # Show combined data view
                self.main_controller.show_combined_data()
                
                # Remove tab when done
                try:
                    progress_callback("Finalizing", 95)
                    self.main_controller.remove_tab(self.view)
                except Exception as e:
                    logging.error(f"Error removing tab: {e}")
                    
                progress_callback("Complete", 100)
            else:
                progress_callback("Failed to load combined data", 100)
                
            return success
        
        # Show progress window
        result = show_progress_for_operation(
            self.root, 
            loading_operation, 
            "Loading Combined Data File"
        )
        return result
        
    def clear_loaded_files(self):
        """Clear all loaded data frames from the model."""
        # Reset data frames and file types
        if hasattr(self.model, 'data_frames'):
            self.model.data_frames = []
        
        if hasattr(self.model, 'file_types'):
            self.model.file_types = []
            
        logging.info("Cleared all loaded files from the model")
