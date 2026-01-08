# ⚡ Quick Reference Card - AI Job Matcher

## 🚀 Quick Commands

```powershell
# First time setup
pip install -r requirements.txt
Copy-Item .env.example .env
notepad .env

# Run once (test)
python main.py

# Run scheduled (daily)
python main.py --schedule

# View matches
python view_matches.py

# Check logs
Get-Content logs\app.log -Tail 50
```

## 📋 Essential Files

| File | Purpose | Action Required |
|------|---------|-----------------|
| `.env` | API keys & credentials | ✅ Must configure |
| `data/resume.txt` | Your resume | ✅ Must add |
| `config/config.yaml` | Preferences | ⚠️ Should customize |
| `data/jobs.db` | Job storage | ℹ️ Auto-created |

## 🔑 Required Credentials

1. **OpenAI API Key**
   - Get: https://platform.openai.com/api-keys
   - Cost: ~$0.01/day
   - Add to `.env`: `OPENAI_API_KEY=sk-...`

2. **Gmail App Password**
   - Get: https://myaccount.google.com/apppasswords
   - Requires 2FA enabled
   - Add to `.env`: `EMAIL_PASSWORD=xxxx xxxx xxxx xxxx`

## ⚙️ Key Settings

### Match Threshold
```yaml
# config/config.yaml
matching:
  threshold: 0.90  # 90% match required
  # Lower (0.85) = more results
  # Higher (0.95) = fewer, better results
```

### Job Search
```yaml
search:
  job_titles: ["Software Engineer", "DevOps"]
  locations: ["Berlin", "Munich", "Remote"]
  min_salary: 60000
```

### Schedule
```yaml
schedule:
  run_time: "08:00"  # 8 AM daily
  timezone: "Europe/Berlin"
```

## 📊 Match Score Guide

| Score | Meaning | Action |
|-------|---------|--------|
| 98-100% | Perfect match | Apply immediately! |
| 95-98% | Excellent match | High priority |
| 90-95% | Good match | Worth applying |
| < 90% | Below threshold | Not shown |

## 🔧 Troubleshooting Quick Fixes

| Problem | Solution |
|---------|----------|
| No jobs found | Check internet, reduce `max_pages` |
| OpenAI error | Verify API key, check billing |
| Email not sending | Use Gmail app password |
| Selenium crash | Update Chrome: `winget install Google.Chrome` |
| Low matches | Lower threshold to 0.85 |
| Too many matches | Raise threshold to 0.95 |

## 📁 File Locations

```
Important Files:
├── .env                    ← Your secrets (DON'T share!)
├── main.py                 ← Run this
├── config/config.yaml      ← All settings
├── data/resume.txt         ← Your resume
├── data/jobs.db            ← All matches stored here
└── logs/app.log            ← Debug info

Quick Access:
├── run.bat                 ← Double-click to run once
├── run_scheduled.bat       ← Double-click for daily runs
├── view_matches.py         ← See your matches
└── USER_GUIDE.md          ← Full documentation
```

## 🎯 Typical Workflow

### Daily (2 minutes)
1. Check email notification ✉️
2. Review top 5-10 matches 🎯
3. Apply to 95%+ matches 📝

### Weekly (10 minutes)
1. Review all matches in database 📊
2. Adjust threshold if needed ⚙️
3. Update resume with new skills 📄

### Monthly (30 minutes)
1. Analyze match patterns 📈
2. Refine job titles/locations 🔍
3. Update keywords 🔑
4. Clean old jobs from database 🧹

## 💡 Pro Tips

✅ **DO:**
- Keep resume detailed and updated
- Include "Remote" in locations
- Start with threshold at 0.90
- Run daily during job search
- Apply within 24-48 hours
- Personalize applications

❌ **DON'T:**
- Use regular Gmail password
- Share API keys
- Set threshold too low (< 0.85)
- Skip manual review
- Apply without reading job description
- Modify resume for each job (that's the point!)

## 📧 Email Settings

### Gmail Setup
```
SMTP Server: smtp.gmail.com
Port: 587
Security: TLS
Password: App Password (not regular password!)
```

### Get App Password
1. Google Account → Security
2. Enable 2-Factor Authentication
3. App Passwords → Generate
4. Use 16-character password

## 🗄️ Database Queries

Open database: `data/jobs.db` with DB Browser for SQLite

```sql
-- Top matches
SELECT title, company, match_score 
FROM jobs 
WHERE match_score >= 0.95 
ORDER BY match_score DESC;

-- Recent jobs
SELECT * FROM jobs 
WHERE created_at >= date('now', '-7 days');

-- By company
SELECT * FROM jobs 
WHERE company LIKE '%Google%';
```

## 🌐 Supported Job Portals

| Portal | Coverage | Reliability | Config Key |
|--------|----------|-------------|------------|
| Indeed.de | 🇩🇪 Germany | ⭐⭐⭐⭐⭐ | `indeed` |
| StepStone.de | 🇩🇪 Germany | ⭐⭐⭐⭐ | `stepstone` |
| LinkedIn | 🌍 Global | ⭐⭐⭐ | `linkedin` |

## 📞 Quick Help

| Issue | Check |
|-------|-------|
| Setup | Read SETUP_GUIDE.md |
| Usage | Read USER_GUIDE.md |
| Errors | Check logs/app.log |
| Config | Review config/config.yaml |
| API | Check OpenAI billing |
| Email | Verify app password |

## 💰 Cost Breakdown

| Item | Cost/Month | Cost/Year |
|------|------------|-----------|
| OpenAI API | $0.30 | $3.60 |
| Gmail | $0 | $0 |
| **Total** | **$0.30** | **$3.60** |

Compare to:
- Premium job boards: $30-100/month
- Recruiter fees: 15-20% of salary
- Time saved: 40+ hours/month

## 🎓 Learning Path

1. **Beginner** (Week 1)
   - Run application once
   - Understand match scores
   - Review daily emails

2. **Intermediate** (Week 2)
   - Customize config.yaml
   - Adjust thresholds
   - Query database

3. **Advanced** (Week 3+)
   - Add custom scrapers
   - Modify matching logic
   - Integrate other tools

## 📚 Documentation

- **README.md** - Project overview
- **SETUP_GUIDE.md** - Installation & setup
- **USER_GUIDE.md** - Complete usage guide
- **PROJECT_SUMMARY.md** - Technical details
- **THIS FILE** - Quick reference

## 🔄 Update Commands

```powershell
# Update all dependencies
pip install -r requirements.txt --upgrade

# Update specific package
pip install --upgrade openai

# Reinstall if broken
pip install -r requirements.txt --force-reinstall

# Check versions
pip list | Select-String "openai|selenium|beautifulsoup"
```

## 🎯 Success Checklist

Setup Phase:
- [ ] Python 3.9+ installed
- [ ] Dependencies installed
- [ ] .env configured with API key
- [ ] Gmail app password set
- [ ] Resume added to data/resume.txt
- [ ] config.yaml customized

Testing Phase:
- [ ] Run once manually
- [ ] Received test email
- [ ] Matches found in database
- [ ] Logs show no errors

Production Phase:
- [ ] Scheduled mode running
- [ ] Daily emails received
- [ ] Applying to matches
- [ ] Getting interviews!

---

**Remember**: This tool finds the jobs, but YOU get the job! 

Good luck! 🍀🚀
