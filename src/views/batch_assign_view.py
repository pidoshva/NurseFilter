import tkinter as tk
from tkinter import messagebox


class BatchAssignView:
    def __init__(self, root, controller, batch_assign_callback, refresh_view_callback):
        self.root = root
        self.controller = controller
        self.batch_assign_callback = batch_assign_callback
        self.refresh_view = refresh_view_callback

    def create_widgets(self):
        window = tk.Frame(self.root, width=400, height=400)

        # Create main frame to hold everything
        main_frame = tk.Frame(window)
        main_frame.pack(expand=True, fill='both', padx=20, pady=20)

        # Filter entries
        tk.Label(main_frame, text="Filter by City:").pack(pady=5)
        city_var = tk.StringVar()
        tk.Entry(main_frame, textvariable=city_var).pack(pady=5)

        tk.Label(main_frame, text="Filter by State:").pack(pady=5)
        state_var = tk.StringVar()
        tk.Entry(main_frame, textvariable=state_var).pack(pady=5)

        tk.Label(main_frame, text="Filter by ZIP Code:").pack(pady=5)
        zip_var = tk.StringVar()
        tk.Entry(main_frame, textvariable=zip_var).pack(pady=5)

        tk.Label(main_frame, text="Nurse Name:").pack(pady=5)
        nurse_var = tk.StringVar()
        tk.Entry(main_frame, textvariable=nurse_var).pack(pady=5)

        # Create a frame for buttons at the bottom
        button_frame = tk.Frame(main_frame)
        button_frame.pack(side='bottom', pady=20)

        def save():
            nurse_name = nurse_var.get().strip()
            if not nurse_name:
                messagebox.showerror("Error", "Nurse name is required.")
                return
            city = city_var.get().strip()
            state = state_var.get().strip()
            zipcode = zip_var.get().strip()
            count = self.batch_assign_callback(nurse_name, city, state, zipcode)
            if count > 0:
                messagebox.showinfo("Success", f"Nurse '{nurse_name}' assigned to {count} children.")
                self.refresh_view()  # Refresh the view after batch assignment
                window.destroy()
            else:
                messagebox.showinfo("No Matches", "No records matched the filters.")

        # Add both Save and Cancel buttons
        tk.Button(button_frame, text="Save", command=save, width=10).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Cancel", command=self.controller.close_batch_assign , width=10).pack(side=tk.LEFT, padx=5)

        return window