import markdown
import re
from bs4 import BeautifulSoup
import json

# Sample markdown text
md_text = """
# Title

This is a **bold** statement, and here is a [link](https://example.com).

- Item 1
- Item 2

## 4. Start Using Tailwind CSS in Your Components

With everything set up, you're ready to use Tailwind CSS classes in your components! Here’s a quick example of creating a simple button using Tailwind CSS https://gist.github.com/mindoffwork/dcf55fe31143b38f1c89aba51b33d326:

https://gist.github.com/mindoffwork/dcf55fe31143b38f1c89aba51b33d326
"""

# Function to encapsulate specific Gist links in a <script> tag only when on a standalone line
def replace_gist_links(md_text):
    # Regex to match Gist links on a standalone line
    gist_pattern = r"^\s*(https://gist\.github\.com/[^\s]+)\s*$"

    # Replace matched Gist links with script tags
    def gist_to_script(match):
        gist_url = match.group(1).replace("https://gist.github.com/", "")
        return f'<script id="gist" src="{gist_url}"></script>'

    # Apply the replacement for standalone links
    return re.sub(gist_pattern, gist_to_script, md_text, flags=re.MULTILINE)

# Convert markdown to HTML
md_with_gist = replace_gist_links(md_text)
html_output = markdown.markdown(md_with_gist)
print(html_output)


def generate_json_from_html(html):
    soup = BeautifulSoup(html, 'html.parser')
    script_tag = soup.find('script')
    html_before_script = str(soup).split(str(script_tag))[0].replace('\n', '').strip()
    script_src = script_tag.get('src', '') if script_tag else ''
    data = []
    if html_before_script:
        data.append({
            "name": "html",
            "content": html_before_script
        })
    if script_src:
        data.append({
            "name": "script",
            "content": "gist",
            "link": script_src
        })
    remaining_html = str(soup).split(str(script_tag))[1] if len(str(soup).split(str(script_tag))) > 1 else ''
    remaining_html = remaining_html.replace('\n', '').strip()
    
    if remaining_html:
        data.append({
            "name": "html_after_script",
            "content": remaining_html
        })
    return json.dumps(data, indent=4)

json_output = generate_json_from_html(html_output)
print(json_output)
