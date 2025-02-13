from abc import ABC, abstractmethod
from tkinter import Tk
from controllers.controller import Controller 

class View(ABC):
    '''Generic View class that all views should inherit from'''

    def __init__(self, root: Tk , controller: Controller):
        '''Simple initializer inculding controller callback and window root'''
        self.root = root
        self.controller = controller
        
    @abstractmethod
    def create_view(self, data):
        '''
        Creates a window/view.
        Typically this method will create widgets and place them in the window.
        '''
        pass

    # @abstractmethod
    # def update_table(self, data):
    #     '''
    #     Updates a table.
    #     '''
    #     pass

    # @abstractmethod
    # def get_selected_child_data(self):
    #     '''
    #     Gets the selected child's data.
    #     '''
    #     pass
