import logging
import os
import pandas as pd
from tkinter import messagebox
from app_crypto import Crypto
import time
import polars as pl

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
    def read_excel_file(self, filepath, progress_callback=None, file_type=None):
        """
        Read an Excel file and store the data.
        
        Args:
            filepath: Path to the Excel file
            progress_callback: Optional callback for progress updates
            file_type: Type of file being read ("Database" or "Medicaid")
            
        Returns:
            The pandas DataFrame if successful, None otherwise
        """
        try:
            # Report initial progress
            if progress_callback:
                progress_callback("Checking file", 10)
                
            # Check if the file exists
            if not os.path.exists(filepath):
                if progress_callback:
                    progress_callback("File not found", 100)
                return None
                
            # Check file size and handle large files
            file_size = os.path.getsize(filepath)
            if file_size > 5_000_000:  # 5MB
                if progress_callback:
                    progress_callback("Reading large file", 20)
                    
            # Check and decrypt if needed
            if self.is_file_encrypted(filepath, logging=False):
                if progress_callback:
                    progress_callback("Decrypting file", 30)
                if not self.decrypt_file(filepath):
                    return None
                    
            # Report progress before reading
            if progress_callback:
                progress_callback("Reading data", 40)
                
            # Read the Excel file
            data = pd.read_excel(filepath, engine='openpyxl')
            
            # Report progress after reading
            if progress_callback:
                progress_callback("Processing data", 70)
                
            # Process column names
            data.columns = [c.replace(" ", "_") for c in data.columns]
            
            # Store the data frame along with its type
            self.data_frames.append(data)
            
            # Store file type information
            if not hasattr(self, 'file_types'):
                self.file_types = []
            self.file_types.append(file_type or ("Database" if len(self.file_types) == 0 else "Medicaid"))
            
            # Final progress
            if progress_callback:
                progress_callback("Completed", 100)
                
            logging.info(f"Data read from {filepath} as {self.file_types[-1]} file")
            return data
            
        except Exception as e:
            logging.error(f"Error reading '{filepath}': {e}")
            
            # Report error
            if progress_callback:
                progress_callback("Error reading file", 100)
                
            messagebox.showerror("Error", f"Error reading file")
            return None

    def combine_data(self):
        start_time = time.time()

        if len(self.data_frames) < 2:
            messagebox.showerror("Error", "Please load two Excel files before combining data.")
            return False

        try:
            # Convert to Polars
            db_df = pl.from_pandas(self.data_frames[0].copy())
            med_df = pl.from_pandas(self.data_frames[1].copy())

            # Rename columns for consistency
            if "DOB" in db_df.columns:
                db_df = db_df.rename({"DOB": "Child_Date_of_Birth"})
            if "Child_DOB" in med_df.columns:
                med_df = med_df.rename({"Child_DOB": "Child_Date_of_Birth"})
            if "Last_Name" in med_df.columns:
                med_df = med_df.rename({"Last_Name": "Mother_Last_Name"})

            # Normalize + generate Match_Key
            def normalize(df):
                return df.with_columns([
                    pl.col("Mother_First_Name").cast(pl.Utf8).str.to_lowercase().str.replace_all(r"\W", ""),
                    pl.col("Mother_Last_Name").cast(pl.Utf8).str.to_lowercase().str.replace_all(r"\W", ""),
                    pl.col("Child_Date_of_Birth").cast(pl.Utf8).str.strip_chars().str.strptime(pl.Date, "%Y-%m-%d", strict=False).cast(pl.Utf8),
                ]).with_columns([
                    (pl.col("Mother_First_Name") + "_" +
                    pl.col("Mother_Last_Name") + "_" +
                    pl.col("Child_Date_of_Birth")).alias("Match_Key")
                ])

            db_df = normalize(db_df)
            med_df = normalize(med_df)

            # Join on Match_Key using Polars
            combined = db_df.join(med_df, on="Match_Key", how="inner", suffix="_medicaid")

            # Drop duplicate `_medicaid` columns
            for col in ["Mother_First_Name", "Mother_Last_Name", "Child_Date_of_Birth"]:
                if f"{col}_medicaid" in combined.columns:
                    combined = combined.drop(f"{col}_medicaid")

            # Add Assigned_Nurse if missing
            if "Assigned_Nurse" not in combined.columns:
                combined = combined.with_columns(pl.lit("None").alias("Assigned_Nurse"))

            # Capitalize child names
            for col in ["Mother_First_Name", "Mother_Last_Name", "Child_First_Name", "Child_Last_Name"]:
                if col in combined.columns:
                    combined = combined.with_columns(pl.col(col).str.to_titlecase())

            # Convert back to Pandas
            combined_df = combined.drop("Match_Key").to_pandas()

            # Detect duplicates with Pandas
            duplicate_df = combined_df[combined_df.duplicated(
                subset=["Mother_ID", "Child_First_Name", "Child_Last_Name"], keep=False)].copy()
            if not duplicate_df.empty:
                duplicate_df.to_excel("duplicate_names.xlsx", index=False)
                self.duplicate_data = duplicate_df
            else:
                self.duplicate_data = pd.DataFrame()

            # Detect unmatched records using hash key
            db_df_pd = db_df.to_pandas()
            med_df_pd = med_df.to_pandas()
            combined_keys = set(combined_df["Mother_First_Name"].str.lower().str.replace(r'\W', '', regex=True) + "_" +
                                combined_df["Mother_Last_Name"].str.lower().str.replace(r'\W', '', regex=True) + "_" +
                                combined_df["Child_Date_of_Birth"])

            unmatched_db = db_df_pd[~db_df_pd["Match_Key"].isin(combined_keys)].copy()
            unmatched_db["Source"] = "Database"

            unmatched_med = med_df_pd[~med_df_pd["Match_Key"].isin(combined_keys)].copy()
            unmatched_med["Source"] = "Medicaid"

            unmatched = pd.concat([unmatched_db, unmatched_med], ignore_index=True) if not unmatched_db.empty or not unmatched_med.empty else pd.DataFrame()
            if not unmatched.empty:
                for col in ['Mother_First_Name', 'Mother_Last_Name', 'Child_First_Name', 'Child_Last_Name']:
                    if col in unmatched.columns:
                        unmatched[col] = unmatched[col].astype(str).str.capitalize()
                unmatched.to_excel("unmatched_data.xlsx", index=False)
            self.unmatched_data = unmatched

            # Save and assign
            combined_df.to_excel("combined_matched_data.xlsx", index=False)
            self.combined_data = combined_df

            print(f"Polars + Pandas combine_data execution time: {time.time() - start_time:.4f} sec")
            return True

        except Exception as e:
            logging.error(f"Error combining data with Polars: {e}")
            messagebox.showerror("Error", f"Error combining data: {e}")
            return False


    def load_combined_data(self, filepath='combined_matched_data.xlsx', progress_callback=None):
        """Load the combined data from the saved Excel file.
        
        Args:
            progress_callback: Optional callback for progress updates
            
        Returns:
            True if successful, False otherwise
        """
        path = filepath
        
        # Initial progress
        if progress_callback:
            progress_callback("Checking file", 10)
            
        if not os.path.exists(path):
            if progress_callback:
                progress_callback("File not found", 100)
            messagebox.showerror("Error", "No combined data file found. Please combine data first.")
            return False

        try:
            # Check encryption
            if progress_callback:
                progress_callback("Checking encryption", 20)
                
            if self.is_file_encrypted(path):
                if progress_callback:
                    progress_callback("Decrypting file", 30)
                self.decrypt_file(path)

            # Read data
            if progress_callback:
                progress_callback("Reading data", 40)
                
            df = pd.read_excel(path)

            # Process data
            if progress_callback:
                progress_callback("Processing data", 60)
                
            # Check and set 'Assigned_Nurse' column to None if it has no value
            if 'Assigned_Nurse' in df.columns:
                df['Assigned_Nurse'] = df['Assigned_Nurse'].fillna('None')

            self.combined_data = df

            # Load supplementary files
            if progress_callback:
                progress_callback("Loading additional files", 80)
                
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

            # Complete
            if progress_callback:
                progress_callback("Complete", 100)
                
            return True

        except Exception as e:
            logging.error(f"Error loading combined data: {e}")
            
            # Report error
            if progress_callback:
                progress_callback("Error loading data", 100)
                
            messagebox.showerror("Error", "Failed to load combined data")
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
