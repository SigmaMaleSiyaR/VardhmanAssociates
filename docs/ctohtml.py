import os
import win32com.client

# Base directory where this script is placed
BASE_DIR = os.path.dirname(__file__)  # docs/
INPUT_ROOT = BASE_DIR

def convert_docx_to_html_using_word(docx_path, output_path):
    word = win32com.client.Dispatch("Word.Application")
    word.Visible = False
    word.DisplayAlerts = 0

    try:
        doc = word.Documents.Open(docx_path)
        doc.SaveAs(output_path, FileFormat=8)  # 8 = wdFormatHTML
        doc.Close()
        print(f"✅ Converted: {docx_path} → {output_path}")
    except Exception as e:
        print(f"❌ Failed to convert {docx_path}: {e}")
    finally:
        word.Quit()

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

            convert_docx_to_html_using_word(docx_path, output_path)

if __name__ == "__main__":
    convert_all_docx_to_html()
