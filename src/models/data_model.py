import logging
import os
import pandas as pd
from tkinter import messagebox
from app_crypto import Crypto
import time

class DataModel:
    """
    Model for handling data logic: reading files, combining data, encryption, unmatched data, etc.
    """

    def __init__(self):
        self.data_frames = []
        self.combined_data = None
        self.unmatched_data = None
        self.duplicate_data = None
        logging.info("DataModel initialized.")

    # Encryption
    def is_file_encrypted(self, filepath, logging=True):
        return Crypto.is_encrypted(filepath, logging)

    def decrypt_file(self, filepath):
        try:
            if not os.path.exists("key.txt"):
                messagebox.showwarning("Error!", "Key does not exist")
                return False
            key = Crypto.loadKey()
            Crypto.decrypt_file(filepath, key)
            logging.info("File decrypted successfully.")
            return True
        except Exception as e:
            logging.error(f"Error decrypting file: {e}")
            messagebox.showerror("Error", f"Error decrypting file: {e}")
            return False

    def encrypt_file(self, filepath):
        try:
            if not os.path.exists("key.txt"):
                messagebox.showwarning("Error!", "Key does not exist")
                return False
            if not os.path.exists(filepath):
                logging.warning(f"Filepath '{filepath}' does not exist; cannot encrypt.")
                return False
            if self.is_file_encrypted(filepath, logging=False):
                logging.warning(f"File '{filepath}' is already encrypted.")
                return False
            key = Crypto.loadKey()
            Crypto.encrypt_file(filepath, key)
            logging.info("File encrypted successfully.")
            return True
        except Exception as e:
            logging.error(f"Error encrypting file: {e}")
            messagebox.showerror("Error", f"Error encrypting file: {e}")
            return False

    # Reading & Combining
    def read_excel_file(self, filepath):
        try:
            data = pd.read_excel(filepath, engine='openpyxl')
            data.columns = [c.replace(" ", "_") for c in data.columns]
            self.data_frames.append(data)
            logging.info(f"Data read from {filepath}")
            return data
        except Exception as e:
            logging.error(f"Error reading '{filepath}': {e}")
            messagebox.showerror("Error", f"Error reading file '{filepath}': {e}")
            return None

    def combine_data(self):
        start_time = time.time()
        if len(self.data_frames) < 2:
            messagebox.showerror("Error", "Please load two Excel files before combining data.")
            return False
        try:
            db_df = self.data_frames[0].copy()
            med_df = self.data_frames[1].copy()

            # Rename columns if needed
            if 'DOB' in db_df.columns:
                db_df.rename(columns={'DOB': 'Child_Date_of_Birth'}, inplace=True)
            if 'Child_DOB' in med_df.columns:
                med_df.rename(columns={'Child_DOB': 'Child_Date_of_Birth'}, inplace=True)
            if 'Last_Name' in med_df.columns:
                med_df.rename(columns={'Last_Name': 'Mother_Last_Name'}, inplace=True)

            # Normalize mother names and create key
            for df in [db_df, med_df]:
                for col in ['Mother_First_Name', 'Mother_Last_Name']:
                    if col in df.columns:
                        df[col] = df[col].astype(str).str.lower().str.replace(r'\W', '', regex=True)
                df['Child_Date_of_Birth'] = pd.to_datetime(df['Child_Date_of_Birth'], errors='coerce').dt.strftime('%Y-%m-%d')
                df['Match_Key'] = (
                    df['Mother_First_Name'] + '_' +
                    df['Mother_Last_Name'] + '_' +
                    df['Child_Date_of_Birth']
                )

            # Merge on optimized hash key
            combined = pd.merge(db_df, med_df, on='Match_Key', how='inner', suffixes=('_db', '_medicaid'))

            # Restore key columns after merge
            for col in ['Mother_First_Name', 'Mother_Last_Name', 'Child_Date_of_Birth']:
                if col + '_db' in combined.columns:
                    combined[col] = combined[col + '_db']
                    combined.drop([col + '_db', col + '_medicaid'], axis=1, errors='ignore', inplace=True)

            # Identify duplicates in the combined dataset
            duplicate_rows = combined[combined.duplicated(subset=['Mother_ID', 'Child_First_Name', 'Child_Last_Name'], keep=False)].copy()
            if not duplicate_rows.empty:
                duplicate_rows.to_excel('duplicate_names.xlsx', index=False)
                self.duplicate_data = duplicate_rows
            else:
                self.duplicate_data = pd.DataFrame()

            # Identify unmatched records
            matched_keys = set(combined['Match_Key'])
            unmatched_db = db_df[~db_df['Match_Key'].isin(matched_keys)].copy()
            unmatched_db['Source'] = 'Database'
            unmatched_med = med_df[~med_df['Match_Key'].isin(matched_keys)].copy()
            unmatched_med['Source'] = 'Medicaid'

            if not unmatched_db.empty or not unmatched_med.empty:
                unmatched = pd.concat([unmatched_db, unmatched_med], ignore_index=True)
                for col in ['Mother_First_Name', 'Mother_Last_Name', 'Child_First_Name', 'Child_Last_Name']:
                    if col in unmatched.columns:
                        unmatched[col] = unmatched[col].str.capitalize()
                unmatched.to_excel('unmatched_data.xlsx', index=False)
                self.unmatched_data = unmatched
            else:
                self.unmatched_data = pd.DataFrame()

            # Capitalize combined columns
            for col in ['Mother_First_Name', 'Mother_Last_Name', 'Child_First_Name', 'Child_Last_Name']:
                if col in combined.columns:
                    combined[col] = combined[col].astype(str).str.capitalize()

            # Ensure Assigned_Nurse exists and is filled
            if 'Assigned_Nurse' in combined.columns:
                combined['Assigned_Nurse'] = combined['Assigned_Nurse'].fillna('None')
            else:
                combined['Assigned_Nurse'] = 'None'

            combined.drop(columns=['Match_Key'], inplace=True, errors='ignore')
            combined.to_excel('combined_matched_data.xlsx', index=False)
            self.combined_data = combined
        
            end_time = time.time()
            elapsed = end_time - start_time

            print(elapsed)

            return True

        except Exception as e:
            logging.error(f"Error combining data: {e}")
            messagebox.showerror("Error", f"Error combining data: {e}")
            return False


    def load_combined_data(self):
        path = 'combined_matched_data.xlsx'
        if not os.path.exists(path):
            messagebox.showerror("Error", "No combined data file found. Please combine data first.")
            return False

        try:
            if self.is_file_encrypted(path):
                self.decrypt_file(path)

            df = pd.read_excel(path)

            # Check and set 'Assigned_Nurse' column to None if it has no value
            if 'Assigned_Nurse' in df.columns:
                df['Assigned_Nurse'] = df['Assigned_Nurse'].fillna('None')

            self.combined_data = df

            unmatched_path = 'unmatched_data.xlsx'
            if os.path.exists(unmatched_path):
                self.unmatched_data = pd.read_excel(unmatched_path)
            else:
                self.unmatched_data = pd.DataFrame()

            duplicate_path = 'duplicate_names.xlsx'
            if os.path.exists(duplicate_path):
                self.duplicate_data = pd.read_excel(duplicate_path)
            else:
                self.duplicate_data = pd.DataFrame()

            return True

        except Exception as e:
            messagebox.showerror("Error", f"Failed to load combined data: {e}")
            return False


    # Nurse assignment
    def update_child_assigned_nurse(self, child_data, nurse_name):
        if self.combined_data is None or self.combined_data.empty:
            return False
        mother_id = child_data.get('Mother_ID')
        fn = child_data.get('Child_First_Name','')
        ln = child_data.get('Child_Last_Name','')
        dob = child_data.get('Child_Date_of_Birth','')

        matches = self.combined_data[
            (self.combined_data['Mother_ID'].astype(str) == str(mother_id)) &
            (self.combined_data['Child_First_Name'].str.lower() == fn.lower()) &
            (self.combined_data['Child_Last_Name'].str.lower() == ln.lower()) &
            (self.combined_data['Child_Date_of_Birth'] == dob)
        ]
        if matches.empty:
            return False

        idx = matches.index[0]
        self.combined_data.at[idx, 'Assigned_Nurse'] = nurse_name
        self.combined_data.to_excel('combined_matched_data.xlsx', index=False)
        return True

    def batch_update_nurses(self, nurse_name, city, state, zipcode):
        if self.combined_data is None or self.combined_data.empty:
            return 0

        df = self.combined_data
        def match_filter(row):
            c_ok = (not city) or (str(row.get('City','')).lower() == city.lower())
            s_ok = (not state) or (str(row.get('State','')).lower() == state.lower())
            z_ok = (not zipcode) or (str(row.get('ZIP','')) == zipcode)
            return c_ok and s_ok and z_ok

        mask = df.apply(match_filter, axis=1)
        count = mask.sum()
        if count == 0:
            return 0

        self.combined_data.loc[mask, 'Assigned_Nurse'] = nurse_name
        self.combined_data.to_excel('combined_matched_data.xlsx', index=False)
        return count

    def find_child_in_combined(self, full_name, dob):
        if self.combined_data is None:
            return None
        parts = full_name.split()
        if len(parts) < 2:
            return None
        fn, ln = parts[0], parts[1]
        row = self.combined_data[
            (self.combined_data['Child_First_Name'].str.lower() == fn.lower()) &
            (self.combined_data['Child_Last_Name'].str.lower() == ln.lower()) &
            (self.combined_data['Child_Date_of_Birth'] == dob)
        ]
        if row.empty:
            return None
        return row.iloc[0]
    
    def updated_data(self):
        """
        Return the current state of the combined data and unmatched data DataFrames.
        """
        path = 'combined_matched_data.xlsx'
        if not os.path.exists(path):
            messagebox.showerror("Error", "No combined data file found. Cannot Refresh")
            return False
        
        try:

            df = pd.read_excel(path)

            # Check and set 'Assigned_Nurse' column to None if it has no value
            if 'Assigned_Nurse' in df.columns:
                df['Assigned_Nurse'] = df['Assigned_Nurse'].fillna('None')

            self.combined_data = df

            unmatched_path = 'unmatched_data.xlsx'
            if os.path.exists(unmatched_path):
                self.unmatched_data = pd.read_excel(unmatched_path)
            else:
                self.unmatched_data = pd.DataFrame()

            duplicate_path = 'duplicate_names.xlsx'
            if os.path.exists(duplicate_path):
                self.duplicate_data = pd.read_excel(duplicate_path)
            else:
                self.duplicate_data = pd.DataFrame()

            return self.combined_data
        
        except Exception as e:
            messagebox.showerror("Error", f"Failed to refresh combined data: {e}")
            return None
