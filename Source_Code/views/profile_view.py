# views/profile_view.py

import tkinter as tk
import pandas as pd

class ProfileView:
    """
    View class for displaying a child's profile.
    """
    def __init__(self, root, controller, child_data):
        self.root = root
        self.controller = controller
        self.child_data = child_data
        self.create_view()

    def create_view(self):
        self.profile_window = tk.Toplevel(self.root)
        self.profile_window.title(f"Profile of {self.child_data['Child_First_Name']} {self.child_data['Child_Last_Name']}")

        self.profile_frame = tk.Frame(self.profile_window, padx=10, pady=10)
        self.profile_frame.pack(fill=tk.BOTH, expand=True)

        # Mother's Information
        mother_info_label = tk.Label(self.profile_frame, text="Mother's Information", font=("Arial", 14, "bold"))
        mother_info_label.pack(anchor='w', pady=(10, 0))

        self.mother_info_text = f"Mother ID: {self.child_data['Mother_ID']}\n" \
                                f"First Name: {self.child_data['Mother_First_Name']}\n" \
                                f"Last Name: {self.child_data['Mother_Last_Name']}\n"

        self.mother_info_label = tk.Label(self.profile_frame, text=self.mother_info_text, anchor='w', justify=tk.LEFT, font=("Arial", 12))
        self.mother_info_label.pack(anchor='w', pady=(5, 10))

        # Child's Information
        child_info_label = tk.Label(self.profile_frame, text="Child's Information", font=("Arial", 14, "bold"))
        child_info_label.pack(anchor='w', pady=(10, 0))

        self.child_info_text = f"First Name: {self.child_data['Child_First_Name']}\n" \
                               f"Last Name: {self.child_data['Child_Last_Name']}\n" \
                               f"Date of Birth: {self.child_data['Child_Date_of_Birth']}\n"

        self.child_info_label = tk.Label(self.profile_frame, text=self.child_info_text, anchor='w', justify=tk.LEFT, font=("Arial", 12))
        self.child_info_label.pack(anchor='w', pady=(5, 10))

        # Address & Contact Information (if available)
        self.address_info_text = ''
        if 'Street' in self.child_data and not pd.isnull(self.child_data['Street']):
            address_info_label = tk.Label(self.profile_frame, text="Address & Contact Information", font=("Arial", 14, "bold"))
            address_info_label.pack(anchor='w', pady=(10, 0))

            self.address_info_text = f"Street: {self.child_data['Street']}\n" \
                                     f"City: {self.child_data['City']}\n" \
                                     f"State: {self.child_data['State']}\n" \
                                     f"ZIP: {self.child_data['ZIP']}\n" \
                                     f"Phone #: {self.child_data['Phone_#']}\n" \
                                     f"Mobile #: {self.child_data['Mobile_#']}\n"

            self.address_info_label = tk.Label(self.profile_frame, text=self.address_info_text, anchor='w', justify=tk.LEFT, font=("Arial", 12))
            self.address_info_label.pack(anchor='w', pady=(5, 10))

        # Assigned Nurse
        nurse_info_label = tk.Label(self.profile_frame, text="Assigned Nurse", font=("Arial", 14, "bold"))
        nurse_info_label.pack(anchor='w', pady=(10, 0))

        assigned_nurse = self.child_data.get('Assigned_Nurse', 'None')
        self.nurse_info_text = f"Name: {assigned_nurse}"

        self.nurse_info_label = tk.Label(self.profile_frame, text=self.nurse_info_text, anchor='w', justify=tk.LEFT, font=("Arial", 12))
        self.nurse_info_label.pack(anchor='w', pady=(5, 10))

        # Buttons
        assign_nurse_button = tk.Button(self.profile_frame, text="Assign Nurse", command=self.controller.assign_nurse)
        assign_nurse_button.pack(pady=(10, 5))

        copy_button = tk.Button(self.profile_frame, text="Copy Profile Info", command=self.controller.copy_to_clipboard)
        copy_button.pack(pady=(10, 5))

        export_button = tk.Button(self.profile_frame, text="Export to PDF", command=self.controller.export_profile_to_pdf)
        export_button.pack(pady=(10, 5))

    def update_nurse_info(self, nurse_info_text):
        self.nurse_info_text = nurse_info_text
        self.nurse_info_label.config(text=self.nurse_info_text)

    def get_mother_info_text(self):
        return self.mother_info_text

    def get_child_info_text(self):
        return self.child_info_text

    def get_address_info_text(self):
        return self.address_info_text

    def get_nurse_info_text(self):
        return self.nurse_info_text
