from tkinter import messagebox
import logging
import os
from views.profile_view import ProfileView
import tempfile
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
import pandas as pd
from datetime import datetime

class ProfileController:
    def __init__(self, root, child_data, model, main_controller, update_callback):
        self.main_controller = main_controller 
        self.root = root
        self.child_data = child_data
        self.model = model
        self.update_callback = update_callback
        self.view = None
        self.visit_log_path = "nurse_log.xlsx"
        logging.info("ProfileController initialized.")

    def show_profile(self):
        self.view = ProfileView(self.root, self, self.child_data)
        frame = self.view.create_widgets()
        self.main_controller.add_tab(frame, self.view.get_title())
        return frame

    def assign_nurse(self, child_data, update_callback):
        logging.info("Assign Nurse button clicked.")

        def both_callback(new_name):
            child_data['Assigned_Nurse'] = new_name # Update current profile’s nurse
            self.child_data['Assigned_Nurse'] = new_name # Also update in this controller
            update_callback(new_name)
            self.update_callback()  # Refresh combined data view

        return self.main_controller.assign_nurse(child_data, both_callback)

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

            # Visit Log
            path = "nurse_log.xlsx"
            mother_id = str(self.child_data.get("Mother_ID", ""))
            first = self.child_data.get("Child_First_Name", "").lower()
            last = self.child_data.get("Child_Last_Name", "").lower()
            if os.path.exists(path):
                df = pd.read_excel(path)
                filtered = df[
                    (df["Mother_ID"].astype(str) == mother_id) &
                    (df["Child_First_Name"].str.lower() == first) &
                    (df["Child_Last_Name"].str.lower() == last)
                ]

                if not filtered.empty:
                    y = draw_section_header("Nurse Visit Log", y - 10)
                    c.setFont("Helvetica-Bold", 10)
                    c.drawString(1.2 * inch, y, f"{'Nurse Name':<25} {'Visit Time'}")
                    y -= 12
                    c.setFont("Helvetica", 10)
                    for _, row in filtered.iterrows():
                        c.drawString(1.2 * inch, y, f"{row['Nurse_Name']:<25} {row['Visit_Time']}")
                        y -= 12
                        if y < 1 * inch:
                            c.showPage()
                            y = 10.5 * inch
                            c.setFont("Helvetica", 10)

            c.save()
            if os.name == 'nt':
                os.startfile(pdf_file.name)
            else:
                os.system(f"open '{pdf_file.name}'")

            logging.info(f"Profile exported to PDF: {pdf_file.name}")
        except Exception as e:
            logging.error(f"Error exporting profile to PDF: {e}")
            messagebox.showerror("Error", f"Error exporting profile: {e}")

    def close(self):
        if self.view:
            self.main_controller.remove_tab(self.view.get_frame())
            self.view = None

    def log_nurse_visit(self, child_data, nurse_name=None, visit_time=None):
        log_file = "nurse_log.xlsx"
        if not nurse_name:
            nurse_name = child_data.get("Assigned_Nurse", "Unknown Nurse")
        if not visit_time:
            visit_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        visit_entry = {
            "Mother_ID": child_data.get("Mother_ID", "N/A"),
            "Child_First_Name": child_data.get("Child_First_Name", "N/A"),
            "Child_Last_Name": child_data.get("Child_Last_Name", "N/A"),
            "Nurse_Name": nurse_name,
            "Visit_Time": visit_time
        }

        if os.path.exists(log_file):
            df = pd.read_excel(log_file)
        else:
            df = pd.DataFrame(columns=["Visit_ID", "Mother_ID", "Child_First_Name", "Child_Last_Name", "Nurse_Name", "Visit_Time"])

        # 🛠 Assign correct Visit ID (not scientific format)
        next_id = 1 if df.empty else int(df["Visit_ID"].max()) + 1
        visit_entry["Visit_ID"] = next_id

        df = pd.concat([df, pd.DataFrame([visit_entry])], ignore_index=True)
        df.to_excel(log_file, index=False)

        # Refresh view
        if self.view:
            self.view.update_visit_log()


    def get_nurse_visits(self, child_data):
        if not os.path.exists(self.visit_log_path):
            return []

        df = pd.read_excel(self.visit_log_path)
        filtered = df[
            (df['Mother_ID'] == child_data.get("Mother_ID")) &
            (df['Child_First_Name'].str.lower() == str(child_data.get("Child_First_Name", "")).lower()) &
            (df['Child_Last_Name'].str.lower() == str(child_data.get("Child_Last_Name", "")).lower())
        ]
        return filtered.to_dict(orient='records')
