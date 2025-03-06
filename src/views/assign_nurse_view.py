import tkinter as tk

class AssignNurseView:
    def __init__(self, root, controller, child_data, update_callback):
        self.root = root
        self.controller = controller
        self.child_data = child_data
        self.update_callback = update_callback
        self.assign_win = None

    def display(self):
        self.assign_win = tk.Toplevel(self.root)
        self.assign_win.title(f"Assign Nurse to {self.child_data['Child_First_Name']} {self.child_data['Child_Last_Name']}")
        self.assign_win.geometry("300x150")

        tk.Label(self.assign_win, text="Enter Nurse Name:").pack(pady=5)
        nurse_var = tk.StringVar()
        tk.Entry(self.assign_win, textvariable=nurse_var).pack(pady=5)

        def save_nurse():
            nurse_name = nurse_var.get().strip()
            self.controller.save_nurse(nurse_name, self.child_data, self.update_callback, self.close)

        tk.Button(self.assign_win, text="Save", command=save_nurse).pack(pady=5)

    def close(self):
        self.assign_win.destroy()
