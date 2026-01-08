# ⚡ QUICK START - FREE AI JOB MATCHER

**100% FREE • Railway Cloud • Google Gemini AI**

---

## 🎯 What You Need From Me (User)

### 1. **Gemini API Key** (FREE)
- Go to: https://makersuite.google.com/app/apikey
- Click "Get API key" → Create new project
- Copy the key (starts with `AIza...`)

### 2. **Gmail App Password** (FREE)
- Go to: https://myaccount.google.com/apppasswords
- Enable 2-Factor Authentication first
- Create app password for "Mail"
- Copy the 16-character password

### 3. **Your Resume** (PDF format)
- Save as: `data/resume.pdf`
- Include: ALL skills, experience, education, languages, certifications
- Be detailed - AI needs full context for best matches!

### 4. **Optional: LinkedIn Credentials**
- If you want LinkedIn scraping (recommended)
- Email + Password

---

## 🚀 Local Setup (Test First)

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run Setup**
   ```bash
   python setup.py
   ```
   This will prompt you for:
   - Gemini API key
   - Gmail credentials
   - LinkedIn (optional)

3. **Add Your Resume**
   ```bash
   # Copy your resume PDF to:
   data/resume.pdf
   ```

4. **Customize Preferences**
   Edit `config/config.yaml`:
   - Job titles (e.g., "Python Developer", "ML Engineer")
   - Locations (e.g., "Berlin", "Munich", "Remote")
   - Minimum salary
   - Keywords to include/exclude

5. **Test Run**
   ```bash
   python main.py
   ```
   Should find jobs and show matches!

6. **Start Automatic Mode**
   ```bash
   python main.py --schedule
   ```
   Runs every 30 minutes, sends emails with top 10 jobs.

---

## ☁️ Railway Deployment (Run 24/7)

### Quick Deploy to Railway

1. **Push to GitHub**
   ```bash
   git init
   git add .
   git commit -m "AI Job Matcher - Ready for Railway"
   git remote add origin https://github.com/YOUR_USERNAME/ai-job-matcher.git
   git push -u origin main
   ```

2. **Deploy on Railway**
   - Go to https://railway.app/
   - Click "New Project" → "Deploy from GitHub repo"
   - Select your repository
   - Railway auto-deploys!

3. **Configure Environment Variables**
   In Railway dashboard → Variables tab:
   ```
   GEMINI_API_KEY=your_key_here
   EMAIL_SENDER=your_gmail@gmail.com
   EMAIL_PASSWORD=your_app_password
   EMAIL_RECIPIENT=where_to_receive@gmail.com
   SMTP_SERVER=smtp.gmail.com
   SMTP_PORT=587
   DATABASE_PATH=data/jobs.db
   SCHEDULE_ENABLED=true
   TIMEZONE=Europe/Berlin
   ```

4. **Resume on Railway**
   **Option A (Easiest):** Include in Git
   ```bash
   git add data/resume.pdf
   git commit -m "Add resume"
   git push
   ```

   **Option B:** Use environment variable
   ```
   RESUME_URL=https://your-cloud-storage/resume.pdf
   ```

5. **Deploy & Monitor**
   - Check Railway logs for "✅ Scheduler started"
   - First email arrives within 30 minutes!

---

## 📋 Architecture

