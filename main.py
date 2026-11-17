import os
from pypdf import PdfReader


def extract_text_pypdf(pdf_path: str) -> str:
    reader = PdfReader(pdf_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
        text += "\n"
    return text


def main():
    files = [f for f in os.listdir("docs") if os.path.isfile(os.path.join("docs", f))]
    text = extract_text_pypdf(f"docs\\{files[4]}")


if __name__ == "__main__":
    main()
