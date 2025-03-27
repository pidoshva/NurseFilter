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
        assign_btn = create_button(button_row, "Assign Nurse", self.assign_nurse, is_primary=True)
        assign_btn.pack(side=tk.LEFT, padx=5)
        add_tooltip(assign_btn, "Assign or change the nurse responsible for this child")
        
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
            messagebox.showerror("Error", "Please assign a nurse before logging a visit.")
            return
        visit_time = pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S")
        self.save_nurse_log(nurse_name, visit_time)
        self.update_visit_log()
        messagebox.showinfo("Success", f"Visit logged for nurse {nurse_name}.")

    def manual_log_visit(self):
        nurse_name = simpledialog.askstring("Manual Log", "Enter Nurse Name:")
        if not nurse_name:
            return
        time_str = simpledialog.askstring("Manual Log", "Enter Visit Time (YYYY-MM-DD HH:MM:SS):")
        try:
            datetime.strptime(time_str, "%Y-%m-%d %H:%M:%S")
        except ValueError:
            messagebox.showerror("Error", "Invalid time format.")
            return
        self.save_nurse_log(nurse_name.strip(), time_str)
        self.update_visit_log()
        messagebox.showinfo("Success", f"Visit logged for nurse {nurse_name}.")

    def save_nurse_log(self, nurse_name, visit_time):
        file = "nurse_log.xlsx"
        if os.path.exists(file):
            df = pd.read_excel(file)
        else:
            df = pd.DataFrame(columns=["Visit_ID", "Mother_ID", "Child_First_Name", "Child_Last_Name", "Nurse_Name", "Visit_Time"])
        visit_id = len(df) + 1
        new_row = {
            "Visit_ID": visit_id,
            "Mother_ID": self.child_data.get("Mother_ID", "N/A"),
            "Child_First_Name": self.child_data.get("Child_First_Name", "N/A"),
            "Child_Last_Name": self.child_data.get("Child_Last_Name", "N/A"),
            "Nurse_Name": nurse_name,
            "Visit_Time": visit_time
        }
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
        df.to_excel(file, index=False)

    def delete_selected_visit(self):
        selected = self.visit_tree.selection()
        if not selected:
            messagebox.showwarning("No selection", "Please select a visit log to delete.")
            return
        nurse_name, visit_time = self.visit_tree.item(selected[0])['values']
        confirm = messagebox.askyesno("Confirm Deletion", f"Delete visit by {nurse_name} on {visit_time}?")
        if not confirm:
            return
        path = "nurse_log.xlsx"
        if not os.path.exists(path):
            messagebox.showerror("Error", "Log file not found.")
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
            messagebox.showerror("Error", "No matching record found in file.")
            return
        df = df[~match_mask]
        df.to_excel(path, index=False)
        self.update_visit_log()
        messagebox.showinfo("Deleted", "Visit log deleted successfully.")