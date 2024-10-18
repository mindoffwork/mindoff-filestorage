import pandas as pd
import re
import markdown
from bs4 import BeautifulSoup
import json
import os

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

# Example usage
df = pd.DataFrame({'link': ['quickly-integrate-tailwind-css-into-an-existing-next-js-app-in-just-4-steps']})
process_md_files(df)
