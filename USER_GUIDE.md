# 🎯 AI Job Matcher - Complete User Guide

## What This Application Does

This intelligent system automatically:
1. **Scrapes** job postings from German job portals (Indeed, StepStone, LinkedIn)
2. **Analyzes** your resume using AI
3. **Matches** jobs with 90%+ compatibility
4. **Filters** duplicates and irrelevant positions
5. **Sends** daily email reports with top matches
6. **Tracks** all jobs in a local database

## Quick Start (3 Steps)

### Step 1: Setup (5 minutes)

1. **Get OpenAI API Key** (Required)
   - Go to: https://platform.openai.com/api-keys
   - Create account if needed (free trial available)
   - Generate new API key
   - Cost: ~$0.01 per day (~$3/year)

2. **Setup Gmail App Password** (Required for notifications)
   - Go to: https://myaccount.google.com/apppasswords
   - Enable 2-Factor Authentication if not already
   - Generate App Password for "Mail"
   - Save this password

3. **Configure the App**
   ```powershell
   # Copy example config
   Copy-Item .env.example .env
   
   # Edit with your details
   notepad .env
   ```
   
   Fill in:
   - `OPENAI_API_KEY` = Your OpenAI key
   - `EMAIL_SENDER` = Your Gmail address
   - `EMAIL_PASSWORD` = App password from step 2
   - `EMAIL_RECIPIENT` = Where to receive notifications

### Step 2: Add Your Resume (5 minutes)

```powershell
notepad data\resume.txt
```

Paste your COMPLETE resume including:
- ✅ All technical skills (Python, AWS, Docker, etc.)
- ✅ Work experience (detailed descriptions)
- ✅ Education and certifications
- ✅ Languages (English, German levels)
- ✅ Projects and achievements

**The more detailed, the better the matching!**

### Step 3: Run It!

**Option A: Run Once (Test)**
```powershell
python main.py
```

**Option B: Daily Automation**
```powershell
python main.py --schedule
```

Or just double-click: `run.bat` (run once) or `run_scheduled.bat` (daily)

## Understanding the Matching Process

### How AI Matching Works

1. **Resume Analysis**
   - Extracts your skills, experience, education
   - Creates an AI embedding (mathematical representation)
   - Identifies key keywords for ATS compatibility

2. **Job Scraping**
   - Searches configured job titles and locations
   - Retrieves full job descriptions
   - Tracks posting dates

3. **Intelligent Matching**
   - **Semantic Similarity (AI)**: Compares meaning, not just keywords
   - **Keyword Match (ATS)**: Ensures resume would pass screening
   - **Weighted Score**: Combines both approaches
   - **Threshold Filter**: Only shows 90%+ matches

4. **Result Ranking**
   - Sorts by match score
   - Removes duplicates
   - Highlights matched keywords

### Match Score Breakdown

- **90-95%**: Good match, worth applying
- **95-98%**: Excellent match, high priority
- **98-100%**: Perfect match, apply immediately!

Each match shows:
- Overall Match Score
- AI Similarity Score
- Keyword Match Score
- Matched Keywords

## Customization Guide

### Adjust Job Search Criteria

Edit `config/config.yaml`:

```yaml
search:
  job_titles:
    - "Software Engineer"
    - "DevOps Engineer"  # Add more
    - "Cloud Architect"
  
  locations:
    - "Berlin"
    - "Munich"
    - "Remote"  # Very important!
  
  min_salary: 70000  # Annual in EUR
  
  required_keywords:  # Must have these
    - "Python"
    - "Docker"
  
  exclude_keywords:  # Filter out these
    - "Internship"
    - "Junior"
```

### Adjust Match Threshold

If getting too many/few results:

```yaml
matching:
  threshold: 0.90  # 90% (default)
  # Try 0.85 for more results
  # Try 0.95 for fewer, higher quality results
```

### Change Schedule

```yaml
schedule:
  run_time: "08:00"  # 8 AM
  timezone: "Europe/Berlin"
  run_days: [0, 1, 2, 3, 4]  # Mon-Fri
  # 0=Monday, 6=Sunday
```

### Enable/Disable Scrapers

