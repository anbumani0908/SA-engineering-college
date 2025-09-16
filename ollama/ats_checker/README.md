# ATS Resume Checker

An intelligent Applicant Tracking System (ATS) resume analyzer powered by Ollama AI. This tool helps optimize your resume for ATS systems and provides detailed feedback on how to improve your resume's compatibility.

## Features

- **Multi-format Support**: Analyzes PDF, DOC, DOCX, and TXT files
- **AI-Powered Analysis**: Uses Ollama AI for comprehensive resume evaluation
- **Job Description Matching**: Compare your resume against specific job descriptions
- **Detailed Reports**: Generates comprehensive analysis reports saved as text files
- **ATS Optimization**: Provides specific recommendations for ATS compatibility

## Installation

1. Install required dependencies:
```bash
pip install -r requirements.txt
```

2. Set up your Ollama API key:
```bash
export OLLAMA_API_KEY="your_api_key_here"
```

## Usage

### Command Line Interface

#### Basic Usage (General Analysis)
```bash
python ats_checker.py path/to/your/resume.pdf
```

#### With Job Description
```bash
python ats_checker.py path/to/your/resume.pdf --job-description path/to/job_description.txt
```

#### Custom Output Path
```bash
python ats_checker.py path/to/your/resume.pdf --output my_analysis.txt
```

#### Using Different Model
```bash
python ats_checker.py path/to/your/resume.pdf --model "gpt-oss:120b"
```

### Python API Usage

```python
from ats_checker import ATSResumeChecker

# Initialize checker
checker = ATSResumeChecker(api_key="your_api_key")

# Analyze resume
output_file = checker.check_resume("resume.pdf")
print(f"Analysis saved to: {output_file}")

# Analyze with job description
output_file = checker.check_resume("resume.pdf", "job_description.txt")
```

## Supported File Formats

- **PDF**: `.pdf` files
- **Microsoft Word**: `.docx` and `.doc` files
- **Text**: `.txt` files

## Analysis Output

The tool generates comprehensive reports including:

- **ATS Compatibility Score** (1-10)
- **Keyword Matching Analysis**
- **Section-by-Section Evaluation**:
  - Contact Information
  - Professional Summary/Objective
  - Work Experience
  - Skills Section
  - Education
- **Strengths and Areas for Improvement**
- **Specific Optimization Recommendations**
- **Overall Assessment**

## Example Output

```
================================================================================
ATS RESUME ANALYSIS REPORT
Generated on: 2024-01-15 14:30:25
Model Used: gpt-oss:120b
================================================================================

## ATS COMPATIBILITY SCORE: 8/10

## KEYWORD MATCHING:
- Matched: Python, Machine Learning, Data Analysis, SQL
- Missing: TensorFlow, AWS, Docker

## SECTION ANALYSIS:
### Contact Information: 9/10
✓ Professional email address
✓ LinkedIn profile included
✓ Phone number present

### Professional Summary: 7/10
✓ Clear and concise
⚠ Could include more specific achievements
⚠ Missing quantifiable results

## STRENGTHS:
- Strong technical skills section
- Relevant work experience
- Clean, professional formatting

## AREAS FOR IMPROVEMENT:
- Add more quantifiable achievements
- Include industry-specific keywords
- Expand professional summary

## ATS OPTIMIZATION RECOMMENDATIONS:
- Use standard section headers (Experience, Education, Skills)
- Include more action verbs
- Add relevant certifications
- Optimize for keyword density

## OVERALL ASSESSMENT:
Your resume shows strong potential with good technical skills and relevant experience. Focus on adding quantifiable achievements and industry-specific keywords to improve ATS compatibility.
```

## Configuration

### Environment Variables
- `OLLAMA_API_KEY`: Your Ollama API key

### Command Line Options
- `--api-key, -k`: Specify API key directly
- `--model, -m`: Choose Ollama model (default: gpt-oss:120b)
- `--job-description, -jd`: Path to job description file
- `--output, -o`: Custom output file path

## Requirements

- Python 3.7+
- requests
- PyPDF2
- python-docx
- python-docx2txt

## Troubleshooting

### Common Issues

1. **API Key Error**: Ensure your Ollama API key is correct and has sufficient credits
2. **File Format Error**: Check that your file is in a supported format
3. **Network Error**: Verify internet connection and API endpoint accessibility

### File Format Issues

- **PDF**: Ensure PDF is not password-protected or image-based
- **DOC**: Requires `python-docx2txt` library for legacy .doc files
- **DOCX**: Standard Word documents work out of the box

## Contributing

Feel free to submit issues and enhancement requests!

## License

This project is open source and available under the MIT License.
