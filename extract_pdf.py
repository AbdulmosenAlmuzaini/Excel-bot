import pdfplumber
import sys

def extract_text(pdf_path):
    try:
        with pdfplumber.open(pdf_path) as pdf:
            content = ""
            for page in pdf.pages:
                text = page.extract_text()
                if text:
                    content += text + "\n"
            print(content)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        extract_text(sys.argv[1])
    else:
        print("Usage: python extract_pdf.py <pdf_path>")
