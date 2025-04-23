# Excel Data Combiner Application (MVC)

The Excel Data Combiner Application is a user-friendly GUI-based tool designed to merge data from two Excel files—typically hospital and Medicaid datasets—into a unified dataset. It enables users to search, filter, and inspect profiles, view unmatched data, assign nurses, and analyze nurse statistics. With additional features like encryption and decryption, it ensures secure handling of sensitive information.

## Features

- **Read Two Excel Files:** Load hospital and Medicaid datasets for merging.
- **Combine Data:** Merge datasets based on Mother's First Name, Last Name, and Child's Date of Birth.
- **Search & Filter:** Search and filter combined data by name, ID, or Date of Birth.
- **View Detailed Profiles:** Double-click an entry to view detailed information, including mother and child details.
- **Copy to Clipboard:** Copy profile details for documentation and sharing.
- **Excel Export:** Save the combined dataset as `combined_matched_data.xlsx`.
- **Unmatched Data Inspection:** View and explore unmatched data records.
- **Duplicate Detection:** Identify and display duplicate records in a separate window.
- **Nurse Assignment:** Assign nurses to children individually or in batch mode by location.
- **Nurse Statistics:** Analyze assigned nurses, view most/least assigned nurses, and inspect their assigned children.
- **Tab-Based Navigation:** Navigate seamlessly between different application views while maintaining state.
- **Fernet Encryption:** Encrypt sensitive data files using industry-standard Fernet encryption.
- **PDF Reports:** Generate and export statistical reports and profiles in PDF format.
- **Detailed Logging:** Track application activity with timestamps for operational insights.
- **High Performance:** Optimized to handle up to 5000 families efficiently.
- **Location-Based Features:** Enhanced ZIP code and address management for better searchability and batch assignment.
- **Notes System:** Dedicated notes area in profile view for additional information.
- **Duplicate Detection:** Advanced system for detecting and managing duplicate records.
- **Automatic Nurse Assignment:** Streamlined nurse assignment process with automatic login in treeview.
- **Simplified Profile Interface:** Removed manual buttons in favor of automated processes.

## Prerequisites

Ensure the following requirements are met to run the application:

- **Python 3.x** installed.
- Required Python Libraries:
- `pandas`
- `tkinter`
- `openpyxl`
- `logging`
- `reportlab`
- `cryptography`
- `platform`
- `app_crypto`

You can install the required dependencies using pip:

```bash
pip install pandas openpyxl tkinter reportlab cryptography
```

## Excel File Requirements

### Hospital Dataset Format

The hospital dataset Excel file must contain the following columns with specified formats:

| Column Name       | Data Type         | Description                      |
| ----------------- | ----------------- | -------------------------------- |
| Mother_ID         | String            | Unique identifier for the mother |
| Mother_First_Name | String            | Mother's first name              |
| Mother_Last_Name  | String            | Mother's last name               |
| Child_First_Name  | String            | Child's first name               |
| Child_Last_Name   | String            | Child's last name                |
| Child_DOB         | Date (YYYY-MM-DD) | Child's date of birth            |
| Street_Address    | String            | Mother's street address          |
| City              | String            | City of residence                |
| State             | String            | Two-letter state code            |
| ZIP               | String            | 5-digit ZIP code                 |
| Phone             | String            | Contact phone number             |
| Mobile            | String            | Mobile phone number              |

### Medicaid Dataset Format

The Medicaid dataset Excel file must contain the following columns with specified formats:

| Column Name         | Data Type         | Description                     |
| ------------------- | ----------------- | ------------------------------- |
| Mother_First_Name   | String            | Mother's first name             |
| Mother_Last_Name    | String            | Mother's last name              |
| Child_First_Name    | String            | Child's first name              |
| Child_Last_Name     | String            | Child's last name               |
| Child_DOB           | Date (YYYY-MM-DD) | Child's date of birth           |
| Medicaid_ID         | String            | Unique Medicaid identifier      |
| Coverage_Start_Date | Date (YYYY-MM-DD) | Start date of Medicaid coverage |
| Coverage_End_Date   | Date (YYYY-MM-DD) | End date of Medicaid coverage   |

### Data Format Requirements

- All date fields must be in YYYY-MM-DD format
- String fields should not contain special characters except for spaces and hyphens
- Phone numbers should be in (XXX) XXX-XXXX format
- ZIP codes must be 5 digits
- State codes should be 2 letters (e.g., UT, CA, NY)

## Test Data Generation

The application includes a `sheetgenerator.py` utility to create test Excel files with realistic data. This tool is useful for testing and development purposes.

### Using the Sheet Generator

1. Run the sheet generator script:

```bash
python sheetgenerator.py
```

2. The script will create two Excel files:

   - `hospital_data.xlsx`: Contains hospital dataset with random but realistic data
   - `medicaid_data.xlsx`: Contains Medicaid dataset with matching records

3. Optional parameters:
   - `--rows N`: Generate N rows of data (default: 100)
   - `--seed S`: Set random seed for reproducible data (default: random)
   - `--output-dir PATH`: Specify output directory (default: current directory)

Example usage:

```bash
python sheetgenerator.py --rows 500 --seed 42 --output-dir ./test_data
```

The generated files will follow the exact format requirements specified above and can be used immediately with the main application.

## Installation

1. Clone or download this repository.
2. Ensure the required Python packages are installed (see above).
3. Place your two Excel files (hospital and Medicaid datasets) in an accessible location.

## Usage

1. Run the `app.py` script:

```bash
python app.py
```

2. The GUI will open with a tab-based interface containing:

