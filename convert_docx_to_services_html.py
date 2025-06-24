import os
from docx import Document
from html import escape

# Set folders
INPUT_ROOT = "docs"
OUTPUT_ROOT = "Services"

def convert_docx_to_html_body(doc):
    html = ""
    inside_list = False

    for para in doc.paragraphs:
        text = escape(para.text.strip())
        if not text:
            continue

        style = para.style.name.lower()

        if "heading" in style:
            level = ''.join(filter(str.isdigit, style)) or "2"
            html += f"<h{level}>{text}</h{level}>\n"
            inside_list = False

        elif para.style.name == "List Paragraph" or para.text.startswith(("•", "●", "-", "–")):
            if not inside_list:
                html += "<ul>\n"
                inside_list = True
            html += f"<li>{text.lstrip('•●–- ')}</li>\n"
        else:
            if inside_list:
                html += "</ul>\n"
                inside_list = False
            html += f"<p>{text}</p>\n"

    if inside_list:
        html += "</ul>\n"

    for table in doc.tables:
        html += "<div class='table-responsive'><table class='table table-bordered'>\n"
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
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet" />
</head>
<body class="container my-5">
  {body}
</body>
</html>
"""

def convert_all():
    for category in os.listdir(INPUT_ROOT):
        category_path = os.path.join(INPUT_ROOT, category)
        if not os.path.isdir(category_path):
            continue  # Skip files at root

        output_folder = os.path.join(OUTPUT_ROOT, category.capitalize())
        os.makedirs(output_folder, exist_ok=True)

        for file in os.listdir(category_path):
            if not file.endswith(".docx"):
                continue

            file_path = os.path.join(category_path, file)
            doc = Document(file_path)

            html_body = convert_docx_to_html_body(doc)
            full_html = wrap_with_bootstrap(file.replace(".docx", ""), html_body)

            output_file = file.replace(".docx", ".html")
            output_path = os.path.join(output_folder, output_file)

            with open(output_path, "w", encoding="utf-8") as f:
                f.write(full_html)

            print(f"✅ Converted: {file_path} → {output_path}")

if __name__ == "__main__":
    convert_all()