```
┌─────────────────────────────────────────────┐
│           RAILWAY CLOUD (24/7)              │
│                                             │
│  ┌──────────────────────────────────────┐  │
│  │   AI Job Matcher App                 │  │
│  │   Runs every 30 minutes              │  │
│  └──────────────────────────────────────┘  │
│               │                             │
│               ▼                             │
│  ┌──────────────────────────────────────┐  │
│  │   Scrape Jobs (Selenium)             │  │
│  │   • Indeed.de                        │  │
│  │   • StepStone.de                     │  │
│  │   • LinkedIn.com                     │  │
│  └──────────────────────────────────────┘  │
│               │                             │
│               ▼                             │
│  ┌──────────────────────────────────────┐  │
│  │   AI Matching (Gemini)               │  │
│  │   • Resume embedding                 │  │
│  │   • Job description embedding        │  │
│  │   • Cosine similarity (90% match)    │  │
│  │   • Urgency scoring                  │  │
│  └──────────────────────────────────────┘  │
│               │                             │
│               ▼                             │
│  ┌──────────────────────────────────────┐  │
│  │   Filter & Sort                      │  │
│  │   • Jobs within 14 days              │  │
│  │   • No duplicates                    │  │
│  │   • Top 10 only                      │  │
│  │   • Urgent jobs prioritized          │  │
│  └──────────────────────────────────────┘  │
│               │                             │
│               ▼                             │
│  ┌──────────────────────────────────────┐  │
│  │   Send Email (Gmail SMTP)            │  │
│  │   • HTML formatted                   │  │
│  │   • Top 10 jobs                      │  │
│  │   • Match scores                     │  │
│  │   • Apply links                      │  │
│  └──────────────────────────────────────┘  │
│               │                             │
└───────────────┼─────────────────────────────┘
                │
                ▼
         📧 YOUR EMAIL
```

---

## ✨ Features

- ✅ **100% FREE** - Google Gemini AI (no OpenAI costs)
- ✅ **Every 30 minutes** - 48 searches/day
- ✅ **Multi-source** - Indeed, StepStone, LinkedIn
- ✅ **90% AI match** - Only send relevant jobs
- ✅ **Top 10 per email** - No spam
- ✅ **No duplicates** - Tracks sent jobs
- ✅ **Fresh jobs** - Within 14 days (fast hiring)
- ✅ **Urgency scoring** - Prioritizes "immediate", "visa sponsor"
- ✅ **Cloud-ready** - Runs 24/7 on Railway

---

## 🎯 Best Practices

### Resume
- Use PDF format (not Word/TXT)
- Include ALL skills (Python, AWS, Docker, etc.)
- List ALL experience (years, companies, roles)
- Add education (degrees, certifications)
- Mention languages (English, German, etc.)
- Keywords matter - use job posting terminology

### Configuration
- Add 5-10 job titles you want
- Include "Remote" in locations (more options)
- Set realistic minimum salary
- Use required_keywords (must-haves)
- Use exclude_keywords (avoid bad matches)

### Email Management
- Create Gmail filter to organize job emails
- Check emails 2-3 times/day
- Apply FAST - urgent jobs fill quickly
- Keep track of applications

---

## 🚨 URGENT MODE (2 Months Visa)

Your setup is optimized for **SPEED**:

- **Frequency:** Every 30 minutes (maximum allowed)
- **Job Age:** Within 14 days (fast-hiring companies)
- **Urgency Boost:** Jobs with "urgent", "visa sponsor", "immediate" ranked higher
- **Top 10 Only:** No noise, just best matches
- **No Duplicates:** Never sends same job twice

**Expected Results:**
- ~20-50 new jobs scraped per run
- ~5-15 matches (90% threshold)
- Top 10 sent via email
- ~10-30 quality jobs per day

---

## 🔧 Troubleshooting

| Issue | Solution |
|-------|----------|
| No Gemini key error | Add `GEMINI_API_KEY` in Railway variables |
| Email not sending | Use Gmail App Password, enable 2FA |
| Resume not found | Add `data/resume.pdf` or set `RESUME_URL` |
| Chrome/Selenium error | Included in `nixpacks.toml`, check Railway logs |
| No job matches | Lower threshold in config.yaml to 0.85 |
| Too many emails | Increase threshold to 0.95 |

---

## 📞 What I Need To Help You

Please provide:
1. ✅ Gemini API key (https://makersuite.google.com/app/apikey)
2. ✅ Gmail app password (https://myaccount.google.com/apppasswords)
3. ✅ Resume PDF location (copy to `data/resume.pdf`)
4. ⭕ LinkedIn credentials (optional)
5. ⭕ GitHub username (for Railway deployment)

Once you provide these, I can:
- ✅ Verify configuration
- ✅ Help with Railway deployment
- ✅ Test the system end-to-end
- ✅ Monitor first runs

---

**Ready? Run `python setup.py` to start!** 🚀
