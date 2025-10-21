# Deploy SurveyAI to Namecheap cPanel (Stellar Plan)

## Your Setup
- **Host**: glowstone.red
- **Plan**: Namecheap Stellar (supports Node.js ✅)
- **Username**: shlinky
- **cPanel**: Available

## Step-by-Step Deployment

### Step 1: Access cPanel

1. **Go to**: https://glowstone.red:2083 or https://cpanel.glowstone.red
   - Or log in through: https://www.namecheap.com → Account → Hosting List → Manage
   
2. **Login with:**
   - Username: `shlinky`
   - Password: Your cPanel password

### Step 2: Upload Files via File Manager

1. **In cPanel, find "File Manager"** (under Files section)

2. **Navigate to the directory:**
   - Go to `/home/shlinky/public_html/` or create `/home/shlinky/ServeyAILL6/`
   - For subdomain/subdirectory, create folder: `ServeyAILL6` or `SurveyAI`

3. **Click "Upload"** button (top menu)

4. **Select and upload these 5 files:**
   - `index.html`
   - `84Metashosan.html`
   - `server.js`
   - `package.json`
   - `.gitignore`

   **Location on your PC**: `C:\Users\mason\SurveyAI\`

5. **Wait for upload to complete** (should be very fast, they're small files)

### Step 3: Set Up Node.js Application in cPanel

1. **In cPanel, find "Setup Node.js App"** (under Software section)
   - If you don't see it, search for "Node" in cPanel search bar

2. **Click "Create Application"**

3. **Configure the application:**
   ```
   Node.js version: 18.x (or latest available)
   Application mode: Production
   Application root: ServeyAILL6 (or the folder where you uploaded files)
   Application URL: glowstone.red/SurveyAI or your preferred path
   Application startup file: server.js
   ```

4. **Click "Create"**

### Step 4: Install Dependencies

1. **In the Node.js App interface**, you should see your application listed

2. **Click "Run NPM Install"** button
   - This installs express, cors, and dotenv

3. **Wait for installation to complete** (may take 1-2 minutes)

### Step 5: Set Environment Variables

1. **In the Node.js App settings**, find "Environment Variables" section

2. **Add these variables:**
   ```
   ADMIN_PASSWORD = YourSecurePassword123
   PORT = 3000
   ```

3. **Click "Save"**

### Step 6: Start the Application

1. **Click "Start App"** or "Restart App" button

2. **Check status** - should show "Running"

3. **Note the port** assigned (might be different from 3000)

### Step 7: Configure .htaccess (if needed)

If your app isn't accessible, create a `.htaccess` file in the application root:

```apache
DirectoryIndex disabled
RewriteEngine On
RewriteRule ^$ http://127.0.0.1:YOUR_PORT/ [P,L]
RewriteCond %{REQUEST_FILENAME} !-f
RewriteCond %{REQUEST_FILENAME} !-d
RewriteRule ^(.*)$ http://127.0.0.1:YOUR_PORT/$1 [P,L]
```

Replace `YOUR_PORT` with the port shown in Node.js app settings.

## Alternative: Quick Upload via FTP

### Using FileZilla:

1. **Download FileZilla**: https://filezilla-project.org/

2. **Connect:**
   ```
   Host: ftp.glowstone.red
   Username: shlinky
   Password: Your cPanel password
   Port: 21
   ```

3. **Navigate to**: `/public_html/ServeyAILL6/`

4. **Drag and drop** your 5 files

5. **Then follow Step 3-6 above** to set up Node.js app

## Access Your Application

After setup, access at:
- **Survey**: https://glowstone.red/SurveyAI/ (or whatever path you configured)
- **Admin**: https://glowstone.red/SurveyAI/84Metashosan

## Troubleshooting

### "Node.js App not showing in cPanel"

Your plan supports it! Try:
1. Look under "Software" section
2. Search for "Node" in cPanel search
3. Contact Namecheap support to enable it

### "Application won't start"

1. Check logs in Node.js App interface
2. Verify `package.json` uploaded correctly
3. Make sure npm install completed
4. Check port isn't already in use

### "Can't access the app via URL"

1. Check if app shows "Running" status
2. Verify .htaccess configuration
3. Check Application URL in Node.js settings
4. May need to set up subdomain first

### "Permission denied" errors

```bash
# In cPanel Terminal (if available):
cd ~/ServeyAILL6
chmod 755 server.js
chmod 644 *.html *.json
```

## Data Storage

Your survey responses will be saved in:
```
/home/shlinky/ServeyAILL6/survey-data.json
```

**Backup regularly** via File Manager → Download

## Quick Reference

### cPanel URLs:
- Main: https://glowstone.red:2083
- Alt: https://cpanel.glowstone.red
- Via Namecheap: Account → Hosting List → Manage

### Files to Upload:
```
C:\Users\mason\SurveyAI\index.html          → Upload
C:\Users\mason\SurveyAI\84Metashosan.html   → Upload
C:\Users\mason\SurveyAI\server.js           → Upload
C:\Users\mason\SurveyAI\package.json        → Upload
C:\Users\mason\SurveyAI\.gitignore          → Upload
```

### After Upload Checklist:
- ✅ Files uploaded to folder
- ✅ Node.js app created in cPanel
- ✅ NPM install completed
- ✅ Environment variables set (ADMIN_PASSWORD, PORT)
- ✅ App started/running
- ✅ Test survey URL
- ✅ Test admin URL

## Need Help?

**Namecheap Support:**
- Live Chat: https://www.namecheap.com/support/live-chat/
- Ticket: https://ap.www.namecheap.com/
- Phone: Available 24/7

**Ask them:**
"I need help deploying a Node.js application on my Stellar hosting plan. I've uploaded the files and need to configure the Node.js App in cPanel."

## Next Steps

1. Log into cPanel
2. Upload the 5 files via File Manager
3. Set up Node.js app
4. Test the URLs
5. **IMPORTANT**: Change the admin password from default!

You're ready to deploy! 🚀

