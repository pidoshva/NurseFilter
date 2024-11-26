# controllers/profile_controller.py

import tkinter as tk
from tkinter import messagebox
import logging
import os
from views.profile_view import ProfileView
from app_crypto import Crypto
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib import colors
import tempfile

class ProfileController:
    """
    Controller class for child profile view.
    """
    def __init__(self, root, child_data, model):
        self.root = root
        self.child_data = child_data
        self.model = model  # Reference to the DataModel instance
        self.view = None
        logging.info("ProfileController initialized.")

    def show_profile(self):
        self.view = ProfileView(self.root, self, self.child_data)
        logging.info("Profile view displayed.")

    def assign_nurse(self):
        """
        Assign a nurse to the selected child.
        """
        logging.info("Assign Nurse button clicked.")
        assign_window = tk.Toplevel(self.root)
        assign_window.title(f"Assign Nurse to {self.child_data['Child_First_Name']} {self.child_data['Child_Last_Name']}")
        assign_window.geometry("300x150")

        tk.Label(assign_window, text="Enter Nurse Name:").pack(pady=5)
        nurse_name_var = tk.StringVar()
        nurse_entry = tk.Entry(assign_window, textvariable=nurse_name_var)
        nurse_entry.pack(pady=5)

        def save_nurse():
            nurse_name = nurse_name_var.get().strip()
            if nurse_name:
                # Update combined data DataFrame
                index = self.model.combined_data[
                    (self.model.combined_data['Mother_ID'].astype(str) == str(self.child_data['Mother_ID'])) &
                    (self.model.combined_data['Child_First_Name'].str.lower() == self.child_data['Child_First_Name'].lower()) &
                    (self.model.combined_data['Child_Last_Name'].str.lower() == self.child_data['Child_Last_Name'].lower()) &
                    (self.model.combined_data['Child_Date_of_Birth'] == self.child_data['Child_Date_of_Birth'])
                ].index

                if not index.empty:
                    self.model.combined_data.at[index[0], 'Assigned_Nurse'] = nurse_name

                    # Save the updated data
                    self.model.combined_data.to_excel('combined_matched_data.xlsx', index=False)
                    logging.info(f"Assigned Nurse '{nurse_name}' to {self.child_data['Child_First_Name']} {self.child_data['Child_Last_Name']}.")

                    # Update the nurse section in the profile display
                    updated_nurse_text = f"Name: {nurse_name}"
                    self.view.update_nurse_info(updated_nurse_text)

                    messagebox.showinfo("Success", f"Nurse '{nurse_name}' assigned successfully.")
                    assign_window.destroy()
                else:
                    logging.error("Error finding the row to update nurse assignment.")
                    messagebox.showerror("Error", "Failed to assign nurse.")
            else:
                logging.warning("Nurse name is empty.")
                messagebox.showerror("Error", "Nurse name cannot be empty.")

        tk.Button(assign_window, text="Add", command=save_nurse).pack(pady=10)

    def copy_to_clipboard(self):
        """
        Copy the profile information to the clipboard.
        """
        logging.info("Copy to Clipboard button clicked.")
        mother_info_text = self.view.get_mother_info_text()
        child_info_text = self.view.get_child_info_text()
        address_info_text = self.view.get_address_info_text()

        copied_text = (
            f"--- Mother's Information ---\n"
            f"{mother_info_text}\n"
            f"--- Child's Information ---\n"
            f"{child_info_text}\n"
        )

        if address_info_text:
            copied_text += (
                f"--- Address & Contact Information ---\n"
                f"{address_info_text}"
            )

        self.root.clipboard_clear()
        self.root.clipboard_append(copied_text)
        messagebox.showinfo("Info", "Profile info copied to clipboard.")
        logging.info("Profile info successfully copied to clipboard.")

    def export_profile_to_pdf(self):
        """
        Export the profile information to a PDF.
        """
        logging.info("Export to PDF button clicked.")
        mother_info_text = self.view.get_mother_info_text()
        child_info_text = self.view.get_child_info_text()
        address_info_text = self.view.get_address_info_text()
        nurse_info_text = self.view.get_nurse_info_text()

        try:
            # Create a temporary file for the PDF
            pdf_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
            c = canvas.Canvas(pdf_file.name, pagesize=letter)

            # PDF Title and document layout settings
            c.setFont("Helvetica-Bold", 14)
            c.drawString(1 * inch, 10.5 * inch, "Profile Information")
            c.line(1 * inch, 10.45 * inch, 7.5 * inch, 10.45 * inch)
            c.setFont("Helvetica", 10)
            y = 10.2 * inch  # Start position

            # Function to draw a section header
            def draw_section_header(title, ypos):
                c.setFont("Helvetica-Bold", 12)
                c.setFillColor(colors.darkblue)
                c.drawString(1 * inch, ypos, title)
                c.setFillColor(colors.black)
                c.line(1 * inch, ypos - 2, 7.5 * inch, ypos - 2)
                return ypos - 14

            # Draw "Mother's Information" section
            y = draw_section_header("Mother's Information", y)
            c.setFont("Helvetica", 10)
            for line in mother_info_text.strip().split('\n'):
                c.drawString(1.2 * inch, y, line)
                y -= 12

            # Draw "Child's Information" section
            y = draw_section_header("Child's Information", y - 10)
            for line in child_info_text.strip().split('\n'):
                c.drawString(1.2 * inch, y, line)
                y -= 12

            # Draw "Address & Contact Information" section if available
            if address_info_text:
                y = draw_section_header("Address & Contact Information", y - 10)
                for line in address_info_text.strip().split('\n'):
                    c.drawString(1.2 * inch, y, line)
                    y -= 12

            # Draw "Assigned Nurse" section if available
            if nurse_info_text:
                y = draw_section_header("Assigned Nurse", y - 10)
                c.drawString(1.2 * inch, y, nurse_info_text)
                y -= 12

            # Save and close PDF
            c.save()

            # Open the generated PDF
            if os.name == 'nt':  # For Windows
                os.startfile(pdf_file.name)
            else:  # For macOS and Linux
                os.system(f"open {pdf_file.name}")

            logging.info(f"Profile exported to PDF: {pdf_file.name}")

        except Exception as e:
            messagebox.showerror("Error", f"Error exporting profile: {e}")
            logging.error(f"Error exporting profile to PDF: {e}")
