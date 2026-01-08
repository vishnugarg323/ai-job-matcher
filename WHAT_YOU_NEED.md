# 🎯 WHAT YOU NEED TO PROVIDE

## ✅ Required Information

### 1. **Google Gemini API Key** (FREE)
- **Where to get:** https://makersuite.google.com/app/apikey
- **How to get:**
  1. Go to the link above
  2. Click "Get API key"
  3. Create new project or select existing
  4. Click "Create API key"
  5. Copy the key (starts with `AIza...`)
- **Cost:** 100% FREE with generous limits
- **Purpose:** AI matching engine for jobs

---

### 2. **Gmail App Password** (FREE)
- **Where to get:** https://myaccount.google.com/apppasswords
- **How to get:**
  1. Enable 2-Factor Authentication on your Gmail (required)
  2. Go to the link above
  3. Select app: "Mail"
  4. Select device: "Other" → type "Job Matcher"
  5. Click "Generate"
  6. Copy the 16-character password (format: xxxx-xxxx-xxxx-xxxx)
- **Purpose:** Send you job notification emails
- **Security:** Use app password, NOT your real Gmail password!

---

### 3. **Your Resume** (PDF Format)
- **Where to save:** `data/resume.pdf`
- **Format:** PDF (not Word/TXT)
- **What to include:**
  - ✅ Full name and contact info
  - ✅ ALL technical skills (Python, AWS, Docker, Kubernetes, etc.)
  - ✅ Work experience (companies, roles, years, responsibilities)
  - ✅ Education (degrees, universities, years)
  - ✅ Certifications (AWS, Azure, etc.)
  - ✅ Languages (English, German, etc.)
  - ✅ Projects (if relevant)
- **Important:** More detail = Better matches! AI needs full context.

---

### 4. **Email Address to Receive Jobs**
- **What:** Your email where you want to receive job notifications
- **Can be:** Same as Gmail sender or different
- **Example:** `your.name@gmail.com` or `your.work@email.com`

---

## ⭕ Optional Information

### 5. **LinkedIn Credentials** (Optional but Recommended)
- **Email:** Your LinkedIn login email
- **Password:** Your LinkedIn password
- **Why:** Better access to LinkedIn job postings (without login, scraping is limited)
- **Security:** Only stored locally in `.env` file, never shared

---

### 6. **GitHub Username** (For Railway Deployment)
- **What:** Your GitHub username (e.g., `vishnu123`)
- **Why:** To push code and deploy on Railway
- **If you don't have:** Create free account at https://github.com/

---

## 📋 Configuration Preferences

### 7. **Job Preferences** (Edit in `config/config.yaml`)
You'll customize these after setup:

**Job Titles** (What roles you want):
- Example: "Python Developer", "Backend Engineer", "ML Engineer"
- Default: Already set to common software roles
- You can: Add/remove based on your target roles

**Locations** (Where you want to work):
- Example: "Berlin", "Munich", "Hamburg", "Remote"
- Default: Major German cities + Remote
- You can: Add specific cities or keep "Remote" only

**Minimum Salary**:
- Example: 60000 (EUR per year)
- Default: 60,000 EUR
- You can: Adjust based on your expectations

**Required Keywords** (Must-have skills):
- Example: "Python", "AWS", "Docker"
- Default: Common tech stack
- You can: Match to your resume skills

**Exclude Keywords** (Filter out):
- Example: "Unpaid", "Internship", "Junior"
- Default: Common exclusions
- You can: Add terms you want to avoid

---

## 📁 File Structure - Where Things Go

```
AI Job Application/
├── .env                      # ← Created by setup.py (your credentials)
├── config/
│   └── config.yaml          # ← Edit this for job preferences
├── data/
│   ├── resume.pdf           # ← PUT YOUR RESUME HERE (PDF format)
│   └── jobs.db              # ← Auto-created (job database)
├── setup.py                 # ← Run this first: python setup.py
├── main.py                  # ← Run this to start: python main.py
└── requirements.txt         # ← Install: pip install -r requirements.txt
```

---

## 🚀 Deployment Options

### Option A: Run Locally (Your Computer)
- **Pros:** Easy to test, no cloud setup needed
- **Cons:** Computer must stay on 24/7
- **Cost:** $0
- **How:** `python main.py --schedule`

### Option B: Deploy on Railway (Cloud - RECOMMENDED)
- **Pros:** Runs 24/7 automatically, no computer needed
- **Cons:** Requires GitHub account, basic cloud setup
- **Cost:** $0-3/month (Railway free tier: $5 credit)
- **How:** See `RAILWAY_DEPLOYMENT.md`

---

## ⏱️ Timeline

**How long does this take?**

1. **Get Gemini API key:** 2 minutes
2. **Get Gmail app password:** 5 minutes
3. **Prepare resume PDF:** 10 minutes (if converting from Word)
4. **Run setup.py:** 3 minutes
5. **Test locally:** 5 minutes
6. **Deploy to Railway:** 15 minutes

**Total:** ~40 minutes to fully deploy and running 24/7!

---

## ✅ Checklist - Before We Start

- [ ] I have a Google account (for Gemini API)
- [ ] I have a Gmail account with 2FA enabled
- [ ] I have my resume ready (PDF format preferred)
- [ ] I know my target job titles and locations in Germany
- [ ] I have a GitHub account (if deploying to Railway)
- [ ] (Optional) I have LinkedIn credentials for better scraping

---

## 🎯 Next Steps

Once you provide:
1. Gemini API key
2. Gmail app password
3. Resume (save to `data/resume.pdf`)

I can:
1. ✅ Help configure the system
2. ✅ Test it locally
3. ✅ Deploy to Railway
4. ✅ Monitor first runs
5. ✅ Verify emails are sent correctly

---

## 💡 Important Notes

### Resume Location
**For Local Testing:**
- Save to: `data/resume.pdf` (in the project folder)

**For Railway Deployment:**
- **Option 1 (Easiest):** Include resume.pdf in Git repository
  ```bash
  git add data/resume.pdf
  git commit -m "Add resume"
  git push
  ```
- **Option 2:** Use cloud storage URL (Dropbox, Google Drive)
  - Set environment variable: `RESUME_URL=https://your-url/resume.pdf`

### Password Security
**DO:**
- ✅ Use Gmail App Password (not real password)
- ✅ Store in `.env` file (never commit to Git)
- ✅ Use Railway environment variables (encrypted)

**DON'T:**
- ❌ Share your `.env` file
- ❌ Commit `.env` to GitHub
- ❌ Use your real Gmail password

### API Key Security
**DO:**
- ✅ Keep Gemini key private
- ✅ Store in `.env` or Railway variables
- ✅ Regenerate if accidentally shared

**DON'T:**
- ❌ Share API keys publicly
- ❌ Commit to public repositories

---

## 📞 Ready to Start?

**I'm waiting for:**
1. ✅ Gemini API key (from https://makersuite.google.com/app/apikey)
2. ✅ Gmail app password (from https://myaccount.google.com/apppasswords)
3. ✅ Confirmation that resume.pdf is saved to `data/resume.pdf`

**Then we can:**
1. Run setup and test locally
2. Deploy to Railway for 24/7 operation
3. Monitor and optimize

**Let me know when you're ready!** 🚀
