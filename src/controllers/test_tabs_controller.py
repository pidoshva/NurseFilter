import unittest
from unittest.mock import MagicMock
from tkinter import Tk
from tabs_controller import TabsController
from views.tabs_view import TabsView

class TestTabsController(unittest.TestCase):

    def setUp(self):
        self.root = Tk()
        self.controller = TabsController(self.root)

    def test_get_tabs_root(self):
        result = self.controller.get_tabs_root()
        self.assertIsNotNone(result)

    def test_add_tab(self):
        tab_view = MagicMock()
        tab_name = "Test Tab"
        self.controller.add_tab(tab_view, tab_name)
        self.controller.view.add_tab.assert_called_once_with(tab_view, tab_name)

    def test_remove_tab(self):
        tab_view = MagicMock()
        self.controller.remove_tab(tab_view)
        self.controller.view.remove_tab.assert_called_once_with(tab_view)

if __name__ == '__main__':
    unittest.main()
