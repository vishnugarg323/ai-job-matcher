"""
Resume parser to extract and analyze resume content.
"""

import os
from pathlib import Path
import re
import pdfplumber
from docx import Document
from utils.logger import setup_logger

logger = setup_logger(__name__)


class ResumeParser:
    """Parse and analyze resume content."""
    
    def __init__(self, config):
        """
        Initialize resume parser.
        
        Args:
            config: Application configuration
        """
        self.config = config
        self.resume_path = Path(config['resume']['path'])
        self.resume_text = None
        self.parsed_data = {
            'skills': [],
            'experience': [],
            'education': [],
            'certifications': [],
            'languages': [],
            'full_text': ''
        }
    
    def parse_resume(self):
        """Parse resume and extract structured data."""
        if not self.resume_path.exists():
            raise FileNotFoundError(f"Resume not found at {self.resume_path}")
        
        # Read resume based on format
        resume_format = self.config['resume']['format'].lower()
        
        if resume_format == 'pdf':
            self.resume_text = self._read_pdf()
        elif resume_format == 'docx':
            self.resume_text = self._read_docx()
        else:  # txt
            with open(self.resume_path, 'r', encoding='utf-8') as f:
                self.resume_text = f.read()
        
        self.parsed_data['full_text'] = self.resume_text
        
        # Extract sections
        self._extract_skills()
        self._extract_experience()
        self._extract_education()
        self._extract_certifications()
        self._extract_languages()
        
        logger.info(f"✓ Resume parsed: {len(self.parsed_data['skills'])} skills, "
                   f"{len(self.parsed_data['experience'])} experiences")
        
        return self.parsed_data
    
    def _read_pdf(self):
        """Read PDF resume."""
        text = ""
        try:
            with pdfplumber.open(self.resume_path) as pdf:
                for page in pdf.pages:
                    text += page.extract_text() + "\n"
            logger.info("✓ PDF resume parsed successfully")
            return text
        except Exception as e:
            logger.error(f"Error reading PDF: {e}")
            raise
    
    def _read_docx(self):
        """Read DOCX resume."""
        try:
            doc = Document(self.resume_path)
            text = "\n".join([para.text for para in doc.paragraphs])
            logger.info("✓ DOCX resume parsed successfully")
            return text
        except Exception as e:
            logger.error(f"Error reading DOCX: {e}")
            raise
    
    def _extract_skills(self):
        """Extract skills from resume."""
        # Look for SKILLS section
        skills_pattern = r'SKILLS?\s*:?\s*(.*?)(?=\n[A-Z]{3,}|\Z)'
        match = re.search(skills_pattern, self.resume_text, re.IGNORECASE | re.DOTALL)
        
        if match:
            skills_text = match.group(1)
            # Extract individual skills (comma or bullet separated)
            skills = re.split(r'[,\n•\-\*]', skills_text)
            self.parsed_data['skills'] = [
                skill.strip() for skill in skills 
                if skill.strip() and len(skill.strip()) > 2
            ]
    
    def _extract_experience(self):
        """Extract work experience from resume."""
        # Look for EXPERIENCE/WORK EXPERIENCE section
        exp_pattern = r'(?:WORK\s+)?EXPERIENCE\s*:?\s*(.*?)(?=\n[A-Z]{3,}|\Z)'
        match = re.search(exp_pattern, self.resume_text, re.IGNORECASE | re.DOTALL)
        
        if match:
            exp_text = match.group(1)
            # Split by job entries (usually separated by company names or dates)
            # Store as list of text blocks
            self.parsed_data['experience'] = [exp_text.strip()]
    
    def _extract_education(self):
        """Extract education from resume."""
        edu_pattern = r'EDUCATION\s*:?\s*(.*?)(?=\n[A-Z]{3,}|\Z)'
        match = re.search(edu_pattern, self.resume_text, re.IGNORECASE | re.DOTALL)
        
        if match:
            edu_text = match.group(1)
            self.parsed_data['education'] = [edu_text.strip()]
    
    def _extract_certifications(self):
        """Extract certifications from resume."""
        cert_pattern = r'CERTIFICATIONS?\s*:?\s*(.*?)(?=\n[A-Z]{3,}|\Z)'
        match = re.search(cert_pattern, self.resume_text, re.IGNORECASE | re.DOTALL)
        
        if match:
            cert_text = match.group(1)
            certs = re.split(r'[\n•\-\*]', cert_text)
            self.parsed_data['certifications'] = [
                cert.strip() for cert in certs if cert.strip()
            ]
    
    def _extract_languages(self):
        """Extract languages from resume."""
        lang_pattern = r'LANGUAGES?\s*:?\s*(.*?)(?=\n[A-Z]{3,}|\Z)'
        match = re.search(lang_pattern, self.resume_text, re.IGNORECASE | re.DOTALL)
        
        if match:
            lang_text = match.group(1)
            langs = re.split(r'[\n•\-\*]', lang_text)
            self.parsed_data['languages'] = [
                lang.strip() for lang in langs if lang.strip()
            ]
    
    def get_resume_text(self):
        """Get full resume text."""
        return self.resume_text
    
    def get_skills(self):
        """Get extracted skills."""
        return self.parsed_data['skills']
    
    def get_all_keywords(self):
        """Get all keywords from resume for ATS matching."""
        keywords = set()
        
        # Add skills
        keywords.update([s.lower() for s in self.parsed_data['skills']])
        
        # Extract keywords from experience
        for exp in self.parsed_data['experience']:
            # Extract technical terms (camelCase, PascalCase, or uppercase)
            tech_terms = re.findall(r'\b[A-Z][a-z]+(?:[A-Z][a-z]+)*|\b[A-Z]{2,}\b', exp)
            keywords.update([t.lower() for t in tech_terms])
        
        return list(keywords)
