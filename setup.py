"""
Interactive setup script for AI Job Matcher.
Prompts for all required credentials and configuration.
"""

import os
from pathlib import Path
from getpass import getpass


def create_env_file():
    """Create .env file with user input."""
    print("=" * 60)
    print("   AI JOB MATCHER - FREE SETUP")
    print("=" * 60)
    print()
    print("🚨 URGENT MODE: Your visa expires in 2 months!")
    print("   This tool will run every 30 minutes to find jobs FAST.")
    print("   ✨ 100% FREE - Using Google Gemini AI!")
    print()
    print("Let's set up your credentials...\n")
    
    # Google Gemini API Key (FREE)
    print("1. Google Gemini API Key (FREE)")
    print("   Get it from: https://makersuite.google.com/app/apikey")
    print("   - Click 'Get API key'")
    print("   - Create new project or use existing")
    print("   - Copy the key (starts with 'AIza...')")
    print("   Cost: 100% FREE with generous limits!")
    gemini_key = input("   Enter your Gemini API key: ").strip()
    
    print()
    
    # Email Configuration
    print("2. Email Configuration (for job notifications)")
    print("   We'll send you TOP 10 matches every 30 minutes.")
    print()
    email_sender = input("   Your Gmail address: ").strip()
    
    print()
    print("   📌 IMPORTANT: Use Gmail App Password, not your regular password!")
    print("   How to get it:")
    print("   1. Go to: https://myaccount.google.com/apppasswords")
    print("   2. Enable 2-Factor Authentication (required)")
    print("   3. Generate app password for 'Mail'")
    print("   4. Copy the 16-character password")
    print()
    email_password = getpass("   Gmail App Password (hidden): ").strip()
    
    print()
    email_recipient = input("   Email to receive job alerts (can be same): ").strip()
    
    print()
    
    # LinkedIn (Optional)
    print("3. LinkedIn Credentials (OPTIONAL - for better job access)")
    use_linkedin = input("   Add LinkedIn credentials? (y/n): ").strip().lower()
    
    linkedin_email = ""
    linkedin_password = ""
    
    if use_linkedin == 'y':
        linkedin_email = input("   LinkedIn email: ").strip()
        linkedin_password = getpass("   LinkedIn password (hidden): ").strip()
    
    # Create .env file
    env_content = f"""# Google Gemini Configuration (FREE)
GEMINI_API_KEY={gemini_key}

# Email Configuration (for notifications)
EMAIL_SENDER={email_sender}
EMAIL_PASSWORD={email_password}
EMAIL_RECIPIENT={email_recipient}
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587

# Optional: LinkedIn Credentials (for better scraping access)
LINKEDIN_EMAIL={linkedin_email}
LINKEDIN_PASSWORD={linkedin_password}

# Database Configuration
DATABASE_PATH=data/jobs.db

# Application Settings
LOG_LEVEL=INFO
SCHEDULE_ENABLED=true
TIMEZONE=Europe/Berlin

# Matching Configuration
MATCH_THRESHOLD=0.90
MIN_JOBS_TO_NOTIFY=1
MAX_JOBS_PER_EMAIL=10

# Scraping Configuration
MAX_PAGES_PER_SITE=5
REQUEST_DELAY=2
USER_AGENT_ROTATION=true
"""
    
    with open('.env', 'w') as f:
        f.write(env_content)
    
    print()
    print("✅ .env file created successfully!")
    print()


def check_resume():
    """Check if resume exists."""
    resume_pdf = Path('data/resume.pdf')
    resume_txt = Path('data/resume.txt')
    
    print("=" * 60)
    print("   RESUME CHECK")
    print("=" * 60)
    print()
    
    if resume_pdf.exists():
        print(f"✅ Found resume: {resume_pdf}")
        print()
        return True
    elif resume_txt.exists():
        print(f"⚠️  Found text resume: {resume_txt}")
        print("   Please convert to PDF and save as: data/resume.pdf")
        print()
        return False
    else:
        print("❌ No resume found!")
        print()
        print("📝 Please add your resume:")
        print(f"   1. Save as PDF: data/resume.pdf")
        print("   2. Include EVERYTHING: skills, experience, education")
        print("   3. Be detailed - more info = better matches!")
        print()
        return False


def show_next_steps():
    """Show what to do next."""
    print("=" * 60)
    print("   SETUP COMPLETE! ✅")
    print("=" * 60)
    print()
    print("🎯 NEXT STEPS:")
    print()
    print("1. Add your resume as PDF:")
    print("   📁 Save to: data/resume.pdf")
    print("   📌 IMPORTANT: Include ALL details - skills, experience, education, languages!")
    print()
    print("2. Customize job preferences:")
    print("   📝 Edit: config/config.yaml")
    print("   - Job titles you want")
    print("   - Locations (Berlin, Munich, Remote)")
    print("   - Minimum salary")
    print()
    print("3. Install dependencies:")
    print("   💻 Run: pip install -r requirements.txt")
    print()
    print("4. Test the system:")
    print("   🧪 Run: python main.py")
    print()
    print("5. Start automatic job hunting:")
    print("   🚀 Run: python main.py --schedule")
    print("   (Runs every 30 minutes)")
    print()
    print("=" * 60)
    print("💰 100% FREE - No paid APIs needed!")
    print("📧 You'll get TOP 10 job matches every 30 minutes!")
    print("🚨 Urgent mode activated - maximum search frequency!")
    print("⏰ Your visa expires in 2 months - let's find you a job FAST!")
    print("=" * 60)
    print()
    print("☁️  TO DEPLOY ON RAILWAY (Run 24/7):")
    print("   See: RAILWAY_DEPLOYMENT.md")
    print()
    print("Good luck! 🍀🚀")
    print()


def main():
    """Main setup function."""
    # Check if .env already exists
    if Path('.env').exists():
        print("⚠️  .env file already exists!")
        overwrite = input("   Overwrite with new configuration? (y/n): ").strip().lower()
        if overwrite != 'y':
            print("Setup cancelled.")
            return
        print()
    
    # Create .env
    create_env_file()
    
    # Check resume
    check_resume()
    
    # Show next steps
    show_next_steps()


if __name__ == "__main__":
    main()
