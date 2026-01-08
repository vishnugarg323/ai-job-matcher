# 🎯 AI Job Matcher - Find Your Dream Job in Germany

**Automated job search with AI matching (90%+) - 100% FREE!**

## ✨ Features

- 🌐 **Web Dashboard** - Upload resumes, view matched jobs
- 🤖 **AI Matching** - Google Gemini finds perfect jobs (FREE!)
- 👥 **Multi-Profile** - Different resumes, different emails
- ⚡ **Auto Runs** - Every 30 minutes, 24/7
- 📧 **Email Alerts** - Top matches to your inbox
- 🇩🇪 **Germany Jobs** - Indeed.de, StepStone.de

## 🚀 Quick Start

1. **Install:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure `.env` file:**
   ```bash
   GEMINI_API_KEY=your-key-from-google
   SECRET_KEY=any-random-string
   
   # Optional - for email notifications (otherwise view in dashboard)
   # EMAIL_SENDER=your-email@gmail.com
   # EMAIL_PASSWORD=your-app-password
   
   # Optional - for LinkedIn jobs (otherwise just Indeed + StepStone)
   # LINKEDIN_EMAIL=your-linkedin@example.com
   # LINKEDIN_PASSWORD=your-password
   ```
   Get Gemini key (FREE): https://makersuite.google.com/app/apikey

3. **Start web server:**
   ```bash
   python web_app.py
   ```

4. **Open browser:**
   ```
   http://localhost:5000
   ```

5. **Create profile:**
   - Enter your job title (e.g., "Software Engineer")
   - Upload your resume PDF
   - Add your email
   - Click Save

**That's it!** System runs every 30 minutes automatically and emails you matches >90%.

## 📧 Email Notifications

Each profile gets emails at their own address with jobs matching their specific resume. Only sends jobs >90% match.

## ☁️ Deploy to Railway (24/7 operation)

1. Push to GitHub:
   ```bash
   git remote add origin https://github.com/YOUR_USERNAME/ai-job-matcher.git
   git push -u origin main
   ```

2. Deploy on Railway:
   - Go to https://railway.app
   - Connect GitHub repo
   - Add environment variables (GEMINI_API_KEY, SECRET_KEY, etc)
   - Deploy

3. Your app runs 24/7 in the cloud!

## 🛠️ Tech Stack

- Python 3.11, Flask
- Google Gemini AI (FREE)
- SQLite database
- Bootstrap 5 UI
- APScheduler

## 📝 License

MIT - Free for personal use

---

**Made for job seekers in Germany** 🇩🇪
