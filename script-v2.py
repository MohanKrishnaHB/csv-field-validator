import os
import pandas as pd
import sys
from tqdm import tqdm

CONSTANTS = {
    "masterFilePath": "source-master.xlsx",
    "processFolderName": "processed",
    "reportFolderName": "report",
    "reportFileName": "report.csv",
    "fileTypes": [
        {
            "fileIdentifier": "SALES_HIST",
            "sheetName": "Store Sales & Inventory (Hist)"
        },
        {
            "fileIdentifier": "SALES",
            "sheetName": "Store Sales & Inventory (Weekl)"
        },
        {
            "fileIdentifier": "DC_HIST",
            "sheetName": "DC Metrics (Hist)"
        },
        {
            "fileIdentifier": "DC",
            "sheetName": "DC Metrics (Weekly)"
        },
        {
            "fileIdentifier": "MOD",
            "sheetName": "Modular Plan Metrics"
        },
        {
            "fileIdentifier": "DEMAND_FCST",
            "sheetName": "Store Demand Forecast"
        },
        {
            "fileIdentifier": "ORDER_FCST",
            "sheetName": "Order Forecast"
        },
        {
            "fileIdentifier": "MUMD",
            "sheetName": "Store Markup and Markdowns"
        },
        {
            "fileIdentifier": "ECOMM_SALES",
            "sheetName": "Ecomm Sales"
        },
        {
            "fileIdentifier": "ECOMM_INV",
            "sheetName": "Ecomm Inventory"
        }
    ]
}

class TextStyle:
    RED = "\033[91m"
    END = "\033[0m"
    GREEN = "\033[92m"

errors = ['----------------------------------ERRORS----------------------------------']

def print_error(text):
    print(f"{TextStyle.RED}{text}{TextStyle.END}")

def print_success(text):
    print(f"{TextStyle.GREEN}{text}{TextStyle.END}")

def create_folder(folder_path):
    try:
        # Create the folder
        os.makedirs(folder_path)
        # print(f"Folder '{folder_path}' created successfully.")
    except FileExistsError:
        print(f"Note: Folder '{folder_path}' already exists.")
    except PermissionError:
        print(f"Error: Permission denied. Check if you have the necessary permissions.")
    except Exception as e:
        print(f"An error occurred: {e}")

def move_file(source_folder, destination_folder, file_name):
    # Create the full path for source and destination
    source_path = os.path.join(source_folder, file_name)
    destination_path = os.path.join(destination_folder, file_name)

    try:
        # Rename the file to move it
        os.rename(source_path, destination_path)
        # print(f"File '{file_name}' moved successfully from '{source_folder}' to '{destination_folder}'.")
    except FileNotFoundError:
        print(f"Error: File '{file_name}' not found in '{source_folder}'.")
    except PermissionError:
        print(f"Error: Permission denied. Check if the file is open or if you have the necessary permissions.")
    except Exception as e:
        print(f"An error occurred: {e}")

def get_files(folder_path):
    try:
        # Get a list of all files in the folder
        files = os.listdir(folder_path)
        
        # Print the list of files
        # print(f"Files in '{folder_path}':")
        # for file in files:
        #     print(file)
        return files
    except FileNotFoundError as e:
        print(f"Error: {e}")

def rename_file(old_name, new_name):
    try:
        # Rename the file
        os.rename(old_name, new_name)
        # print(f"File '{old_name}' successfully renamed to '{new_name}'.")
    except FileNotFoundError:
        print(f"Error: File '{old_name}' not found.")
    except PermissionError:
        print(f"Error: Permission denied. Check if the file is open or if you have the necessary permissions.")
    except Exception as e:
        print(f"An error occurred: {e}")

def validate_file(file_name, predefined_columns):
    target = pd.read_csv(file_name)
    actual_columns = target.columns.tolist()
    missing_columns = set(predefined_columns) - set(actual_columns)
    return missing_columns

def get_file_type(file_name):
    global errors
    try:
        fileType = list(filter(lambda item: item['fileIdentifier'] in (file_name), CONSTANTS['fileTypes']))[0]
        return fileType
    except Exception as e:
        errors = errors + [f"ERROR: File type not found for file {file_name}"]
        return None

def get_predefined_columns(file_type):
    global errors
    try:
        master = pd.read_excel(CONSTANTS['masterFilePath'], sheet_name=file_type['sheetName'])
        return master.iloc[:, 2].tolist()
    except Exception as e:
        errors = errors + [f"ERROR: Sheet {file_type['sheetName']} not found for type {file_type['fileIdentifier']}"]
        return None

def report_error_files(file_path, error_list):
    try:
        reporting_df = pd.DataFrame(error_list)
        reporting_df.to_csv(file_path, index=False)
    except Exception as e:
        print_error(f"ERROR: An error occurred: {e}")

def isCSV(fileName):
    if len(os.path.splitext(fileName)) > 1 and os.path.splitext(fileName)[1].lower() == '.csv':
        return True
    return False

def process_files(folder, date):
    files = [item for item in get_files(folder) if item is not None and isCSV(item)]
    total_csv_files_in_folder = len(files)
    total_files_matched_format = 0
    total_error_files = 0
    error_list = []
    create_folder(folder + '\\' + CONSTANTS['reportFolderName'])
    create_folder(folder + '\\' + CONSTANTS['processFolderName'])
    for file in tqdm(files, desc="Processing files", unit="file"):
        file_type = get_file_type(file)
        if file_type:
            predefined_columns = get_predefined_columns(file_type)
            if predefined_columns:
                total_files_matched_format = total_files_matched_format + 1
                missing_columns = validate_file(folder + '\\' + file, predefined_columns)
                if missing_columns:
                    error_list = error_list + [{
                        'Error_File': file,
                        'Missing_Columns': missing_columns
                    }]
                    total_error_files = total_error_files + 1
                    # print_error(f"ERROR: Missing Columns for file {file}")
                else:
                    move_file(folder, folder + '\\' + CONSTANTS['processFolderName'], file)
                    rename_file(folder + '\\' + CONSTANTS['processFolderName'] + '\\' + file, folder + '\\' + CONSTANTS['processFolderName'] + '\\' + os.path.splitext(file)[0] + date + '.csv')
                    # print_success(f"SUCCESS: File {file} validated and renamed successfully")
    print('Total CSV files: ', total_csv_files_in_folder)
    print('Total format matched files: ', total_files_matched_format)
    print_error('Total missing column files: ' + str(total_error_files))
    print_success('Total processed files: ' + str(total_files_matched_format - total_error_files))
    
    report_error_files(folder + '\\' + CONSTANTS['reportFolderName'] + '\\' + CONSTANTS['reportFileName'], error_list)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script-v2.py <folder-path> <date Ex: -2024-12-31>")
    else:
        folder_path = sys.argv[1]
        date = sys.argv[2]
        process_files(folder_path, date)
        for error in errors:
            print_error(error)
