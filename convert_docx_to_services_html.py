import os
from docx import Document
from html import escape
import re

# Input/output folders
INPUT_ROOT = "docs"
OUTPUT_ROOT = "Services"

# Emoji-like indicators that suggest heading
HEADING_INDICATORS = ["✅", "📈", "🧠", "🛠️", "📍", "🕰️", "🎯", "👉", "🚀", "📊", "💡", "🧾", "📱"]

def clean_emoji(text):
    """Remove known emoji-like prefixes"""
    pattern = r"^(" + "|".join(re.escape(e) for e in HEADING_INDICATORS) + r")\s*"
    return re.sub(pattern, "", text).strip()

def is_heading_like(text_raw):
    """Check if text looks like a heading"""
    if not text_raw:
        return False
    if any(text_raw.startswith(e) for e in HEADING_INDICATORS):
        return True
    if text_raw.isupper() and len(text_raw.split()) <= 6:
        return True
    return False

def convert_docx_to_html_body(doc):
    html = ""
    inside_list = False

    for para in doc.paragraphs:
        text_raw = para.text.strip()
        text = escape(text_raw)
        if not text:
            continue

        style = para.style.name.lower()

        if "heading" in style:
            level = ''.join(filter(str.isdigit, style)) or "2"
            cleaned = escape(clean_emoji(text_raw))
            html += f"<h{level} class='mt-4 fw-bold'>{cleaned}</h{level}>\n"
            inside_list = False

        elif para.style.name == "List Paragraph" or text_raw.startswith(("•", "●", "-", "–")):
            if not inside_list:
                html += "<ul class='mb-3'>\n"
                inside_list = True
            html += f"<li>{escape(text_raw.lstrip('•●–- ').strip())}</li>\n"

        elif is_heading_like(text_raw):
            cleaned = escape(clean_emoji(text_raw))
            html += f"<h3 class='mt-4 fw-semibold'>{cleaned}</h3>\n"
            inside_list = False

        else:
            if inside_list:
                html += "</ul>\n"
                inside_list = False
            html += f"<p class='mb-3'>{text}</p>\n"

    if inside_list:
        html += "</ul>\n"

    # Tables
    for table in doc.tables:
        html += "<div class='table-responsive my-4'><table class='table table-bordered table-striped'>\n"
        for row in table.rows:
            html += "<tr>\n"
            for cell in row.cells:
                html += f"<td>{escape(cell.text.strip())}</td>\n"
            html += "</tr>\n"
        html += "</table></div>\n"

    return html

def wrap_with_bootstrap(title, body):
    return f"""
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>{escape(title)}</title>
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.7/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-LN+7fdVzj6u52u30Kp6M/trliBMCMKTyK833zpbD+pXdCLuTusPj697FH4R/5mcr" crossorigin="anonymous">
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600&family=Merriweather:wght@400;700&display=swap" rel="stylesheet">
  <style>
    :root {{
      --primary: #003366;
      --secondary: #005b96;
      --light-bg: #f8f9fa;
      --highlight: #e9ecef;
      --border: #dee2e6;
    }}
    body {{
      font-family: 'Merriweather', serif;
      background-color: var(--light-bg);
      color: #212529;
      font-size: 1.05rem;
      line-height: 1.8;
      padding: 3rem 2rem;
    }}
    h1, h2, h3 {{
      font-family: 'Inter', sans-serif;
      font-weight: 600;
      color: var(--primary);
      margin-top: 2.5rem;
      margin-bottom: 1rem;
    }}
    h1 {{
      font-size: 2rem;
      border-bottom: 2px solid var(--secondary);
      padding-bottom: 0.5rem;
    }}
    h2 {{
      font-size: 1.5rem;
      color: var(--secondary);
    }}
    h3 {{
      font-size: 1.3rem;
      margin-top: 2rem;
    }}
    p, li {{
      font-size: 1.05rem;
    }}
    ul {{
      padding-left: 1.5rem;
      margin-bottom: 1.5rem;
    }}
    .highlight-section {{
      background-color: var(--highlight);
      padding: 1rem 1.5rem;
      border-left: 4px solid var(--secondary);
      margin: 2rem 0;
    }}
    table {{
      background-color: #fff;
    }}
    thead {{
      background-color: var(--highlight);
    }}
    table.table-bordered th, table.table-bordered td {{
      border-color: var(--border);
    }}
  </style>
</head>
<body class="px-3 px-md-5">
  <h1>{escape(title)}</h1>
  {body}
</body>
</html>
"""

def convert_all():
    for category in os.listdir(INPUT_ROOT):
        category_path = os.path.join(INPUT_ROOT, category)
        if not os.path.isdir(category_path):
            continue

        output_folder = os.path.join(OUTPUT_ROOT, category.capitalize())
        os.makedirs(output_folder, exist_ok=True)

        for file in os.listdir(category_path):
            if not file.endswith(".docx") or file.startswith("~$"):
                continue

            file_path = os.path.join(category_path, file)
            try:
                doc = Document(file_path)
                html_body = convert_docx_to_html_body(doc)
                title = file.replace(".docx", "").replace("-", " ").replace("_", " ")
                full_html = wrap_with_bootstrap(title, html_body)

                output_file = file.replace(".docx", ".html")
                output_path = os.path.join(output_folder, output_file)

                with open(output_path, "w", encoding="utf-8") as f:
                    f.write(full_html)

                print(f"✅ Converted: {file_path} → {output_path}")
            except Exception as e:
                print(f"❌ Error converting {file_path}: {e}")

if __name__ == "__main__":
    convert_all()
