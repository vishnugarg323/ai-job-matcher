# 🎨 Web UI Dashboard - User Guide

**Multi-Profile AI Job Matcher with Beautiful Web Interface**

---

## 🚀 New Features

### ✨ What's New in Version 3.0

1. **Web-Based Dashboard** - Beautiful UI accessible from any browser
2. **Multi-Profile Support** - Manage multiple resumes/job searches simultaneously
3. **Resume Upload via UI** - No more manual file copying
4. **Live Statistics** - Real-time dashboard with stats
5. **Manual Triggers** - Start job search instantly with one click
6. **Run History** - View last 10 runs with success/failure status
7. **Job Results Table** - See all matched jobs in a sortable table
8. **Per-Profile Configuration** - Each resume has its own settings

---

## 📊 Dashboard Overview

### Main Screen Features

```
┌─────────────────────────────────────────────────────────────────┐
│  🎯 Dashboard Statistics (Top Bar)                              │
│  • Active Profiles: Count of profiles with resumes              │
│  • Jobs (7 Days): Total jobs found in last week                 │
│  • Success Rate: % of successful runs                           │
│  • Avg Jobs/Run: Average matches per execution                  │
└─────────────────────────────────────────────────────────────────┘

┌──────────────────────┬──────────────────────────────────────────┐
│  📋 Profiles (Left)  │  📊 Content Area (Right)                 │
│                      │                                          │
│  • List of profiles  │  When Profile Selected:                 │
│  • Add new profile   │  • Recent Jobs Table (20 latest)        │
│  • Edit/Delete       │  • Run History (10 latest)              │
│  • Manual trigger    │                                          │
│                      │  When No Profile:                        │
│                      │  • Welcome message                       │
│                      │  • Create first profile button           │
└──────────────────────┴──────────────────────────────────────────┘
```

---

## 🎯 How to Use

### 1. Access the Dashboard

**Local:**
```bash
python web_app.py
# Open browser: http://localhost:5000
```

**Railway (after deployment):**
```
https://your-app-name.up.railway.app/
```

### 2. Create Your First Profile

1. Click **"+ Add Profile"** button (top right)
2. Fill in the form:

   **Basic Info:**
   - **Profile Name:** e.g., "Python Developer - Berlin"
   - **Email:** Where to send job alerts
   
   **API Key (Optional):**
   - **Gemini API Key:** Leave empty to use global key
   - Or add profile-specific key
   
   **Resume:**
   - Click "Choose File"
   - Select your resume (PDF or DOCX)
   - Max 16MB
   
   **Job Preferences:**
   - **Job Titles:** Python Developer, Backend Engineer
   - **Locations:** Berlin, Munich, Remote
   - **Min Salary:** 60000
   - **Required Keywords:** Python, AWS, Docker
   - **Exclude Keywords:** Unpaid, Internship

3. Click **"Save Profile"**

### 3. Upload Resume

- Resume is uploaded when you save the profile
- Supported formats: PDF, DOCX, DOC
- File is saved to `data/uploads/profile_{id}_{filename}`
- Can re-upload by editing profile

### 4. Trigger Manual Run

- Click the **▶️ Play** button on any profile card
- Job search starts immediately in background
- Check "Run History" for progress
- Email sent when jobs are found

### 5. View Results

**Jobs Table:**
- Shows last 20 matched jobs
- Each job displays:
  - Title, Company, Location
  - Match percentage (90%+ highlighted)
  - Apply button (opens job URL)
  - Date found

**Run History:**
- Last 10 executions
- Shows: Time, Status, Jobs Found, Duration
- Green = Success, Red = Failed, Blue = Running

---

## 🎨 UI Features Explained

### Profile Card

```
┌─────────────────────────────────────────────────────┐
│  👤 Python Developer - Berlin                       │
│  ✉️  vishnu@email.com                               │
│  📄 Resume uploaded                                  │
│                                              [▶][✏][🗑] │
└─────────────────────────────────────────────────────┘
```

**Buttons:**
- **▶️ Play:** Trigger manual run
- **✏️ Edit:** Modify profile settings
- **🗑️ Delete:** Remove profile (with confirmation)

### Job Row

```
┌─────────────────────────────────────────────────────┐
│  Senior Python Developer                        95% │
│  🏢 TechCorp | 📍 Berlin                            │
│  📅 Jan 8, 2026                          [Apply →] │
└─────────────────────────────────────────────────────┘
```

**Match Colors:**
- **Green (95%+):** Excellent match
- **Blue (90-95%):** Good match  
- **Yellow (85-90%):** Fair match

---

## 🔧 Configuration

### Global Settings

Set via environment variables (Railway):

```env
# Scheduling
SCHEDULE_INTERVAL_MINUTES=30

# Email (if not using per-profile)
EMAIL_SENDER=your@gmail.com
EMAIL_PASSWORD=your_app_password

# Gemini (if not using per-profile)
GEMINI_API_KEY=your_key

# Job Settings
MAX_JOBS_PER_EMAIL=10
MAX_JOB_AGE_DAYS=14
```

### Per-Profile Settings

Each profile can have:
- **Own Gemini API Key** (or use global)
- **Own Email** (always required)
- **Own Job Preferences:**
  - Job titles to search
  - Locations
  - Salary range
  - Required keywords
  - Exclude keywords

---

## 🚀 Deployment on Railway

### Step 1: Push Code with Web UI

```bash
git add .
git commit -m "Add web UI dashboard"
git push
```

### Step 2: Railway Auto-Deploys

Railway detects the web server and:
- Runs `python web_app.py`
- Exposes PORT environment variable
- Provides public URL

### Step 3: Access Your Dashboard

```
https://your-app-name.up.railway.app/
```

