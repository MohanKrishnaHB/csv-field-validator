import os
import pandas as pd
import sys
from tqdm import tqdm
from config import CONSTANTS
from utils import *
import re
import math 
import gzip
import shutil


errors = ['----------------------------------ERRORS----------------------------------']
invalid_files_info = []

def get_files(folder_path):
    try:
        files = os.listdir(folder_path)
        return [item for item in files if item is not None and isCSV(item)]
    except FileNotFoundError as e:
        print(f"Error: {e}")

def get_head(file_name):
    target = pd.read_csv(file_name, nrows=0)
    return target.columns.tolist()

def validate_columns(file_name, predefined_columns):
    actual_columns = get_head(file_name)
    missing_columns = set(predefined_columns) - set(actual_columns)
    return missing_columns

def get_dates(file_name, file_type):
    global errors
    try:
        target = pd.read_csv(file_name, usecols=[file_type['Date Field']], dtype={file_type['Date Field']: str})
        return target.values
    except Exception as e:
        errors = errors + [f"ERROR: Date field {file_type['Date Field']} not found in file {file_name} of type {file_type['File Type']}"]
        return []

def validate_date(file_name, file_type, date):
    
    if str(file_type['Date Field']) != 'nan':
        dates = get_dates(file_name, file_type)
        matching_dates = [item for item in date.split(',') if item in dates]
        if len(matching_dates)>0:
            return True
        return False
    else:
        return True

def get_file_type(file_name, master_data):
    global errors
    try:
        fileType = list(filter(lambda item: (item['File Type'] and (re.search(str(item['File Type']), file_name))), master_data))[0]
        return fileType
    except Exception as e:
        errors = errors + [f"ERROR: File type not found for file {file_name}"]
        return None

def get_predefined_columns(file_type):
    global errors
    try:
        master = pd.read_excel(CONSTANTS['masterFilePath'], sheet_name=file_type['Report Definition'])
        return master.iloc[:, 3].tolist()
    except Exception as e:
        errors = errors + [f"ERROR: Sheet {file_type['Report Definition']} not found for type {file_type['File Type']}"]
        return None

def report_invalid_files(file_path, error_list):
    try:
        reporting_df = pd.DataFrame(error_list)
        reporting_df.to_csv(file_path, index=False)
    except Exception as e:
        print_error(f"ERROR: An error occurred: {e}")

def create_required_folders(folder):
    create_folder(folder + '\\' + CONSTANTS['reportFolderName'])
    create_folder(folder + '\\' + CONSTANTS['processFolderName'])

def delete_file(file_path):
    try:
        os.remove(file_path)
        print(f"File '{file_path}' has been deleted successfully.")
    except FileNotFoundError:
        print(f"File '{file_path}' not found.")
    except PermissionError:
        print(f"Permission denied: Unable to delete file '{file_path}'.")
    except Exception as e:
        print(f"Error occurred while trying to delete file '{file_path}': {e}")

def move_processed_file(folder, filename, date_to_append):
    unzipped_dir = os.path.join(folder, "Unzipped")
    gz_file_path = os.path.join(unzipped_dir, filename + ".gz")
    if os.path.isfile(gz_file_path):
        move_file(unzipped_dir, folder + '\\' + CONSTANTS['processFolderName'], filename + ".gz")
        rename_file(folder + '\\' + CONSTANTS['processFolderName'] + '\\' + filename + ".gz", folder + '\\' + CONSTANTS['processFolderName'] + '\\' + os.path.splitext(filename)[0] + date_to_append + '.csv.gz')
        delete_file(os.path.join(folder, filename))
    else:
        move_file(folder, folder + '\\' + CONSTANTS['processFolderName'], filename)
        rename_file(folder + '\\' + CONSTANTS['processFolderName'] + '\\' + filename, folder + '\\' + CONSTANTS['processFolderName'] + '\\' + os.path.splitext(filename)[0] + date_to_append + '.csv')

