# 🤖 Resume Analysis Agent

An AI-powered resume extraction and analysis system that supports multiple file formats and provides intelligent resume-to-job matching scores using Large Language Models.

## 📋 Features

### 1. **Universal Resume Extractor** (`Extract_agent.py`)
- **Multi-format Support**: PDF, DOCX, TXT, Images (JPG/PNG), Excel, CSV
- **Intelligent Text Extraction**: Automatically detects file type and uses appropriate extraction method
- **AI-Powered Parsing**: Uses LLM to structure resume data into clean JSON format
- **Output**: Structured JSON with sections like name, email, phone, education, experience, skills, etc.

### 2. **Resume Scoring System** (`Analysis_agent.py`)
- **Job Description Matching**: Compares resume against job requirements
- **AI-Powered Scoring**: Generates 0-100 score based on:
  - Relevant skills match
  - Experience alignment
  - Education requirements
  - Keyword relevance
- **Detailed Reasoning**: Provides explanation for the assigned score

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- HuggingFace API Token ([Get one here](https://huggingface.co/settings/tokens))
- Tesseract OCR (only if processing images)

### Installation

1. **Clone or download the project**

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Set up environment variables**

Create a `.env` file in the project root:
```env
HF_TOKEN=your_huggingface_token_here
```

4. **For image OCR (optional)**
   - Windows: [Download Tesseract](https://github.com/UB-Mannheim/tesseract/wiki)
   - Mac: `brew install tesseract`
   - Linux: `apt-get install tesseract-ocr`

## 📖 Usage

### Step 1: Extract Resume Data

```python
# Edit Extract_agent.py - Set your file path
path = "path/to/your/resume.pdf"  # Supports: .pdf, .docx, .txt, .jpg, .xlsx, .csv
output_path = "resume_output.json"

# Run the extractor
python Extract_agent.py
```

**Output**: `resume_output.json` with structured resume data

### Step 2: Analyze Resume Against Job Description

```python
# Edit Analysis_agent.py - Set your paths
path = "resume_output.json"        # Output from Step 1
jd_path = "jd.txt"                 # Your job description text file

# Run the analyzer
python Analysis_agent.py
```

**Output**: Match score (0-100) with detailed reasoning

## 📂 Project Structure

```
resume_Analysis_agent/
├── Extract_agent.py          # Resume extraction & parsing
├── Analysis_agent.py          # Resume scoring & analysis
├── requirements.txt          # Python dependencies
├── .env                      # Environment variables (create this)
├── .gitignore               # Git ignore rules
├── README.md                # This file
├── jd.txt                   # Job description (user-provided)
└── resume_output.json       # Extracted resume data (generated)
```

## 🛠️ Supported File Formats

| Format | Extensions | Library Used |
|--------|-----------|--------------|
| PDF | `.pdf` | pdfplumber, PyPDF2 |
| Word | `.docx`, `.doc` | python-docx |
| Text | `.txt` | Native Python |
| Images | `.jpg`, `.png`, `.bmp`, `.tiff` | Pillow + pytesseract |
| Excel | `.xlsx`, `.xls` | pandas + openpyxl |
| CSV | `.csv` | pandas |

## 🔧 Configuration

### Change LLM Model

Edit the `InferenceClient` in both scripts:

```python
client = InferenceClient(
    model="meta-llama/Llama-3.3-70B-Instruct",  # Change model here
    token=os.getenv("HF_TOKEN"),
)
```

### Adjust Output Format

Modify the prompt in `Extract_agent.py` to customize JSON structure:

```python
prompt = """Your custom extraction prompt..."""
```

### Customize Scoring Criteria

Edit the prompt in `Analysis_agent.py` to adjust scoring logic:

```python
prompt = """Your custom scoring criteria..."""
```

## 📊 Example Output

### Extracted Resume JSON
```json
{
  "name": "John Doe",
  "email": "john@example.com",
  "phone": "+1 234 567 8900",
  "education": [...],
  "experience": [...],
  "skills": {...}
}
```

### Analysis Score
```
Score: 85/100

Reasoning:
- Strong technical skills match (Python, ML, AI)
- 3 years experience aligns with requirement
- Relevant education in Computer Science
- Missing: Cloud platform experience
```

## ⚠️ Important Notes

1. **API Costs**: LLM API calls consume tokens - monitor your HuggingFace usage
2. **Privacy**: Never commit `.env` file or resumes with personal data to git
3. **File Size**: Large files may hit token limits - consider preprocessing
4. **OCR Accuracy**: Image-based extraction depends on image quality

## 🔐 Security Best Practices

✅ Store tokens in `.env` file (already in `.gitignore`)  
✅ Never hardcode API keys in source code  
✅ Don't commit personal resume data  
✅ Review extracted data before sharing  

## 🐛 Troubleshooting

### UnicodeDecodeError
- Files must be UTF-8 encoded
- Scripts already handle this with `encoding="utf-8"`

### Import Errors
```bash
# Reinstall dependencies
pip install -r requirements.txt
```

### OCR Not Working
- Install Tesseract system package
- Check pytesseract path configuration

### API Errors
- Verify HF_TOKEN in `.env`
- Check HuggingFace API status
- Ensure model is accessible

## 📝 License

This project is open source. Customize and use as needed.

## 🤝 Contributing

Feel free to enhance the prompts, add new file format support, or improve scoring algorithms!

## 📧 Support

For issues or questions, please check the code comments or modify the prompts to suit your needs.

---

**Built with ❤️ using HuggingFace LLMs and Python**
