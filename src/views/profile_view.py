import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import pandas as pd
from datetime import datetime
import os
from views.tooltip import add_tooltip

class ProfileView:
    def __init__(self, root, controller, child_data):
        self.root = root
        self.controller = controller
        self.child_data = child_data
        self.view = None
        self.visit_tree = None
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
        frame = tk.Frame(self.view, padx=10, pady=10)
        frame.pack(fill=tk.BOTH, expand=True)

        # Info Frame
        info_frame = tk.Frame(frame, padx=10, pady=10)
        info_frame.grid(row=0, column=0, rowspan=2, sticky='nsew', padx=(0, 10), pady=(0, 10))

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
            f"First Name: {self.child_data.get('Child_First_Name','')}\n"
            f"Last Name: {self.child_data.get('Child_Last_Name','')}\n"
            f"Date of Birth: {self.child_data.get('Child_Date_of_Birth','')}\n"
        )
        child_info = tk.Label(frame, text=self.child_info_text, anchor='w', justify=tk.LEFT, font=("Arial",12))
        child_info.pack(anchor='w', pady=(5,10))
        add_tooltip(child_info, "Name and date of birth information for the child")

        # Address
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
                f"City: {self.child_data.get('City','')}\n"
                f"State: {self.child_data.get('State','')}\n"
                f"ZIP: {self.child_data.get('ZIP','')}\n"
                f"Phone #: {self.child_data.get('Phone_#','')}\n"
                f"Mobile #: {self.child_data.get('Mobile_#','')}\n"
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
        self.nurse_label = tk.Label(info_frame, text=self.nurse_info_text, anchor='w', justify=tk.LEFT, font=("Arial",12))
        self.nurse_label.pack(anchor='w', pady=(5,10))
        add_tooltip(self.nurse_label, "The currently assigned nurse for this child" if nurse != "None" else "No nurse has been assigned yet")

        # Visit Log
        log_frame = tk.Frame(frame, padx=10, pady=10)
        log_frame.grid(row=0, column=1, sticky='nsew', padx=(10, 0), pady=(0, 10))
        tk.Label(log_frame, text="Nurse Visit Log", font=("Arial",14,"bold")).pack(anchor='w', pady=(10,0))
        self.visit_tree = ttk.Treeview(log_frame, columns=("Nurse", "Time"), show='headings', height=6)
        self.visit_tree.heading("Nurse", text="Nurse Name")
        self.visit_tree.heading("Time", text="Visit Time")
        self.visit_tree.column("Nurse", anchor="center", width=150)
        self.visit_tree.column("Time", anchor="center", width=200)
        self.visit_tree.pack(fill=tk.BOTH, expand=True, pady=(0, 10))

        log_btn_frame = tk.Frame(log_frame)
        log_btn_frame.pack(pady=(0,10))
        tk.Button(log_btn_frame, text="Auto Log Visit", command=self.auto_log_visit).pack(side=tk.LEFT, padx=5)
        tk.Button(log_btn_frame, text="Manual Log Visit", command=self.manual_log_visit).pack(side=tk.LEFT, padx=5)
        tk.Button(log_btn_frame, text="Delete Selected Visit", command=self.delete_selected_visit).pack(side=tk.LEFT, padx=5)

        self.update_visit_log()

        # General Buttons
        btn_frame = tk.Frame(frame)
        btn_frame.grid(row=1, column=1, sticky='nsew', padx=(10, 0), pady=(10, 0))
        tk.Button(btn_frame, text="Assign Nurse", command=self.assign_nurse).pack(pady=(10,5))
        tk.Button(btn_frame, text="Copy Profile Info", command=self.controller.copy_to_clipboard).pack(pady=(5,5))
        tk.Button(btn_frame, text="Export to PDF", command=self.controller.export_profile_to_pdf).pack(pady=(5,5))
        tk.Button(btn_frame, text="Close", command=self.controller.close).pack(pady=(5,5))

        frame.grid_columnconfigure(0, weight=1)
        frame.grid_columnconfigure(1, weight=1)
        frame.grid_rowconfigure(0, weight=1)
        frame.grid_rowconfigure(1, weight=0)

        return self.view

    def assign_nurse(self):
        self.controller.assign_nurse(self.child_data , self.update_nurse_info)

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