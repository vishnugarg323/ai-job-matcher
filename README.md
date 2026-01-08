# AI Job Matcher - Germany Edition (100% FREE + WEB UI)

An intelligent job matching system that automatically finds jobs matching your resume with 90%+ accuracy, specifically targeting the German job market. **Now with FREE Google Gemini AI and Beautiful Web Dashboard!**

## 🎨 NEW in Version 3.0 - WEB UI DASHBOARD!

**Professional multi-profile system with beautiful web interface:**
- ✅ **Web Dashboard** - Manage everything via browser
- ✅ **Multi-Profile Support** - Upload multiple resumes
- ✅ **Resume Upload via UI** - No more manual file copying
- ✅ **Manual Triggers** - Start job search with one click
- ✅ **Live Statistics** - Real-time dashboard
- ✅ **Job Results Table** - See all matches in UI
- ✅ **Run History** - Track success/failure of runs
- ✅ **Per-Profile Configuration** - Each resume has own settings

## 🚨 URGENT MODE - Visa Expires in 2 Months!

This system is optimized for **FAST job hunting**:
- ✅ Runs **every 30 minutes** (48 times/day)
- ✅ **100% FREE** - Google Gemini AI (no paid APIs!)
- ✅ Finds jobs posted **within 14 days** (fast hiring)
- ✅ Sends **TOP 10** matches per email (no spam)
- ✅ **NO duplicates** - tracks sent jobs
- ✅ **Cloud-ready** - Deploy on Railway for 24/7 operation

## Features

- 🎨 **Web Dashboard**: Beautiful UI to manage profiles, upload resumes, view jobs
- ✨ **AI-Powered Matching**: Uses Google Gemini embeddings for semantic similarity (FREE!)
- 👥 **Multi-Profile Support**: Create unlimited job search profiles with different resumes
- 🎯 **High Accuracy**: Targets 90%+ match rate using advanced AI
- 🔄 **Every 30 Minutes**: Maximum search frequency for urgent job hunting
- 🌐 **Multiple Sources**: Scrapes from LinkedIn, Indeed, StepStone German portals
- 📊 **ATS Analysis**: Ensures your resume would pass ATS systems for matched jobs
- 📧 **Email Notifications**: Sends top 10 matches every 30 minutes
- 🗄️ **Duplicate Prevention**: Tracks previously sent jobs to avoid repetition
- 🇩🇪 **Germany Focused**: Specifically targets German job market
- ☁️ **Cloud-Ready**: Deploy on Railway for 24/7 operation
- 💰 **100% Free Tools**: Google Gemini AI (no OpenAI costs!)

## Project Structure

```
AI Job Application/
├── web_app.py                # Flask web server (NEW!)
├── templates/
│   └── dashboard.html        # Beautiful UI (NEW!)
├── config/
│   └── config.yaml          # Main configuration
├── data/
│   ├── uploads/             # Resume uploads (NEW!)
│   ├── resume.pdf           # Your resume (PDF format)
│   └── jobs.db              # SQLite database
├── src/
│   ├── scrapers/
│   │   ├── linkedin_scraper.py
│   │   ├── indeed_scraper.py
│   │   └── stepstone_scraper.py
│   ├── matchers/
│   │   ├── resume_parser.py   # PDF/DOCX support
│   │   └── job_matcher.py     # Gemini AI matching
│   ├── database/
│   │   ├── db_manager.py      # Original DB
│   │   └── multi_profile_db.py # Multi-profile DB (NEW!)
│   └── notifiers/
│       └── email_notifier.py  # Email notifications
│   │   └── email_notifier.py  # Email notifications
│   └── scheduler/
│       └── job_scheduler.py    # Daily scheduling
├── logs/                       # Application logs
├── main.py                     # Main application entry point
├── requirements.txt            # Python dependencies
├── .env.example                # Environment variables template
└── .gitignore                  # Git ignore file
```

## Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Credentials

Copy `.env.example` to `.env` and fill in your credentials:

```bash
cp .env.example .env
```

Required credentials:
- OpenAI API key (for AI matching)
- Email credentials (for notifications)
- Optional: LinkedIn credentials (for better scraping)

### 3. Add Your Resume

Place your resume in `data/resume.txt` as plain text. Keep all your:
- Skills
- Experience
- Education
- Certifications
- Languages

### 4. Configure Preferences

