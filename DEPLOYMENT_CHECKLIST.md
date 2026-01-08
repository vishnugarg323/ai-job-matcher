# ✅ DEPLOYMENT CHECKLIST

Use this checklist to track your setup progress.

---

## 🎯 Pre-Deployment (What You Need)

- [ ] **Gemini API Key** (FREE)
  - Get from: https://makersuite.google.com/app/apikey
  - Copy key (starts with `AIza...`)
  - Save somewhere safe

- [ ] **Gmail App Password** (FREE)
  - Enable 2FA on Gmail first
  - Get from: https://myaccount.google.com/apppasswords
  - Copy 16-character password
  - Save somewhere safe

- [ ] **Resume PDF**
  - Format: PDF (not Word/TXT)
  - Content: ALL skills, experience, education, languages
  - Ready to copy to `data/resume.pdf`

- [ ] **Optional: LinkedIn Credentials**
  - Email + Password
  - For better LinkedIn job access

- [ ] **Optional: GitHub Account**
  - Create at https://github.com/ (if deploying to Railway)
  - Username: _______________

---

## 🖥️ Local Setup (Test Before Cloud)

- [ ] **Install Python 3.11+**
  - Check: `python --version`
  - Should be 3.11 or higher

- [ ] **Clone/Download Project**
  - Project folder: `AI Job Application`

- [ ] **Install Dependencies**
  ```bash
  pip install -r requirements.txt
  ```

- [ ] **Run Interactive Setup**
  ```bash
  python setup.py
  ```
  - Enter Gemini API key
  - Enter Gmail credentials
  - Optionally add LinkedIn credentials

- [ ] **Add Resume**
  - Copy resume PDF to: `data/resume.pdf`
  - Verify file exists: Check `data/` folder

- [ ] **Customize Preferences**
  - Edit: `config/config.yaml`
  - Update job titles (e.g., "Python Developer", "ML Engineer")
  - Update locations (e.g., "Berlin", "Munich", "Remote")
  - Update minimum salary (e.g., 60000)
  - Add required keywords (your core skills)
  - Add exclude keywords (what to avoid)

- [ ] **Test Run (Manual)**
  ```bash
  python main.py
  ```
  - Should scrape jobs
  - Should show matches
  - Should send email (check inbox!)

- [ ] **Test Scheduled Mode**
  ```bash
  python main.py --schedule
  ```
  - Should show "Scheduler started"
  - Wait 30 minutes for first run
  - Check email for job matches
  - Press Ctrl+C to stop

---

## ☁️ Railway Deployment (24/7 Operation)

### Prerequisites
- [ ] Local testing completed successfully
- [ ] GitHub account created
- [ ] Git installed on your computer

### Push to GitHub
- [ ] Initialize Git repository
  ```bash
  git init
  ```

- [ ] Add files
  ```bash
  git add .
  ```

- [ ] Commit
  ```bash
  git commit -m "AI Job Matcher - Ready for Railway"
  ```

- [ ] Create GitHub repository
  - Go to https://github.com/new
  - Name: `ai-job-matcher`
  - Don't initialize with README (already have one)

- [ ] Push to GitHub
  ```bash
  git remote add origin https://github.com/YOUR_USERNAME/ai-job-matcher.git
  git push -u origin main
  ```

### Deploy on Railway
- [ ] Sign up for Railway
  - Go to https://railway.app/
  - Sign in with GitHub (recommended)

- [ ] Create New Project
  - Click "New Project"
  - Select "Deploy from GitHub repo"
  - Choose `ai-job-matcher` repository
  - Railway starts building automatically

- [ ] Add Environment Variables
  - Go to your service in Railway
  - Click "Variables" tab
  - Add these variables:

```
GEMINI_API_KEY=your_gemini_api_key_here
EMAIL_SENDER=your_gmail@gmail.com
EMAIL_PASSWORD=your_gmail_app_password
EMAIL_RECIPIENT=where_to_receive_jobs@gmail.com
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
DATABASE_PATH=data/jobs.db
LOG_LEVEL=INFO
SCHEDULE_ENABLED=true
TIMEZONE=Europe/Berlin
MATCH_THRESHOLD=0.90
MIN_JOBS_TO_NOTIFY=1
MAX_JOBS_PER_EMAIL=10
MAX_PAGES_PER_SITE=5
REQUEST_DELAY=2
USER_AGENT_ROTATION=true
```

- [ ] Optional: Add LinkedIn variables
```
LINKEDIN_EMAIL=your_linkedin@email.com
LINKEDIN_PASSWORD=your_linkedin_password
```

### Upload Resume to Railway

Choose ONE method:

**Option A: Include in Git (EASIEST)**
- [ ] Add resume to Git
  ```bash
  git add data/resume.pdf
  git commit -m "Add resume for deployment"
  git push
  ```
- [ ] Railway auto-redeploys with resume

**Option B: Cloud Storage URL**
- [ ] Upload resume to Dropbox/Google Drive
- [ ] Get public/shareable link
- [ ] Add Railway variable: `RESUME_URL=https://your-url/resume.pdf`

**Option C: Base64 Encoding**
- [ ] Encode resume
  ```bash
  base64 data/resume.pdf > resume_base64.txt
  ```
