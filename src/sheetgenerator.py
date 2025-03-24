"""
Fake Data Generator

by Vadim Pidoshva
"""
import pandas as pd
from faker import Faker
from datetime import timedelta, date
import random

# Initialize Faker instance
fake = Faker()

# Function to generate birthdates for children under 4 years old
def generate_child_dob():
    today = date.today()
    max_age = timedelta(days=365 * 3 + 9 * 30)  # 3 years and 9 months
    birth_date = today - timedelta(days=fake.random_int(min=0, max=max_age.days))
    return birth_date

# Function to generate shared data for both lists
def generate_shared_data(num_entries=1000):
    shared_data = []
    for _ in range(num_entries):
        child_last_name = fake.last_name()
        child_first_name = fake.first_name()
        child_middle_name = fake.first_name()
        mom_last_name = fake.last_name()
        mom_first_name = fake.first_name()
        child_dob = generate_child_dob().strftime("%Y-%m-%d")
        mother_id = fake.unique.random_number(digits=9)
        shared_data.append({
            "child_last_name": child_last_name,
            "child_first_name": child_first_name,
            "child_middle_name": child_middle_name,
            "mom_last_name": mom_last_name,
            "mom_first_name": mom_first_name,
            "child_dob": child_dob,
            "mother_id": mother_id
        })
    return shared_data

# Function to generate "Database" data with optional duplicates
def generate_database_data(shared_data, unmatched_entries=0, num_duplicates=0):
    database_data = []
    for entry in shared_data:
        state_file_number = fake.unique.random_number(digits=9)
        street = fake.street_address()
        city = fake.city()
        state = fake.state_abbr()
        zip_ = fake.zipcode()
        phone = fake.phone_number()
        mobile = fake.phone_number()
        
        database_data.append([
            entry["child_last_name"], entry["child_first_name"], entry["child_middle_name"], entry["child_dob"],
            entry["mom_last_name"], entry["mom_first_name"], state_file_number,
            street, city, state, zip_, phone, mobile
        ])

    # Generate unmatched entries
    for _ in range(unmatched_entries):
        child_last_name = fake.last_name()
        child_first_name = fake.first_name()
        child_middle_name = fake.first_name()
        mom_last_name = fake.last_name()
        mom_first_name = fake.first_name()
        child_dob = generate_child_dob().strftime("%Y-%m-%d")
        state_file_number = fake.unique.random_number(digits=9)
        street = fake.street_address()
        city = fake.city()
        state = fake.state_abbr()
        zip_ = fake.zipcode()
        phone = fake.phone_number()
        mobile = fake.phone_number()

        database_data.append([
            child_last_name, child_first_name, child_middle_name, child_dob,
            mom_last_name, mom_first_name, state_file_number,
            street, city, state, zip_, phone, mobile
        ])

    # Generate duplicates
    for _ in range(num_duplicates):
        duplicate = random.choice(database_data)
        database_data.append(duplicate)

    return pd.DataFrame(database_data, columns=[
        "Child Last Name", "Child First Name", "Child Middle Name", "DOB",
        "Mother Last Name", "Mother First Name", "State File Number",
        "Street", "City", "State", "ZIP", "Phone #", "Mobile #"
    ])

# Function to generate "Medicaid List" data with optional duplicates
def generate_medicaid_data(shared_data, unmatched_entries=0, num_duplicates=0):
    medicaid_data = []
    for entry in shared_data:
        mom_dob = fake.date_of_birth(minimum_age=18, maximum_age=50).strftime("%Y-%m-%d")
        child_id = fake.unique.random_number(digits=5)
        phone = fake.phone_number()
        city = fake.city()
        zip_ = fake.zipcode()
        street_address = fake.street_address()

        medicaid_data.append([
            entry["mom_first_name"], entry["mom_last_name"], mom_dob, entry["mother_id"], child_id, entry["child_dob"], city, zip_,phone,street_address
        ])

    # Generate unmatched entries
    for _ in range(unmatched_entries):
        mom_first_name = fake.first_name()
        mom_last_name = fake.last_name()
        mom_dob = fake.date_of_birth(minimum_age=18, maximum_age=50).strftime("%Y-%m-%d")
        child_first_name = fake.first_name()
        child_last_name = fake.last_name()
        child_dob = generate_child_dob().strftime("%Y-%m-%d")
        mother_id = fake.unique.random_number(digits=9)
        child_id = fake.unique.random_number(digits=5)
        city = fake.city()
        zip_ = fake.zipcode()
        phone = fake.phone_number()
        street_address = fake.street_address()
        
        medicaid_data.append([
            mom_first_name, mom_last_name, mom_dob, mother_id, child_id, child_dob, city, zip_, phone, street_address
        ])

    # Generate duplicates
    for _ in range(num_duplicates):
        duplicate = random.choice(medicaid_data)
        medicaid_data.append(duplicate)

    return pd.DataFrame(medicaid_data, columns=[
        "Mother First Name", "Last Name", "Mother DOB", "Mother ID", "Child ID", "Child DOB","City","Zip","Phone","Street_address"
    ])

