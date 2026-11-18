from analysis import Resume, generate_resume
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
    resumes: list[Resume] = []
    for file in files:
        print(f'File {file} ready.')
        context = extract_text_pypdf(f"docs\\{file}")
        resumes.append(generate_resume(context))
        print(f'File {file} generated.')

    for r in resumes:
        print(r)


if __name__ == "__main__":
    main()
