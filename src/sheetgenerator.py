import pandas as pd
from faker import Faker
from datetime import timedelta, date
import random
from faker.providers import BaseProvider

class CustomCounty(BaseProvider):
    def county(self):
        counties = ['Utah', 'Salt Lake']
        return self.random_element(counties)

fake = Faker()
fake.add_provider(CustomCounty)

# Maps original column names to a standard name for internal consistency
STANDARD_NAME_MAP = {
    # First names
    "Mother First Name": "Mother_First_Name",
    "HOH/Mother's First Name": "Mother_First_Name",
    "Mothers First Name": "Mother_First_Name",
    "Mother’s First Name": "Mother_First_Name",
    "First Name": "Mother_First_Name",  # <-- for database where it's ambiguous

    # Last names
    "Mother Last Name": "Mother_Last_Name",
    "HOH/Mother's Last Name": "Mother_Last_Name",
    "Mothers Last Name": "Mother_Last_Name",
    "Mother’s Last Name": "Mother_Last_Name",
    "Last Name": "Mother_Last_Name",

    # DOB variations
    "DOB": "Child Date of Birth",
    "Date of Birth": "Child Date of Birth",
    "Child DOB": "Child Date of Birth",

    # Phone/City
    "Telephone": "Phone Number",
    "PhoneNumber": "Phone Number",
    "Town": "City",
    "Municipality": "City"
}



# Reverses the standard names back to original
REVERSE_NAME_MAP = {v: k for k, v in STANDARD_NAME_MAP.items()}

def standardize_column_names(df):
    """Standardizes column names in a DataFrame to internal standard names."""
    return df.rename(columns={old: new for old, new in STANDARD_NAME_MAP.items() if old in df.columns})

def restore_original_names(df):
    """Restores internal standard column names back to original names."""
    return df.rename(columns={std: original for std, original in REVERSE_NAME_MAP.items() if std in df.columns})

def generate_child_dob():
    today = date.today()
    max_age = timedelta(days=365 * 3 + 9 * 30)
    birth_date = today - timedelta(days=fake.random_int(min=0, max=max_age.days))
    return birth_date

def generate_shared_data(num_entries=1000):
    shared_data = []
    for _ in range(num_entries):
        mom_first = fake.first_name()
        mom_last = fake.last_name()
        child_dob = generate_child_dob().strftime("%Y-%m-%d")
        match_key = f"{mom_first.lower()}_{mom_last.lower()}_{child_dob}"

        shared_data.append({
            "child_dob": child_dob,
            "mom_first_name": mom_first,
            "mom_last_name": mom_last,
            "phone": fake.phone_number(),
            "city": fake.city(),
            "street": fake.street_address(),
            "match_key": match_key
        })
    return shared_data


def generate_database_data(shared_data, unmatched_entries=0, num_duplicates=0):
    database_data = []
    for entry in shared_data:
        database_data.append([
            fake.last_name(), fake.first_name(), fake.first_name(),
            entry["child_dob"],
            entry["mom_last_name"], entry["mom_first_name"],
            entry["phone"], entry["city"], entry["street"],
            entry["match_key"]  # ✅ Just reference it
        ])
    
    for _ in range(unmatched_entries):
        database_data.append([
            fake.last_name(), fake.first_name(), fake.first_name(),
            generate_child_dob().strftime("%Y-%m-%d"),
            fake.last_name(), fake.first_name(),
            fake.phone_number(), fake.city(), fake.street_address(),
            ""  # unmatched entries get an empty match_key
        ])

    for _ in range(num_duplicates):
        duplicate = random.choice(database_data)
        database_data.append(duplicate)

    return pd.DataFrame(database_data, columns=[
        "Child Last Name", "Child First Name", "Child Middle Name", "Child Date of Birth",
        "Mother Last Name", "Mother First Name", "Phone Number", "City", "Address",
        "Match_Key"  # ✅ Last column
    ])