# Function to check and display formatted duplicate records
def check_duplicates(df, list_name, subset_columns):
    duplicates = df[df.duplicated(subset=subset_columns, keep=False)]
    
    if not duplicates.empty:
        print(f"\nDuplicates found in {list_name} (based on {', '.join(subset_columns)}):\n")

        for _, group in duplicates.groupby(subset_columns):
            print(f"Duplicate Group: {tuple(group.iloc[0][subset_columns])}")
            print(group.to_string(index=False))  # Formats output beautifully
            print("-" * 50)  # Divider for clarity
    else:
        print(f"No duplicates found in {list_name}.\n")

# Function to verify mismatched names
def verify_names(database_file, medicaid_data_file):
    database_df = pd.read_excel(database_file)
    medicaid_df = pd.read_excel(medicaid_data_file)

    database_names = set((database_df["Mother First Name"].str.strip() + " " + database_df["Mother Last Name"].str.strip()).unique())
    medicaid_names = set((medicaid_df["Mother First Name"].str.strip() + " " + medicaid_df["Last Name"].str.strip()).unique())

    missing_in_medicaid = database_names - medicaid_names
    missing_in_database = medicaid_names - database_names

    print("\nMismatched Names Found:\n")
    if missing_in_medicaid:
        print("Names in Database but missing in Medicaid List:")
        print("--------------------------------------------------")
        for name in missing_in_medicaid:
            print(f"  - {name}")
        print("\n")
    else:
        print("No names missing in Medicaid List.\n")

    if missing_in_database:
        print("Names in Medicaid List but missing in Database List:")
        print("--------------------------------------------------")
        for name in missing_in_database:
            print(f"  - {name}")
        print("\n")
    else:
        print("No names missing in Database List.\n")

# Main function to generate the files
def generate_excel_files():
    names_count = int(input("How many names to generate in each list? "))
    
    add_duplicates = input("Add duplicates to lists? (y/n): ").strip().lower()
    num_duplicates = 0
    duplicate_target = "both"
    if add_duplicates == 'y':
        num_duplicates = int(input("Enter the number of duplicates: "))
        duplicate_target = input("Add duplicates to (database/medicaid/both): ").strip().lower()

    add_unmatched = input("Generate unmatched data? (y/n): ").strip().lower()
    unmatched_entries = 0
    unmatched_target = "both"
    if add_unmatched == 'y':
        unmatched_entries = int(input("Enter the number of unmatched entries: "))
        unmatched_target = input("Add unmatched entries to (database/medicaid/both): ").strip().lower()

    shared_data = generate_shared_data(names_count)
    
    database_data_df = generate_database_data(
        shared_data, 
        unmatched_entries if unmatched_target in ["database", "both"] else 0,
        num_duplicates if duplicate_target in ["database", "both"] else 0
    )
    medicaid_data_df = generate_medicaid_data(
        shared_data, 
        unmatched_entries if unmatched_target in ["medicaid", "both"] else 0,
        num_duplicates if duplicate_target in ["medicaid", "both"] else 0
    )
    
    database_filename = "database_data.xlsx"
    medicaid_filename = "medicaid_data.xlsx"
    database_data_df.to_excel(database_filename, index=False)
    medicaid_data_df.to_excel(medicaid_filename, index=False)
    
    print(f"\nFiles created: {database_filename}, {medicaid_filename}")
    
    verify_names(database_filename, medicaid_filename)
    check_duplicates(database_data_df, "Database List", ["Child Last Name", "Child First Name", "DOB"])
    check_duplicates(medicaid_data_df, "Medicaid List", ["Mother First Name", "Last Name", "Child DOB"])

# Run the program
if __name__ == "__main__":
    generate_excel_files()

