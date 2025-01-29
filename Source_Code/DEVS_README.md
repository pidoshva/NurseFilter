# **Nurse Filter (Developers ReadMe)**
 
### **Version:** Refactored with MVC Pattern  
### **Last Updated:** January 2025  

---

## **1. Overview**
The **Excel Data Combiner Application** is a GUI-based tool designed to merge data from two Excel files (hospital and Medicaid datasets) based on **Mother’s Name and Child’s Date of Birth**. The application provides features such as **searching, sorting, profile viewing, nurse assignment, encryption, and report generation**.  

This refactored version implements the **Model-View-Controller (MVC) design pattern** to improve **maintainability, scalability, and modularity**.  

---

## **2. Features**
✅ **Read Two Excel Files** – Load hospital and Medicaid datasets  
✅ **Combine Data** – Merge datasets based on `Mother_First_Name`, `Mother_Last_Name`, and `Child_Date_of_Birth`  
✅ **Search & Filter** – Search by **name, ID, DOB, or nurse assignment**  
✅ **Profile View** – View detailed **mother-child profile**  
✅ **Nurse Assignment** – Assign nurses manually or in **batch mode**  
✅ **Nurse Statistics** – View **most & least assigned nurses**  
✅ **Unmatched Data Handling** – Identify and store unmatched records  
✅ **Encryption & Decryption** – Secure sensitive data using **Fernet encryption**  
✅ **Generate Reports** – Export statistics as **PDF reports**  
✅ **Unit Testing** – **Test cases** for encryption, merging, and assignment  

---

## **3. Project Structure (MVC Architecture)**  
The refactored project follows an **MVC pattern**, ensuring separation of concerns:

```
.
├── app.py
├── app_crypto.py
├── controllers/
│   ├── main_controller.py
│   ├── combined_data_controller.py
│   ├── profile_controller.py
├── models/
│   ├── data_model.py
├── views/
│   ├── main_view.py
│   ├── combined_data_view.py
│   ├── profile_view.py
├── invoker.py
├── test.py
├── test_assign_nurse.py
├── test_encryption.py
├── sheetgenerator.py
├── database_data.xlsx
├── medicaid_data.xlsx
├── combined_matched_data.xlsx
├── unmatched_data.xlsx
├── report.pdf
├── key.txt
```

### **Roles of Each Component**
| **Component** | **Purpose** |
|--------------|-------------|
| `app.py` | Main entry point to initialize the GUI |
| `app_crypto.py` | Handles **encryption & decryption** using **Fernet** |
| `controllers/` | **Manages logic & event handling** |
| `models/` | **Handles data processing & storage** |
| `views/` | **UI components for displaying data** |
| `test_*.py` | Unit tests for encryption, merging, and nurse assignment |  

---  

## **MVC Architecture Breakdown**
This version of the project follows the **Model-View-Controller (MVC)** pattern for better separation of concerns and maintainability. Below is a detailed breakdown of each component:

### **1. Model (Data Handling & Business Logic)**
#### `models/data_model.py`
- **Handles reading, writing, and processing Excel data.**
- **Methods include:**
  - `read_excel_file(filepath)`: Reads an Excel file.
  - `combine_data()`: Merges hospital and Medicaid datasets.
  - `load_combined_data()`: Loads existing merged data.
  - `update_child_assigned_nurse(child_data, nurse_name)`: Assigns a nurse.
  - `batch_update_nurses(nurse_name, city, state, zipcode)`: Batch assigns nurses.
  - `encrypt_file(filepath)`, `decrypt_file(filepath)`: Handles file encryption.

### **2. Views (User Interface / UI Representation)**
#### `views/main_view.py`
- **Displays main application window with buttons to load files, combine data, and view reports.**

#### `views/combined_data_view.py`
- **Displays combined data in a TreeView (table-like UI).**
- **Allows searching, sorting, nurse assignment, and batch assigning nurses.**

#### `views/profile_view.py`
- **Displays an individual child’s profile.**
- **Shows mother’s and child’s details along with assigned nurse info.**
- **Allows users to copy profile info, assign a nurse, and export the profile to PDF.**

### **3. Controllers (Handles Application Logic & User Interaction)**
#### `controllers/main_controller.py`
- **Manages interactions between UI and Model.**
- **Handles file loading, data combination, and encryption.**
- **Triggers `CombinedDataView` and `ProfileView`.**

#### `controllers/combined_data_controller.py`
- **Manages the combined dataset view.**
- **Handles search, filtering, sorting, and nurse statistics.**
- **Updates UI when new data is available.**

#### `controllers/profile_controller.py`
- **Manages individual child profiles.**
- **Handles nurse assignment and PDF export.**

---

## **4. Application Workflow**
### **Step 1: Load Excel Files**
- User selects **two Excel files** (hospital & Medicaid datasets).
- The system reads the files, normalizes column names, and prepares the data.

### **Step 2: Merge Data**
- The application **matches records** based on `Mother_First_Name`, `Mother_Last_Name`, and `Child_Date_of_Birth`.  
- **Unmatched data** is stored separately in `unmatched_data.xlsx`.

### **Step 3: View & Search Data**
- The **merged dataset** is displayed in a **Treeview table**.
- Users can **search by name, ID, DOB, or nurse**.
- Clicking on an entry opens a **detailed profile view**.

### **Step 4: Nurse Assignment**
- Nurses can be **assigned individually** or **in bulk**.
- Assigned nurses are stored in `combined_matched_data.xlsx`.

### **Step 5: Data Security (Encryption)**
- The **combined data file** can be encrypted for **secure storage**.
- The application detects **encrypted files** and **decrypts them before use**.

### **Step 6: Generate Reports**
- Users can generate **statistical reports** (total children, nurse distribution, youngest/oldest child, etc.).
- Reports can be **exported as PDF**.

---
### Current Bug Report

1. Assigned Nurses column **does not refresh** upon nurse assignment in the main ("Combined Names") window.
2. Unmatched Data functionality is broken: **Does not provide expandable view of unmatched data.**  
_See screenshot below:_

Before:  
<img width="796" alt="Screen Shot 2025-01-28 at 7 53 24 PM" src="https://github.com/user-attachments/assets/9e4d5ce8-2800-485f-96e6-6661484902ea" />  
After:  
<img width="796" alt="Screen Shot 2025-01-28 at 7 54 47 PM" src="https://github.com/user-attachments/assets/2b8fcf78-e18c-4fcd-a564-7f6ab5613ee5" />
