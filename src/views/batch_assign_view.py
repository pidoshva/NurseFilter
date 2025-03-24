import tkinter as tk
from tkinter import messagebox
from views.tooltip import add_tooltip


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
        city_label = tk.Label(main_frame, text="Filter by City:")
        city_label.pack(pady=5)
        add_tooltip(city_label, "Enter a city name to assign a nurse to all children in this city")
        
        city_var = tk.StringVar()
        city_entry = tk.Entry(main_frame, textvariable=city_var)
        city_entry.pack(pady=5)
        add_tooltip(city_entry, "Leave blank to ignore this filter")

        state_label = tk.Label(main_frame, text="Filter by State:")
        state_label.pack(pady=5)
        add_tooltip(state_label, "Enter a state abbreviation to assign a nurse to all children in this state")
        
        state_var = tk.StringVar()
        state_entry = tk.Entry(main_frame, textvariable=state_var)
        state_entry.pack(pady=5)
        add_tooltip(state_entry, "Leave blank to ignore this filter")

        zip_label = tk.Label(main_frame, text="Filter by ZIP Code:")
        zip_label.pack(pady=5)
        add_tooltip(zip_label, "Enter a ZIP code to assign a nurse to all children in this area")
        
        zip_var = tk.StringVar()
        zip_entry = tk.Entry(main_frame, textvariable=zip_var)
        zip_entry.pack(pady=5)
        add_tooltip(zip_entry, "Leave blank to ignore this filter")

        nurse_label = tk.Label(main_frame, text="Nurse Name:")
        nurse_label.pack(pady=5)
        add_tooltip(nurse_label, "Enter the name of the nurse to assign (required)")
        
        nurse_var = tk.StringVar()
        nurse_entry = tk.Entry(main_frame, textvariable=nurse_var)
        nurse_entry.pack(pady=5)
        add_tooltip(nurse_entry, "Required - name of the nurse who will be assigned to all matching children")

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
        save_btn = tk.Button(button_frame, text="Save", command=save, width=10)
        save_btn.pack(side=tk.LEFT, padx=5)
        add_tooltip(save_btn, "Assign the specified nurse to all children matching your criteria")
        
        cancel_btn = tk.Button(button_frame, text="Cancel", command=self.controller.close_batch_assign, width=10)
        cancel_btn.pack(side=tk.LEFT, padx=5)
        add_tooltip(cancel_btn, "Cancel this operation and close the window")

        return window