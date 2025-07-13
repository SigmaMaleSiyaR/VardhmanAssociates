import os
from docx import Document
from html import escape
import re
import glob


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

    formatted_title = title.replace(" ", "_").replace("&", "").replace(",", "")
    relative_path = f"../images/{category}/{formatted_title}.jpg"
    absolute_path = os.path.join("Services", "images", category, f"{formatted_title}.jpg")
    image_exists = os.path.exists(absolute_path)

    # 🖼️ Insert image once at the top of the HTML section (before any content)
    if image_exists:
        html += f"""
<div class="text-center my-4">
  <img src="{relative_path}" alt="{title}" class="img-fluid rounded shadow-sm" style="max-height: 350px; object-fit: cover;">
</div>
"""
    else:
        print(f"⚠️ Image missing for: {category}/{formatted_title}.jpg")


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

        inside_list = False
        
        if is_heading:
            cleaned = escape(clean_emoji(text_raw))
            html += f"<h{heading_level} class='mt-4 fw-bold'>{cleaned}</h{heading_level}>\n"
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

def wrap_with_bootstrap(title, body, category, sidebar_items):
    banner_image_url = f"/img/ServicesHeader.jpg"

    # Find actual filenames in the category folder
    category_dir = os.path.join(OUTPUT_ROOT, category)
    all_html_files = os.listdir(category_dir)

    service_list_html = ""
    for service in sidebar_items:
        match = next((f for f in all_html_files if service in f and f.endswith(".html")), None)
        if match:
            href = f"../{category}/{match}"
        else:
            href = "#"
        service_list_html += f"<li><a href='{href}' class='d-flex'><p>{escape(service)}</p></a></li>\n"


    return f"""<!DOCTYPE html>
  <html lang="en">
  <head>
    <meta charset="utf-8">
    <title>{escape(title)} - {category} Services</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">

    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Open+Sans:wght@400;500&family=Roboto:wght@500;700&display=swap" rel="stylesheet">

    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.2/css/all.min.css" rel="stylesheet">

        <style>
        body {{
            font-family: 'Open Sans', sans-serif;
            font-size: 14px;
        }}
        .banner {{
            height: 20vh;
            background: url('{banner_image_url}') center/cover no-repeat;
            position: relative;
        }}
        .banner h1 {{
            position: absolute;
            bottom: 10px;
            left: 30px;
            color: white;
            font-weight: 700;
            background: rgba(0, 0, 0, 0.5);
            padding: 10px 20px;
            border-radius: 5px;
        }}
        .content-wrapper {{
            display: flex;
            flex-wrap: wrap;
            margin-top: 2rem;
            gap: 2%;
        }}
        .main-content {{
            flex: 0 0 60%;
        }}
        .sidebar {{
            flex: 0 0 33%;
            background: #f8f9fa;
            padding: 1.5rem;
            border-radius: 5px;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
            border-left: 1px solid #ddd;
            padding-left: 1.5rem;
        }}
        .sidebar h4 {{
            font-weight: 600;
        }}
        .sidebar ul {{
            list-style: none;
            padding: 0;
        }}
        .sidebar li {{
            margin-bottom: 10px;
        }}
        .sidebar a {{
            text-decoration: none;
            color: #007bff;
        }}
        .sidebar a:hover {{
            text-decoration: underline;
        }}
    </style>

</head>
<body>

    <div id="navbar-placeholder"></div>
    <div class="banner">
        <h1>{escape(title)}</h1>
    </div>
    <div class="container">
        <div class="content-wrapper">
            <div class="main-content">
                {body}
            </div>
            <div class="sidebar">
                <h4>Our Services</h4>
                <ul>
                    {service_list_html}
                </ul>
            </div>
        </div>
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

                # Sidebar items for the given category
                SIDEBAR_SERVICES = {
                    "CA": [
                        "Start A Business", "Business Registration & Licence", "Income Tax", "GST Services",
                        "TDS Services", "ESI & PF Services", "Income Tax Notice & Appeal", "Accounting & Auditing",
                        "Society and NGO", "CMA Data & Project Report", "Loans & Project Finance"
                    ],
                    "CS": [
                        "Annual Compliances", "Corporate & Financial Restructuring", "Due Diligence",
                        "Company Incorporation & Amendment", "Company Strike off & Closer", "Winding Up & Disslution",
                        "Secretarial Audit", "Insolvency and Bankruptcy Matters", "XBRL Filing", "NCLT Appeal",
                        "Appointment & Resignation", "RBI & FEMA Overseas Law Compliance", "Mintues & Resolutions",
                        "XML Data Conversion", "Share Certificate & Transfer"
                    ],
                    "Advocate": [
                        "Civil Law", "Banking & Finance Law", "Legal Advisory", "Consumer Law & Protection",
                        "Corporate Law & Advisory", "Family Law", "Deed Making & Drafting", "Debt Recovery & Suit",
                        "Labour & Employment Law", "NIA Matter", "Property Valuation Services",
                        "Real Estate & Regulatory Act (RERA)", "Appeal", "SARFAESI Law"
                    ]
                }

                sidebar_items = SIDEBAR_SERVICES.get(category, [])
                full_html = wrap_with_bootstrap(title, html_body, category, sidebar_items)


                output_file = file.replace(".docx", ".html")
                output_path = os.path.join(output_folder, output_file)

                with open(output_path, "w", encoding="utf-8") as f:
                    f.write(full_html)

                print(f"✅ Converted: {file_path} → {output_path}")
            except Exception as e:
                print(f"❌ Error converting {file_path}: {e}")

if __name__ == "__main__":
    convert_all()
