"""
ATS (Applicant Tracking System) analyzer.
"""

import re
from utils.logger import setup_logger

logger = setup_logger(__name__)


class ATSAnalyzer:
    """Analyze ATS compatibility between resume and job description."""
    
    def __init__(self, config, resume_parser):
        """
        Initialize ATS analyzer.
        
        Args:
            config: Application configuration
            resume_parser: ResumeParser instance
        """
        self.config = config
        self.resume_parser = resume_parser
        self.min_keyword_match = config['matching']['min_keyword_match']
    
    def analyze_compatibility(self, job_description):
        """
        Analyze if resume would pass ATS for this job.
        
        Args:
            job_description: Job description text
            
        Returns:
            Dict with compatibility analysis
        """
        # Extract required skills from job description
        required_skills = self._extract_required_skills(job_description)
        
        # Get resume skills
        resume_skills = set([s.lower() for s in self.resume_parser.get_skills()])
        
        # Check matches
        matched_skills = []
        missing_skills = []
        
        for skill in required_skills:
            if skill.lower() in resume_skills:
                matched_skills.append(skill)
            else:
                missing_skills.append(skill)
        
        # Calculate score
        if required_skills:
            score = len(matched_skills) / len(required_skills)
        else:
            score = 0.0
        
        # Determine pass/fail
        passes_ats = score >= self.min_keyword_match
        
        return {
            'passes_ats': passes_ats,
            'score': score,
            'required_skills': required_skills,
            'matched_skills': matched_skills,
            'missing_skills': missing_skills,
            'match_percentage': f"{score*100:.0f}%"
        }
    
    def _extract_required_skills(self, job_description):
        """
        Extract required skills from job description.
        
        Args:
            job_description: Job description text
            
        Returns:
            List of skills
        """
        skills = set()
        
        # Common skill patterns
        patterns = [
            r'(?:required|must have|should have|experience with)[\s:]+(.*?)(?:\.|;|\n)',
            r'(?:skills|qualifications|requirements)[\s:]+.*?([A-Za-z][A-Za-z+#/.]+)',
            r'\b([A-Z][a-z]+(?:[A-Z][a-z]+)+)\b',  # CamelCase
            r'\b([A-Z]{2,})\b',  # Acronyms
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, job_description, re.IGNORECASE)
            for match in matches:
                if isinstance(match, tuple):
                    match = match[0]
                # Clean and split
                words = re.split(r'[,\s]+', match.strip())
                for word in words:
                    word = word.strip('.,;:')
                    if len(word) > 2 and not word.lower() in ['and', 'or', 'the', 'with']:
                        skills.add(word)
        
        return list(skills)
    
    def generate_recommendations(self, analysis):
        """
        Generate recommendations for improving ATS score.
        
        Args:
            analysis: Analysis dict from analyze_compatibility
            
        Returns:
            List of recommendations
        """
        recommendations = []
        
        if not analysis['passes_ats']:
            recommendations.append(
                f"⚠️ ATS Score: {analysis['match_percentage']} "
                f"(minimum: {self.min_keyword_match*100:.0f}%)"
            )
            
            if analysis['missing_skills']:
                top_missing = analysis['missing_skills'][:5]
                recommendations.append(
                    f"Consider gaining experience with: {', '.join(top_missing)}"
                )
        else:
            recommendations.append(
                f"✓ ATS Compatible: {analysis['match_percentage']} match"
            )
        
        return recommendations
