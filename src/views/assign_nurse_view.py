import tkinter as tk

class AssignNurseView:
    def __init__(self, root, controller, child_data, update_callback):
        self.root = root
        self.controller = controller
        self.child_data = child_data
        self.update_callback = update_callback

    def create_widgets(self):
        view = tk.Frame(self.root, width=300, height=150)
        tk.Label(view, text=f"Assign Nurse to {self.child_data['Child_First_Name']} {self.child_data['Child_Last_Name']}").pack(pady=5)
        tk.Label(view, text="Enter Nurse Name:").pack(pady=5)
        nurse_var = tk.StringVar()
        tk.Entry(view, textvariable=nurse_var).pack(pady=5)

        def save_nurse():
            nurse_name = nurse_var.get().strip()
            self.controller.save_nurse(nurse_name, self.child_data, self.update_callback, self.controller.close_assign_nurse)

        tk.Button(view, text="Save", command=save_nurse).pack(pady=5)
        tk.Button(view, text="Close", command=self.controller.close_assign_nurse).pack(padx=5)

        return view