If a scraper fails or is slow:

```yaml
scraping:
  enabled_scrapers:
    - "indeed"      # Usually reliable
    - "stepstone"   # Germany-specific
    # - "linkedin"  # Comment out to disable
```

### Notification Settings

```yaml
notifications:
  email_enabled: true
  min_jobs: 1  # Minimum matches to send email
  max_jobs_per_email: 20
  include_description: true  # Include job descriptions
```

## Advanced Features

### Database Queries

View all your matches using SQLite:

```powershell
# Install DB Browser
winget install DB.Browser.SQLiteBrowser

# Open database
& "C:\Program Files\DB Browser for SQLite\DB Browser for SQLite.exe" data\jobs.db
```

Example queries:
```sql
-- Top 10 matches
SELECT title, company, match_score, url 
FROM jobs 
ORDER BY match_score DESC 
LIMIT 10;

-- Jobs from specific company
SELECT * FROM jobs 
WHERE company LIKE '%Amazon%';

-- Recent high matches
SELECT title, company, match_score, created_at
FROM jobs
WHERE match_score >= 0.95
ORDER BY created_at DESC;
```

### Logs and Debugging

Check application logs:
```powershell
notepad logs\app.log
```

View recent activity:
```powershell
Get-Content logs\app.log -Tail 50
```

### LinkedIn Integration (Optional)

For better LinkedIn access, add credentials to `.env`:

```
LINKEDIN_EMAIL=your.email@example.com
LINKEDIN_PASSWORD=your_password
```

⚠️ **Warning**: LinkedIn may flag automated access. Use carefully!

### Proxy Configuration (Optional)

If scraping is blocked:

```
PROXY_URL=http://your-proxy:port
```

## Troubleshooting

### Issue: "No jobs found"

**Solutions:**
1. Check internet connection
2. Verify job titles are not too specific
3. Check logs for errors: `notepad logs\app.log`
4. Try disabling problematic scrapers
5. Increase max_pages in config

### Issue: "Match scores too low"

**Solutions:**
1. Update resume with more details
2. Lower threshold: `matching.threshold: 0.85`
3. Add more relevant keywords to resume
4. Check if job descriptions are being scraped fully

### Issue: "OpenAI API error"

**Solutions:**
1. Verify API key is correct in `.env`
2. Check billing: https://platform.openai.com/account/billing
3. Ensure you have credits ($5 free trial usually included)
4. Model cost: ~$0.01 per 100 jobs

### Issue: "Email not sending"

**Solutions:**
1. Use Gmail App Password, not regular password
2. Enable 2FA on Google Account first
3. Check SMTP settings (Gmail: smtp.gmail.com:587)
4. Verify no firewall blocking port 587

### Issue: "Selenium/ChromeDriver error"

**Solutions:**
```powershell
# Update webdriver
pip install --upgrade webdriver-manager selenium

# Ensure Chrome is installed
winget install Google.Chrome
```

### Issue: "Application crashes"

**Solutions:**
1. Check Python version: `python --version` (need 3.9+)
2. Reinstall dependencies: `pip install -r requirements.txt --force-reinstall`
3. Check full error in logs
4. Run with debug: Edit config → `advanced.debug: true`

## Performance Optimization

### Speed Up Scraping

```yaml
scraping:
  max_pages: 3  # Reduce from 5
  enabled_scrapers: ["indeed"]  # Use only one scraper
```

### Reduce API Costs

The app is already very cheap (~$0.01/day), but to reduce further:

```yaml
matching:
  threshold: 0.92  # Higher threshold = fewer API calls
```

### Reduce Email Noise

```yaml
notifications:
  min_jobs: 5  # Only notify if 5+ matches
  max_jobs_per_email: 10  # Show top 10 only
```

## Best Practices

### Resume Tips

✅ **DO:**
- Include all relevant technical skills
- Use industry-standard terminology
- List specific technologies/tools you've used
- Include quantifiable achievements
- Keep updated with recent experience
- Add German language level if applicable

❌ **DON'T:**
- Use vague descriptions
- Omit important skills
- Use proprietary/internal tool names only
- Include irrelevant personal info

### Search Strategy

