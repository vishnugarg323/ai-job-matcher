"""
AI-powered job matcher using Google Gemini AI (FREE).
"""

import os
import google.generativeai as genai
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from datetime import datetime, timedelta
from utils.logger import setup_logger

logger = setup_logger(__name__)


class JobMatcher:
    """Match jobs with resume using FREE Google Gemini AI."""
    
    def __init__(self, config, resume_parser):
        """
        Initialize job matcher.
        
        Args:
            config: Application configuration
            resume_parser: ResumeParser instance
        """
        self.config = config
        self.resume_parser = resume_parser
        
        # Initialize Google Gemini (FREE)
        api_key = os.getenv('GEMINI_API_KEY')
        if not api_key:
            raise ValueError("GEMINI_API_KEY not found in environment variables. Get it free from https://makersuite.google.com/app/apikey")
        
        genai.configure(api_key=api_key)
        self.embedding_model = config['matching']['gemini_embedding_model']
        self.use_advanced = config['matching'].get('use_gemini_pro', True)
        self.chat_model = config['matching'].get('gemini_chat_model', 'gemini-1.5-pro')
        self.threshold = config['matching']['threshold']
        
        # Cache resume embedding
        self.resume_embedding = None
    
    def _get_embedding(self, text):
        """
        Get embedding for text using Google Gemini (FREE).
        
        Args:
            text: Text to embed
            
        Returns:
            Numpy array of embedding
        """
        try:
            result = genai.embed_content(
                model=self.embedding_model,
                content=text,
                task_type="retrieval_document"
            )
            return np.array(result['embedding'])
        except Exception as e:
            logger.error(f"Error getting embedding: {e}")
            return None
    
    def _get_resume_embedding(self):
        """Get or cache resume embedding."""
        if self.resume_embedding is None:
            resume_text = self.resume_parser.get_resume_text()
            if not resume_text:
                raise ValueError("Resume not parsed yet")
            
            logger.info("🧠 Generating resume embedding...")
            self.resume_embedding = self._get_embedding(resume_text)
        
        return self.resume_embedding
    
    def _calculate_similarity(self, job_description):
        """
        Calculate similarity between resume and job description.
        
        Args:
            job_description: Job description text
            
        Returns:
            Similarity score (0-1)
        """
        resume_emb = self._get_resume_embedding()
        if resume_emb is None:
            return 0.0
        
        job_emb = self._get_embedding(job_description)
        if job_emb is None:
            return 0.0
        
        # Calculate cosine similarity
        similarity = cosine_similarity(
            resume_emb.reshape(1, -1),
            job_emb.reshape(1, -1)
        )[0][0]
        
        return float(similarity)
    
    def _analyze_with_gemini(self, job_description, resume_text):
        """
        Use Gemini Pro to deeply analyze job fit (FREE, optional for critical matches).
        
        Args:
            job_description: Job description
            resume_text: Resume text
            
        Returns:
            Analysis score and insights
        """
        if not self.use_advanced:
            return None
        
        try:
            prompt = f"""Analyze this job match for urgency and fit. Rate 0-100.
            
Resume Summary: {resume_text[:1000]}

Job Description: {job_description[:1000]}

Consider:
1. Skills match
2. Experience level fit
3. Fast hiring indicators (urgent, immediate, ASAP)
4. Visa sponsorship mentions
5. Remote work options

Return JSON: {{"score": 0-100, "urgency": "low/medium/high", "reason": "brief explanation"}}"""
            
            model = genai.GenerativeModel(self.chat_model)
            response = model.generate_content(
                prompt,
                generation_config=genai.types.GenerationConfig(
                    temperature=0.3,
                    max_output_tokens=200
                )
            )
            
            return response.text
        except Exception as e:
            logger.debug(f"Gemini analysis skipped: {e}")
            return None
    
    def _calculate_keyword_match(self, job_description):
        """
        Calculate keyword match score for ATS compatibility.
        
        Args:
            job_description: Job description text
            
        Returns:
            Tuple of (score, matched_keywords)
        """
        resume_keywords = set(self.resume_parser.get_all_keywords())
        job_text_lower = job_description.lower()
        
        matched = []
        for keyword in resume_keywords:
            if keyword in job_text_lower:
                matched.append(keyword)
        
        if not resume_keywords:
            return 0.0, []
        
        score = len(matched) / len(resume_keywords)
        return score, matched
    
    def match_jobs(self, jobs):
        """
        Match jobs with resume and filter by threshold.
        Now includes urgency scoring for fast hiring.
        
        Args:
            jobs: List of job dictionaries
            
        Returns:
            List of matched jobs with scores (TOP 10 only)
        """
        matched_jobs = []
        max_age_days = self.config['search'].get('max_job_age_days', 14)
        cutoff_date = datetime.now() - timedelta(days=max_age_days)
        
        for i, job in enumerate(jobs):
            try:
                logger.info(f"  Matching {i+1}/{len(jobs)}: {job['title']} at {job['company']}")
                
                # Get job description
                description = job.get('description', '')
                if not description:
                    logger.warning(f"  ⚠️  No description for {job['title']}, skipping")
                    continue
                
                # Check job age (if posted_date available)
                if job.get('posted_date'):
                    try:
                        posted = datetime.fromisoformat(job['posted_date'])
                        if posted < cutoff_date:
                            logger.debug(f"  ✗ Job too old: {job['posted_date']}")
                            continue
                    except:
                        pass
                
                # Calculate AI similarity
                ai_score = self._calculate_similarity(description)
                
                # Calculate keyword match
                keyword_score, matched_keywords = self._calculate_keyword_match(description)
                
                # Check for urgency indicators
                urgency_boost = self._calculate_urgency_score(description)
                
                # Weighted score with urgency boost
                weights = self.config['matching']['weights']
                final_score = (
                    ai_score * weights['description_match'] + 
                    keyword_score * weights['skills'] +
                    urgency_boost * 0.1  # 10% boost for urgent positions
                )
                
                # Normalize to 0-1 range
                final_score = min(1.0, max(0.0, final_score))
                
                job['match_score'] = round(final_score, 3)
                job['ai_similarity'] = round(ai_score, 3)
                job['keyword_match'] = round(keyword_score, 3)
                job['urgency_score'] = round(urgency_boost, 3)
                job['keywords_matched'] = matched_keywords[:20]  # Top 20
                
                # Check threshold
                if final_score >= self.threshold:
                    matched_jobs.append(job)
                    logger.info(f"  ✓ Match: {final_score:.1%} (AI: {ai_score:.1%}, Keywords: {keyword_score:.1%}, Urgency: +{urgency_boost:.1%})")
                else:
                    logger.debug(f"  ✗ Below threshold: {final_score:.1%}")
                    
            except Exception as e:
                logger.error(f"  ❌ Error matching job {job.get('title')}: {e}")
                continue
        
        # Sort by score and return TOP 10 only
        matched_jobs.sort(key=lambda x: x['match_score'], reverse=True)
        top_jobs = matched_jobs[:10]
        
        if len(matched_jobs) > 10:
            logger.info(f"  🎯 Returning top 10 matches (out of {len(matched_jobs)} total matches)")
        
        return top_jobs
    
    def _calculate_urgency_score(self, job_description):
        """
        Calculate urgency score based on job description keywords.
        Prioritizes fast-hiring companies.
        
        Args:
            job_description: Job description text
            
        Returns:
            Urgency score (0-1)
        """
        urgency_keywords = [
            'urgent', 'immediate', 'asap', 'immediately', 'fast track',
            'quick hire', 'start now', 'start immediately', 'soon as possible',
            'visa sponsor', 'sponsorship', 'relocation', 'expedited',
            'hiring now', 'join immediately', 'immediate start'
        ]
        
        desc_lower = job_description.lower()
        matches = sum(1 for keyword in urgency_keywords if keyword in desc_lower)
        
        # Score: 0-1 based on urgency keyword density
        urgency_score = min(1.0, matches / 5.0)
        
        return urgency_score
    
    def analyze_match(self, job):
        """
        Provide detailed analysis of why a job matched.
        
        Args:
            job: Job dictionary with match scores
            
        Returns:
            Analysis text
        """
        analysis = []
        analysis.append(f"Match Score: {job['match_score']:.1%}")
        analysis.append(f"AI Similarity: {job['ai_similarity']:.1%}")
        analysis.append(f"Keyword Match: {job['keyword_match']:.1%}")
        
        if job.get('keywords_matched'):
            top_keywords = job['keywords_matched'][:10]
            analysis.append(f"Matched Keywords: {', '.join(top_keywords)}")
        
        return '\n'.join(analysis)
