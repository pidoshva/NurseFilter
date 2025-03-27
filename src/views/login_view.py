import tkinter as tk
import logging
from tkinter import font as tkfont
from PIL import Image, ImageTk
import os

class LoginView:
    """
    The login window with 2 text fields and 2 buttons:
      - Username
      - Password
      - Log In
      - Forgot Password
    """
    def __init__(self, root, controller):
        # Create the main view frame
        self.view = tk.Frame(root, bg="#ffffff")
        self.controller = controller
        self.style_config()
        self.load_assets()
        logging.info("LoginView initialized.")
        
    def load_assets(self):
        """Load icons and images needed for the view"""
        try:
            # Try to find the icon in several possible locations
            icon_paths = [
                "nursefilter_icon.png",
                "assets/nursefilter_icon.png",
                "src/assets/nursefilter_icon.png",
                "../assets/nursefilter_icon.png",
            ]
            
            for path in icon_paths:
                if os.path.exists(path):
                    # Load the nurse filter icon
                    icon_image = Image.open(path)
                    # Resize the image to fit our header
                    icon_image = icon_image.resize((60, 60), Image.LANCZOS)
                    self.icon = ImageTk.PhotoImage(icon_image)
                    logging.info(f"Loaded icon from {path}")
                    break
            else:
                # If icon not found, we'll create a fallback
                logging.warning("Icon not found - will use a placeholder")
                self.icon = None
        except Exception as e:
            logging.error(f"Error loading assets: {e}")
            self.icon = None

    def style_config(self):
        """Configure fonts and styles for the view"""
        # Medical/healthcare style fonts
        self.title_font = tkfont.Font(family="Arial", size=20, weight="bold")
        self.label_font = tkfont.Font(family="Arial", size=11)
        self.button_font = tkfont.Font(family="Arial", size=11, weight="bold")
        self.small_font = tkfont.Font(family="Arial", size=9)
        
        # Color scheme based on the nurse filter icon
        self.bg_color = "#ffffff"  # White background
        self.primary_color = "#d8e6ed"  # Light blue-gray (nurse hat background)
        self.accent_color = "#ff3b30"   # Red (cross color)
        self.text_color = "#000000"     # Black text
        self.light_gray = "#f0f5f7"     # Very light blue-gray for form background
        self.border_color = "#000000"   # Black borders like in the icon
        self.success_color = "#34c759"  # Green for success messages
        
        # Input styling
        self.input_bg = "#ffffff"
        self.input_border = "#b8c8d1"
        self.input_focus_border = "#7fb2c9"
        
        # Hover colors
        self.button_hover_color = "#c52b21"  # Darker red for hover
        self.link_hover_color = "#0071bc"    # Medical blue for links

    def login_button(self):
        username = self.entry_username.get()
        password = self.entry_password.get()

        self.controller.login(username, password)

    def forgot_password(self):
        # Placeholder for forgot password functionality
        logging.info("Forgot password requested")
        # self.controller.forgot_password()
    
    def _on_enter_button(self, event, button, original_color, hover_color):
        """Handle mouse enter event for buttons"""
        button.config(bg=hover_color)
    
    def _on_leave_button(self, event, button, original_color):
        """Handle mouse leave event for buttons"""
        button.config(bg=original_color)
    
    def _on_enter_link(self, event, link, hover_color):
        """Handle mouse enter event for links"""
        link.config(fg=hover_color)
        link.config(cursor="hand2")
    
    def _on_leave_link(self, event, link, original_color):
        """Handle mouse leave event for links"""
        link.config(fg=original_color)
    
    def _on_focus_in(self, event, entry):
        """Handle focus in event for entry fields"""
        entry.config(highlightbackground=self.input_focus_border, highlightcolor=self.input_focus_border)
    
    def _on_focus_out(self, event, entry):
        """Handle focus out event for entry fields"""
        entry.config(highlightbackground=self.input_border, highlightcolor=self.input_border)

    def create_widgets(self):
        # First make sure we clear any existing content
        for widget in self.view.winfo_children():
            widget.destroy()
            
        # Simple approach: make the main frame fill the window
        self.view.pack(fill=tk.BOTH, expand=True)
        
        # Create a fixed-size login frame that will be centered
        login_frame = tk.Frame(self.view, bg=self.bg_color, width=400, height=500)
        login_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        
        # Make sure the frame stays the fixed size
        login_frame.pack_propagate(0)
        
        # Header with logo and title
        header_frame = tk.Frame(login_frame, bg=self.bg_color)
        header_frame.pack(pady=(20, 30))
        
        # Use the nurse filter icon
        if self.icon:
            logo_label = tk.Label(header_frame, image=self.icon, bg=self.bg_color)
            logo_label.pack(side=tk.LEFT)
        else:
            # Fallback - create a custom medical icon with canvas
            logo_canvas = tk.Canvas(header_frame, width=60, height=60, bg=self.bg_color, 
                                    highlightthickness=0)
            # Draw nurse cap shape
            logo_canvas.create_arc(5, 5, 55, 55, fill=self.primary_color, outline=self.border_color, 
                                  start=0, extent=180, width=2)
            # Draw red cross
            logo_canvas.create_rectangle(25, 15, 35, 45, fill=self.accent_color, outline=self.border_color, width=2)
            logo_canvas.create_rectangle(15, 25, 45, 35, fill=self.accent_color, outline=self.border_color, width=2)
            logo_canvas.pack(side=tk.LEFT)
        
        # Title label - healthcare style
        title_label = tk.Label(
            header_frame, 
            text="NurseFilter", 
            font=self.title_font, 
            bg=self.bg_color,
            fg=self.text_color,
            padx=15
        )
        title_label.pack(side=tk.LEFT)
        
        # Create the login form with a light blue-gray background
        form_container = tk.Frame(
            login_frame, 
            bg=self.light_gray,
            highlightbackground=self.border_color,
            highlightthickness=1
        )
        form_container.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)
        
        # Login instruction text
        instructions_label = tk.Label(
            form_container,
            text="Please log in to access your account",
            font=self.label_font,
            bg=self.light_gray,
            fg=self.text_color,
        )
        instructions_label.pack(pady=(20, 15))
        
        # Username field
        username_label = tk.Label(
            form_container, 
            text="Username", 
            font=self.label_font,
            bg=self.light_gray,
            fg=self.text_color,
            anchor="w"
        )
        username_label.pack(fill=tk.X, padx=30, pady=(5, 5))
        
        self.entry_username = tk.Entry(
            form_container, 
            font=self.label_font,
            bg=self.input_bg,
            fg=self.text_color,
            relief=tk.SOLID,
            bd=1,
            highlightthickness=1,
            highlightbackground=self.input_border
        )
        self.entry_username.pack(fill=tk.X, padx=30, ipady=8)
        
        # Bind focus events
        self.entry_username.bind("<FocusIn>", lambda event: self._on_focus_in(event, self.entry_username))
        self.entry_username.bind("<FocusOut>", lambda event: self._on_focus_out(event, self.entry_username))
        
        # Password field
        password_label = tk.Label(
            form_container, 
            text="Password", 
            font=self.label_font,
            bg=self.light_gray,
            fg=self.text_color,
            anchor="w"
        )
        password_label.pack(fill=tk.X, padx=30, pady=(15, 5))
        
        self.entry_password = tk.Entry(
            form_container, 
            show="*", 
            font=self.label_font,
            bg=self.input_bg,
            fg=self.text_color,
            relief=tk.SOLID,
            bd=1,
            highlightthickness=1,
            highlightbackground=self.input_border
        )
        self.entry_password.pack(fill=tk.X, padx=30, ipady=8)
        
        # Bind focus events
        self.entry_password.bind("<FocusIn>", lambda event: self._on_focus_in(event, self.entry_password))
        self.entry_password.bind("<FocusOut>", lambda event: self._on_focus_out(event, self.entry_password))
        
        # Login button - use accent red color from the medical cross
        login_button = tk.Button(
            form_container, 
            text="LOGIN", 
            command=self.login_button,
            bg=self.accent_color,
            fg="white",
            font=self.button_font,
            padx=10,
            pady=10,
            relief=tk.FLAT,
            borderwidth=0,
            activebackground=self.button_hover_color,
            activeforeground="white",
            cursor="hand2"
        )
        login_button.pack(fill=tk.X, padx=30, pady=(25, 15))
        
        # Add hover effect
        login_button.bind("<Enter>", lambda event: self._on_enter_button(event, login_button, self.accent_color, self.button_hover_color))
        login_button.bind("<Leave>", lambda event: self._on_leave_button(event, login_button, self.accent_color))
        
        # Forgot password link - medical blue for links
        forgot_link = tk.Label(
            form_container, 
            text="Forgot your password?", 
            font=self.small_font,
            bg=self.light_gray,
            fg="#0071bc",  # Medical blue
            cursor="hand2"
        )
        forgot_link.pack(pady=(0, 25))
        forgot_link.bind("<Button-1>", lambda event: self.forgot_password())
        
        # Add hover effect to the link
        forgot_link.bind("<Enter>", lambda event: self._on_enter_link(event, forgot_link, self.link_hover_color))
        forgot_link.bind("<Leave>", lambda event: self._on_leave_link(event, forgot_link, "#0071bc"))
        
        # Footer
        footer_label = tk.Label(
            login_frame,
            text="© 2023 NurseFilter. All rights reserved.",
            font=self.small_font,
            bg=self.bg_color,
            fg="#95a5a6"
        )
        footer_label.pack(pady=10)
        
        # Bind Enter key to login button
        self.entry_password.bind("<Return>", lambda event: self.login_button())
        self.entry_username.bind("<Return>", lambda event: self.entry_password.focus_set())
        
        return self.view
