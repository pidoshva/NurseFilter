# models/data_model.py

import pandas as pd
import os
from tkinter import messagebox, filedialog
import logging
from app_crypto import Crypto

class DataModel:
    """
    Model class responsible for data operations.
    """
    def __init__(self):
        self.data_frames = []
        self.combined_data = None
        self.unmatched_data = None
        logging.info("DataModel initialized.")

    def read_excel_file(self, filepath):
        logging.info(f"Attempting to read Excel file: {filepath}")
        try:
            # Read the Excel file into a DataFrame and normalize column names
            data = pd.read_excel(filepath, engine='openpyxl')
            data.columns = [column.replace(" ", "_") for column in data.columns]
            logging.info(f"Successfully read file: {filepath}")
            self.data_frames.append(data)
            return data
        except Exception as e:
            logging.error(f"Error reading file '{filepath}': {e}")
            messagebox.showerror("Error", f"Error reading file '{filepath}': {e}")
            return None

    def combine_data(self):
        logging.info("Starting data combination process.")
        try:
            # Ensure there are exactly two data frames
            if len(self.data_frames) < 2:
                logging.error("Not enough data frames to combine. Need at least two.")
                messagebox.showerror("Error", "Please load two Excel files before combining data.")
                return None

            # Extract the two data frames
            database_data = self.data_frames[0]
            medicaid_data = self.data_frames[1]

            # Standardize columns for merging
            logging.info("Standardizing column names for merging.")
            database_data.rename(columns={'DOB': 'Child_Date_of_Birth'}, inplace=True)
            medicaid_data.rename(columns={'Child_DOB': 'Child_Date_of_Birth', 'Last_Name': 'Mother_Last_Name'}, inplace=True)

            # Normalize the names for matching
            logging.info("Normalizing names for matching.")
            for df in [database_data, medicaid_data]:
                for col in ['Mother_First_Name', 'Mother_Last_Name']:
                    df[col] = df[col].str.lower().str.replace(r'\W', '', regex=True)

            # Convert DOB columns to consistent date format
            logging.info("Converting 'Child_Date_of_Birth' columns to datetime format.")
            database_data['Child_Date_of_Birth'] = pd.to_datetime(database_data['Child_Date_of_Birth'], errors='coerce').dt.strftime('%Y-%m-%d')
            medicaid_data['Child_Date_of_Birth'] = pd.to_datetime(medicaid_data['Child_Date_of_Birth'], errors='coerce').dt.strftime('%Y-%m-%d')

            # Merge to get combined data
            logging.info("Merging data frames on 'Mother_First_Name', 'Mother_Last_Name', and 'Child_Date_of_Birth'.")
            combined_data = pd.merge(
                database_data,
                medicaid_data,
                on=['Mother_First_Name', 'Mother_Last_Name', 'Child_Date_of_Birth'],
                how='inner',
                suffixes=('_db', '_medicaid')
            )
            logging.info("Matched data combined successfully.")

            # Identify unmatched data
            logging.info("Identifying unmatched data from the database.")
            unmatched_database = database_data[~database_data.apply(
                lambda row: ((combined_data['Mother_First_Name'] == row['Mother_First_Name']) &
                             (combined_data['Mother_Last_Name'] == row['Mother_Last_Name']) &
                             (combined_data['Child_Date_of_Birth'] == row['Child_Date_of_Birth'])).any(), axis=1)].copy()
            unmatched_database['Source'] = 'Database'

            logging.info("Identifying unmatched data from Medicaid.")
            unmatched_medicaid = medicaid_data[~medicaid_data.apply(
                lambda row: ((combined_data['Mother_First_Name'] == row['Mother_First_Name']) &
                             (combined_data['Mother_Last_Name'] == row['Mother_Last_Name']) &
                             (combined_data['Child_Date_of_Birth'] == row['Child_Date_of_Birth'])).any(), axis=1)].copy()
            unmatched_medicaid['Source'] = 'Medicaid'

            # Check if there are unmatched rows in either data frame
            if not unmatched_database.empty or not unmatched_medicaid.empty:
                logging.info("Processing unmatched data.")

                # Standardize unmatched data columns to align with combined_data
                unmatched_database = unmatched_database.reindex(columns=combined_data.columns.tolist() + ['Source'], fill_value='')
                unmatched_medicaid = unmatched_medicaid.reindex(columns=combined_data.columns.tolist() + ['Source'], fill_value='')

                # Concatenate unmatched records
                unmatched_data = pd.concat([unmatched_database, unmatched_medicaid], ignore_index=True)

                # Capitalize all names in unmatched data
                for col in ['Mother_First_Name', 'Mother_Last_Name', 'Child_First_Name', 'Child_Last_Name']:
                    if col in unmatched_data.columns:
                        unmatched_data[col] = unmatched_data[col].str.capitalize()

                # Save the unmatched data to an Excel file
                unmatched_file_path = 'unmatched_data.xlsx'
                unmatched_data.to_excel(unmatched_file_path, index=False)
                logging.info(f"Unmatched data saved to {unmatched_file_path}")
                self.unmatched_data = unmatched_data
            else:
                logging.info("No unmatched data found; skipping unmatched data file creation.")

            # Capitalize all names in matched data
            for col in ['Mother_First_Name', 'Mother_Last_Name', 'Child_First_Name', 'Child_Last_Name']:
                if col in combined_data.columns:
                    combined_data[col] = combined_data[col].str.capitalize()

            # Save the matched data
            matched_file_path = 'combined_matched_data.xlsx'
            combined_data.to_excel(matched_file_path, index=False)
            logging.info(f"Matched data saved to {matched_file_path}")

            # Store the combined data in the model
            self.combined_data = combined_data

            return combined_data

        except Exception as e:
            logging.error(f"Error combining data: {e}")
            messagebox.showerror("Error", f"Error combining data: {e}")
            return None

    def load_combined_data(self):
        logging.info("Attempting to load combined data.")
        file_path = 'combined_matched_data.xlsx'
        if not os.path.exists(file_path):
            messagebox.showerror("Error", "No combined data file found. Please combine data first.")
            logging.error("No combined data file found.")
            return None

        try:
            if Crypto.is_encrypted(file_path):
                logging.info("Combined data file is encrypted. Decrypting...")
                Crypto.decrypt_file(file_path, Crypto.loadKey())
                logging.info("File decrypted successfully.")

            # Load the existing combined data
            self.combined_data = pd.read_excel(file_path)
            logging.info("Successfully loaded combined data from 'combined_matched_data.xlsx'")
            return self.combined_data

        except Exception as e:
            messagebox.showerror("Error", f"Failed to load combined data file: {e}")
            logging.error(f"Failed to load combined data file: {e}")
            return None


    def decrypt_file(self, filepath=None):
        logging.info("Attempting to decrypt file.")

        if filepath is None:
            filepath = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx *.xls")])

        if not os.path.exists("key.txt"):
            messagebox.showwarning("Error!", "Key does not exist")
        else:
            try:
                key = Crypto.loadKey()
                Crypto.decrypt_file(filepath, key)
                logging.info("File decrypted successfully.")
                return True
            except Exception as e:
                logging.error(f"Error decrypting file: {e}")
                messagebox.showerror("Error", f"Error decrypting file: {e}")
                return False

    def encrypt_file(self, filepath=None):
        logging.info("Attempting to encrypt file.")

        if not os.path.exists("key.txt"):
            messagebox.showwarning("Error!", "Key does not exist")
        else:
            try:
                if filepath is None:
                    filepath = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx *.xls")])

                if not os.path.exists(filepath):
                    logging.warning(f"Filepath {filepath} does not exist, cannot encrypt")
                    return False

                key = Crypto.loadKey()
                Crypto.encrypt_file(filepath, key)
                logging.info("File encrypted successfully.")
                return True
            except Exception as e:
                logging.error(f"Error encrypting file: {e}")
                messagebox.showerror("Error", f"Error encrypting file: {e}")
                return False

    def generate_encryption_key(self):
        logging.info("Attempting to generate encryption key.")

        if not os.path.exists("key.txt") or os.stat("key.txt").st_size <= 0:
            try:
                Crypto.generateKey()
                messagebox.showinfo("Success", "Encryption key generated.")
                logging.info("Encryption key generated successfully.")
            except Exception as e:
                logging.error(f"Error generating encryption key: {e}")
                messagebox.showerror("Error", f"Error generating encryption key: {e}")
        else:
            logging.warning("Encryption key already exists.")
            messagebox.showerror("Error", "To generate a new key, delete the previous key.")

    def delete_encryption_key(self):
        logging.info("Attempting to delete encryption key.")
        answer = messagebox.askquestion(
            "WARNING!",
            "Are you sure you want to proceed? Any file encrypted with this key will become permanently unusable."
        )
        if answer == 'no':
            logging.info("Action aborted by user.")
            return
        if os.path.exists("key.txt"):
            os.remove("key.txt")
            logging.info("Encryption key successfully deleted.")
            messagebox.showinfo("Success", "Encryption key successfully deleted.")
        else:
            logging.warning("Encryption key does not exist.")
            messagebox.showerror("Error", "No encryption key exists.")
