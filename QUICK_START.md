# ⚡ Quick Start - 5 Minutes Setup

## Step 1: Install Dependencies (1 min)
```bash
pip install -r requirements.txt
```

## Step 2: Get Free Gemini API Key (2 min)
1. Go to: https://makersuite.google.com/app/apikey
2. Click "Create API Key"
3. Copy the key

## Step 3: Configure Environment (1 min)
Create `.env` file in project root:
```bash
GEMINI_API_KEY=paste-your-key-here
SECRET_KEY=any-random-string-12345
EMAIL_SENDER=your-email@gmail.com
EMAIL_PASSWORD=your-gmail-app-password
```

**Gmail App Password Setup:**
1. Google Account → Security → 2-Step Verification (enable)
2. Search "App passwords" → Generate → Copy

## Step 4: Start Application (1 min)
```bash
python web_app.py
```

Open browser: http://localhost:5000

## Step 5: Create Your First Profile
1. Click "+" button
2. Enter name: "Software Engineer Search"
3. Enter email: your-email@gmail.com
4. Enter job title: "Software Engineer"
5. Click "Upload Resume" → Select your PDF
6. Click "Save"

## Done! 🎉

Your system is now running! It will:
- ✅ Search jobs every 30 minutes automatically
- ✅ Find jobs matching >90% with your resume
- ✅ Email you the top matches
- ✅ Never send duplicates

## Manual Trigger
Click "▶ Run" button next to your profile to start search immediately.

## Deploy to Cloud
See README.md for Railway deployment (24/7 operation).

---

**That's it! Happy job hunting!** 🚀
