import os
import pandas as pd
import json


# Load the Excel file
excel_file_path = 'db_sheet.xlsx'  # Update this with your file path
output_directory = 'dist/'
files_deleted= 0
for filename in os.listdir(output_directory):
    file_path = os.path.join(output_directory, filename)
    if os.path.isfile(file_path):
        os.remove(file_path) 
        files_deleted += 1
print(f"Deleted successfully -- {files_deleted} files")

# 1. Export Topics JSON
sheet_name = 'topics'
topics_df = pd.read_excel(excel_file_path, sheet_name=sheet_name)
topics_df.columns = topics_df.columns.str.lower()
topics_df = topics_df.astype(str)
output_file_path = os.path.join(output_directory, 'topics.json')  
os.makedirs(output_directory, exist_ok=True)
topics_df.to_json(output_file_path, orient='records', lines=False)
print("Exported successfully -- Topics")


# 2. Export POSTLIST JSON 
sheet_name = 'posts'
posts_df = pd.read_excel(excel_file_path, sheet_name=sheet_name)
posts_df.columns = posts_df.columns.str.lower()
posts_df['id'] = posts_df['id'].astype(str)
posts_df['created_on'] = posts_df['created_on'].dt.strftime('%Y-%m-%d')
posts_df['updated_on'] = posts_df['updated_on'].dt.strftime('%Y-%m-%d')

# 2a. Topicwise Postlist JSON
topic_list = posts_df['topic'].unique()
for topic in topic_list:
    filtered_by_topic_df = posts_df[posts_df['topic'] == topic]
    filtered_by_topic_df = filtered_by_topic_df.drop(['is_featured', 'is_popular', 'is_recommended'], axis=1)
    output_file_path = os.path.join(output_directory, f'posts_topic__{topic}.json')
    os.makedirs(output_directory, exist_ok=True)
    filtered_by_topic_df.to_json(output_file_path, orient='records', lines=False)
print("Exported successfully -- Topicwise Posts")

# 2b. HomePage Postlist Json
homepage_posts_list = {
    "is_featured": posts_df[posts_df["is_featured"]].to_dict(orient='records'),
    "is_popular": posts_df[posts_df["is_popular"]].to_dict(orient='records'),
    "is_recommended": posts_df[posts_df["is_recommended"]].to_dict(orient='records'),
}
# Write to JSON file
with open(output_directory + 'posts_home.json', 'w') as json_file:
    json.dump(homepage_posts_list, json_file)
print("Exported successfully -- Home Posts")

# 3. Export POSTS JSON 
# Generate JSON-LD for each row and save to individual JSON files
output_directory = 'posts/'
for index, row in posts_df.iterrows():
    # Construct the file path
    output_file_path = os.path.join(output_directory, row['link'], 'post.json')
    os.makedirs(os.path.dirname(output_file_path), exist_ok=True)
    row.to_json(output_file_path, orient='records', lines=False)
print("Exported successfully -- Posts")
print("Process Completed 😇")


### SUPPORTING FUNCTIONS ###