def generate_medicaid_data(shared_data, unmatched_entries=0, num_duplicates=0):
    medicaid_data = []
    for entry in shared_data:
        medicaid_data.append([
            fake.company(), fake.company(), fake.unique.random_number(digits=5),
            entry["child_dob"], fake.unique.random_number(digits=9),
            entry["mom_first_name"], entry["mom_last_name"],
            fake.date_of_birth(minimum_age=18, maximum_age=50).strftime("%Y-%m-%d"),
            f"CASE{fake.unique.random_number(digits=6)}",
            entry["phone"], fake.phone_number(), entry["street"], entry["city"],
            fake.state_abbr(), fake.zipcode(), fake.county(),
            "Yes" if fake.boolean() else "No", "Yes" if fake.boolean() else "No",
            entry["match_key"]
        ])
    for _ in range(unmatched_entries):
        medicaid_data.append([
            fake.company(), fake.company(), fake.unique.random_number(digits=5),
            generate_child_dob().strftime("%Y-%m-%d"), fake.unique.random_number(digits=9),
            fake.first_name(), fake.last_name(),
            fake.date_of_birth(minimum_age=18, maximum_age=50).strftime("%Y-%m-%d"),
            f"CASE{fake.unique.random_number(digits=6)}",
            fake.phone_number(), fake.phone_number(), fake.street_address(), fake.city(),
            fake.state_abbr(), fake.zipcode(), fake.county(),
            "Yes" if fake.boolean() else "No", "Yes" if fake.boolean() else "No"
        ])
    for _ in range(num_duplicates):
        duplicate = random.choice(medicaid_data)
        medicaid_data.append(duplicate)
    return pd.DataFrame(medicaid_data, columns=[
        "LHD", "MCO Name", "Child ID", "Child Date of Birth", "Mother ID",
        "HOH/Mother's First Name", "HOH/Mother's Last Name", "Mother's Date of Birth",
        "Case ID", "Phone Number", "Mobile Phone Number", "Street", "City",
        "State", "Zip", "County", "Tobacco Use", "First Time Mom","Match_key"
    ])

def merge_and_export(database_df, medicaid_df):
    # Standardize columns for merge
    db_std = standardize_column_names(database_df)
    med_std = standardize_column_names(medicaid_df)

    print("Database columns:", db_std.columns.tolist())
    print("Medicaid columns:", med_std.columns.tolist())

    required = ["Mother_First_Name", "Mother_Last_Name", "Child Date of Birth", "Phone Number", "City"]
    for col in required:
        if col not in db_std.columns:
            print(f"❌ MISSING in database: {col}")
        if col not in med_std.columns:
            print(f"❌ MISSING in medicaid: {col}")
  

    merged_df = pd.merge(
        db_std,
        med_std,
        on=["Mother_First_Name", "Mother_Last_Name", "Child Date of Birth", "Phone Number", "City"],
        how="inner"
    )

    # Restore names to original before export
    merged_df = restore_original_names(merged_df)
    merged_df.to_excel("merged_combined.xlsx", index=False)
    print("Merged file saved as merged_combined.xlsx")

def generate_excel_files():
    names_count = int(input("How many names to generate in each list? "))
    num_duplicates = int(input("How many duplicates to add to each list? "))
    unmatched_entries = int(input("How many unmatched entries to add? "))

    shared_data = generate_shared_data(names_count)

    database_df = generate_database_data(shared_data, unmatched_entries, num_duplicates)
    medicaid_df = generate_medicaid_data(shared_data, unmatched_entries, num_duplicates)

    database_df.to_excel("database_data.xlsx", index=False)
    medicaid_df.to_excel("medicaid_data.xlsx", index=False)
    print("Files created: database_data.xlsx, medicaid_data.xlsx")

    merge_and_export(database_df, medicaid_df)

if __name__ == "__main__":
    generate_excel_files()


