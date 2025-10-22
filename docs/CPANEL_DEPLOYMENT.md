# cPanel Deployment Guide (NameCheap Stellar)

## Step-by-Step Deployment via cPanel

### Step 1: Upload Files

1. **Login to cPanel** at your NameCheap Stellar hosting
2. **Open File Manager**
3. Navigate to `public_html/`
4. **Create new folder**: `SurveyAIUIUC`
5. **Upload all files** from your local `SurveyAIUIUC/` folder:
   - Upload via "Upload" button or drag-and-drop
   - Or use FTP client (FileZilla) to upload entire folder

### Step 2: Setup Python Application

#### Option A: Using cPanel Python App Manager

1. In cPanel, find **"Setup Python App"** (or "Python Selector")
2. Click **"Create Application"**
3. Configure:
   - **Python version**: 3.9 or higher
   - **Application root**: `SurveyAIUIUC`
   - **Application URL**: `glowstone.red/SurveyAIUIUC`
   - **Application startup file**: `passenger_wsgi.py`
   - **Application Entry point**: `application`

4. Click **Create**

5. In the app configuration, enter virtual environment and run:
   ```bash
   pip install -r requirements.txt
   ```

6. **Restart** the application

#### Option B: Manual Setup via Terminal (if available)

1. In cPanel, open **"Terminal"** (if available)
2. Navigate to your directory:
   ```bash
   cd public_html/SurveyAIUIUC
   ```

3. Create virtual environment:
   ```bash
   virtualenv -p python3.9 venv
   source venv/bin/activate
   ```

4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

5. Test locally:
   ```bash
   python main.py
   ```

### Step 3: Configure .htaccess

The `.htaccess` file is already included, but you need to **edit it**:

1. Open `public_html/SurveyAIUIUC/.htaccess`
2. Replace `username` with your actual cPanel username
3. Update paths:
   ```apache
   PassengerAppRoot /home/YOUR_USERNAME/public_html/SurveyAIUIUC
   PassengerPython /home/YOUR_USERNAME/virtualenv/SurveyAIUIUC/3.9/bin/python3
   ```

### Step 4: Set File Permissions

1. In File Manager, select all Python files
2. Click **"Permissions"** or **"Change Permissions"**
3. Set to `644` for most files
4. Set to `755` for:
   - `passenger_wsgi.py`
   - `main.py`

### Step 5: Configure Domain/Subdomain

#### If using subdomain:
1. In cPanel, go to **"Subdomains"**
2. Create: `survey.glowstone.red`
3. Point document root to: `public_html/SurveyAIUIUC`

#### If using path:
The app should be accessible at: `glowstone.red/SurveyAIUIUC`

### Step 6: Test the Application

Visit: `https://glowstone.red/SurveyAIUIUC`

You should see the survey page. Test:
- Main survey page
- Submit a response
- Admin panel: `https://glowstone.red/SurveyAIUIUC/admin`
- API endpoint: `https://glowstone.red/SurveyAIUIUC/api/responses`

## Troubleshooting

### Error 500 - Internal Server Error

**Check error logs**:
1. In cPanel, go to **"Errors"** or **"Error Log"**
2. Look for Python/Passenger errors

**Common fixes**:
- Ensure Python version is 3.8+
- Check file permissions (644 for files, 755 for directories)
- Verify virtual environment path in `.htaccess`
- Check that all dependencies installed: `pip list`

### Application Not Starting

**Check passenger_wsgi.py path**:
```bash
# In cPanel Terminal or File Manager, verify:
/home/username/public_html/SurveyAIUIUC/passenger_wsgi.py
```

**Check Python path**:
```bash
which python3
# Should match the path in .htaccess
```

### Static Files Not Loading

**Ensure .htaccess allows them**:
```apache
<FilesMatch "\.(html|css|js|json)$">
    Allow from all
</FilesMatch>
```

### Database/JSON Permission Issues

```bash
# Set permissions for survey-data.json
chmod 666 survey-data.json
```

### Module Not Found Errors

**Reinstall dependencies**:
1. Access Terminal or SSH (if available)
2. Navigate to app directory
3. Activate virtual environment
4. Run: `pip install -r requirements.txt`

## Alternative: No Python App Support?

If your cPanel doesn't support Python apps, you have two options:

### Option 1: Use a Subdomain with Different Hosting
Deploy on a platform that supports Python:
- PythonAnywhere (free tier available)
- Heroku
- DigitalOcean App Platform
- Railway
- Render

### Option 2: Contact NameCheap Support
Ask them to:
1. Enable Python application support
2. Install required Python version
3. Configure Passenger for your account

## Files Uploaded Checklist

Make sure these files are in `public_html/SurveyAIUIUC/`:

```
✓ main.py
✓ passenger_wsgi.py
✓ .htaccess
✓ requirements.txt
✓ index.html
✓ 84Metashosan.html
✓ survey-data.json
✓ README.md
```

## Update Procedure

To update the application:

1. **Backup data**:
   - Download `survey-data.json` via File Manager

2. **Upload new files**:
   - Upload updated files via File Manager
   - Overwrite existing files

3. **Update dependencies** (if changed):
   - Use Python App Manager to reinstall
   - Or via Terminal: `pip install -r requirements.txt`

4. **Restart app**:
   - In Python App Manager, click "Restart"
   - Or create/touch a `tmp/restart.txt` file

## Security Settings

1. **Change admin password** in `main.py`:
   ```python
   ADMIN_PASSWORD_HASH = "your_generated_hash"
   ```

2. **Ensure HTTPS**:
   - Install SSL certificate (free with NameCheap)
   - Force HTTPS in `.htaccess`:
   ```apache
   RewriteEngine On
   RewriteCond %{HTTPS} off
   RewriteRule ^(.*)$ https://%{HTTP_HOST}%{REQUEST_URI} [L,R=301]
   ```

3. **Set restrictive permissions**:
   - Files: 644
   - Directories: 755
   - survey-data.json: 666 (writable by app)

## cPanel-Specific Tips

1. **Python version**: Use cPanel's Python Selector to choose 3.9+
2. **Resource limits**: Check your hosting plan's Python resource limits
3. **Logs**: Monitor through cPanel's Error Log viewer
4. **Backups**: Use cPanel's backup feature to backup `survey-data.json`
5. **Cron jobs**: Can set up automatic backups via cPanel Cron Jobs

## Getting Help

1. **cPanel Documentation**: Check NameCheap's knowledge base
2. **Support**: Contact NameCheap support for Python app setup
3. **Application Logs**: Check error_log in your home directory
4. **Test locally**: Download files and test with `python main.py`

## Performance Notes

- cPanel shared hosting may have resource limits
- For high traffic, consider upgrading to VPS
- Monitor CPU/memory usage in cPanel
- Consider enabling caching if available

