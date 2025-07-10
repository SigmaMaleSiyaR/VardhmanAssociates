import os
from docx import Document
from html import escape
import re

# Input/output folders
INPUT_ROOT = "docs"
OUTPUT_ROOT = "Services"

# Known emoji indicators to detect headings
HEADING_INDICATORS = ["✅", "📈", "🧠", "🛠️", "📍", "🕰️", "🎯", "👉", "🚀", "📊", "💡", "🧾", "📱"]

def clean_emoji(text):
    pattern = r"^(" + "|".join(re.escape(e) for e in HEADING_INDICATORS) + r")\s*"
    return re.sub(pattern, "", text).strip()

def is_heading_like(text_raw):
    if not text_raw:
        return False
    if any(text_raw.startswith(e) for e in HEADING_INDICATORS):
        return True
    if text_raw.isupper() and len(text_raw.split()) <= 6:
        return True
    return False

def remove_leading_numbering(text):
    """Remove numbering like '1.', '2.3.', or even just '.'"""
    return re.sub(r"^\s*(\d+(\.\d+)*\.?|\.)\s*", "", text).strip()

def convert_docx_to_html_body(doc, category, title):
    html = ""
    inserted_image = False
    heading_count = 0

    formatted_title = title.replace(" ", "_").replace("&", "").replace(",", "")
    relative_path = f"../images/{category}/{formatted_title}.jpg"
    absolute_path = os.path.join("Services", "images", category, f"{formatted_title}.jpg")
    image_exists = os.path.exists(absolute_path)

    inside_list = False

    for para in doc.paragraphs:
        text_raw = para.text.strip()
        text = escape(text_raw)
        if not text:
            continue

        style = para.style.name.lower()

        is_heading = False
        heading_level = 0

        if "heading" in style:
            heading_level = int(''.join(filter(str.isdigit, style)) or 2)
            is_heading = True

        elif is_heading_like(text_raw):
            heading_level = 3
            is_heading = True

        if is_heading:
            heading_count += 1

            # 🖼️ Insert image above second heading only
            if heading_count == 2 and not inserted_image and image_exists:
                html += f"""
<div class="text-center my-4">
  <img src="{relative_path}" alt="{title}" class="img-fluid rounded shadow-sm" style="max-height: 350px; object-fit: cover;">
</div>
"""

                inserted_image = True

            cleaned = escape(clean_emoji(text_raw))
            html += f"<h{heading_level} class='mt-4 fw-bold'>{cleaned}</h{heading_level}>\n"
            inside_list = False
            continue

        # List handling
        if para.style.name == "List Paragraph" or text_raw.startswith(("•", "●", "-", "–")):
            if not inside_list:
                html += "<ul class='mb-3'>\n"
                inside_list = True
            html += f"<li>{escape(text_raw.lstrip('•●–- ').strip())}</li>\n"
            continue
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

def get_image_tag(category, title):
    """Generate <img> tag with correct relative path from HTML to image."""
    formatted_title = title.replace(" ", "_").replace("&", "").replace(",", "")
    relative_path = f"../images/{category}/{formatted_title}.jpg"
    absolute_path = os.path.join("Services", "images", category, f"{formatted_title}.jpg")
    
    if os.path.exists(absolute_path):
        return f'<img src="{relative_path}" alt="{title}" class="img-fluid rounded mb-4 shadow-sm" style="max-height: 400px; object-fit: cover;">'
    return ""  # Return nothing if image doesn't exist

def wrap_with_bootstrap(title, body, category):
    image_html = get_image_tag(category, title)
    return f"""
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>{escape(title)}</title>
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.7/dist/css/bootstrap.min.css" rel="stylesheet" crossorigin="anonymous">
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
    table {{
      background-color: #fff;
    }}
    table.table-bordered th, table.table-bordered td {{
      border-color: var(--border);
    }}
    #navbar-placeholder {{
      display: block;
      width: 100%;
      height: auto;
      overflow: visible;
    }}
  </style>
</head>
<body>
  <div id="navbar-placeholder"></div>
  <div class="px-3 px-md-5" style="margin-top: 100px;">
    <h1>{escape(title)}</h1>
    {body}
  </div>
  <div id="footer-placeholder"></div>
</body>
<script src="../../js/navbar-inject.js"></script>
<script src="../../js/footer-inject.js"></script>
<script src="../../Services/disable-copy.js"></script>
</html>
"""

def convert_all():
    for category in os.listdir(INPUT_ROOT):
        category_path = os.path.join(INPUT_ROOT, category)
        if not os.path.isdir(category_path):
            continue

        output_folder = os.path.join(OUTPUT_ROOT, category)
        os.makedirs(output_folder, exist_ok=True)

        for file in os.listdir(category_path):
            if not file.endswith(".docx") or file.startswith("~$"):
                continue

            file_path = os.path.join(category_path, file)
            try:
                doc = Document(file_path)

                # Clean the file name to get a readable title
                raw_title = file.replace(".docx", "").replace("-", " ").replace("_", " ")
                title = remove_leading_numbering(raw_title)

                # ✅ Pass the category and title
                html_body = convert_docx_to_html_body(doc, category, title)

                full_html = wrap_with_bootstrap(title, html_body, category)
                output_file = file.replace(".docx", ".html")
                output_path = os.path.join(output_folder, output_file)

                with open(output_path, "w", encoding="utf-8") as f:
                    f.write(full_html)

                print(f"✅ Converted: {file_path} → {output_path}")
            except Exception as e:
                print(f"❌ Error converting {file_path}: {e}")

if __name__ == "__main__":
    convert_all()
