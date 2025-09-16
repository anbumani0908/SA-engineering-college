import os
import sys
import json
import requests
import argparse
from datetime import datetime
from pathlib import Path
import PyPDF2
import docx
from docx import Document
import re

class ATSResumeChecker:
    def __init__(self, api_key = '75abea0b9b8d4d329432a2fbb6fcf1c8.dr3IdxNsGm0IMSgpN4pKIdDt', model="gpt-oss:120b"):
        """
        Initialize the ATS Resume Checker
        
        Args:
            api_key (str): Ollama API key
            model (str): Model to use for analysis
        """
        self.api_key = api_key
        self.model = model
        self.api_url = "https://ollama.com/api/chat"
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
    
    def extract_text_from_pdf(self, pdf_path):
        """
        Extract text from PDF file
        
        Args:
            pdf_path (str): Path to PDF file
            
        Returns:
            str: Extracted text
        """
        try:
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                text = ""
                for page_num in range(len(pdf_reader.pages)):
                    page = pdf_reader.pages[page_num]
                    text += page.extract_text() + "\n"
                return text.strip()
        except Exception as e:
            raise Exception(f"Error extracting text from PDF: {str(e)}")
    
    def extract_text_from_docx(self, docx_path):
        """
        Extract text from DOCX file
        
        Args:
            docx_path (str): Path to DOCX file
            
        Returns:
            str: Extracted text
        """
        try:
            doc = Document(docx_path)
            text = ""
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
            return text.strip()
        except Exception as e:
            raise Exception(f"Error extracting text from DOCX: {str(e)}")
    
    def extract_text_from_doc(self, doc_path):
        """
        Extract text from DOC file (legacy format)
        Note: This requires python-docx2txt or similar library
        
        Args:
            doc_path (str): Path to DOC file
            
        Returns:
            str: Extracted text
        """
        try:
            # For .doc files, we'll try to use docx2txt
            import docx2txt
            text = docx2txt.process(doc_path)
            return text.strip()
        except ImportError:
            raise Exception("docx2txt library is required for .doc files. Install with: pip install docx2txt")
        except Exception as e:
            raise Exception(f"Error extracting text from DOC: {str(e)}")
    
    def extract_text_from_file(self, file_path):
        """
        Extract text from various file formats
        
        Args:
            file_path (str): Path to the file
            
        Returns:
            str: Extracted text
        """
        file_path = Path(file_path)
        
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        
        file_extension = file_path.suffix.lower()
        
        if file_extension == '.pdf':
            return self.extract_text_from_pdf(file_path)
        elif file_extension == '.docx':
            return self.extract_text_from_docx(file_path)
        elif file_extension == '.doc':
            return self.extract_text_from_doc(file_path)
        elif file_extension == '.txt':
            with open(file_path, 'r', encoding='utf-8') as file:
                return file.read().strip()
        else:
            raise ValueError(f"Unsupported file format: {file_extension}")
    
    def analyze_resume_with_ollama(self, resume_text, job_description=None):
        """
        Analyze resume using Ollama AI
        
        Args:
            resume_text (str): Resume text content
            job_description (str): Optional job description for targeted analysis
            
        Returns:
            str: Analysis results
        """
        # Create comprehensive prompt for ATS analysis
        if job_description:
            prompt = f"""
            As an expert ATS (Applicant Tracking System) analyst and career coach, please analyze this resume against the provided job description. Provide a comprehensive assessment covering:

            RESUME TEXT:
            {resume_text}

            JOB DESCRIPTION:
            {job_description}

            Please provide analysis in the following format:

            ## ATS COMPATIBILITY SCORE: [X/10]

            ## KEYWORD MATCHING:
            - [List matched keywords]
            - [List missing important keywords]

            ## SECTION ANALYSIS:
            ### Contact Information: [Score/10]
            [Analysis and recommendations]

            ### Professional Summary/Objective: [Score/10]
            [Analysis and recommendations]

            ### Work Experience: [Score/10]
            [Analysis and recommendations]

            ### Skills Section: [Score/10]
            [Analysis and recommendations]

            ### Education: [Score/10]
            [Analysis and recommendations]

            ## STRENGTHS:
            - [List key strengths]

            ## AREAS FOR IMPROVEMENT:
            - [List specific improvement areas]

            ## ATS OPTIMIZATION RECOMMENDATIONS:
            - [Specific actionable recommendations]

            ## OVERALL ASSESSMENT:
            [Comprehensive summary and next steps]
            """
        else:
            prompt = f"""
            As an expert ATS (Applicant Tracking System) analyst and career coach, please analyze this resume for general ATS compatibility and optimization. Provide a comprehensive assessment covering:

            RESUME TEXT:
            {resume_text}

            Please provide analysis in the following format:

            ## ATS COMPATIBILITY SCORE: [X/10]

            ## SECTION ANALYSIS:
            ### Contact Information: [Score/10]
            [Analysis and recommendations]

            ### Professional Summary/Objective: [Score/10]
            [Analysis and recommendations]

            ### Work Experience: [Score/10]
            [Analysis and recommendations]

            ### Skills Section: [Score/10]
            [Analysis and recommendations]

            ### Education: [Score/10]
            [Analysis and recommendations]

            ## STRENGTHS:
            - [List key strengths]

            ## AREAS FOR IMPROVEMENT:
            - [List specific improvement areas]

            ## ATS OPTIMIZATION RECOMMENDATIONS:
            - [Specific actionable recommendations]

            ## KEYWORD OPTIMIZATION:
            - [Suggestions for industry-relevant keywords]

            ## OVERALL ASSESSMENT:
            [Comprehensive summary and next steps]
            """
        
        payload = {
            "model": self.model,
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "stream": False
        }
        
        try:
            response = requests.post(
                self.api_url, 
                headers=self.headers, 
                data=json.dumps(payload),
                timeout=60
            )
            
            if response.status_code == 200:
                data = response.json()
                return data.get("message", {}).get("content", "No analysis received")
            else:
                raise Exception(f"API request failed: {response.status_code} - {response.text}")
                
        except requests.exceptions.RequestException as e:
            raise Exception(f"Network error: {str(e)}")
    
    def save_analysis_to_file(self, analysis_text, output_path=None):
        """
        Save analysis results to a text file
        
        Args:
            analysis_text (str): Analysis results
            output_path (str): Optional custom output path
            
        Returns:
            str: Path to saved file
        """
        if output_path is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = f"ats_analysis_{timestamp}.txt"
        
        # Ensure output directory exists
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Add header to the analysis
        header = f"""
================================================================================
ATS RESUME ANALYSIS REPORT
Generated on: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
Model Used: {self.model}
================================================================================

"""
        
        full_content = header + analysis_text
        
        with open(output_path, 'w', encoding='utf-8') as file:
            file.write(full_content)
        
        return str(output_path)
    
    def check_resume(self, resume_path, job_description_path=None, output_path=None):
        """
        Main method to check resume
        
        Args:
            resume_path (str): Path to resume file
            job_description_path (str): Optional path to job description file
            output_path (str): Optional custom output path
            
        Returns:
            str: Path to saved analysis file
        """
        print("🔍 Starting ATS Resume Analysis...")
        
        # Extract resume text
        print(f"📄 Extracting text from resume: {resume_path}")
        resume_text = self.extract_text_from_file(resume_path)
        
        # Extract job description if provided
        job_description = None
        if job_description_path:
            print(f"📋 Extracting job description from: {job_description_path}")
            job_description = self.extract_text_from_file(job_description_path)
        
        # Analyze with Ollama
        print("🤖 Analyzing resume with Ollama AI...")
        analysis = self.analyze_resume_with_ollama(resume_text, job_description)
        
        # Save results
        print("💾 Saving analysis results...")
        saved_path = self.save_analysis_to_file(analysis, output_path)
        
        print(f"✅ Analysis complete! Results saved to: {saved_path}")
        return saved_path

def main():
    """Main function to run the ATS checker from command line"""
    parser = argparse.ArgumentParser(description="ATS Resume Checker using Ollama AI")
    parser.add_argument("resume", help="Path to resume file (PDF, DOC, DOCX, or TXT)")
    parser.add_argument("--job-description", "-jd", help="Path to job description file (optional)")
    parser.add_argument("--output", "-o", help="Output file path (optional)")
    parser.add_argument("--api-key", "-k", help="Ollama API key (or set OLLAMA_API_KEY env var)")
    parser.add_argument("--model", "-m", default="gpt-oss:120b", help="Ollama model to use")
    
    args = parser.parse_args()
    
    # Get API key (use default from class if not provided)
    api_key = args.api_key or os.getenv("OLLAMA_API_KEY")
    
    # Initialize checker (will use default API key if none provided)
    checker = ATSResumeChecker(api_key, args.model)
    
    try:
        # Run analysis
        output_file = checker.check_resume(
            args.resume,
            args.job_description,
            args.output
        )
        
        print(f"\n🎉 Analysis completed successfully!")
        print(f"📁 Results saved to: {output_file}")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
