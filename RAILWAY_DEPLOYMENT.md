# 🚀 Railway Deployment Guide

Deploy your AI Job Matcher to run **24/7** on Railway (Cloud Platform)

---

## 📋 Prerequisites

1. ✅ **Railway Account** (Free)
   - Sign up: https://railway.app/
   - Free tier: $5 credit/month (enough for this app!)

2. ✅ **GitHub Account**
   - Push your code to GitHub
   - Railway will deploy from your repo

3. ✅ **Gemini API Key** (FREE)
   - Get from: https://makersuite.google.com/app/apikey
   - 100% free with generous limits

4. ✅ **Gmail App Password**
   - Get from: https://myaccount.google.com/apppasswords
   - Enable 2FA first, then create app password

---

## 🎯 Quick Deployment Steps

### Step 1: Prepare Your Code

1. Make sure all files are committed:
   ```bash
   git add .
   git commit -m "Ready for Railway deployment"
   ```

2. Push to GitHub:
   ```bash
   git remote add origin https://github.com/YOUR_USERNAME/ai-job-matcher.git
   git push -u origin main
   ```

### Step 2: Create Railway Project

1. Go to https://railway.app/
2. Click **"New Project"**
3. Select **"Deploy from GitHub repo"**
4. Choose your **ai-job-matcher** repository
5. Railway will auto-detect Python and start building

### Step 3: Configure Environment Variables

In Railway dashboard:

1. Click on your service
2. Go to **"Variables"** tab
3. Add these environment variables:

```
GEMINI_API_KEY=your_gemini_key_here
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

**Optional** (if using LinkedIn):
```
LINKEDIN_EMAIL=your_linkedin_email
LINKEDIN_PASSWORD=your_linkedin_password
```

### Step 4: Upload Your Resume

**⚠️ IMPORTANT: Where to Put Resume on Railway**

Railway doesn't have a GUI for uploading files, so you have **3 options**:

#### Option A: Include Resume in Git Repository (EASIEST)
```bash
# On your local machine
cp /path/to/your/resume.pdf data/resume.pdf
git add data/resume.pdf
git commit -m "Add resume for deployment"
git push
```
Railway will automatically redeploy with your resume included.

#### Option B: Use Railway Volume (PERSISTENT)
1. In Railway dashboard, go to your service
2. Click **"Variables"** → **"New Variable"**
3. Add: `RESUME_URL=https://your-cloud-storage.com/resume.pdf`
4. Modify code to download from URL (see below)

#### Option C: Base64 Encode Resume (SIMPLE)
```bash
# Encode resume to base64
base64 data/resume.pdf > resume_base64.txt

# Add as environment variable in Railway
RESUME_BASE64=<paste base64 content here>
```
Then modify code to decode (see below)

**Recommendation:** Use **Option A** (commit resume to repo) for simplicity.

### Step 5: Deploy!

1. Railway will automatically build and deploy
2. Check **"Deployments"** tab for progress
3. View logs in **"Observability"** tab
4. Wait 2-3 minutes for first deployment

---

## 🔍 Verify Deployment

### Check Logs
In Railway dashboard → **"Observability"** → **"Logs"**

You should see:
```
🚀 AI Job Matcher Starting...
📧 Email configured: your_email@gmail.com
🔑 Gemini API initialized
⏰ Scheduler started: Every 30 minutes
✅ First run starting now...
```

### Test Email
Within 30 minutes, you should receive your first email with job matches!

---

## 🛠️ Configuration Tips

### Resume Location Options

If you chose **Option B** (URL download), update `src/matchers/resume_parser.py`:
```python
def __init__(self, config):
    resume_url = os.getenv('RESUME_URL')
    if resume_url:
        import requests
        response = requests.get(resume_url)
        with open(self.resume_path, 'wb') as f:
            f.write(response.content)
```

If you chose **Option C** (Base64), update `src/matchers/resume_parser.py`:
```python
def __init__(self, config):
    resume_base64 = os.getenv('RESUME_BASE64')
    if resume_base64:
        import base64
        with open(self.resume_path, 'wb') as f:
            f.write(base64.b64decode(resume_base64))
```

### Email Password Security
**✅ DO:**
- Use Gmail App Passwords (not your real password)
- Store in Railway environment variables (encrypted)

