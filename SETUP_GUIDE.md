# AI Job Matcher - Quick Setup Guide

## Prerequisites

- Python 3.9 or higher
- Google Chrome browser (for web scraping)
- OpenAI API key
- Email account (Gmail recommended)

## Step-by-Step Setup

### 1. Install Python Dependencies

Open PowerShell in the project directory and run:

```powershell
pip install -r requirements.txt
```

This will install all required packages including:
- OpenAI for AI matching
- Selenium for web scraping
- APScheduler for automation
- And more...

### 2. Configure Environment Variables

Create a `.env` file in the project root:

```powershell
Copy-Item .env.example .env
notepad .env
```

Fill in your credentials:

```
# Required: OpenAI API Key
OPENAI_API_KEY=sk-your-openai-api-key-here

# Required: Email for notifications
EMAIL_SENDER=your.email@gmail.com
EMAIL_PASSWORD=your-app-password
EMAIL_RECIPIENT=your.email@gmail.com
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587

# Optional: LinkedIn (for better scraping)
LINKEDIN_EMAIL=your.linkedin@email.com
LINKEDIN_PASSWORD=your-linkedin-password
```

**Important for Gmail:**
- Don't use your regular Gmail password!
- Use an "App Password": https://support.google.com/accounts/answer/185833
- Go to: Google Account → Security → 2-Step Verification → App Passwords
- Generate an app password and use that in EMAIL_PASSWORD

### 3. Add Your Resume

Edit `data/resume.txt` and paste your complete resume:

```powershell
notepad data\resume.txt
```

**Tips:**
- Include ALL your skills (programming languages, frameworks, tools)
- Include detailed work experience
- Include education, certifications, languages
- More detail = better matching!

### 4. Configure Job Preferences

Edit `config/config.yaml`:

```powershell
notepad config\config.yaml
```

Customize:
- Job titles you're interested in
- Locations in Germany (Berlin, Munich, Hamburg, Remote, etc.)
- Required keywords (skills you have)
- Excluded keywords (things to avoid)
- Minimum salary

### 5. Test the Application

Run once to test:

```powershell
python main.py
```

This will:
1. Parse your resume
2. Scrape jobs from Indeed, StepStone, LinkedIn
3. Match jobs using AI
4. Save results to database
5. Send email with matches

### 6. Set Up Daily Automation

To run automatically every morning at 8 AM:

```powershell
python main.py --schedule
```

Keep this terminal window open (or run as a background service).

**Alternative: Windows Task Scheduler**

Create a scheduled task to run daily:

1. Open Task Scheduler
2. Create Basic Task
3. Name: "AI Job Matcher"
4. Trigger: Daily at 8:00 AM
5. Action: Start a program
   - Program: `python`
   - Arguments: `main.py`
   - Start in: `C:\Users\vishn\AI Job Application`

## Troubleshooting

### ChromeDriver Issues

If Selenium can't find Chrome:
```powershell
pip install --upgrade webdriver-manager
```

### OpenAI API Errors

- Check your API key is valid
- Check you have credits: https://platform.openai.com/account/billing
- The app uses `text-embedding-3-small` model (very cheap, ~$0.01 per run)

### Email Not Sending

- Use Gmail App Password, not regular password
- Enable 2-Factor Authentication first
- Allow "Less secure app access" if needed

### No Jobs Found

- Check your internet connection
- Some sites may block automated scraping
- Try adjusting search keywords in config
- Check logs in `logs/app.log`

### Too Many/Few Matches

Adjust match threshold in `config/config.yaml`:
```yaml
matching:
  threshold: 0.85  # Lower = more results (try 0.85-0.95)
```

## Usage Tips

### View All Matches

Jobs are stored in SQLite database at `data/jobs.db`

View with any SQLite browser:
```powershell
# Install SQLite browser
winget install DB.Browser.SQLiteBrowser

# Open database
& "C:\Program Files\DB Browser for SQLite\DB Browser for SQLite.exe" data\jobs.db
```

### Check Logs

```powershell
notepad logs\app.log
```

### Run Different Times

Edit `config/config.yaml`:
```yaml
schedule:
  run_time: "09:30"  # 9:30 AM
```

### Disable Scrapers

If a scraper fails, disable it:
```yaml
scraping:
  enabled_scrapers:
    - "indeed"
    - "stepstone"
    # - "linkedin"  # Commented out
```

## Cost Estimate

**OpenAI API Costs:**
- Embedding model: ~$0.01 per 1000 jobs analyzed
- Daily run with ~100 jobs: ~$0.001/day = ~$0.30/year
- Very affordable!

**Time Saved:**
- Manual job search: 1-2 hours/day
- This tool: 2 minutes/day to review matches
- **Saves ~10+ hours per week!**

## Next Steps

1. Run the application once manually
2. Review the matches you receive
3. Adjust threshold and keywords as needed
4. Set up daily automation
5. Check your email every morning for new matches!

## Support

Check logs for errors:
```powershell
Get-Content logs\app.log -Tail 50
```

Common commands:
```powershell
# Run once
python main.py

# Run with scheduling
python main.py --schedule

# Check if it's working
Get-Process | Where-Object {$_.ProcessName -eq "python"}
```

Good luck with your job search! 🚀
