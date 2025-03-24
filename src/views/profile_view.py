import tkinter as tk
import pandas as pd
from views.tooltip import add_tooltip

class ProfileView:
    """
    View class for displaying a single child's profile.
    """
    def __init__(self, root, controller, child_data):
        self.root = root
        self.controller = controller
        self.child_data = child_data
        self.view = None

        # We'll store text versions so we can copy/export them
        self.mother_info_text = ""
        self.child_info_text = ""
        self.address_info_text = ""
        self.nurse_info_text = ""

    def get_frame(self):
        return self.view
    
    def get_title(self):
        first = self.child_data.get('Child_First_Name','')
        last = self.child_data.get('Child_Last_Name','')
        return f"{first} {last} Profile"

    def create_widgets(self):
        self.view = tk.Frame(self.root)

        first = self.child_data.get('Child_First_Name','')
        last = self.child_data.get('Child_Last_Name','')

        frame = tk.Frame(self.view, padx=10, pady=10)
        frame.pack(fill=tk.BOTH, expand=True)

        # Mother's Info
        mother_header = tk.Label(frame, text="Mother's Information", font=("Arial",14,"bold"))
        mother_header.pack(anchor='w', pady=(10,0))
        add_tooltip(mother_header, "Information about the child's mother")
        
        self.mother_info_text = (
            f"Mother ID: {self.child_data.get('Mother_ID','')}\n"
            f"First Name: {self.child_data.get('Mother_First_Name','')}\n"
            f"Last Name: {self.child_data.get('Mother_Last_Name','')}\n"
        )
        mother_info = tk.Label(frame, text=self.mother_info_text, anchor='w', justify=tk.LEFT, font=("Arial",12))
        mother_info.pack(anchor='w', pady=(5,10))
        add_tooltip(mother_info, "Unique identifier and name details of the mother")

        # Child's Info
        child_header = tk.Label(frame, text="Child's Information", font=("Arial",14,"bold"))
        child_header.pack(anchor='w', pady=(10,0))
        add_tooltip(child_header, "Personal information about the child")
        
        dob = self.child_data.get('Child_Date_of_Birth','')
        self.child_info_text = (
            f"First Name: {first}\n"
            f"Last Name: {last}\n"
            f"Date of Birth: {dob}\n"
        )
        child_info = tk.Label(frame, text=self.child_info_text, anchor='w', justify=tk.LEFT, font=("Arial",12))
        child_info.pack(anchor='w', pady=(5,10))
        add_tooltip(child_info, "Name and date of birth information for the child")

        # Address & Contact
        street = self.child_data.get('Street','')
        if pd.notnull(street) and street != '':
            address_header = tk.Label(frame, text="Address & Contact Information", font=("Arial",14,"bold"))
            address_header.pack(anchor='w', pady=(10,0))
            add_tooltip(address_header, "Contact and address details for this family")
            
            city = self.child_data.get('City','')
            state = self.child_data.get('State','')
            zip_ = self.child_data.get('ZIP','')
            phone = self.child_data.get('Phone_#','')
            mobile = self.child_data.get('Mobile_#','')

            self.address_info_text = (
                f"Street: {street}\n"
                f"City: {city}\n"
                f"State: {state}\n"
                f"ZIP: {zip_}\n"
                f"Phone #: {phone}\n"
                f"Mobile #: {mobile}\n"
            )
            address_info = tk.Label(frame, text=self.address_info_text, anchor='w',
                     justify=tk.LEFT, font=("Arial",12))
            address_info.pack(anchor='w', pady=(5,10))
            add_tooltip(address_info, "Full address and contact phone numbers")

        # Assigned Nurse
        nurse_header = tk.Label(frame, text="Assigned Nurse", font=("Arial",14,"bold"))
        nurse_header.pack(anchor='w', pady=(10,0))
        add_tooltip(nurse_header, "Nurse currently assigned to this child")
        
        nurse = self.child_data.get('Assigned_Nurse','None')
        if pd.isna(nurse):
            nurse = "None"
        self.nurse_info_text = f"Name: {nurse}"
        self.nurse_label = tk.Label(frame, text=self.nurse_info_text, anchor='w', justify=tk.LEFT, font=("Arial",12))
        self.nurse_label.pack(anchor='w', pady=(5,10))
        add_tooltip(self.nurse_label, "The currently assigned nurse for this child" if nurse != "None" else "No nurse has been assigned yet")

        # Buttons
        assign_btn = tk.Button(frame, text="Assign Nurse", command=self.assign_nurse)
        assign_btn.pack(pady=(10,5))
        add_tooltip(assign_btn, "Assign or change the nurse responsible for this child")
        
        copy_btn = tk.Button(frame, text="Copy Profile Info", command=self.controller.copy_to_clipboard)
        copy_btn.pack(pady=(5,5))
        add_tooltip(copy_btn, "Copy all profile information to clipboard")
        
        export_btn = tk.Button(frame, text="Export to PDF", command=self.controller.export_profile_to_pdf)
        export_btn.pack(pady=(5,5))
        add_tooltip(export_btn, "Export this profile information to a PDF file")
        
        close_btn = tk.Button(frame, text="Close", command=self.controller.close)
        close_btn.pack(pady=(5,5))
        add_tooltip(close_btn, "Close this profile view")
        
        return self.view
    
    def assign_nurse(self):
        self.controller.assign_nurse(self.child_data , self.update_nurse_info)

    def update_nurse_info(self, text):
        self.nurse_info_text = text
        self.nurse_label.config(text=self.nurse_info_text)

    # The controller calls these getters to build PDF or do copy/paste
    def get_mother_info_text(self):
        return self.mother_info_text

    def get_child_info_text(self):
        return self.child_info_text

    def get_address_info_text(self):
        return self.address_info_text

    def get_nurse_info_text(self):
        return self.nurse_info_text
