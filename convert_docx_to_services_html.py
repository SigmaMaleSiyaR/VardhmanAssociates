import os
from docx import Document
from html import escape
import re
import glob
import chardet
from bs4 import BeautifulSoup

def extract_body_content(html):
    soup = BeautifulSoup(html, "html.parser")
    body = soup.body
    return body.decode_contents() if body else html



INPUT_HTML_FOLDERS = {
    "CA": "docs/htmlCA",
    "CS": "docs/htmlCS",
    "Advocate": "docs/htmlAdvocate"
}

OUTPUT_ROOT = "Services"

SIDEBAR_SERVICES = {
    "CA": [
        "Start A Business",
        "Business Registration & Licence",
        "Income Tax",
        "GST Services",
        "TDS Services",
        "ESI & PF Services",
        "Income Tax Notice & Appeal",
        "Accounting & Auditing",
        "Society and NGO",
        "CMA Data & Project Report",
        "Loans & Project Finance"
    ],
    "CS": [
        "Annual Compliances",
        "Corporate & Financial Restructuring",
        "Due Diligence",
        "Company Incorporation & Amendment",
        "Company Strike off & Closer",
        "Winding Up & Dissolution",
        "Secretarial Audit",
        "Insolvency and Bankruptcy Matters",
        "XBRL Filing",
        "NCLT Appeal",
        "Appointment & Resignation",
        "RBI & FEMA Overseas Law Compliance",
        "Minutes & Resolutions",
        "XML Data Conversion",
        "Share Certificate & Transfer"
    ],
    "Advocate": [
        "Civil Law",
        "Banking & Finance Law",
        "Legal Advisory",
        "Consumer Law & Protection",
        "Corporate Law & Advisory",
        "Family Law",
        "Deed Making & Drafting",
        "Debt Recovery & Suit",
        "Labour & Employment Law",
        "NIA Matter",
        "Property Valuation Services",
        "Real Estate & Regulatory Act (RERA)",
        "Appeal",
        "SARFAESI Law"
    ]
}


def remove_leading_numbering(text):
    """Remove numbering like '1.', '2.3.', or even just '.'"""
    return re.sub(r"^\s*(\d+(\.\d+)*\.?|\.)\s*", "", text).strip()

def detect_encoding(file_path):
    with open(file_path, 'rb') as f:
        raw_data = f.read(10000)
    result = chardet.detect(raw_data)
    return result['encoding']

def convert_preconverted_html():
    for category, input_folder in INPUT_HTML_FOLDERS.items():
        output_folder = os.path.join(OUTPUT_ROOT, category)
        os.makedirs(output_folder, exist_ok=True)

        for file in os.listdir(input_folder):
            if not file.endswith(".html"):
                continue

            file_path = os.path.join(input_folder, file)

            try:
                encoding = detect_encoding(file_path)
                with open(file_path, "r", encoding=encoding, errors='replace') as f:
                    raw_html = f.read()

                # 🧹 Remove outer <body> wrapper if present
                cleaned_body = extract_body_content(raw_html)

                raw_title = file.replace(".html", "").replace("-", " ").replace("_", " ")
                title = remove_leading_numbering(raw_title)
                sidebar_items = SIDEBAR_SERVICES.get(category, [])
                full_html = wrap_with_bootstrap(title, cleaned_body, category, sidebar_items)

                output_path = os.path.join(output_folder, file)
                with open(output_path, "w", encoding="utf-8") as f:
                    f.write(full_html)

                print(f"✅ Wrapped: {file_path} → {output_path}")
            except Exception as e:
                print(f"❌ Error processing {file_path}: {e}")


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

    category_heading = {
    "CA": "CA Services",
    "CS": "CS Services",
    "Advocate": "Advocate Services"
    }.get(category, "Services")
    
    # Find actual filenames in the category folder
    category_dir = os.path.join(OUTPUT_ROOT, category)
    all_html_files = os.listdir(category_dir)

    service_list_html = ""
    for service in sidebar_items:
        match = next((f for f in all_html_files if service in f and f.endswith(".html")), None)
        if match:
            href = f"../{category.capitalize()}/{match}"
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
        height: 30vh;
        background: url('/img/ServicesHeader.jpg') center/cover no-repeat;
        position: relative;
    }}
    .banner h1 {{
        position: absolute;
        bottom: 10px;
        left: 30px;
        color: white;
        font-weight: 700;
        /* background: rgba(0, 0, 0, 0.5); */
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
    #sidebar {{
        height: fit-content;
        flex: 0 0 33%;
        background: #f8f9fa;
        padding: 1.5rem;
        border-radius: 5px;
        box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
        border-left: 1px solid #ddd;
        padding-left: 1.5rem;
        position: sticky;
        top: 100px; /* adjust this based on your navbar height */
        align-self: start;
    }}
   #sidebar h4 {{
        font-weight: 600;
        color: black;
        text-decoration: none;
        font-style: normal;
        font-size: x-large;
    }}
    #sidebar ul {{
        padding: 1rem;
        list-style: disc;
    }}
    #sidebar li {{
        margin-bottom: 10px;
    }}
    #sidebar a {{
        text-decoration: none;
        color: #007bff;
    }}
    #sidebar a:hover {{
        color: var(--primary) !important;
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
            <div id="sidebar">
                <h4>{escape(category_heading)}</h4>
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

convert_preconverted_html()
