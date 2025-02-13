from abc import ABC, abstractmethod
from models.data_model import DataModel

class Controller(ABC):
    '''Generic Controller class that all controllers should inherit from'''
    

    def __init__(self, model: DataModel ):
        '''Simple initializer inculding model callback'''
        self.model = model
        
    # @abstractmethod
    # def read_excel_file(self):
    #     '''
    #     Reads an Excel file.
    #     '''
    #     pass

    # @abstractmethod
    # def combine_data(self):
    #     '''
    #     Combines data from two Excel files.
    #     '''
    #     pass

    # @abstractmethod
    # def load_combined_data(self):
    #     '''
    #     Loads a combined data file.
    #     '''
    #     pass

    # @abstractmethod
    # def show_nurse_statistics(self):
    #     '''
    #     Shows nurse statistics.
    #     '''
    #     pass

    # @abstractmethod
    # def show_child_profile(self):
    #     '''
    #     Shows a child's profile.
    #     '''
    #     pass

    # @abstractmethod
    # def display_in_excel(self):
    #     '''
    #     Displays data in Excel.
    #     '''
    #     pass

    # @abstractmethod
    # def batch_assign_nurses(self):
    #     '''
    #     Assigns a nurse to multiple children.
    #     '''
    #     pass

    # @abstractmethod
    # def generate_report(self):
    #     '''
    #     Generates a report.
    #     '''
    #     pass

    # @abstractmethod
    # def view_unmatched_data(self):
    #     '''
    #     Views unmatched data.
    #     '''
    #     pass

    # @abstractmethod
    # def view_duplicate_data(self):
    #     '''
    #     Views duplicate data.
    #     '''
    #     pass

    # @abstractmethod
    # def assign_nurse(self):
    #     '''
    #     Assigns a nurse to a child.
    #     '''
    #     pass

    # @abstractmethod
    # def copy_to_clipboard(self):
    #     '''
    #     Copies data to the clipboard.
    #     '''
    #     pass

    # @abstractmethod
    # def export_profile_to_pdf(self):
    #     '''
    #     Exports a profile to PDF.
    #     '''
    #     pass
    