- [ ] Copy content to Railway variable: `RESUME_BASE64=<paste content>`

### Verify Deployment
- [ ] Check deployment status in Railway
  - Go to "Deployments" tab
  - Status should be "Success" (green)

- [ ] Check logs
  - Go to "Observability" → "Logs"
  - Should see: "🚀 AI Job Matcher Starting..."
  - Should see: "✅ Scheduler started"

- [ ] Wait for first email (within 30 minutes)
  - Check your email inbox
  - Should receive HTML-formatted job matches

---

## 🔍 Post-Deployment Verification

- [ ] **Email Received**
  - Within 30 minutes of deployment
  - Contains top 10 job matches
  - HTML formatted with job details

- [ ] **Railway Logs Look Good**
  - No error messages
  - Shows job scraping activity
  - Shows "Email sent successfully"

- [ ] **Jobs Are Relevant**
  - Match your skills (90%+)
  - Correct locations
  - Recent postings (within 14 days)

- [ ] **No Duplicates**
  - Same job not sent multiple times
  - Database tracking working

---

## 🎯 Optimization (After 1-2 Days)

- [ ] **Too Many Emails?**
  - Edit `config/config.yaml`
  - Increase `threshold` to 0.95

- [ ] **Too Few Matches?**
  - Edit `config/config.yaml`
  - Decrease `threshold` to 0.85

- [ ] **Wrong Job Types?**
  - Edit `config/config.yaml`
  - Update `job_titles` list
  - Update `required_keywords`
  - Update `exclude_keywords`

- [ ] **Change Frequency?**
  - Edit `config/config.yaml`
  - Change `interval_minutes` (e.g., 60 for hourly)
  - Push to GitHub (Railway auto-redeploys)

---

## 📊 Success Metrics

Track your progress:

- [ ] **Week 1**
  - [ ] Receiving 20-50 jobs/day
  - [ ] Applied to 10-20 jobs
  - [ ] 1-2 interviews scheduled

- [ ] **Week 2**
  - [ ] Refined job preferences
  - [ ] Applied to 30-50 jobs total
  - [ ] 3-5 interviews completed

- [ ] **Week 3-4**
  - [ ] Applied to 50-100 jobs total
  - [ ] 5-10 interviews completed
  - [ ] 1-2 final round interviews

- [ ] **Week 5-8**
  - [ ] Applied to 100+ jobs
  - [ ] 10+ interviews completed
  - [ ] 1-3 job offers received
  - [ ] **JOB SECURED!** 🎉

---

## 🆘 Troubleshooting Checklist

### No Emails Received
- [ ] Check Railway logs for errors
- [ ] Verify `EMAIL_SENDER` and `EMAIL_PASSWORD` correct
- [ ] Check Gmail allows app passwords (2FA enabled)
- [ ] Check spam folder
- [ ] Test email manually (send test email)

### Low Job Matches
- [ ] Lower threshold to 0.85 in config.yaml
- [ ] Add more job titles to search
- [ ] Broaden location search (add "Remote")
- [ ] Check resume has enough detail

### Railway Deployment Failed
- [ ] Check build logs for errors
- [ ] Verify all environment variables set
- [ ] Check Python version (3.11)
- [ ] Verify requirements.txt has all dependencies

### Resume Not Found Error
- [ ] Verify resume.pdf in data/ folder (if in Git)
- [ ] Or verify RESUME_URL is set and accessible
- [ ] Check file is named exactly `resume.pdf`
- [ ] Check file is PDF format (not Word/TXT)

### Selenium/Chrome Errors
- [ ] Check nixpacks.toml includes Chrome/ChromeDriver
- [ ] Verify Railway build logs show Chrome installation
- [ ] Try redeploying (Railway → Settings → Redeploy)

---

## 📞 Support Resources

- **Documentation:**
  - [QUICK_START.md](QUICK_START.md) - Fast setup
  - [RAILWAY_DEPLOYMENT.md](RAILWAY_DEPLOYMENT.md) - Detailed cloud guide
  - [WHAT_YOU_NEED.md](WHAT_YOU_NEED.md) - Requirements

- **Railway Help:**
  - Docs: https://docs.railway.app/
  - Discord: https://discord.gg/railway

- **Gemini API Help:**
  - Docs: https://ai.google.dev/docs
  - Get API Key: https://makersuite.google.com/app/apikey

---

## ✅ Final Checklist

Before considering setup complete:

- [ ] Local testing successful (received email)
- [ ] Railway deployment successful (logs look good)
- [ ] Receiving emails every 30 minutes
- [ ] Job matches are relevant (90%+ match)
- [ ] No duplicate jobs in emails
- [ ] Applied to first 5-10 jobs
- [ ] Tracking applications in spreadsheet

---

## 🎉 Success!

If all checkboxes above are checked:
- ✅ System is running 24/7 on Railway
- ✅ You're receiving quality job matches
- ✅ You're applying regularly
- ✅ On track to land job before visa expires!

**GOOD LUCK!** 🍀🚀

---

**Last Updated:** January 8, 2026
**System Version:** 2.0 (FREE & RAILWAY-READY)
