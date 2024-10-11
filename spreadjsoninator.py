import os
import pandas as pd

# Load the Excel file
excel_file_path = 'db_sheet.xlsx'  # Update this with your file path

# 1. Export TopicsList JSON
sheet_name = 'topics'  # Name of the sheet
topics_df = pd.read_excel(excel_file_path, sheet_name=sheet_name)
topics_df.columns = topics_df.columns.str.lower()
topics_df = topics_df.astype(str)

# Export the DataFrame to a JSON file
output_directory = f'dist/{sheet_name}/'  # Update this with desired output directory
output_file_path = os.path.join(output_directory, 'topicslist.json')  # Change the output file name as needed

# Create the directory if it doesn't exist
os.makedirs(output_directory, exist_ok=True)
topics_df.to_json(output_file_path, orient='records', lines=False)

print("Topics List exported successfully.")

# 2. Export Invidual Topic JSON
sheet_name = 'posts'
posts_df = pd.read_excel(excel_file_path, sheet_name=sheet_name)
posts_df.columns = posts_df.columns.str.lower()

# Export the DataFrame to a JSON file
output_directory = f'dist/{sheet_name}/'  # Update this with desired output directory
output_file_path = os.path.join(output_directory, 'topicslist.json')  # Change the output file name as needed

# 1. Get the unique topics as List
topic_list = posts_df['topic'].unique()
posts_df['updated_on'] = posts_df['updated_on'].dt.strftime('%Y-%m-%d')
for topic in topic_list:
    filtered_by_topic_df = posts_df[posts_df['topic'] == topic]
    output_directory = f'dist/{sheet_name}/'  # Update this with desired output directory
    output_file_path = os.path.join(output_directory, f'{topic}.json')  # Change the output file name as needed
    
    # Create the directory if it doesn't exist
    os.makedirs(output_directory, exist_ok=True)
    filtered_by_topic_df.to_json(output_file_path, orient='records', lines=False)

    print(f"Posts Exported successfully for '{topic}'")
    