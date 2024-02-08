import os
import pandas as pd
import sys
from tqdm import tqdm
from config import CONSTANTS

class TextStyle:
    RED = "\033[91m"
    END = "\033[0m"
    GREEN = "\033[92m"

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

def isCSV(fileName):
    if len(os.path.splitext(fileName)) > 1 and os.path.splitext(fileName)[1].lower() == '.csv':
        return True
    return False


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