**❌ DON'T:**
- Commit passwords to Git
- Share your .env file

---

## 📊 Monitor Your Application

### View Logs
Railway Dashboard → Your Service → **"Observability"**

### Check Database
The SQLite database is stored in Railway's ephemeral storage. For persistence, consider:
1. **Railway Volume** (persistent storage)
2. **PostgreSQL** (upgrade for production)

### Cost Monitoring
- Railway Free Tier: $5 credit/month
- This app uses: ~$2-3/month
- If you exceed, Railway will pause (no charges)

---

## 🔧 Troubleshooting

### App Not Starting
**Check logs for:**
```
GEMINI_API_KEY not found
```
**Fix:** Add GEMINI_API_KEY in environment variables

### No Emails Received
**Check:**
1. Gmail App Password is correct
2. 2FA enabled on Gmail
3. Logs show "Email sent successfully"

**Test manually:**
```bash
# In Railway Shell (Service → Settings → Shell)
python -c "import smtplib; print('SMTP test OK')"
```

### Resume Not Found
**Check:**
- `data/resume.pdf` exists in repository
- Or environment variable `RESUME_URL` is set
- Logs show "Resume parsed successfully"

### Selenium/Chrome Issues
Railway includes Chrome in `nixpacks.toml`:
```toml
nixPkgs = ['python311', 'chromium', 'chromedriver']
```
If issues persist, check logs for "ChromeDriver" errors.

---

## 🎉 Success Checklist

- [ ] Code pushed to GitHub
- [ ] Railway project created
- [ ] Environment variables configured
- [ ] Resume uploaded (via Git or URL)
- [ ] First deployment successful
- [ ] Logs show scheduler running
- [ ] Received first email within 30 minutes
- [ ] Monitoring dashboard set up

---

## 🚨 Urgent Mode Features

Your app will:
- ✅ Run every **30 minutes** (48 times/day)
- ✅ Search Indeed, StepStone, LinkedIn
- ✅ Find jobs posted **within 14 days**
- ✅ Match **90%** with your resume
- ✅ Send **TOP 10** jobs per email
- ✅ **NO duplicates** - tracks sent jobs
- ✅ Prioritize **urgent/visa sponsor** jobs
- ✅ **100% FREE** - Gemini AI

---

## 💡 Pro Tips

1. **Check emails regularly** - You'll get 48 emails/day max
2. **Apply FAST** - Jobs posted within 14 days fill quickly
3. **Customize config.yaml** - Add your preferred job titles/locations
4. **Monitor logs** - Railway shows all activity
5. **Keep resume updated** - Push changes to GitHub, Railway auto-redeploys

---

## 🆘 Support

**Issues?**
- Check Railway logs first
- Verify all environment variables
- Test locally before deploying: `python main.py`

**Railway Help:**
- Docs: https://docs.railway.app/
- Discord: https://discord.gg/railway

---

## 🎯 What You Need to Provide Me

For Railway deployment to work perfectly, I need:

### ✅ From You
1. **Gemini API Key**
   - Get from: https://makersuite.google.com/app/apikey
   - Free, instant setup

2. **Gmail App Password**
   - Get from: https://myaccount.google.com/apppasswords
   - Need 2FA enabled first

3. **Resume PDF**
   - Save as: `data/resume.pdf`
   - Include: ALL skills, experience, education, languages
   - The more detailed, the better matches!

4. **GitHub Repository** (optional, but recommended)
   - Push your code there
   - Railway deploys from GitHub

### ✅ Optional
5. **LinkedIn Credentials** (if you want LinkedIn scraping)
   - Email + Password

---

## 📁 File Structure for Railway

Your repository should have:
```
ai-job-matcher/
├── Procfile                  # Railway start command
├── railway.json              # Railway configuration
├── nixpacks.toml            # Build configuration (Chrome/ChromeDriver)
├── runtime.txt              # Python version
├── requirements.txt         # Dependencies
├── main.py                  # Application entry point
├── config/
│   └── config.yaml          # Job preferences
├── data/
│   └── resume.pdf          # YOUR RESUME HERE
├── src/
│   ├── scrapers/           # Job scrapers
│   ├── matchers/           # AI matching
│   ├── database/           # SQLite
│   └── notifiers/          # Email sender
└── README.md
```

---

**Ready to deploy? Let me know if you need help with any step!** 🚀
