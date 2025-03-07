import tkinter as tk
from tkinter import messagebox, ttk
import pandas as pd


class StatisticalView:
    def __init__(self, root, controller):
        self.controller = controller
        self.root = root

    def display(self, df):
        report_win = tk.Frame(self.root, width=600, height=650)

        # Ensure 'Assigned_Nurse' column exists and replace NaN with 'None'
        df['Assigned_Nurse'] = df['Assigned_Nurse'].fillna("None").astype(str).str.strip()

        # Count Assigned and Unassigned Children Correctly
        total_children = len(df)
        assigned_df = df[df['Assigned_Nurse'].str.lower() != "none"]  # Proper filtering
        assigned_count = len(assigned_df)
        unassigned_count = total_children - assigned_count
        assigned_percentage = (assigned_count / total_children * 100) if total_children > 0 else 0
        unassigned_percentage = 100 - assigned_percentage

        tk.Label(report_win, text=f"📌 Total Children: {total_children}", font=("Arial", 12)).pack(pady=5)
        tk.Label(report_win, text=f"👶 Assigned to Nurses: {assigned_count} ({assigned_percentage:.1f}%)", font=("Arial", 12)).pack(pady=5)
        tk.Label(report_win, text=f"🚨 Unassigned Children: {unassigned_count} ({unassigned_percentage:.1f}%)", font=("Arial", 12)).pack(pady=5)

        # Handle Date of Birth correctly
        if 'Child_Date_of_Birth' in df.columns:
            df['dob_temp'] = pd.to_datetime(df['Child_Date_of_Birth'], errors='coerce')
            valid_ages = df.dropna(subset=['dob_temp'])

            if not valid_ages.empty:
                today = pd.Timestamp.today()
                avg_age_years = (today - valid_ages['dob_temp']).dt.days.mean() / 365
                tk.Label(report_win, text=f"🧒 Average Age: {avg_age_years:.1f} years", font=("Arial", 12)).pack(pady=5)

                youngest = valid_ages.loc[valid_ages['dob_temp'].idxmax()]
                oldest = valid_ages.loc[valid_ages['dob_temp'].idxmin()]
                tk.Label(report_win, text=f"👶 Youngest: {youngest['Child_First_Name']} {youngest['Child_Last_Name']} ({youngest['Child_Date_of_Birth']})", font=("Arial", 12)).pack(pady=5)
                tk.Label(report_win, text=f"🧓 Oldest: {oldest['Child_First_Name']} {oldest['Child_Last_Name']} ({oldest['Child_Date_of_Birth']})", font=("Arial", 12)).pack(pady=5)

        # Display Children Per Town (Clickable Towns)
        if 'City' in df.columns:
            town_counts = df['City'].value_counts().to_dict()

            town_frame = tk.Frame(report_win)
            town_frame.pack(pady=10, fill=tk.X)
            tk.Label(town_frame, text="🏙️ Children per Town (Click to View):", font=("Arial", 12, "bold")).pack()

            tree = ttk.Treeview(town_frame, columns=("Town", "Count"), show="headings", height=8)
            tree.heading("Town", text="Town")
            tree.heading("Count", text="Children")
            tree.column("Town", anchor="center", width=250)
            tree.column("Count", anchor="center", width=80)
            tree.pack(fill=tk.X)

            # Make Town Clickable to Show Children
            def open_town_window(event):
                selected_item = tree.selection()
                if not selected_item:
                    return
                
                town_name = tree.item(selected_item[0], 'values')[0]
                children_df = df[df['City'] == town_name]
                
                if children_df.empty:
                    messagebox.showinfo("No Data", f"No children found for {town_name}")
                    return
                
                town_window = tk.Toplevel(report_win)
                town_window.title(f"Children in {town_name}")
                town_window.geometry("400x500")

                tk.Label(town_window, text=f"Children in {town_name}:", font=("Arial", 12, "bold")).pack(pady=5)

                child_tree = ttk.Treeview(town_window, columns=("Child Name", "Child ID"), show="headings", height=15)
                child_tree.heading("Child Name", text="Child Name")
                child_tree.heading("Child ID", text="Child ID")
                child_tree.column("Child Name", anchor="center", width=250)
                child_tree.column("Child ID", anchor="center", width=100)
                child_tree.pack(fill=tk.BOTH, expand=True)

                # Insert child records
                for _, row in children_df.iterrows():
                    child_name = f"{row['Child_First_Name']} {row['Child_Last_Name']}"
                    child_id = row.get("Mother_ID", "N/A")
                    child_tree.insert("", "end", values=(child_name, child_id))

                # Clicking a Child Opens Profile
                def open_profile(event):
                    selected_child = child_tree.selection()
                    if not selected_child:
                        return

                    child_values = child_tree.item(selected_child[0], 'values')
                    child_name, child_id = child_values

                    # Locate child data
                    selected_child_data = df[(df["Mother_ID"].astype(str) == str(child_id)) & (df["Child_First_Name"] + " " + df["Child_Last_Name"] == child_name)]
                    
                    if selected_child_data.empty:
                        messagebox.showerror("Error", "Child data not found.")
                        return

                    child_row = selected_child_data.iloc[0]
                    self.main_controller.show_profile(child_row)

                child_tree.bind("<Double-1>", open_profile)

            tree.bind("<Double-1>", open_town_window)

            # Populate Town List
            for town, count in town_counts.items():
                tree.insert("", "end", values=(town, count))

        tk.Button(report_win, text="Export as PDF", command=lambda: self.controller.export_report_to_pdf(df)).pack(pady=10)
        report_win.pack()
        return report_win