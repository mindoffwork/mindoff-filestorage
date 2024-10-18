import os
import pandas as pd
import json
import warnings
import re
import markdown
from bs4 import BeautifulSoup

# Suppress Warnings
warnings.filterwarnings("ignore", category=UserWarning, module="openpyxl")

### SUPPORTING FUNCTIONS ###
def replace_gist_links(md_text):
    return re.sub(r"^\s*(https://gist\.github\.com/[^\s]+)\s*$", 
                  lambda m: f'<script id="gist" src="{m.group(1).replace("https://gist.github.com/", "")}"></script>', 
                  md_text, flags=re.MULTILINE)

def generate_json_from_html(html):
    soup = BeautifulSoup(html, 'html.parser')
    elements = []
    current_html_content = ""

    for el in soup.contents:
        if el.name == 'script':
            if current_html_content:
                elements.append({"name": "text", "content": current_html_content.strip()})
                current_html_content = ""
            elements.append({"name": "script", "content": "gist", "link": el.get('src', '')})
        elif el.name == 'p' and len(el.contents) == 1 and el.img:
            if current_html_content:
                elements.append({"name": "text", "content": current_html_content.strip()})
                current_html_content = ""
            elements.append({"name": "img", "content": el.img.get('alt', ''), "link": el.img.get('src', '')})
        else:
            current_html_content += str(el).replace('\n', '').strip()

    if current_html_content:  # Add any remaining HTML content
        elements.append({"name": "text", "content": current_html_content.strip()})

    return json.dumps(elements, indent=4)

def process_md_files(df):
    for link in df['link']:
        md_path = os.path.join("posts/" + link, 'post.md')
        json_path = os.path.join("posts/" + link, 'post_body.json')
        try:
            with open(md_path, 'r', encoding='utf-8') as f:
                md_text = f.read()
            html_output = markdown.markdown(replace_gist_links(md_text))
            print(html_output)
            with open(json_path, 'w', encoding='utf-8') as json_file:
                json_file.write(generate_json_from_html(html_output))
        except FileNotFoundError:
            pass

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
    "is_featured": posts_df[posts_df["is_featured"]].sort_values(by="updated_on", ascending=False).to_dict(orient='records'),
    "is_popular": posts_df[posts_df["is_popular"]].sort_values(by="updated_on", ascending=False).to_dict(orient='records'),
    "is_recommended": posts_df[posts_df["is_recommended"]].sort_values(by="updated_on", ascending=False).to_dict(orient='records'),
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
    post_head_file_path = os.path.join(output_directory, row['link'], 'post_head.json')
    os.makedirs(os.path.dirname(post_head_file_path), exist_ok=True)
    row.to_json(post_head_file_path, orient='index', lines=False)
    post_md_file_path = os.path.join(output_directory, row['link'], 'post.md')
    post_body_file_path = os.path.join(output_directory, row['link'], 'post_body.json')
    if not os.path.exists(post_md_file_path):
        with open(post_md_file_path, 'w') as md_file:
            md_file.write("")
    try:
        with open(post_md_file_path, 'r', encoding='utf-8') as f:
            md_text = f.read()
        html_output = markdown.markdown(replace_gist_links(md_text))
        with open(post_body_file_path, 'w', encoding='utf-8') as json_file:
            generated_json_from_html = json.loads(generate_json_from_html(html_output))
            json.dump(generated_json_from_html, json_file)
    except FileNotFoundError:
        pass
print("Exported successfully -- Posts")
print("Process Completed 😇")