def process_files(folder, date_to_append, master_data, date_to_validate, debug):
    files = get_files(folder)
    total_csv_files_in_folder = len(files)
    total_files_matched_format = 0
    total_error_files = 0
    error_list = []
    create_required_folders(folder)
    for file in tqdm(files, desc="Processing files", unit="file"):
        if debug == 'debug':
            print(f'file: {file}')
        file_type = get_file_type(file, master_data)
        if debug == 'debug':
            print(f'file_type: {file_type}')
        if file_type:
            predefined_columns = get_predefined_columns(file_type)
            if debug == 'debug':
                print(f'predefined_columns: {predefined_columns}')
            if predefined_columns:
                total_files_matched_format = total_files_matched_format + 1
                missing_columns = validate_columns(folder + '\\' + file, predefined_columns)
                if debug == 'debug':
                    print(f'missing_columns: {missing_columns}')
                is_date_present = validate_date(folder + '\\' + file, file_type, date_to_validate)
                if debug == 'debug':
                    print(f'is_date_present: {is_date_present}')
                if missing_columns or (not is_date_present):
                    error_list = error_list + [{
                        'Error_File': file,
                        'Missing_Columns': missing_columns if len(missing_columns)>0 else 'All Columns are present in this file but date is missing',
                        'date_missing': "Date not found in this file" if not is_date_present else "Date is present in this file but column is missing"
                    }]
                    total_error_files = total_error_files + 1
                    # print_error(f"ERROR: Missing Columns for file {file}")
                else:
                    move_processed_file(folder, file, date_to_append)
                    # print_success(f"SUCCESS: File {file} validated and renamed successfully")
    print('Total CSV files: ', total_csv_files_in_folder)
    print('Total format matched files: ', total_files_matched_format)
    print_error('Total missing column files: ' + str(total_error_files))
    print_success('Total processed files: ' + str(total_files_matched_format - total_error_files))
    
    report_invalid_files(folder + '\\' + CONSTANTS['reportFolderName'] + '\\' + CONSTANTS['reportFileName'], error_list)

def get_master_data(master_file_path, master_sheet_name):
    master_data = pd.read_excel(master_file_path, sheet_name=master_sheet_name)
    return master_data.to_dict(orient='records')

def process_validated_file(folder, file):
    move_file(folder, folder + '\\' + CONSTANTS['processFolderName'], file)
    rename_file(folder + '\\' + CONSTANTS['processFolderName'] + '\\' + file, folder + '\\' + CONSTANTS['processFolderName'] + '\\' + os.path.splitext(file)[0] + date + '.csv')

def update_invalid_list(invalid_info):
    global invalid_files_info
    invalid_files_info = invalid_files_info + [{
        'Error_File': invalid_info.file,
        'Missing_Columns': invalid_info.missing_columns,
        'Date_Not_Found': invalid_info.date_not_found
    }]

# def print_finishing_info():
#     pass

# def process(folder, date_to_validate, date_to_append):
#     global invalid_files_info
#     global errors
#     files = get_files(folder)
#     create_required_folders()
#     for file in tqdm(files, desc="Processing files", unit="file"):
#         predefined_columns = get_predefined_columns(file)
#         date_field = get_predefined_columns(file)
#         invalid_info = validate_file(file, date_to_validate, date_field, predefined_columns)
#         if invalid_info:
#             update_invalid_list(invalid_info)
#         else:
#             process_validated_file(folder, file)
#     report_invalid_files(folder + '\\' + CONSTANTS['reportFolderName'] + '\\' + CONSTANTS['reportFileName'], invalid_files_info)
#     print_finishing_info(files, invalid_files_info, errors)

# Unzip and move files

def get_gz_files(folder_path):
    try:
        files = os.listdir(folder_path)
        return [item for item in files if item.lower().endswith('.gz')]
    except FileNotFoundError as e:
        print(f"Error: {e}")

def unzip_gz_files(folder_path):
    create_folder(folder_path + '\\Unzipped')
    count = 0
    successCount = 0
    files = get_gz_files(folder_path)
    try:
        for file_name in tqdm(files, desc="Extracting files", unit="file"):
            gz_file_path = os.path.join(folder_path, file_name)
            if file_name.lower().endswith('.gz'):
                count = count + 1
                extracted_file_path = os.path.join(folder_path, file_name[:-3])  # Remove the .gz extension

                with gzip.open(gz_file_path, 'rb') as gz_file:
                    with open(extracted_file_path, 'wb') as extracted_file:
                        shutil.copyfileobj(gz_file, extracted_file)
                move_file(folder_path, folder_path + '\\Unzipped', file_name)
                successCount = successCount + 1
                # print(f"Extracted: {gz_file_path} -> {extracted_file_path}")

        if count == 0:
            print_success(f'No .gz files to extract.')
        else:
            print_success(f'{successCount} out of {count} .gz files have been successfully extracted.')
    except Exception as e:
        print_error(f"Error while unzipping: {e}")
    

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: python script-v2.py <folder-path> <date to append Ex: -2024-12-31> <date to validate Ex: -2024-12-31>")
    else:
        try:
            debug = sys.argv[4]
        except Exception as e:
            debug = ''

        folder_path = sys.argv[1]
        date_to_append = sys.argv[2]
        date_to_validate = sys.argv[3]
        unzip_gz_files(folder_path)
        master_data = get_master_data(CONSTANTS['masterFilePath'], CONSTANTS['masterSheetName'])
        process_files(folder_path, date_to_append, master_data, date_to_validate, debug)
        if len(errors) > 1:
            for error in errors:
                print_error(error)