- **Data Loader Tab:** Read Excel files and combine datasets.
- **Combined Data Tab:** View, search, and filter merged data.
- **Profile View Tab:** Examine detailed information for selected entries.
- **Unmatched Data Tab:** Review records that couldn't be matched.
- **Duplicate Data Tab:** Identify and examine duplicate records.
- **Nurse Statistics Tab:** Analyze nurse assignment distribution.
- **Batch Assign Tab:** Assign nurses to multiple children based on location criteria.
- **Statistical Report Tab:** Generate comprehensive reports with PDF export options.

## Application Workflow

- **Read Excel Files:** Click the "Read Excel File" buttons to load two Excel files (hospital and Medicaid datasets).
- **Combine Data:** After loading both files, click "Combine Data" to merge the files based on "Mother's First Name," "Mother's Last Name," and "Child's Date of Birth."
- **Search & Filter:** Use the search bar to filter the displayed names.
- **View Profiles:** Double-click an entry to view a detailed profile in a new tab.
- **Copy Profile Info:** Copy profile details to the clipboard by clicking the "Copy Profile Info" button.
- **Assign Nurses:** Assign nurses individually from profile view or in batch mode based on location.
- **Analyze Nurse Statistics:** View detailed statistics on nurse assignments.
- **Generate Reports:** Create statistical reports and export as PDF.
- **Manage Notes:** Add and edit notes in the profile view for additional information.
- **Handle Duplicates:** Review and manage duplicate records through the duplicate detection system.
- **Batch Assign by Location:** Assign nurses to multiple children based on ZIP code, city, or state.

## Application Layout

### Tab-Based Interface

The application uses a tabbed interface to organize functionality while maintaining application state:

- Switch between tabs without losing data
- Each functional area has its own dedicated tab
- New tabs open automatically when needed (e.g., when viewing profiles)

### Data Loader Tab

- **Read Excel File 1:** Opens a file dialog for selecting the first Excel file.
- **Read Excel File 2:** Opens a file dialog for selecting the second Excel file.
- **Combine Data:** Merges the two datasets.
- **Load Existing File:** Opens previously combined data files.

### Combined Data Tab

- **Search Bar:** Filter entries by Mother ID, Child Name, or Child DOB.
- **Results List:** Displays "Mother ID," "Child Name," "Child DOB," and "Assigned Nurse."
- **Double-click Feature:** Opens a detailed profile for the selected entry in a new tab.
- **Batch Assign Nurses:** Opens interface for assigning nurses to multiple children.
- **Generate Report:** Creates statistical reports on children and nurse assignments.
- **Display in Excel:** Opens the data in Excel for additional analysis.

### Profile View Tab

Displays detailed information including:

- **Mother's Information:** Mother ID, First Name, Last Name.
- **Child's Information:** First Name, Last Name, Date of Birth.
- **Contact Information:** Street Address, City, State, ZIP, Phone, and Mobile Number.
- **Notes Section:** Dedicated area for adding and editing notes about the child.
- **Assign Nurse:** Interface to assign a nurse to the specific child.
- **Export to PDF:** Save profile information as a PDF document.
- **Copy Profile Info:** Copies the profile details to the clipboard.

### Unmatched Data Tab

Includes unmatched data with origin specified and an ability to view the details in a drop-down format.

### Duplicate Data Tab

Shows records that appear multiple times across the datasets with detailed information.

### Nurse Statistics Tab

- **Most Assigned Nurse:** Displays the name of the most assigned nurse with count.
- **Least Assigned Nurse:** Displays the name of the least assigned nurse with count.
- **Assignments by Nurse:** Lists all nurses with their assignment counts.
- **Clickable Nurse Names:** Display assigned children for specific nurses.

## Performance Considerations

- **Large Dataset Support:** Optimized to handle up to 5000 families efficiently.
- **Batch Processing:** Efficient batch assignment of nurses based on location criteria.
- **Search Optimization:** Enhanced search capabilities for ZIP codes and addresses.
- **Memory Management:** Efficient handling of large datasets to prevent memory issues.

## Security Features

- **Fernet Symmetric Encryption:** Industry-standard encryption for protecting sensitive data.
- **Automatic Encryption/Decryption:** Files are automatically encrypted after use and decrypted when needed.
- **Encryption Key Management:** Generate and manage encryption keys securely.
- **Secure File Handling:** All sensitive data files are protected through encryption.
- **Data Validation:** Strict validation of input data to prevent security issues.

## Logging

The application logs key events with timestamps for better traceability:

- **INFO:** Successful operations with timestamps.
- **WARNING:** Operations that did not complete as expected (e.g., no file selected).
- **ERROR:** Issues encountered (e.g., data combination errors).

## Excel File Output

- **Combined Data:** Saved as `combined_matched_data.xlsx` in the current working directory.
- **Unmatched Data:** Saved as `unmatched_data.xlsx` for records that couldn't be matched.
- **Duplicate Records:** Saved as `duplicate_names.xlsx` for examination and review.

## Unit Testing

The application includes comprehensive unit tests to ensure functionality:

- **Test for Reading Excel Files:** Verifies data is correctly loaded and processed.
- **Test for Data Combination:** Ensures datasets are properly merged based on matching criteria.
- **Test for Encryption/Decryption:** Validates data integrity through the encryption/decryption cycle.
- **Test for Nurse Assignment:** Confirms both individual and batch nurse assignment work correctly.
- **Test for Excel File Generation:** Verifies output files are correctly created and formatted.

You can run the tests using `pytest` with rich formatting for enhanced readability:

```bash
pytest --rich --tb=short -v test.py
```
