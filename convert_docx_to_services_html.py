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
        "NI Matter",
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

def create_firebase_content_script():
    """Create a script to help add existing content to Firebase"""
    script_content = '''# Firebase Content Migration Script
# This script helps you add existing static content to Firebase

import firebase_admin
from firebase_admin import credentials, firestore
import os

# Initialize Firebase (you'll need to add your service account key)
# cred = credentials.Certificate("path/to/your/serviceAccountKey.json")
# firebase_admin.initialize_app(cred)
# db = firestore.client()

def add_service_to_firebase(service_type, service_title, content):
    """Add a service to Firebase Firestore"""
    try:
        doc_ref = db.collection('services').document()
        doc_ref.set({
            'type': service_type,
            'title': service_title,
            'content': content
        })
        print(f"✅ Added to Firebase: {service_title} ({service_type})")
    except Exception as e:
        print(f"❌ Error adding {service_title}: {e}")

# Example usage:
# add_service_to_firebase("CA", "Start A Business", "<h2>Starting Your Business</h2><p>Content here...</p>")

print("📋 To migrate existing content to Firebase:")
print("1. Install firebase-admin: pip install firebase-admin")
print("2. Add your Firebase service account key")
print("3. Uncomment the Firebase initialization code")
print("4. Add your existing content using the add_service_to_firebase function")
print("5. Or use the admin panel at /admin/manage-services.html")
'''
    
    with open("firebase_migration_helper.py", "w", encoding="utf-8") as f:
        f.write(script_content)
    print("📄 Created firebase_migration_helper.py - use this to migrate existing content to Firebase")

def main():
    print("🚀 Starting Firebase-ready service page generation...")
    print("=" * 60)
    
    convert_preconverted_html()
    
    print("=" * 60)
    print("✅ All service pages have been updated with Firebase integration!")
    print("📋 Next steps:")
    print("1. All pages now have Firebase content loading capability")
    print("2. Pages will show 'Content Coming Soon' until you add content to Firebase")
    print("3. Add content via admin panel: /admin/manage-services.html")
    print("4. Or use the migration helper script to preserve existing content")
    
    create_firebase_content_script()

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
                
                # Create Firebase-ready HTML with static content as fallback
                full_html = wrap_with_bootstrap(title, cleaned_body, category, sidebar_items)

                output_path = os.path.join(output_folder, file)
                with open(output_path, "w", encoding="utf-8") as f:
                    f.write(full_html)

                print(f"✅ Created Firebase-ready page: {file_path} → {output_path}")
                print(f"   📝 Service: {title} ({category})")
                print(f"   🔗 Add content via admin panel: /admin/manage-services.html")
            except Exception as e:
                print(f"❌ Error processing {file_path}: {e}")