### Step 4: Create Profiles via UI

1. Open the web dashboard
2. Click "+ Add Profile"
3. Upload resume via browser
4. Configure job preferences
5. Trigger manual runs or wait for schedule

---

## 📊 Multi-Profile Use Cases

### Use Case 1: Different Job Types

```
Profile 1: "Python Backend Developer"
  • Resume: backend_resume.pdf
  • Titles: Backend Engineer, Python Developer
  • Locations: Berlin, Munich
  • Keywords: Python, Django, PostgreSQL

Profile 2: "Machine Learning Engineer"
  • Resume: ml_resume.pdf
  • Titles: ML Engineer, Data Scientist
  • Locations: Remote
  • Keywords: Python, TensorFlow, ML
```

### Use Case 2: Different Countries

```
Profile 1: "Germany Jobs"
  • Resume: resume_de.pdf
  • Locations: Berlin, Munich, Hamburg
  • Keywords: German language

Profile 2: "Remote International"
  • Resume: resume_en.pdf
  • Locations: Remote
  • Keywords: English, international
```

### Use Case 3: Family Members

```
Profile 1: "Vishnu - Python Dev"
  • Email: vishnu@email.com
  • Resume: vishnu_resume.pdf

Profile 2: "Partner - Frontend Dev"
  • Email: partner@email.com
  • Resume: partner_resume.pdf
```

---

## 🔄 Automatic Scheduling

### How It Works

The web server runs continuously and:
1. Checks every 30 minutes (configurable)
2. Runs job search for **all enabled profiles**
3. Each profile gets its own email
4. Results saved to database

### Enable/Disable Profiles

- Edit profile and toggle "Enabled" checkbox
- Disabled profiles skip automatic runs
- Can still trigger manually

---

## 📈 Statistics & Monitoring

### Dashboard Stats

- **Active Profiles:** Profiles with resumes uploaded
- **Jobs (7 Days):** Total jobs found across all profiles
- **Success Rate:** % of runs that completed successfully
- **Avg Jobs/Run:** Average matches per execution

### Per-Profile Stats

- **Total Jobs Found:** Lifetime count
- **Last Run:** Timestamp of last execution
- **Success Rate:** Per-profile success percentage

---

## 🛠️ Advanced Features

### API Endpoints

The web UI is powered by REST APIs:

```
GET  /api/profiles              # List all profiles
POST /api/profiles              # Create profile
PUT  /api/profiles/:id          # Update profile
DELETE /api/profiles/:id        # Delete profile

POST /api/profiles/:id/resume   # Upload resume
POST /api/profiles/:id/run      # Trigger manual run

GET  /api/profiles/:id/jobs     # Get jobs
GET  /api/profiles/:id/history  # Get run history

GET  /api/dashboard/stats       # Dashboard stats
GET  /health                    # Health check
```

### Database Schema

**profiles Table:**
- id, name, email, resume_path
- gemini_key, job_preferences (JSON)
- enabled, created_at, updated_at

**jobs Table:**
- id, profile_id, job_hash
- title, company, location, url
- match_score, ai_similarity, keyword_match
- created_at, notified, notification_sent_at

**run_history Table:**
- id, profile_id, status
- jobs_found, jobs_scraped
- started_at, completed_at, error_message

---

## 🔒 Security

### Production Recommendations

1. **Add Authentication**
   - Use Flask-Login or JWT tokens
   - Password-protect dashboard

2. **HTTPS Only**
   - Railway provides free HTTPS
   - Never use HTTP in production

3. **Environment Variables**
   - Store sensitive keys in Railway vars
   - Never commit `.env` to Git

4. **File Upload Security**
   - Max file size: 16MB
   - Allowed types: PDF, DOCX only
   - Files sanitized with `secure_filename()`

---

## 🐛 Troubleshooting

### Issue: Web UI Not Loading

**Check:**
1. Server running: `python web_app.py`
2. Port 5000 available
3. No firewall blocking

**Solution:**
```bash
# Kill process on port 5000
lsof -ti:5000 | xargs kill -9

# Restart web server
python web_app.py
```

### Issue: Resume Upload Fails

**Check:**
1. File size under 16MB
2. File format is PDF or DOCX
3. `data/uploads/` folder exists

**Solution:**
```bash
# Create upload folder
mkdir -p data/uploads
chmod 777 data/uploads
```

### Issue: Manual Run Doesn't Work

**Check:**
1. Resume uploaded for profile
2. Gemini API key configured
3. Check browser console for errors

**Solution:**
- Open browser DevTools (F12)
- Check "Network" tab for API errors
- Verify Gemini API key is valid

---

## 🎯 Best Practices

1. **Organize Profiles**
   - Use descriptive names
   - One profile per job type/location
   - Keep resume updated

2. **Monitor Regularly**
   - Check dashboard daily
   - Review run history for errors
   - Adjust preferences based on results

3. **Optimize Settings**
   - Start with broad keywords
   - Narrow down if too many results
   - Increase salary if too many low-paying jobs

4. **Act Fast**
   - Apply within 24 hours of notification
   - Jobs expire quickly (14-day filter)
   - Check emails frequently

---

## 📱 Mobile Access

The dashboard is **responsive** and works on:
- 📱 Mobile phones
- 📲 Tablets
- 💻 Laptops
- 🖥️ Desktops

Access from anywhere with internet!

---

## 🎉 Success!

You now have a **professional, multi-tenant job matching system** with:
- ✅ Beautiful web dashboard
- ✅ Multiple resume support
- ✅ Resume upload via UI
- ✅ Manual triggers
- ✅ Live statistics
- ✅ Job results table
- ✅ Run history
- ✅ Per-profile configuration

**Ready to deploy and land your dream job!** 🚀
