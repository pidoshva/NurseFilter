import tkinter as tk

class Tooltip:
    """
    Creates a tooltip for a given widget.
    
    Parameters:
        widget: The widget to add the tooltip to
        text: The text to display in the tooltip
        delay: Delay in milliseconds before the tooltip appears (default: 500)
        wrap_length: Maximum line length for wrapped text (default: 250)
        background: Background color of the tooltip (default: light yellow)
        padding: Padding around the tooltip text (default: 5 pixels)
    """
    def __init__(self, widget, text, delay=500, wrap_length=250,
                 background="#FFFFDD", padding=5):
        self.widget = widget
        self.text = text
        self.delay = delay
        self.wrap_length = wrap_length
        self.background = background
        self.padding = padding
        self.tooltip_window = None
        self.id = None
        
        # Bind events
        widget.bind("<Enter>", self.on_enter)
        widget.bind("<Leave>", self.on_leave)
        widget.bind("<Motion>", self.on_motion, add="+")
        widget.bind("<ButtonPress>", self.on_leave)
    
    def on_enter(self, event=None):
        # Schedule tooltip to appear after delay
        self.id = self.widget.after(self.delay, self.show_tooltip)
    
    def on_leave(self, event=None):
        # Cancel scheduled tooltip or hide if showing
        if self.id:
            self.widget.after_cancel(self.id)
            self.id = None
        self.hide_tooltip()
    
    def on_motion(self, event=None):
        # Update tooltip position when mouse moves
        if self.tooltip_window:
            x, y = self.calculate_position(event)
            self.tooltip_window.wm_geometry(f"+{x}+{y}")
    
    def show_tooltip(self):
        # Display the tooltip
        self.tooltip_window = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(True)  # No window decorations
        
        # Position tooltip near the cursor
        x, y = self.calculate_position()
        tw.wm_geometry(f"+{x}+{y}")
        
        # Create tooltip content
        label = tk.Label(tw, text=self.text, justify=tk.LEFT,
                         background=self.background, relief="solid", borderwidth=1,
                         wraplength=self.wrap_length, padx=self.padding, pady=self.padding)
        label.pack()
    
    def hide_tooltip(self):
        # Destroy the tooltip window if it exists
        if self.tooltip_window:
            self.tooltip_window.destroy()
            self.tooltip_window = None
    
    def calculate_position(self, event=None):
        # Calculate tooltip position based on mouse or widget position
        if event:  # Position near cursor if event provided
            x = event.x_root + 15
            y = event.y_root + 10
        else:  # Otherwise position near widget
            x = self.widget.winfo_rootx() + self.widget.winfo_width() + 5
            y = self.widget.winfo_rooty() + 5
        return x, y

def add_tooltip(widget, text):
    """
    Convenience function to add a tooltip to a widget
    
    Parameters:
        widget: The widget to add the tooltip to
        text: The text to display in the tooltip
    """
    return Tooltip(widget, text) 