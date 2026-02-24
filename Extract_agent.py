"""
Universal Resume Extractor - Supports Multiple File Formats
============================================================
Supported formats: PDF, DOCX, TXT, Images (JPG/PNG), Excel, CSV

Requirements (install as needed):
- PDF: pip install pdfplumber PyPDF2
- Word: pip install python-docx
- Images (OCR): pip install Pillow pytesseract
- Excel/CSV: pip install pandas openpyxl

Usage Examples:
- PDF: path = "resume.pdf"
- Word: path = "resume.docx"
- Text: path = "resume.txt"
- Image: path = "resume.jpg"
- Excel: path = "data.xlsx"
- CSV: path = "data.csv"
"""

from huggingface_hub import InferenceClient
import json
import re
import os
from pathlib import Path
from dotenv import load_dotenv
load_dotenv()  # Load environment variables from .env file

# Import libraries for different file formats
try:
    import pdfplumber
except ImportError:
    pdfplumber = None

try:
    import PyPDF2
except ImportError:
    PyPDF2 = None

try:
    import docx
except ImportError:
    docx = None

try:
    from PIL import Image
    import pytesseract
except ImportError:
    Image = None
    pytesseract = None

try:
    import pandas as pd
except ImportError:
    pd = None


def extract_text_from_file(file_path):
    """
    Automatically detect file format and extract text content.
    Supports: PDF, DOCX, TXT, images (JPG, PNG), Excel, CSV
    """
    file_ext = Path(file_path).suffix.lower()
    
    print(f"Detected file type: {file_ext}")
    
    # PDF files
    if file_ext == '.pdf':
        if pdfplumber:
            print("Using pdfplumber to extract PDF...")
            with pdfplumber.open(file_path) as pdf:
                text = ""
                for page in pdf.pages:
                    text += page.extract_text() + "\n"
            return text
        elif PyPDF2:
            print("Using PyPDF2 to extract PDF...")
            with open(file_path, "rb") as f:
                reader = PyPDF2.PdfReader(f)
                text = ""
                for page in reader.pages:
                    text += page.extract_text() + "\n"
            return text
        else:
            raise ImportError("Please install pdfplumber or PyPDF2: pip install pdfplumber PyPDF2")
    
    # Word documents
    elif file_ext in ['.docx', '.doc']:
        if docx:
            print("Extracting from Word document...")
            doc = docx.Document(file_path)
            text = "\n".join([para.text for para in doc.paragraphs])
            return text
        else:
            raise ImportError("Please install python-docx: pip install python-docx")
    
    # Plain text files
    elif file_ext == '.txt':
        print("Reading plain text file...")
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    
    # Image files (OCR)
    elif file_ext in ['.jpg', '.jpeg', '.png', '.bmp', '.tiff']:
        if Image and pytesseract:
            print("Extracting text from image using OCR...")
            image = Image.open(file_path)
            text = pytesseract.image_to_string(image)
            return text
        else:
            raise ImportError("Please install Pillow and pytesseract: pip install Pillow pytesseract")
    
    # Excel files
    elif file_ext in ['.xlsx', '.xls']:
        if pd:
            print("Extracting from Excel file...")
            df = pd.read_excel(file_path)
            text = df.to_string(index=False)
            return text
        else:
            raise ImportError("Please install pandas and openpyxl: pip install pandas openpyxl")
    
    # CSV files
    elif file_ext == '.csv':
        if pd:
            print("Extracting from CSV file...")
            df = pd.read_csv(file_path)
            text = df.to_string(index=False)
            return text
        else:
            raise ImportError("Please install pandas: pip install pandas")
    
    else:
        raise ValueError(f"Unsupported file format: {file_ext}. Supported formats: .pdf, .docx, .txt, .jpg, .png, .xlsx, .csv")


# Initialize the HuggingFace client
client = InferenceClient(
    model="meta-llama/Llama-3.3-70B-Instruct",
    token=os.getenv("HF_TOKEN"),
)

output_path = "resume_output.json"
path = "D:\\Projects\\714022202033_MUTHURAJA_M (1) (1).pdf"

# Extract text from file (auto-detect format)
print(f"Processing file: {os.path.basename(path)}")
print("-" * 50)
resume_text = extract_text_from_file(path)
print(f"✓ Extracted {len(resume_text)} characters\n")

# Prepare the prompt for the LLM
prompt = """You are a resume text extractor. Extract all sections of the resume like name, email, phone number, education, experience, skills, etc and the one more section should be years of experience with role in json calculate the years of experience based on the experience section correctly. from the following resume text and return ONLY a valid JSON object with these fields. Do not include any markdown formatting or additional text."""

messages = [
    {"role": "system", "content": prompt},
    {"role": "user", "content": f"Extract and structure this resume content into JSON:\n\n{resume_text}"},
]

# Call the LLM API
print("Sending to LLM for parsing...")
print("-" * 50)
response = client.chat_completion(messages=messages, max_tokens=2048)
llm_output = response.choices[0].message.content

print("LLM Response:")
print(llm_output)
print()

# Try to extract JSON from the response
try:
    # Try to parse directly as JSON
    resume_data = json.loads(llm_output)
except json.JSONDecodeError:
    # If that fails, try to extract JSON from markdown code blocks
    json_match = re.search(r'```(?:json)?\s*([\s\S]*?)\s*```', llm_output)
    if json_match:
        resume_data = json.loads(json_match.group(1))
    else:
        # Last resort: try to find JSON object in the text
        json_match = re.search(r'\{[\s\S]*\}', llm_output)
        if json_match:
            resume_data = json.loads(json_match.group(0))
        else:
            raise ValueError("Could not extract valid JSON from LLM response")

# Save to JSON file
print("-" * 50)
with open(output_path, "w", encoding="utf-8") as f:
    json.dump(resume_data, f, indent=4, ensure_ascii=False)

print(f"✓ Resume data successfully saved to {output_path}")
print(f"✓ Extracted fields: {', '.join(resume_data.keys())}")
print(f"\n✅ Process completed successfully!")