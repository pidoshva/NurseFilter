import logging
import pandas as pd
from tkinter import messagebox
from models.data_model import DataModel
from views.statistical_view import StatisticalView
from views.nurse_statistics_view import NursesStatisticalView
from views.batch_assign_view import BatchAssignView
from views.assign_nurse_view import AssignNurseView


class NurseController:
    def __init__(self, root, model: DataModel, main_controller):
        self.main_controller = main_controller
        self.root = root
        self.model = model
        self.report_view = None
        self.nurse_stats_view = None
        self.batch_assign_view = None
        self.assign_nurse_view = None
        logging.info("NurseController initialized.")

    def generate_report(self):
        df = self.model.combined_data
        if df is None or df.empty:
            messagebox.showerror("Error", "No data available to generate a report.")
            return
        
        # Ensure 'Assigned_Nurse' column exists and replace NaN with 'None'
        if 'Assigned_Nurse' not in df.columns:
            messagebox.showerror("Error", "No 'Assigned_Nurse' column found in data.")
            return
        
        return self._show_report()
    
        
    def _show_report(self):
        view = StatisticalView(self.root, self)
        frame = view.display(self.model.combined_data)
        self.main_controller.add_tab(frame, "Statistical Report")
        self.report_view = frame
        logging.info("StatisticalView displayed.")
        return frame
        
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
            c.drawString(100, 750, "Statistical Report")
            c.setFont("Helvetica", 12)

            total_children = len(df)
            assigned_count = len(df[df['Assigned_Nurse'] != 'None'])
            unassigned_count = total_children - assigned_count
            assigned_percentage = (assigned_count / total_children * 100) if total_children > 0 else 0
            unassigned_percentage = 100 - assigned_percentage

            c.drawString(100, 730, f"Total Children: {total_children}")
            c.drawString(100, 710, f"Total Nurses Assigned: {df['Assigned_Nurse'].nunique()}")
            c.drawString(100, 690, f"Children Assigned to Nurses: {assigned_count} ({assigned_percentage:.1f}%)")
            c.drawString(100, 670, f"Unassigned Children: {unassigned_count} ({unassigned_percentage:.1f}%)")

            df['dob_temp'] = pd.to_datetime(df['Child_Date_of_Birth'], errors='coerce')
            valid_ages = df.dropna(subset=['dob_temp'])
            if not valid_ages.empty:
                today = pd.Timestamp.today()
                avg_age_years = (today - valid_ages['dob_temp']).dt.days.mean() / 365
                c.drawString(100, 650, f"Average Age: {avg_age_years:.1f} years")

                youngest = valid_ages.loc[valid_ages['dob_temp'].idxmax()]
                oldest = valid_ages.loc[valid_ages['dob_temp'].idxmin()]
                c.drawString(100, 630, f"Youngest: {youngest['Child_First_Name']} {youngest['Child_Last_Name']} ({youngest['Child_Date_of_Birth']})")
                c.drawString(100, 610, f"Oldest: {oldest['Child_First_Name']} {oldest['Child_Last_Name']} ({oldest['Child_Date_of_Birth']})")

            if 'City' in df.columns:
                town_counts = df['City'].value_counts().head(5)
                c.drawString(100, 590, "Children per Town:")
                y_position = 570
                for town, count in town_counts.items():
                    c.drawString(120, y_position, f"{town}: {count} children")
                    y_position -= 20

            c.save()
            messagebox.showinfo("Success", f"Report saved at {pdf_path}")
        except ImportError:
            messagebox.showerror("Error", "reportlab is not installed.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export PDF: {e}")

    def show_nurse_statistics(self):
        """
        Display nurse statistics window
        """
        df = self.model.combined_data
        if df is None or df.empty:
            messagebox.showinfo("No Data", "No nurse assignment data to display.")
            return
        if 'Assigned_Nurse' not in df.columns:
            messagebox.showinfo("No Data", "No 'Assigned_Nurse' column in the data.")
            return

        assigned = df[df['Assigned_Nurse'].notna() & (df['Assigned_Nurse'] != 'None')]
        if assigned.empty:
            messagebox.showinfo("No Data", "No nurse assignments found.")
            return

        return self._show_nurse_stats(assigned)


    def _show_nurse_stats(self, assigned):
        """
        Show nurse statistics window
        """
        frame = NursesStatisticalView(self.root, self).display(assigned)
        self.main_controller.add_tab(frame, "Nurse Statistics")
        self.nurse_stats_view = frame
        logging.info("NursesStatisticalView displayed.")


    def batch_assign_nurses(self, refresh_view_callback):
        """Handle batch nurse assignment"""
        if self.model.combined_data is None or self.model.combined_data.empty:
            messagebox.showerror("Error", "No data available for batch assignment.")
            return
        
        logging.info("BatchAssignView displayed.")
        frame = BatchAssignView(self.root, self, self.model.batch_update_nurses, refresh_view_callback).display()
        self.main_controller.add_tab(frame, "Batch Assign Nurses")
        self.batch_assign_view = frame
        return frame


    def assign_nurse(self, child_data, update_callback):
        frame = AssignNurseView(self.root, self, child_data, update_callback).display()
        self.main_controller.add_tab(frame, "Assign Nurse")
        self.assign_nurse_view = frame
        return frame

    def save_nurse(self, nurse_name, child_data, update_callback, close_window_callback):
        if nurse_name:
            df = self.model.combined_data
            idx = df[
                (df['Mother_ID'].astype(str) == str(child_data['Mother_ID'])) &
                (df['Child_First_Name'].str.lower() == child_data['Child_First_Name'].lower()) &
                (df['Child_Last_Name'].str.lower() == child_data['Child_Last_Name'].lower()) &
                (df['Child_Date_of_Birth'] == child_data['Child_Date_of_Birth'])
            ].index
            if not idx.empty:
                df.at[idx[0], 'Assigned_Nurse'] = nurse_name
                df.to_excel('combined_matched_data.xlsx', index=False)
                logging.info(f"Assigned Nurse '{nurse_name}'")
                
                update_callback(f"Name: {nurse_name}")
                # messagebox.showinfo("Success", f"Nurse '{nurse_name}' assigned.")
                close_window_callback()
            else:
                logging.error("No matching record to update.")
                messagebox.showerror("Error", "Failed to assign nurse.")
        else:
            logging.warning("Nurse name empty.")
            messagebox.showerror("Error", "Nurse name cannot be empty.")
    
    def close_report(self):
        if self.report_view:
            self.main_controller.remove_tab(self.report_view)
            self.report_view = None

    def close_nurse_stats(self):
        if self.nurse_stats_view:
            self.main_controller.remove_tab(self.nurse_stats_view)
            self.nurse_stats_view = None
    
    def close_batch_assign(self):
        if self.batch_assign_view:
            self.main_controller.remove_tab(self.batch_assign_view)
            self.batch_assign_view = None
    
    def close_assign_nurse(self):
        if self.assign_nurse_view:
            self.main_controller.remove_tab(self.assign_nurse_view)
            self.assign_nurse_view = None