Edit `config/config.yaml` to set:
- Job titles you're interested in
- Locations in Germany
- Minimum salary expectations
- Experience level
- Work arrangement (remote/hybrid/onsite)

### 5. Run the Application

## Quick Start

### ⚡ Super Fast Setup (5 minutes)

1. **Get Free Gemini API Key**
   ```
   https://makersuite.google.com/app/apikey
   ```

2. **Run Setup**
   ```bash
   python setup.py
   ```
   Prompts for: Gemini key, Gmail credentials

3. **Add Resume**
   ```bash
   # Copy your resume PDF to:
   data/resume.pdf
   ```

4. **Start Job Hunting**
   ```bash
   # Test run (once)
   python main.py

   # Automatic mode (every 30 minutes)
   python main.py --schedule
   ```

5. **Deploy to Cloud (Optional)**
   See [RAILWAY_DEPLOYMENT.md](RAILWAY_DEPLOYMENT.md) for 24/7 operation

### 📚 Documentation
- **[QUICK_START.md](QUICK_START.md)** - Fast setup guide
- **[WHAT_YOU_NEED.md](WHAT_YOU_NEED.md)** - What to provide
- **[RAILWAY_DEPLOYMENT.md](RAILWAY_DEPLOYMENT.md)** - Cloud deployment guide

---

## How It Works

1. **Scraping**: Every 30 minutes, scrapes job postings from German portals (Indeed, StepStone, LinkedIn)
2. **Parsing**: Extracts job details (title, description, requirements, location, salary)
3. **AI Matching** (Google Gemini - FREE): 
   - Converts your resume and job descriptions into embeddings
   - Calculates semantic similarity scores
   - Filters jobs with 90%+ match
   - Adds urgency scoring for fast-hiring jobs
4. **ATS Analysis**: Checks if your resume has keywords matching the job description
5. **Duplicate Removal**: Tracks sent jobs to avoid repetition
6. **Storage**: Saves matched jobs to SQLite database
7. **Notification**: Sends email with **TOP 10** matches only

## Technical Stack

- **Python 3.11**
- **Google Gemini AI**: For semantic embeddings and matching (FREE!)
- **BeautifulSoup4 & Selenium**: For web scraping with Chrome
- **SQLite**: For local database
- **APScheduler**: For 30-minute scheduling
- **SMTP**: For Gmail notifications
- **Railway**: Cloud hosting (optional, $0-3/month)

## Configuration Options

### Match Threshold
Adjust the matching threshold in `config/config.yaml`:
```yaml
matching:
  threshold: 0.90  # 90% similarity
  min_keyword_match: 0.75  # 75% keyword overlap for ATS
  gemini_embedding_model: "models/text-embedding-004"
  use_gemini_pro: true  # Advanced analysis
```

### Scraping Schedule
```yaml
schedule:
  interval_minutes: 30  # Every 30 minutes (URGENT MODE)
  timezone: "Europe/Berlin"
  max_job_age_days: 14  # Only fresh jobs (within 2 weeks)
```

### Email Notifications
```yaml
notifications:
  enabled: true
  max_jobs_per_email: 10  # Top 10 only (no spam)
  smtp_server: "smtp.gmail.com"
```

## Privacy & Data

- All data is stored locally on your machine (or Railway cloud if deployed)
- Your resume never leaves your system except for Gemini API calls (encrypted HTTPS)
- Job data is stored in a local SQLite database
- Gemini API: Google's privacy policy applies
- No third-party tracking or data sharing
- Credentials stored in `.env` file (never committed to Git)

## Troubleshooting

### Scraping Issues
- Some websites may block automated scraping. The system uses rotating user agents and delays.
- For LinkedIn, you may need to provide credentials for better access.

### Low Match Rates
- Review your resume format - ensure it's comprehensive
- Adjust the threshold in config if too strict
- Check logs for any parsing errors

## Future Enhancements

- [ ] Add more German job portals (XING, Monster.de)
- [ ] Web dashboard for viewing matches
- [ ] Mobile app notifications
- [ ] Machine learning to learn your preferences over time
- [ ] Integration with job application tracking
- [ ] Auto-apply feature (optional)

## Legal Note

This tool is for personal use only. Ensure you comply with the terms of service of job portals you scrape. Always respect robots.txt and rate limits.

## License

MIT License - Free for personal use

## Support

For issues or questions, check the logs in the `logs/` directory or review the configuration files.
