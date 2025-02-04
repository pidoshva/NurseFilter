import logging
import os
import platform
import tkinter as tk
from tkinter import messagebox, filedialog, ttk
from datetime import datetime
import pandas as pd

from models.data_model import DataModel
from views.main_view import MainView
from views.combined_data_view import CombinedDataView
from views.profile_view import ProfileView

from controllers.combined_data_controller import CombinedDataController


class MainController:
    """
    The main controller for the application.
    Wires up the Model (DataModel) and the Views (MainView, CombinedDataView, ProfileView, etc.).
    """

    def __init__(self, root):
        self.root = root
        self.model = DataModel()
        self.view = MainView(root, self)
        # Create and store the combined data controller
        self.root.combined_data_controller = CombinedDataController(root, self.model)
        logging.info("MainController initialized.")

    def on_closing(self):
        """
        Called when the user closes the main window.
        Optionally encrypt 'combined_matched_data.xlsx' or do cleanup.
        """
        logging.info("Closing App")
        filepath = 'combined_matched_data.xlsx'
        # If the file exists, try to encrypt it
        if os.path.exists(filepath):
            self.model.encrypt_file(filepath)
        self.root.destroy()

    # 1. Reading Excel Files
    def read_excel_file(self):
        logging.info("Selecting Excel file...")
        filepath = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx *.xls")])
        if not filepath:
            return
        # Decrypt if needed
        if self.model.is_file_encrypted(filepath):
            if not self.model.decrypt_file(filepath):
                return
        self.model.read_excel_file(filepath)
        # Re-encrypt
        try:
            self.model.encrypt_file(filepath)
        except Exception as e:
            logging.warning(f"Error re-encrypting file: {e}")
            messagebox.showwarning("Warning", "Error re-encrypting file.")

    # 2. Combining Data
    def combine_data(self):
        combined_df = self.model.combine_data()
        if combined_df is None or combined_df.empty:
            return
        
        # Just use the CombinedDataController to show the view
        if combined_df is not None and not combined_df.empty:
            unmatched_count = len(self.model.unmatched_data) if self.model.unmatched_data is not None else 0
            self.root.combined_data_controller.show_combined_data()

    def load_combined_data(self):
        combined_df = self.model.load_combined_data()
        if combined_df is not None and not combined_df.empty:
            unmatched_count = len(self.model.unmatched_data) if self.model.unmatched_data is not None else 0
            CombinedDataView(self.root, self, combined_df, unmatched_count=unmatched_count)

    # 3. Display Excel
    def display_in_excel(self):
        filepath = 'combined_matched_data.xlsx'
        if not os.path.exists(filepath):
            messagebox.showerror("Error", "The combined data file does not exist.")
            return
        try:
            if platform.system() == "Darwin":
                os.system(f"open {filepath}")
            elif platform.system() == "Windows":
                os.startfile(filepath)
            else:
                os.system(f"xdg-open {filepath}")
        except Exception as e:
            messagebox.showerror("Error", f"Error opening Excel file: {e}")

    # 4. Show Child Profile (double-click in CombinedDataView)
    def show_child_profile(self, event, view):
        selected_data = view.get_selected_child_data()
        if selected_data is not None:
            from controllers.profile_controller import ProfileController
            profile_controller = ProfileController(self.root, selected_data, self.model)
            profile_controller.show_profile()
        else:
            logging.warning("No child data found for selected item.")

    # 5. Assign Nurse
    def assign_nurse(self, profile_view):
        child_data = profile_view.child_data
        if child_data is None:
            return

        win = tk.Toplevel(profile_view.profile_window)
        win.title("Assign Nurse")
        win.geometry("300x120")

        tk.Label(win, text="Enter Nurse Name:").pack(pady=5)
        nurse_var = tk.StringVar()
        tk.Entry(win, textvariable=nurse_var).pack(pady=5)

        def save_nurse():
            name = nurse_var.get().strip()
            if not name:
                messagebox.showerror("Error", "Nurse name cannot be empty.")
                return
            updated = self.model.update_child_assigned_nurse(child_data, name)
            if updated:
                messagebox.showinfo("Success", f"Nurse '{name}' assigned successfully.")
                profile_view.update_nurse_info(f"Name: {name}")
            else:
                messagebox.showerror("Error", "Failed to assign nurse.")
            win.destroy()

        tk.Button(win, text="Save", command=save_nurse).pack(pady=10)

    # 5(b). Batch Assign
    def batch_assign_nurses(self):
        if self.model.combined_data is None or self.model.combined_data.empty:
            messagebox.showerror("Error", "No data available for batch assignment.")
            return

        window = tk.Toplevel(self.root)
        window.title("Batch Assign Nurses")
        window.geometry("400x300")

        tk.Label(window, text="Filter by City:").pack(pady=5)
        city_var = tk.StringVar()
        tk.Entry(window, textvariable=city_var).pack(pady=5)

        tk.Label(window, text="Filter by State:").pack(pady=5)
        state_var = tk.StringVar()
        tk.Entry(window, textvariable=state_var).pack(pady=5)

        tk.Label(window, text="Filter by ZIP Code:").pack(pady=5)
        zip_var = tk.StringVar()
        tk.Entry(window, textvariable=zip_var).pack(pady=5)

        tk.Label(window, text="Nurse Name:").pack(pady=5)
        nurse_var = tk.StringVar()
        tk.Entry(window, textvariable=nurse_var).pack(pady=5)

        def apply():
            nurse_name = nurse_var.get().strip()
            if not nurse_name:
                messagebox.showerror("Error", "Nurse name is required.")
                return
            city = city_var.get().strip()
            state = state_var.get().strip()
            zipcode = zip_var.get().strip()
            count = self.model.batch_update_nurses(nurse_name, city, state, zipcode)
            if count > 0:
                messagebox.showinfo("Success", f"Nurse '{nurse_name}' assigned to {count} children.")
            else:
                messagebox.showinfo("No Matches", "No records matched the filters.")
            window.destroy()

        tk.Button(window, text="Apply", command=apply).pack(pady=10)

    # 6. Nurse Statistics
    def show_nurse_statistics(self):
        df = self.model.combined_data
        if df is None or df.empty:
            messagebox.showinfo("No Data", "No nurse assignment data to display.")
            return
        if 'Assigned_Nurse' not in df.columns:
            messagebox.showinfo("No Data", "No 'Assigned_Nurse' column in the data.")
            return

        assigned = df[df['Assigned_Nurse'] != 'None']
        if assigned.empty:
            messagebox.showinfo("No Data", "No nurse assignments found.")
            return

        counts = assigned['Assigned_Nurse'].value_counts()
        stats = tk.Toplevel(self.root)
        stats.title("Nurse Statistics")
        stats.geometry("400x400")

        most_assigned = counts.idxmax()
        least_assigned = counts.idxmin()
        tk.Label(stats, text=f"Most Assigned Nurse: {most_assigned} ({counts.max()})", font=("Arial",12)).pack(pady=5)
        tk.Label(stats, text=f"Least Assigned Nurse: {least_assigned} ({counts.min()})", font=("Arial",12)).pack(pady=5)

        tk.Label(stats, text="Assignments by Nurse:", font=("Arial",12,"bold")).pack(pady=5)
        for nurse, c in counts.items():
            lbl = tk.Label(stats, text=f"{nurse}: {c} assignment(s)",
                           fg="blue", cursor="hand2")
            lbl.pack(anchor='w')
            lbl.bind("<Button-1>", lambda e, name=nurse: self.show_children_for_nurse(name))

    def show_children_for_nurse(self, nurse_name):
        df = self.model.combined_data
        assigned_df = df[df['Assigned_Nurse'] == nurse_name]
        if assigned_df.empty:
            messagebox.showinfo("No Data", f"No children assigned to {nurse_name}")
            return

        w = tk.Toplevel(self.root)
        w.title(f"Children assigned to {nurse_name}")
        w.geometry("500x400")

        tree = ttk.Treeview(w, columns=("Name","DOB"), show='headings')
        tree.heading("Name", text="Child's Name")
        tree.heading("DOB", text="DOB")
        tree.column("Name", anchor="center", width=200)
        tree.column("DOB", anchor="center", width=120)
        tree.pack(fill=tk.BOTH, expand=True)

        for _, row in assigned_df.iterrows():
            cname = f"{row.get('Child_First_Name','')} {row.get('Child_Last_Name','')}".strip()
            cdob = row.get('Child_Date_of_Birth','')
            tree.insert("", "end", values=(cname, cdob))

        def open_profile(event):
            sel = tree.selection()
            if not sel:
                return
            name_val, dob_val = tree.item(sel[0], 'values')
            child_data = self.model.find_child_in_combined(name_val, dob_val)
            if child_data is not None:
                ProfileView(self.root, self, child_data)

        tree.bind("<Double-1>", open_profile)

    # 7. Viewing Unmatched
    def view_unmatched_data(self):
        """
        Calls the unmatched data display function from CombinedDataController.
        """
        if self.root.combined_data_controller is not None:
            logging.info("Calling view_unmatched_data in CombinedDataController.")
            self.root.combined_data_controller.view_unmatched_data()
        else:
            logging.error("CombinedDataController is not initialized!")


    # 8. Generating a Report
    def generate_report(self):
        df = self.model.combined_data
        if df is None or df.empty:
            messagebox.showerror("Error", "No data available to generate a report.")
            return

        report_win = tk.Toplevel(self.root)
        report_win.title("Statistical Report")
        report_win.geometry("600x500")

        total = len(df)
        unassigned = len(df[df['Assigned_Nurse'] == 'None'])
        tk.Label(report_win, text=f"Total Children: {total}", font=("Arial",12)).pack(pady=5)
        tk.Label(report_win, text=f"Unassigned Children: {unassigned}", font=("Arial",12)).pack(pady=5)

        df['dob_temp'] = pd.to_datetime(df['Child_Date_of_Birth'], errors='coerce')
        valid = df.dropna(subset=['dob_temp'])
        if not valid.empty:
            today = datetime.today()
            days = valid['dob_temp'].apply(lambda d: (today - d).days)
            avg_yrs = days.mean()/365 if not days.empty else None
            if avg_yrs is not None:
                tk.Label(report_win, text=f"Average Age: {avg_yrs:.1f} years", font=("Arial",12)).pack(pady=5)
            ydx = valid['dob_temp'].idxmax()
            odx = valid['dob_temp'].idxmin()
            if ydx is not None:
                yrow = valid.loc[ydx]
                yn = f"{yrow.get('Child_First_Name','')} {yrow.get('Child_Last_Name','')}"
                tk.Label(report_win, text=f"Youngest Child: {yn}", font=("Arial",12)).pack(pady=5)
            if odx is not None:
                orow = valid.loc[odx]
                on = f"{orow.get('Child_First_Name','')} {orow.get('Child_Last_Name','')}"
                tk.Label(report_win, text=f"Oldest Child: {on}", font=("Arial",12)).pack(pady=5)

        # Nurse assignment counts
        nurse_counts = df['Assigned_Nurse'].value_counts(dropna=False)
        nf = tk.Frame(report_win)
        nf.pack(pady=10, fill=tk.X)
        tk.Label(nf, text="Assignments per Nurse:", font=("Arial",12,"bold")).pack()

        tree = ttk.Treeview(nf, columns=("Nurse","Count"), show="headings", height=5)
        tree.heading("Nurse", text="Nurse")
        tree.heading("Count", text="Count")
        tree.column("Nurse", anchor="center", width=200)
        tree.column("Count", anchor="center", width=80)
        tree.pack(fill=tk.X)

        for nurse, count in nurse_counts.items():
            tree.insert("", "end", values=(nurse, count))

        tk.Button(report_win, text="Export as PDF", command=lambda: self.export_report_to_pdf(df)).pack(pady=10)

    def export_report_to_pdf(self, df):
        try:
            from reportlab.lib.pagesizes import letter
            from reportlab.pdfgen import canvas
            from tkinter import filedialog

            pdf_path = filedialog.asksaveasfilename(defaultextension=".pdf",
                                                    filetypes=[("PDF Files", "*.pdf")],
                                                    title="Save Report As")
            if not pdf_path:
                return

            c = canvas.Canvas(pdf_path, pagesize=letter)
            c.setFont("Helvetica-Bold", 14)
            c.drawString(100, 750, "Statistical Report for Combined Data")
            c.setFont("Helvetica", 12)

            total = len(df)
            unassigned = len(df[df['Assigned_Nurse'] == 'None'])
            c.drawString(100, 730, f"Total Children: {total}")
            c.drawString(100, 710, f"Unassigned Children: {unassigned}")
            # More stats can be added...

            c.save()
            messagebox.showinfo("Success", f"Report saved at {pdf_path}")
        except ImportError:
            messagebox.showerror("Error", "reportlab is not installed.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export PDF: {e}")
