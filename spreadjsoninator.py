import os
import pandas as pd

# Load the Excel file
excel_file_path = 'db_sheet.xlsx'  # Update this with your file path
sheet_name = 'topics'  # Name of the sheet

# Read the Excel file
df = pd.read_excel(excel_file_path, sheet_name=sheet_name)
df.columns = df.columns.str.lower()
df = df.astype(str)

# Export the DataFrame to a JSON file
output_directory = f'dist/{sheet_name}/'  # Update this with desired output directory
output_file_path = os.path.join(output_directory, 'topicslist.json')  # Change the output file name as needed

# Create the directory if it doesn't exist
os.makedirs(output_directory, exist_ok=True)
df.to_json(output_file_path, orient='records', lines=False)

print(f"Data exported to \'{output_file_path}\' successfully.")
