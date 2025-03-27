import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import pandas as pd
from tkinter import font as tkfont
from views.tooltip import add_tooltip
from PIL import Image, ImageTk
import os
import platform
from datetime import datetime


class ProfileView:
    def __init__(self, root, controller, child_data):
        self.root = root
        self.controller = controller
        self.child_data = child_data
        self.view = None
        
        # Style configuration
        self.style_config()
        self.load_assets()

        # We'll store text versions so we can copy/export them
        self.mother_info_text = ""
        self.child_info_text = ""
        self.address_info_text = ""
        self.nurse_info_text = ""
        
    def style_config(self):
        """Configure fonts and styles for the view"""
        # Medical/healthcare style fonts
        self.title_font = tkfont.Font(family="Arial", size=18, weight="bold")
        self.section_font = tkfont.Font(family="Arial", size=14, weight="bold")
        self.label_font = tkfont.Font(family="Arial", size=12)
        self.button_font = tkfont.Font(family="Arial", size=11, weight="bold")
        
        # Color scheme based on the nurse filter icon
        self.bg_color = "#ffffff"         # White background
        self.primary_color = "#d8e6ed"    # Light blue-gray (nurse hat background)
        self.accent_color = "#ff3b30"     # Red (cross color)
        self.text_color = "#2c3e50"       # Dark blue-gray for text
        self.light_gray = "#f0f5f7"       # Very light blue-gray for form background
        self.border_color = "#000000"     # Black borders like in the icon
        self.success_color = "#34c759"    # Green for success messages
        self.section_bg = "#f0f5f7"       # Section background
        self.button_hover_color = "#c52b21"  # Darker red for hover
        
    def load_assets(self):
        """Load icons and images needed for the view"""
        try:
            # Try to find the icon in several possible locations
            icon_paths = [
                "baby_icon.png",
                "assets/baby_icon.png",
                "src/assets/baby_icon.png",
                "../assets/baby_icon.png",
            ]
            
            for path in icon_paths:
                if os.path.exists(path):
                    # Load the nurse filter icon
                    icon_image = Image.open(path)
                    # Resize the image to fit our header
                    icon_image = icon_image.resize((40, 40), Image.LANCZOS)
                    self.icon = ImageTk.PhotoImage(icon_image)
                    break
            else:
                self.icon = None
        except Exception as e:
            self.icon = None
            
    def _on_enter_button(self, event, button, original_color, hover_color):
        """Handle mouse enter event for buttons"""
        button.config(bg=hover_color)
    
    def _on_leave_button(self, event, button, original_color):
        """Handle mouse leave event for buttons"""
        button.config(bg=original_color)
        
    def _on_mousewheel(self, event, canvas):
        """Handle mouse wheel scrolling"""
        # Cross-platform scroll handling
        if platform.system() == "Windows":
            # For Windows
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        elif platform.system() == "Darwin":
            # For macOS
            canvas.yview_scroll(int(-1 * event.delta), "units")
        else:
            # For Linux and other Unix systems
            if event.num == 4:
                canvas.yview_scroll(-1, "units")
            elif event.num == 5:
                canvas.yview_scroll(1, "units")

    def get_frame(self):
        return self.view

    def get_title(self):
        first = self.child_data.get('Child_First_Name','')
        last = self.child_data.get('Child_Last_Name','')
        return f"{first} {last} Profile"

    def create_widgets(self):
        # Main view frame
        self.view = tk.Frame(self.root, bg=self.bg_color)
        self.view.pack(fill=tk.BOTH, expand=True)
        self.view.grid_rowconfigure(0, weight=1)  # Content area expands
        self.view.grid_rowconfigure(1, weight=0)  # Button area fixed height
        self.view.grid_columnconfigure(0, weight=1)  # Full width
        
        first = self.child_data.get('Child_First_Name','')
        last = self.child_data.get('Child_Last_Name','')

        # === Create a scrollable content frame ===
        # Canvas for scrolling
        content_canvas = tk.Canvas(self.view, bg=self.bg_color, highlightthickness=0)
        content_canvas.grid(row=0, column=0, sticky="nsew")
        
        # Add scrollbar
        scrollbar = tk.Scrollbar(self.view, orient="vertical", command=content_canvas.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")
        content_canvas.configure(yscrollcommand=scrollbar.set)
        
        # Frame inside canvas that will hold all content
        content_frame = tk.Frame(content_canvas, bg=self.bg_color, padx=20, pady=20)
        canvas_frame = content_canvas.create_window((0, 0), window=content_frame, anchor="nw")
        
        # Make the content frame expand to the width of the canvas
        def configure_frame(event):
            # Update the width of the canvas window to fill canvas
            content_canvas.itemconfig(canvas_frame, width=event.width)
            # Update the scroll region to include the entire frame
            content_canvas.configure(scrollregion=content_canvas.bbox("all"))
            
        content_canvas.bind('<Configure>', configure_frame)
        content_frame.bind('<Configure>', lambda e: content_canvas.configure(scrollregion=content_canvas.bbox("all")))
        
        # Bind mouse wheel for scrolling
        # Windows and macOS
        self.view.bind("<MouseWheel>", lambda event: self._on_mousewheel(event, content_canvas))
        content_canvas.bind("<MouseWheel>", lambda event: self._on_mousewheel(event, content_canvas))
        content_frame.bind("<MouseWheel>", lambda event: self._on_mousewheel(event, content_canvas))
        
        # Linux scrolling
        self.view.bind("<Button-4>", lambda event: self._on_mousewheel(event, content_canvas))
        self.view.bind("<Button-5>", lambda event: self._on_mousewheel(event, content_canvas))
        content_canvas.bind("<Button-4>", lambda event: self._on_mousewheel(event, content_canvas))
        content_canvas.bind("<Button-5>", lambda event: self._on_mousewheel(event, content_canvas))
        content_frame.bind("<Button-4>", lambda event: self._on_mousewheel(event, content_canvas))
        content_frame.bind("<Button-5>", lambda event: self._on_mousewheel(event, content_canvas))
        
        # Header with patient name and icon
        header_frame = tk.Frame(content_frame, bg=self.bg_color)
        header_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Profile icon/logo
        if self.icon:
            logo_label = tk.Label(header_frame, image=self.icon, bg=self.bg_color)
            logo_label.pack(side=tk.LEFT, padx=(0, 15))
            
        # Patient name header
        patient_header = tk.Label(
            header_frame, 
            text=f"{first} {last}'s Profile", 
            font=self.title_font, 
            bg=self.bg_color, 
            fg=self.text_color
        )
        patient_header.pack(side=tk.LEFT)
        
        # Create main content area
        main_content = tk.Frame(content_frame, bg=self.bg_color)
        main_content.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Configure grid layout for responsive sections
        main_content.columnconfigure(0, weight=1)
        main_content.columnconfigure(1, weight=1)
        
        # Mother's Info Section
        mother_section = self.create_section_frame(main_content)
        mother_section.grid(row=0, column=0, sticky="nsew", padx=(0, 10), pady=(0, 10))
        
        mother_header = tk.Label(
            mother_section, 
            text="Mother's Information", 
            font=self.section_font, 
            bg=self.section_bg, 
            fg=self.text_color,
            anchor='w'
        )
        mother_header.pack(fill=tk.X, pady=(10, 10), padx=15)
        add_tooltip(mother_header, "Information about the child's mother")
        
        separator1 = tk.Frame(mother_section, height=2, bg=self.primary_color)
        separator1.pack(fill=tk.X, padx=10)
        
        self.mother_info_text = (
            f"Mother ID: {self.child_data.get('Mother_ID','')}\n"
            f"First Name: {self.child_data.get('Mother_First_Name','')}\n"
            f"Last Name: {self.child_data.get('Mother_Last_Name','')}\n"
        )
        mother_info = tk.Label(
            mother_section, 
            text=self.mother_info_text, 
            anchor='w', 
            justify=tk.LEFT, 
            font=self.label_font,
            bg=self.section_bg,
            fg=self.text_color,
            padx=15
        )
        mother_info.pack(fill=tk.X, pady=(10, 15))
        add_tooltip(mother_info, "Unique identifier and name details of the mother")

        # Child's Info Section
        child_section = self.create_section_frame(main_content)
        child_section.grid(row=0, column=1, sticky="nsew", padx=(10, 0), pady=(0, 10))
        
        child_header = tk.Label(
            child_section, 
            text="Child's Information", 
            font=self.section_font, 
            bg=self.section_bg, 
            fg=self.text_color,
            anchor='w'
        )
        child_header.pack(fill=tk.X, pady=(10, 10), padx=15)
        add_tooltip(child_header, "Personal information about the child")
        
        separator2 = tk.Frame(child_section, height=2, bg=self.primary_color)
        separator2.pack(fill=tk.X, padx=10)
        
        dob = self.child_data.get('Child_Date_of_Birth','')
        self.child_info_text = (
            f"First Name: {self.child_data.get('Child_First_Name','')}\n"
            f"Last Name: {self.child_data.get('Child_Last_Name','')}\n"
            f"Date of Birth: {self.child_data.get('Child_Date_of_Birth','')}\n"
        )
        child_info = tk.Label(
            child_section, 
            text=self.child_info_text, 
            anchor='w', 
            justify=tk.LEFT, 
            font=self.label_font,
            bg=self.section_bg,
            fg=self.text_color,
            padx=15
        )
        child_info.pack(fill=tk.X, pady=(10, 15))
        add_tooltip(child_info, "Name and date of birth information for the child")

        # Address & Contact Section
        street = self.child_data.get('Street','')
        if pd.notnull(street) and street != '':
            address_section = self.create_section_frame(main_content)
            address_section.grid(row=1, column=0, columnspan=2, sticky="nsew", pady=(10, 10))
            
            address_header = tk.Label(
                address_section, 
                text="Address & Contact Information", 
                font=self.section_font, 
                bg=self.section_bg, 
                fg=self.text_color,
                anchor='w'
            )
            address_header.pack(fill=tk.X, pady=(10, 10), padx=15)
            add_tooltip(address_header, "Contact and address details for this family")
            
            separator3 = tk.Frame(address_section, height=2, bg=self.primary_color)
            separator3.pack(fill=tk.X, padx=10)
            
            city = self.child_data.get('City','')
            state = self.child_data.get('State','')
            zip_ = self.child_data.get('ZIP','')
            phone = self.child_data.get('Phone_#','')
            mobile = self.child_data.get('Mobile_#','')

            self.address_info_text = (
                f"Street: {street}\n"
                f"City: {self.child_data.get('City','')}\n"
                f"State: {self.child_data.get('State','')}\n"
                f"ZIP: {self.child_data.get('ZIP','')}\n"
                f"Phone #: {self.child_data.get('Phone_#','')}\n"
                f"Mobile #: {self.child_data.get('Mobile_#','')}\n"
            )
            address_info = tk.Label(
                address_section, 
                text=self.address_info_text, 
                anchor='w',
                justify=tk.LEFT, 
                font=self.label_font,
                bg=self.section_bg,
                fg=self.text_color,
                padx=15
            )
            address_info.pack(fill=tk.X, pady=(10, 15))
            add_tooltip(address_info, "Full address and contact phone numbers")

        # Assigned Nurse Section
        nurse_section = self.create_section_frame(main_content)
        row_pos = 2 if pd.notnull(street) and street != '' else 1
        nurse_section.grid(row=row_pos, column=0, columnspan=2, sticky="nsew", pady=(10, 10))
        
        nurse_header = tk.Label(
            nurse_section, 
            text="Assigned Nurse", 
            font=self.section_font, 
            bg=self.section_bg, 
            fg=self.text_color,
            anchor='w'
        )
        nurse_header.pack(fill=tk.X, pady=(10, 10), padx=15)
        add_tooltip(nurse_header, "Nurse currently assigned to this child")
        
        separator4 = tk.Frame(nurse_section, height=2, bg=self.primary_color)
        separator4.pack(fill=tk.X, padx=10)
        
        nurse = self.child_data.get('Assigned_Nurse','None')
        if pd.isna(nurse):
            nurse = "None"
        self.nurse_info_text = f"Name: {nurse}"
        self.nurse_label = tk.Label(
            nurse_section, 
            text=self.nurse_info_text, 
            anchor='w', 
            justify=tk.LEFT, 
            font=self.label_font,
            bg=self.section_bg,
            fg=self.text_color,
            padx=15
        )
        self.nurse_label.pack(fill=tk.X, pady=(10, 15))
        add_tooltip(self.nurse_label, "The currently assigned nurse for this child" if nurse != "None" else "No nurse has been assigned yet")

        # Visit Log Section
        visit_section = self.create_section_frame(main_content)
        visit_section.grid(row=row_pos + 1, column=0, columnspan=2, sticky="nsew", pady=(10, 10))
        
        visit_header = tk.Label(
            visit_section,
            text="Visit Log",
            font=self.section_font,
            bg=self.section_bg,
            fg=self.text_color,
            anchor='w'
        )
        visit_header.pack(fill=tk.X, pady=(10, 10), padx=15)
        add_tooltip(visit_header, "Log of nurse visits for this child")

        separator5 = tk.Frame(visit_section, height=2, bg=self.primary_color)
        separator5.pack(fill=tk.X, padx=10)

        # Create frame for visit log table
        visit_frame = tk.Frame(visit_section, bg=self.section_bg)
        visit_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=(10, 15))

        # Create Treeview for visit log
        self.visit_tree = ttk.Treeview(visit_frame, columns=("Nurse_Name", "Visit_Time"), show="headings", height=5)
        self.visit_tree.heading("Nurse_Name", text="Nurse Name")
        self.visit_tree.heading("Visit_Time", text="Visit Time")
        self.visit_tree.column("Nurse_Name", width=150)
        self.visit_tree.column("Visit_Time", width=150)
        self.visit_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Add scrollbar to treeview
        visit_scrollbar = ttk.Scrollbar(visit_frame, orient=tk.VERTICAL, command=self.visit_tree.yview)
        visit_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.visit_tree.configure(yscrollcommand=visit_scrollbar.set)

        # Load initial visit log data
        self.update_visit_log()

        # Add spacing at the bottom of scrollable content
        tk.Frame(content_frame, height=30, bg=self.bg_color).pack(fill=tk.X)
        
        # === FIXED ACTION BUTTONS SECTION (Always visible) ===
        button_container = tk.Frame(self.view, bg=self.primary_color, bd=0)
        button_container.grid(row=1, column=0, columnspan=2, sticky="ew")
        
        # Create a styled button
        def create_button(parent, text, command, is_primary=False):
            if is_primary:
                bg_color = self.accent_color
                fg_color = "white"
                hover_color = self.button_hover_color
            else:
                bg_color = "#ffffff"
                fg_color = self.text_color
                hover_color = "#ecf0f1"  # Light gray on hover for normal buttons
            
            button = tk.Button(
                parent,
                text=text,
                command=command,
                bg=bg_color,
                fg=fg_color,
                font=self.button_font,
                relief=tk.RAISED,
                borderwidth=1,
                padx=15,
                pady=8,
                cursor="hand2"
            )
            
            # Add hover effect
            button.bind("<Enter>", lambda event, b=button, o=bg_color, h=hover_color: self._on_enter_button(event, b, o, h))
            button.bind("<Leave>", lambda event, b=button, o=bg_color: self._on_leave_button(event, b, o))
            
            return button
        
        # Button row with padding
        button_row = tk.Frame(button_container, bg=self.primary_color, padx=20, pady=10)
        button_row.pack(fill=tk.X)
        
        # Assign Nurse button (primary action)
        assign_btn = create_button(button_row, "Assign Nurse", self.assign_nurse)
        assign_btn.pack(side=tk.LEFT, padx=5)
        add_tooltip(assign_btn, "Assign or change the nurse responsible for this child")

        # Log Visit button
        log_btn = create_button(button_row, "Log Visit", self.auto_log_visit)
        log_btn.pack(side=tk.LEFT, padx=5)
        add_tooltip(log_btn, "Log a visit for the currently assigned nurse")
        
        # Copy Profile Info button
        copy_btn = create_button(button_row, "Copy Profile Info", self.controller.copy_to_clipboard)
        copy_btn.pack(side=tk.LEFT, padx=5)
        add_tooltip(copy_btn, "Copy all profile information to clipboard")
        
        # Export to PDF button
        export_btn = create_button(button_row, "Export to PDF", self.controller.export_profile_to_pdf)
        export_btn.pack(side=tk.LEFT, padx=5)
        add_tooltip(export_btn, "Export this profile information to a PDF file")
        
        # Close button
        close_btn = create_button(button_row, "Close", self.controller.close)
        close_btn.pack(side=tk.RIGHT, padx=5)
        add_tooltip(close_btn, "Close this profile view")
        
        return self.view
    
    def create_section_frame(self, parent):
        """Create a styled section frame with rounded corners"""
        frame = tk.Frame(
            parent, 
            bg=self.section_bg,
            highlightbackground=self.border_color,
            highlightthickness=1,
        )
        return frame
    
    def assign_nurse(self):
        self.controller.assign_nurse(self.child_data, self.update_nurse_info)

    def update_nurse_info(self, nurse_name):
        if nurse_name.startswith("Name: "):
            nurse_name = nurse_name.replace("Name: ", "", 1)
        self.child_data['Assigned_Nurse'] = nurse_name
        self.nurse_info_text = f"Name: {nurse_name}"
        self.nurse_label.config(text=self.nurse_info_text)

    def get_mother_info_text(self):
        return self.mother_info_text

    def get_child_info_text(self):
        return self.child_info_text

    def get_address_info_text(self):
        return self.address_info_text

    def get_nurse_info_text(self):
        return self.nurse_info_text

    def update_visit_log(self):
        path = "nurse_log.xlsx"
        if not os.path.exists(path):
            return
        df = pd.read_excel(path)
        mother_id = str(self.child_data.get("Mother_ID", ""))
        first = self.child_data.get("Child_First_Name", "").lower()
        last = self.child_data.get("Child_Last_Name", "").lower()
        filtered = df[
            (df["Mother_ID"].astype(str) == mother_id) &
            (df["Child_First_Name"].str.lower() == first) &
            (df["Child_Last_Name"].str.lower() == last)
        ]
        for row in self.visit_tree.get_children():
            self.visit_tree.delete(row)
        for _, row in filtered.iterrows():
            self.visit_tree.insert("", "end", values=(row["Nurse_Name"], row["Visit_Time"]))

    def auto_log_visit(self):
        nurse_name = self.child_data.get("Assigned_Nurse")
        if pd.isna(nurse_name) or not nurse_name or nurse_name.lower() in ["none", "n/a", "nan"]:
            self.show_custom_dialog("Error", "Please assign a nurse before logging a visit.", "error")
            return
        self.controller.log_nurse_visit(self.child_data)
        self.update_visit_log()
        self.show_custom_dialog("Success", f"Visit logged for nurse {nurse_name}.", "info")

    def show_custom_dialog(self, title, message, dialog_type="info"):
        """Show a custom dialog with the baby icon"""
        dialog = tk.Toplevel(self.root)
        dialog.title(title)
        dialog.geometry("400x220")  # Increased size for more padding
        dialog.resizable(False, False)
        
        # Make dialog modal
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Center the dialog on the screen
        dialog.update_idletasks()
        width = dialog.winfo_width()
        height = dialog.winfo_height()
        x = (dialog.winfo_screenwidth() // 2) - (width // 2)
        y = (dialog.winfo_screenheight() // 2) - (height // 2)
        dialog.geometry(f'+{x}+{y}')
        
        # Configure dialog style
        dialog.configure(bg=self.bg_color)
        
        # Main container with padding
        main_container = tk.Frame(dialog, bg=self.bg_color, padx=30, pady=20)
        main_container.pack(fill=tk.BOTH, expand=True)
        
        # Icon frame
        icon_frame = tk.Frame(main_container, bg=self.bg_color)
        icon_frame.pack(pady=(0, 15))
        
        # Use the baby icon if available
        if hasattr(self, 'icon') and self.icon:
            icon_label = tk.Label(icon_frame, image=self.icon, bg=self.bg_color)
            icon_label.pack()
        
        # Message
        message_label = tk.Label(
            main_container,
            text=message,
            font=self.label_font,
            bg=self.bg_color,
            fg=self.text_color,
            wraplength=300,  # Increased wraplength for better text flow
            justify=tk.CENTER  # Center-align text
        )
        message_label.pack(pady=(0, 20))  # More space between message and button
        
        # OK button
        ok_button = tk.Button(
            main_container,
            text="OK",
            command=dialog.destroy,
            font=self.button_font,
            bg=self.accent_color if dialog_type == "error" else self.success_color,
            fg="black",
            padx=30,  # Wider button
            pady=8,   # Taller button
            cursor="hand2"
        )
        ok_button.pack(pady=(0, 10))
        
        # Add hover effect to OK button
        hover_color = self.button_hover_color if dialog_type == "error" else "#2da146"  # Darker green for success
        ok_button.bind("<Enter>", lambda e: ok_button.config(bg=hover_color))
        ok_button.bind("<Leave>", lambda e: ok_button.config(
            bg=self.accent_color if dialog_type == "error" else self.success_color
        ))
        
        # Bind Enter key to close dialog
        dialog.bind("<Return>", lambda e: dialog.destroy())
        dialog.bind("<Escape>", lambda e: dialog.destroy())
        
        # Focus the OK button
        ok_button.focus_set()
        
        # Wait for the dialog to be closed
        dialog.wait_window()

    def manual_log_visit(self):
        nurse_name = simpledialog.askstring("Manual Log", "Enter Nurse Name:")
        if not nurse_name:
            return
        time_str = simpledialog.askstring("Manual Log", "Enter Visit Time (YYYY-MM-DD HH:MM:SS):")
        try:
            datetime.strptime(time_str, "%Y-%m-%d %H:%M:%S")
        except ValueError:
            self.show_custom_dialog("Error", "Invalid time format.", "error")
            return
        self.controller.log_nurse_visit(self.child_data, nurse_name.strip(), time_str)
        self.update_visit_log()
        self.show_custom_dialog("Success", f"Visit logged for nurse {nurse_name}.", "info")

    def delete_selected_visit(self):
        selected = self.visit_tree.selection()
        if not selected:
            self.show_custom_dialog("Warning", "Please select a visit log to delete.", "warning")
            return
        nurse_name, visit_time = self.visit_tree.item(selected[0])['values']
        
        # Create confirmation dialog
        confirm = tk.Toplevel(self.root)
        confirm.title("Confirm Deletion")
        confirm.geometry("350x200")
        confirm.resizable(False, False)
        confirm.transient(self.root)
        confirm.grab_set()
        
        # Center the dialog
        confirm.update_idletasks()
        width = confirm.winfo_width()
        height = confirm.winfo_height()
        x = (confirm.winfo_screenwidth() // 2) - (width // 2)
        y = (confirm.winfo_screenheight() // 2) - (height // 2)
        confirm.geometry(f'+{x}+{y}')
        
        # Configure dialog style
        confirm.configure(bg=self.bg_color)
        
        # Icon
        if hasattr(self, 'icon') and self.icon:
            icon_label = tk.Label(confirm, image=self.icon, bg=self.bg_color)
            icon_label.pack(pady=(15, 5))
        
        # Message
        message = f"Delete visit by {nurse_name}\non {visit_time}?"
        message_label = tk.Label(
            confirm,
            text=message,
            font=self.label_font,
            bg=self.bg_color,
            fg=self.text_color,
            wraplength=300
        )
        message_label.pack(pady=10)
        
        # Button frame
        button_frame = tk.Frame(confirm, bg=self.bg_color)
        button_frame.pack(pady=10)
        
        result = [False]  # Use list to store result since Python 3 doesn't have nonlocal
        
        def on_yes():
            result[0] = True
            confirm.destroy()
            
        def on_no():
            confirm.destroy()
        
        # Yes button
        yes_btn = tk.Button(
            button_frame,
            text="Yes",
            command=on_yes,
            font=self.button_font,
            bg=self.accent_color,
            fg="white",
            padx=20,
            pady=5,
            cursor="hand2"
        )
        yes_btn.pack(side=tk.LEFT, padx=5)
        
        # No button
        no_btn = tk.Button(
            button_frame,
            text="No",
            command=on_no,
            font=self.button_font,
            bg="#ffffff",
            fg=self.text_color,
            padx=20,
            pady=5,
            cursor="hand2"
        )
        no_btn.pack(side=tk.LEFT, padx=5)
        
        # Wait for dialog
        confirm.wait_window()
        
        if not result[0]:
            return
            
        path = "nurse_log.xlsx"
        if not os.path.exists(path):
            self.show_custom_dialog("Error", "Log file not found.", "error")
            return
            
        df = pd.read_excel(path)
        match_mask = (
            (df["Mother_ID"].astype(str) == str(self.child_data.get("Mother_ID", ""))) &
            (df["Child_First_Name"].str.lower() == self.child_data.get("Child_First_Name", "").lower()) &
            (df["Child_Last_Name"].str.lower() == self.child_data.get("Child_Last_Name", "").lower()) &
            (df["Nurse_Name"] == nurse_name) &
            (df["Visit_Time"] == visit_time)
        )
        if not match_mask.any():
            self.show_custom_dialog("Error", "No matching record found in file.", "error")
            return
            
        df = df[~match_mask]
        df.to_excel(path, index=False)
        self.update_visit_log()
        self.show_custom_dialog("Success", "Visit log deleted successfully.", "info")