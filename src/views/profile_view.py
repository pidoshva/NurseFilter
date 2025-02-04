import tkinter as tk
import pandas as pd

class ProfileView:
    """
    View class for displaying a single child's profile.
    """
    def __init__(self, root, controller, child_data):
        self.root = root
        self.controller = controller
        self.child_data = child_data
        self.profile_window = None

        # We'll store text versions so we can copy/export them
        self.mother_info_text = ""
        self.child_info_text = ""
        self.address_info_text = ""
        self.nurse_info_text = ""

        self.create_view()

    def create_view(self):
        self.profile_window = tk.Toplevel(self.root)
        first = self.child_data.get('Child_First_Name','')
        last = self.child_data.get('Child_Last_Name','')
        self.profile_window.title(f"Profile of {first} {last}")

        frame = tk.Frame(self.profile_window, padx=10, pady=10)
        frame.pack(fill=tk.BOTH, expand=True)

        # Mother's Info
        tk.Label(frame, text="Mother's Information", font=("Arial",14,"bold")).pack(anchor='w', pady=(10,0))
        self.mother_info_text = (
            f"Mother ID: {self.child_data.get('Mother_ID','')}\n"
            f"First Name: {self.child_data.get('Mother_First_Name','')}\n"
            f"Last Name: {self.child_data.get('Mother_Last_Name','')}\n"
        )
        tk.Label(frame, text=self.mother_info_text, anchor='w', justify=tk.LEFT, font=("Arial",12)).pack(anchor='w', pady=(5,10))

        # Child's Info
        tk.Label(frame, text="Child's Information", font=("Arial",14,"bold")).pack(anchor='w', pady=(10,0))
        dob = self.child_data.get('Child_Date_of_Birth','')
        self.child_info_text = (
            f"First Name: {first}\n"
            f"Last Name: {last}\n"
            f"Date of Birth: {dob}\n"
        )
        tk.Label(frame, text=self.child_info_text, anchor='w', justify=tk.LEFT, font=("Arial",12)).pack(anchor='w', pady=(5,10))

        # Address & Contact
        street = self.child_data.get('Street','')
        if pd.notnull(street) and street != '':
            tk.Label(frame, text="Address & Contact Information", font=("Arial",14,"bold")).pack(anchor='w', pady=(10,0))
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
            tk.Label(frame, text=self.address_info_text, anchor='w',
                     justify=tk.LEFT, font=("Arial",12)).pack(anchor='w', pady=(5,10))

        # Assigned Nurse
        tk.Label(frame, text="Assigned Nurse", font=("Arial",14,"bold")).pack(anchor='w', pady=(10,0))
        nurse = self.child_data.get('Assigned_Nurse','None')
        self.nurse_info_text = f"Name: {nurse}"
        self.nurse_label = tk.Label(frame, text=self.nurse_info_text, anchor='w', justify=tk.LEFT, font=("Arial",12))
        self.nurse_label.pack(anchor='w', pady=(5,10))

        # Buttons
        tk.Button(frame, text="Assign Nurse", command=self.controller.assign_nurse).pack(pady=(10,5))
        tk.Button(frame, text="Copy Profile Info", command=self.controller.copy_to_clipboard).pack(pady=(5,5))
        tk.Button(frame, text="Export to PDF", command=self.controller.export_profile_to_pdf).pack(pady=(5,5))

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
