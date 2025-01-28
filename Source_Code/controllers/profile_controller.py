import tkinter as tk
from tkinter import messagebox
import logging
import os
from views.profile_view import ProfileView
import tempfile
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch

class ProfileController:
    def __init__(self, root, child_data, model):
        self.root = root
        self.child_data = child_data
        self.model = model
        self.view = None
        logging.info("ProfileController initialized.")

    def show_profile(self):
        self.view = ProfileView(self.root, self, self.child_data)
        logging.info("Profile view displayed.")

    def assign_nurse(self):
        logging.info("Assign Nurse button clicked.")
        assign_win = tk.Toplevel(self.root)
        assign_win.title(f"Assign Nurse to {self.child_data['Child_First_Name']} {self.child_data['Child_Last_Name']}")
        assign_win.geometry("300x150")

        tk.Label(assign_win, text="Enter Nurse Name:").pack(pady=5)
        nurse_var = tk.StringVar()
        tk.Entry(assign_win, textvariable=nurse_var).pack(pady=5)

        def save_nurse():
            nurse_name = nurse_var.get().strip()
            if nurse_name:
                df = self.model.combined_data
                idx = df[
                    (df['Mother_ID'].astype(str) == str(self.child_data['Mother_ID'])) &
                    (df['Child_First_Name'].str.lower() == self.child_data['Child_First_Name'].lower()) &
                    (df['Child_Last_Name'].str.lower() == self.child_data['Child_Last_Name'].lower()) &
                    (df['Child_Date_of_Birth'] == self.child_data['Child_Date_of_Birth'])
                ].index
                if not idx.empty:
                    df.at[idx[0], 'Assigned_Nurse'] = nurse_name
                    df.to_excel('combined_matched_data.xlsx', index=False)
                    logging.info(f"Assigned Nurse '{nurse_name}'")
                    self.view.update_nurse_info(f"Name: {nurse_name}")
                    # Refresh combined data view
                    if hasattr(self.root, 'combined_data_controller'):
                        self.root.combined_data_controller.refresh_view()
                    messagebox.showinfo("Success", f"Nurse '{nurse_name}' assigned.")
                    assign_win.destroy()
                else:
                    logging.error("No matching record to update.")
                    messagebox.showerror("Error", "Failed to assign nurse.")
            else:
                logging.warning("Nurse name empty.")
                messagebox.showerror("Error", "Nurse name cannot be empty.")

        tk.Button(assign_win, text="Save", command=save_nurse).pack(pady=5)

    def copy_to_clipboard(self):
        mother = self.view.get_mother_info_text()
        child = self.view.get_child_info_text()
        address = self.view.get_address_info_text()
        nurse = self.view.get_nurse_info_text()

        clip_text = (
            f"--- Mother's Information ---\n{mother}\n"
            f"--- Child's Information ---\n{child}\n"
            f"--- Address & Contact ---\n{address}\n"
            f"--- Assigned Nurse ---\n{nurse}\n"
        )
        self.root.clipboard_clear()
        self.root.clipboard_append(clip_text)
        messagebox.showinfo("Copied", "Profile info copied to clipboard.")
        logging.info("Profile info copied to clipboard.")

    def export_profile_to_pdf(self):
        mother = self.view.get_mother_info_text()
        child = self.view.get_child_info_text()
        address = self.view.get_address_info_text()
        nurse = self.view.get_nurse_info_text()
        try:
            pdf_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
            c = canvas.Canvas(pdf_file.name, pagesize=letter)

            def draw_section_header(title, y):
                c.setFont("Helvetica-Bold", 12)
                c.setFillColor(colors.darkblue)
                c.drawString(1 * inch, y, title)
                c.setFillColor(colors.black)
                c.line(1 * inch, y - 2, 7.5 * inch, y - 2)
                return y - 14

            y = 10.5 * inch
            c.setFont("Helvetica", 10)

            # Mother's Info
            y = draw_section_header("Mother's Information", y)
            for line in mother.split('\n'):
                c.drawString(1.2 * inch, y, line.strip())
                y -= 12

            # Child's Info
            y = draw_section_header("Child's Information", y - 10)
            for line in child.split('\n'):
                c.drawString(1.2 * inch, y, line.strip())
                y -= 12

            # Address & Contact
            if address.strip():
                y = draw_section_header("Address & Contact", y - 10)
                for line in address.split('\n'):
                    c.drawString(1.2 * inch, y, line.strip())
                    y -= 12

            # Nurse Info
            if nurse.strip():
                y = draw_section_header("Assigned Nurse", y - 10)
                for line in nurse.split('\n'):
                    c.drawString(1.2 * inch, y, line.strip())
                    y -= 12

            c.save()
            if os.name == 'nt':
                os.startfile(pdf_file.name)
            else:
                os.system(f"open '{pdf_file.name}'")

            logging.info(f"Profile exported to PDF: {pdf_file.name}")
        except Exception as e:
            logging.error(f"Error exporting profile to PDF: {e}")
            messagebox.showerror("Error", f"Error exporting profile: {e}")