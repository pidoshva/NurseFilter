import tkinter as tk

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
        profile_window = tk.Toplevel(self.root)
        profile_window.title(f"Profile of {self.child_data['Child_First_Name']} {self.child_data['Child_Last_Name']}")

        profile_frame = tk.Frame(profile_window, padx=10, pady=10)
        profile_frame.pack(fill=tk.BOTH, expand=True)

        # Display mother's information
        mother_info_label = tk.Label(profile_frame, text="Mother's Information", font=("Arial", 14, "bold"))
        mother_info_label.pack(anchor='w', pady=(10, 0))

        mother_info_text = f"Mother ID: {self.child_data['Mother_ID']}\n" \
                           f"First Name: {self.child_data['Mother_First_Name']}\n" \
                           f"Last Name: {self.child_data['Mother_Last_Name']}\n"

        tk.Label(profile_frame, text=mother_info_text, anchor='w', justify=tk.LEFT, font=("Arial", 12)).pack(anchor='w', pady=(5, 10))

        # ... (Display other sections similarly)

        # Buttons for actions
        copy_button = tk.Button(profile_frame, text="Copy Profile Info", command=self.controller.copy_to_clipboard)
        copy_button.pack(pady=(10, 5))

        export_button = tk.Button(profile_frame, text="Export to PDF", command=self.controller.export_profile_to_pdf)
        export_button.pack(pady=(10, 5))