1. **Start Broad**: Use general job titles first
2. **Monitor Results**: Run for a week to see patterns
3. **Refine**: Adjust threshold and keywords based on results
4. **Location**: Always include "Remote" if open to it
5. **Salary**: Set realistic minimum to filter out low offers

### Application Workflow

1. **Morning**: Check email for new matches
2. **Review**: Look at top 5-10 matches (90%+)
3. **Research**: Visit company websites, check reviews
4. **Apply**: Prioritize 95%+ matches
5. **Track**: Keep spreadsheet of applications
6. **Follow-up**: Check database for company history

## Privacy & Security

### What Data is Stored?

- **Locally**: Resume, job listings, match scores (in SQLite)
- **External**: Resume text sent to OpenAI API (encrypted)
- **Not Stored**: Application passwords (in memory only)

### Data Protection

- All data stored on your machine only
- Database not shared anywhere
- Email password encrypted in memory
- Can delete `data/jobs.db` anytime

### GDPR Compliance

- This tool is for personal use
- You control all data
- No third-party tracking
- Can request data deletion from OpenAI: https://openai.com/privacy

## Cost Analysis

### Monthly Costs

| Service | Cost | Required |
|---------|------|----------|
| OpenAI API | ~$0.30/month | ✅ Yes |
| Email (Gmail) | Free | ✅ Yes |
| LinkedIn Account | Free | ❌ Optional |
| **Total** | **~$0.30/month** | |

Compare to:
- Premium job boards: €30-100/month
- Career coaching: €100-500/session
- Time saved: 10+ hours/week

**ROI: Priceless!** 🚀

## Frequently Asked Questions

### Q: Do I need to keep my computer running?

**A:** For scheduled mode (daily automation), yes. Alternatively:
- Use Windows Task Scheduler to run at specific times
- Run manually when convenient
- Use a cloud VM (AWS, Azure) to run 24/7

### Q: Will this apply to jobs automatically?

**A:** No, it only finds and matches jobs. You review and apply manually. This ensures quality applications.

### Q: How accurate is the 90% match?

**A:** Very accurate! The AI understands context, not just keywords. However, always review jobs yourself before applying.

### Q: Can I modify the code?

**A:** Absolutely! It's open source. Add features, customize logic, integrate other job boards.

### Q: Does this work outside Germany?

**A:** Yes! Just update scraper URLs and location settings. Indeed and LinkedIn work globally.

### Q: Is web scraping legal?

**A:** For personal use, generally yes. Always respect:
- Terms of Service
- robots.txt
- Rate limits (already implemented)

### Q: What if a job portal blocks me?

**A:** The app uses:
- Rotating user agents
- Delays between requests
- Headless browser mode
- Still, some sites may block. Use proxy if needed.

## Future Enhancements

Planned features:
- [ ] Web dashboard for viewing matches
- [ ] Auto-apply with custom cover letters
- [ ] Chrome extension for quick resume updates
- [ ] Machine learning to learn your preferences
- [ ] Integration with Xing, Monster.de
- [ ] Mobile app notifications
- [ ] Interview preparation suggestions

## Getting Help

1. **Check logs**: `logs/app.log`
2. **Review config**: Ensure settings are correct
3. **Test components**: Run once manually first
4. **Update dependencies**: `pip install -r requirements.txt --upgrade`

## Contributing

Found a bug? Want to add a feature?
- Fork the project
- Make improvements
- Share with the community!

## Legal Disclaimer

This tool is for **personal use only**. When using it:
- Respect website terms of service
- Don't overload servers (rate limiting included)
- Manually verify all matches before applying
- Be honest in applications

## Success Tips

🎯 **Set realistic expectations**
- 5-10 high-quality matches per day is excellent
- Focus on 95%+ matches first
- Quality over quantity

📧 **Check email daily**
- Best jobs get filled quickly
- Apply within 24-48 hours

🔄 **Keep resume updated**
- Add new skills as you learn
- Update experience regularly
- Reflect recent projects

💼 **Personalize applications**
- Use matched keywords in cover letter
- Reference specific job requirements
- Show enthusiasm for the role

Good luck with your job search in Germany! 🇩🇪🚀
