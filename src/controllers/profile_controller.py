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
    def __init__(self, root, child_data, model, main_controller, update_callback):
        self.main_controller = main_controller 
        self.root = root
        self.child_data = child_data
        self.model = model
        self.update_callback = update_callback
        self.view = None
        logging.info("ProfileController initialized.")

    def show_profile(self):
        self.view = ProfileView(self.root, self, self.child_data)
        return (self.view.get_frame(), self.view.get_title())

    def assign_nurse(self, child_data, update_callback):
        logging.info("Assign Nurse button clicked.")
        
        def both_callback(e):
            update_callback(e)
            self.update_callback()

        self.main_controller.assign_nurse(child_data, both_callback)

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

    def close(self):
        if self.view:
            self.main_controller.remove_tab(self.view.get_frame())
            self.view = None
