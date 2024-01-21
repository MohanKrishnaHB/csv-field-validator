import os
import pandas as pd
import sys

def check_header(file_path, predefined_file_name):
    try:
        script_dir = os.path.dirname(os.path.realpath(__file__))
        predefined_file_path = os.path.join(script_dir, predefined_file_name)

        with open(predefined_file_path, 'r') as f:
            predefined_fields = f.read().strip().split(',')
            
        #Read predefined column names from the text file were each name in a newline
        '''with open(predefined_file_path, 'r') as f:
            predefined_fields = [line.strip() for line in f.readlines()]'''

        df = pd.read_csv(file_path, nrows=5) if file_path.endswith('.csv') else pd.read_excel(file_path, nrows=5)

        missing_fields = [field for field in predefined_fields if field not in df.columns]
        if not missing_fields:
            print("Success: All matching headings found!")
        else:
            print(f"Error: Predefined fields {', '.join(missing_fields)} not found in the file.")

    except pd.errors.EmptyDataError:
        print("Error: The file is empty.")
    except pd.errors.ParserError:
        print("Error: Unable to parse the file. Make sure it's a valid CSV or Excel file.")
    except Exception as e:
        print(f"Error: An unexpected error occurred - {e}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <file_path>")
    else:
        file_path = sys.argv[1]
        predefined_file_name = "source.csv"
        check_header(file_path, predefined_file_name)