if __name__ == "__main__":
    main()


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
        # Find the best matching file for this service
        best_match = None
        for f in all_html_files:
            if f.endswith(".html"):
                # Check if service name is contained in filename
                if service in f:
                    # Prefer files with correct spelling
                    if "Dissolution" in service and "Dissolution" in f:
                        best_match = f
                        break
                    elif "Licence" in service and "Licence" in f and "Licences" not in f:
                        best_match = f
                        break
                    elif service in f:
                        best_match = f
        
        if best_match:
            # Use correct directory casing based on actual folder names
            if category == "CA":
                href = f"../Ca/{best_match}"
            elif category == "CS":
                href = f"../Cs/{best_match}"
            else:
                href = f"../{category}/{best_match}"
        else:
            href = "#"
        service_list_html += f"<li><a href='{href}' class='d-flex'><p>{escape(service)}</p></a></li>\n"


    return f"""<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <title>{escape(title)} - {category} Services</title>
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no" />

    <link rel="preconnect" href="https://fonts.googleapis.com" />
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
    <link
      href="https://fonts.googleapis.com/css2?family=Open+Sans:wght@400;500&family=Roboto:wght@500;700&display=swap"
      rel="stylesheet"
    />

    <link
      href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css"
      rel="stylesheet"
    />
    <link
      href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.2/css/all.min.css"
      rel="stylesheet"
    />

    <style>
      body {{
        font-family: "Open Sans", sans-serif;
        font-size: 14px;
        overflow-x: hidden;
      }}
      .banner {{
        height: 30vh;
        background: url("/img/ServicesHeader.jpg") center/cover no-repeat;
        position: relative;
      }}
      .banner h1 {{
        position: absolute;
        bottom: 10px;
        left: 30px;
        color: white;
        font-weight: 700;
        padding: 10px 20px;
        border-radius: 5px;
      }}
      .content-wrapper {{
        display: flex;
        flex-wrap: wrap;
        margin-top: 2rem;
        gap: 2%;
        max-width: 1400px;
        margin-left: auto;
        margin-right: auto;
      }}
      .main-content {{
        flex: 0 0 65%;
        max-width: 65%;
      }}
      #sidebar {{
        flex: 0 0 33%;
        max-width: 33%;
        height: fit-content;
        background: #f8f9fa;
        padding: 1.5rem;
        border-radius: 5px;
        box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
        border-left: 1px solid #ddd;
        padding-left: 1.5rem;
        position: sticky;
        top: 100px;
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
      
      /* Touch-friendly improvements for mobile */
      #sidebar a {{
        padding: 8px 0;
        display: block;
        min-height: 44px;
        display: flex;
        align-items: center;
      }}
      
      /* Better spacing for mobile */
      .content-wrapper {{
        gap: 1.5rem;
      }}
      
      @media (max-width: 768px) {{
        .content-wrapper {{
          gap: 1rem;
        }}
      }}
      @media (max-width: 991px) {{
        .content-wrapper {{
          flex-direction: column;
          gap: 1rem;
        }}
        .main-content,
        #sidebar {{
          flex: 1 1 100%;
          max-width: 100%;
        }}
        #sidebar {{
          position: static;
          margin-top: 1rem;
        }}
        /* Mobile sidebar styling */
        #sidebar.collapse:not(.show) {{
          display: none !important;
        }}
        #sidebar.collapsing {{
          height: 0;
          overflow: hidden;
          transition: height 0.35s ease;
        }}
        #sidebar.collapse.show {{
          display: block !important;
        }}
      }}
      
      @media (max-width: 768px) {{
        .banner {{
          height: 25vh;
        }}
        .banner h1 {{
          font-size: 1.5rem;
          left: 15px;
          bottom: 15px;
          padding: 8px 15px;
        }}
        .content-wrapper {{
          flex-direction: column;
          gap: 1rem;
          margin-top: 1rem;
        }}
        .main-content,
        #sidebar {{
          flex: 1 1 100%;
          max-width: 100%;
        }}
        #sidebar {{
          position: static;
          margin-top: 1rem;
          padding: 1rem;
        }}
        #sidebar h4 {{
          font-size: 1.25rem;
        }}
        #sidebar ul {{
          padding: 0.5rem;
        }}
        .container {{
          padding-left: 15px;
          padding-right: 15px;
        }}
      }}
      
      @media (max-width: 576px) {{
        .banner {{
          height: 20vh;
        }}
        .banner h1 {{
          font-size: 1.25rem;
          left: 10px;
          bottom: 10px;
          padding: 6px 12px;
        }}
        #sidebar {{
          padding: 0.75rem;
        }}
        #sidebar h4 {{
          font-size: 1.1rem;
        }}
        #sidebar ul {{
          padding: 0.25rem;
        }}
        #sidebar li {{
          margin-bottom: 8px;
        }}
        .main-content {{
          padding: 0;
        }}
      }}

      /* Large Screen Optimizations (TV Screens) */
      @media (min-width: 1200px) {{
        .content-wrapper {{
          max-width: 1600px;
          gap: 3%;
        }}
        .main-content {{
          flex: 0 0 70%;
          max-width: 70%;
        }}
        #sidebar {{
          flex: 0 0 27%;
          max-width: 27%;
          padding: 2rem;
        }}
        #sidebar h4 {{
          font-size: 1.5rem;
        }}
        #sidebar ul {{
          padding: 1.5rem;
        }}
        #sidebar li {{
          margin-bottom: 15px;
          font-size: 1.1rem;
        }}
        #sidebar a {{
          padding: 12px 0;
          min-height: 50px;
        }}
        .banner {{
          height: 35vh;
        }}
        .banner h1 {{
          font-size: 2.5rem;
          left: 50px;
          bottom: 20px;
          padding: 15px 30px;
        }}
      }}

      /* Extra Large Screen Optimizations (4K TV Screens) */
      @media (min-width: 1920px) {{
        .content-wrapper {{
          max-width: 1800px;
          gap: 4%;
        }}
        .main-content {{
          flex: 0 0 72%;
          max-width: 72%;
        }}
        #sidebar {{
          flex: 0 0 24%;
          max-width: 24%;
          padding: 2.5rem;
        }}
        #sidebar h4 {{
          font-size: 1.75rem;
        }}
        #sidebar ul {{
          padding: 2rem;
        }}
        #sidebar li {{
          margin-bottom: 20px;
          font-size: 1.2rem;
        }}
        #sidebar a {{
          padding: 15px 0;
          min-height: 55px;
        }}
        .banner {{
          height: 40vh;
        }}
        .banner h1 {{
          font-size: 3rem;
          left: 60px;
          bottom: 25px;
          padding: 20px 40px;
        }}
        body {{
          font-size: 16px;
        }}
      }}

      /* Ultra Wide Screen Support */
      @media (min-width: 2560px) {{
        .content-wrapper {{
          max-width: 2000px;
        }}
        .main-content {{
          flex: 0 0 75%;
          max-width: 75%;
        }}
        #sidebar {{
          flex: 0 0 22%;
          max-width: 22%;
        }}
      }}

      /* Service content styling */
      #service-content {{
        line-height: 1.6;
        color: #333;
      }}

      /* Large screen content improvements */
      @media (min-width: 1200px) {{
        #service-content {{
          font-size: 16px;
          line-height: 1.7;
        }}
        #service-content h1,
        #service-content h2,
        #service-content h3 {{
          font-size: 2rem;
          margin-top: 2rem;
          margin-bottom: 1.5rem;
        }}
        #service-content h4,
        #service-content h5,
        #service-content h6 {{
          font-size: 1.5rem;
          margin-top: 1.5rem;
          margin-bottom: 1rem;
        }}
        #service-content p {{
          margin-bottom: 1.5rem;
        }}
        #service-content ul,
        #service-content ol {{
          margin-bottom: 1.5rem;
          padding-left: 2.5rem;
        }}
        #service-content li {{
          margin-bottom: 0.75rem;
        }}
      }}

      @media (min-width: 1920px) {{
        #service-content {{
          font-size: 18px;
          line-height: 1.8;
        }}
        #service-content h1,
        #service-content h2,
        #service-content h3 {{
          font-size: 2.5rem;
          margin-top: 2.5rem;
          margin-bottom: 2rem;
        }}
        #service-content h4,
        #service-content h5,
        #service-content h6 {{
          font-size: 1.75rem;
          margin-top: 2rem;
          margin-bottom: 1.5rem;
        }}
        #service-content p {{
          margin-bottom: 2rem;
        }}
        #service-content ul,
        #service-content ol {{
          margin-bottom: 2rem;
          padding-left: 3rem;
        }}
        #service-content li {{
          margin-bottom: 1rem;
        }}
      }}
      
      /* Mobile content improvements */
      @media (max-width: 768px) {{
        #service-content {{
          font-size: 16px;
          line-height: 1.7;
        }}
        #service-content h1,
        #service-content h2,
        #service-content h3 {{
          font-size: 1.5rem;
        }}
        #service-content h4,
        #service-content h5,
        #service-content h6 {{
          font-size: 1.25rem;
        }}
      }}

      #service-content h1,
      #service-content h2,
      #service-content h3,
      #service-content h4,
      #service-content h5,
      #service-content h6 {{
        color: #1b365d;
        margin-top: 1.5rem;
        margin-bottom: 1rem;
      }}

      #service-content p {{
        margin-bottom: 1rem;
      }}

      #service-content ul,
      #service-content ol {{
        margin-bottom: 1rem;
        padding-left: 2rem;
      }}

      #service-content li {{
        margin-bottom: 0.5rem;
      }}

      #service-content img {{
        max-width: 100%;
        height: auto;
        border-radius: 5px;
        margin: 1rem 0;
      }}

      #service-content table {{
        width: 100%;
        border-collapse: collapse;
        margin: 1rem 0;
      }}

      #service-content table,
      #service-content th,
      #service-content td {{
        border: 1px solid #ddd;
      }}

      #service-content th,
      #service-content td {{
        padding: 0.75rem;
        text-align: left;
      }}

      #service-content th {{
        background-color: #f8f9fa;
        font-weight: 600;
      }}
    </style>
  </head>
  <body>
    <div id="navbar-placeholder"></div>
    <div class="banner">
      <h1>{escape(title)}</h1>
    </div>
    <div class="container-fluid px-4">
      <!-- Mobile Sidebar Toggle Button -->
      <div class="d-lg-none text-center mb-3">
        <button class="btn btn-primary" type="button" data-bs-toggle="collapse" data-bs-target="#sidebar" aria-expanded="false" aria-controls="sidebar">
          <i class="fas fa-bars me-2"></i>Show Services Menu
        </button>
      </div>
      
      <div class="content-wrapper">
        <div class="main-content">
          <div id="service-content">
            <!-- Content will be loaded from Firebase here -->
          </div>
        </div>
        <div id="sidebar" class="collapse d-lg-block">
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
  <script src="../disable-copy.js"></script>
  <script type="module" src="../auto-load-service.js"></script>
  <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
</html>
"""

convert_preconverted_html()
