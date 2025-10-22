# Quick Start: cPanel Deployment (5 Minutes)

## What You Need
- cPanel login credentials
- Files in `SurveyAIUIUC/` folder

## Step 1: Upload (2 min)
1. Login to cPanel
2. Open **File Manager**
3. Go to `public_html/`
4. Create folder: `SurveyAIUIUC`
5. **Upload all files** from your local folder

## Step 2: Setup Python App (2 min)
1. In cPanel, find **"Setup Python App"**
2. Click **"Create Application"**
3. Fill in:
   - Python: 3.9
   - App root: `SurveyAIUIUC`
   - URL: `yourdomain.com/SurveyAIUIUC`
   - Startup: `passenger_wsgi.py`
4. Click **Create**
5. Copy the pip install command shown
6. Paste in terminal and run to install dependencies

## Step 3: Edit .htaccess (1 min)
1. Open `.htaccess` in File Manager
2. Replace `username` with YOUR cPanel username (2 places)
3. Save

## Step 4: Test
Visit: `https://yourdomain.com/SurveyAIUIUC`

## Done!

### Access Points:
- Survey: `https://glowstone.red/SurveyAIUIUC`
- Admin: `https://glowstone.red/SurveyAIUIUC/admin`
- Password: `password` (change this!)

## Need Help?
See full guide: `CPANEL_DEPLOYMENT.md`

## Changing Admin Password

1. Open Terminal or use Python to generate hash:
```python
import hashlib
hashlib.sha256(b"YourNewPassword").hexdigest()
```

2. Copy the hash

3. Edit `main.py` line 22:
```python
ADMIN_PASSWORD_HASH = "paste_your_hash_here"
```

4. Restart app in Python App Manager

