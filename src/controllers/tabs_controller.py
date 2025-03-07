from views.tabs_view import TabsView

class TabsController:
    def __init__(self, root):
        self.root = root
        self.view = TabsView(root)
        self.notebook_root = self.view.create_widgets()

    def get_tabs_root(self):
        return self.notebook_root

    def add_tab(self, tab_view, tab_name):
        """Add a new tab to the Notebook."""
        self.view.add_tab(tab_view, tab_name)

    def remove_tab(self, tab_view):
        """Remove a tab from the Notebook."""
        self.view.remove_tab(tab_view)

