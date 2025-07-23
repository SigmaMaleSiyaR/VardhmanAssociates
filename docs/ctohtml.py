import os
import re
from docx import Document
from bs4 import BeautifulSoup

# Base directory where this script is placed
BASE_DIR = os.path.dirname(__file__)  # docs/
INPUT_ROOT = BASE_DIR

# Directory containing the input DOCX files
def remove_emojis(text):
    # Remove emojis based on Unicode range
    return re.sub(r'[\U00010000-\U0010ffff]', '', text)

def looks_like_heading(text):
    return bool(re.match(r'^([A-Z][A-Z\s]+:?|.{1,60}:)$', text))

def is_bullet_like(text):
    return bool(re.match(r'^(\s*[•\-–‣▪🔹✅🟢➡️🚫✍️💰💼📂🔍⚖️🏛️🧾👪🧱🔎🏠]|\d+[\.\)])\s+', text))

def convert_docx_to_bootstrap_html(docx_path, output_path):
    doc = Document(docx_path)

    html = ['<!DOCTYPE html>',
            '<html lang="en">',
            '<head>',
            '<meta charset="UTF-8">',
            '<meta name="viewport" content="width=device-width, initial-scale=1">',
            '<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">',
            f'<title>{os.path.basename(docx_path)}</title>',
            '</head>',
            '<body class="p-4">',
            '<div class="container">']

    in_list = False

    for para in doc.paragraphs:
        raw_text = para.text.strip()
        if not raw_text:
            continue

        text = remove_emojis(raw_text)

        # Client perspective block
        if "Client Perspective:" in text:
            if in_list:
                html.append('</ul>')
                in_list = False
            html.append(f'<div class="alert alert-secondary"><strong>{remove_emojis(text)}</strong></div>')

        # Bullet-style line
        elif is_bullet_like(text):
            if not in_list:
                html.append('<ul>')
                in_list = True
            cleaned = re.sub(r'^(\s*[•\-–‣▪🔹✅🟢➡️🚫✍️💰💼📂🔍⚖️🏛️🧾👪🧱🔎🏠]|\d+[\.\)])\s*', '', text)
            html.append(f'<li>{cleaned}</li>')

        # Heading
        elif looks_like_heading(text):
            if in_list:
                html.append('</ul>')
                in_list = False
            html.append(f'<h3 class="mt-4">{remove_emojis(text)}</h3>')

        # Regular paragraph
        else:
            if in_list:
                html.append('</ul>')
                in_list = False
            html.append(f'<p class="mb-3">{remove_emojis(text)}</p>')

    if in_list:
        html.append('</ul>')

    html.append('</div></body></html>')

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(html))

    print(f"✅ Converted {docx_path} → {output_path}")
    
def convert_all_docx_to_html():
    for category in os.listdir(INPUT_ROOT):
        category_path = os.path.join(INPUT_ROOT, category)

        # Skip non-folders and the output folders
        if not os.path.isdir(category_path) or category.startswith("html") or category == "__pycache__":
            continue

        output_category_name = "html" + category
        output_category_path = os.path.join(INPUT_ROOT, output_category_name)
        os.makedirs(output_category_path, exist_ok=True)

        for filename in os.listdir(category_path):
            if not filename.endswith(".docx") or filename.startswith("~$"):
                continue

            docx_path = os.path.join(category_path, filename)
            html_filename = filename.replace(".docx", ".html")
            output_path = os.path.join(output_category_path, html_filename)

            convert_docx_to_bootstrap_html(docx_path, output_path)

if __name__ == "__main__":
    convert_all_docx_to_html()
