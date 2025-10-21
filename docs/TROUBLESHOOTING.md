# Troubleshooting 404 Error on glowstone.red/SurveyAILL6

## You're seeing 404 because the Node.js app isn't running yet

The files being uploaded is only **Step 1**. You also need to configure and start the Node.js application in cPanel.

## Complete Setup Checklist

### ✅ Step 1: Files Uploaded (You probably did this)
- [ ] Files in `/home/shlinky/ServeyAILL6/`
- [ ] All 5 files present: index.html, 84Metashosan.html, server.js, package.json, .gitignore

### ⚠️ Step 2: Node.js App Setup (You need to do this!)

1. **In cPanel, search for "Node.js"** or look under "Software" section
   - Should be called "Setup Node.js App" or "Node.js Selector"

2. **Click "Create Application"**

3. **Fill in these settings:**
   ```
   Node.js version: 18.x (or 16.x, 20.x - whatever is available)
   Application mode: Production
   Application root: ServeyAILL6
   Application URL: /SurveyAILL6 or /SurveyAI (your choice)
   Application startup file: server.js
   ```

4. **Click "Create"**

### ⚠️ Step 3: Install Dependencies

1. **In the Node.js app interface**, look for button that says:
   - "Run NPM Install" or "Install Packages"
   
2. **Click it and wait** (takes 1-2 minutes)

3. **Check that it completed successfully**

### ⚠️ Step 4: Set Environment Variables

1. **In the Node.js app settings**, find "Environment Variables"

2. **Add two variables:**
   ```
   Name: ADMIN_PASSWORD
   Value: YourSecurePassword123
   
   Name: PORT  
   Value: 3000
   ```

3. **Save the variables**

### ⚠️ Step 5: Start the Application

1. **Look for "Start" or "Restart" button**

2. **Click it**

3. **Status should show "Running" or "Active"**

### ⚠️ Step 6: Check the URL

After completing steps 2-5, the app should be accessible at:
- https://glowstone.red/SurveyAILL6/ (note the trailing slash)
- or whatever URL you configured in Application URL

## Common Issues

### Issue 1: Can't find "Node.js" in cPanel

**Solution:**
- Search for "Node" in cPanel search bar (top right)
- Look under "Software" section
- If still not found, contact Namecheap support: "Please enable Node.js on my Stellar hosting plan"

### Issue 2: App shows "Stopped" status

**Solution:**
- Check the logs (in Node.js app interface)
- Make sure npm install completed
- Make sure server.js uploaded correctly
- Try clicking "Restart"

### Issue 3: App shows "Running" but still 404

**Solution:**

**Option A: Check Application URL**
- In Node.js settings, verify the "Application URL" field
- Try accessing with that exact path
- Try with and without trailing slash: `/SurveyAILL6/` vs `/SurveyAILL6`

**Option B: Create .htaccess**
1. In File Manager, go to `/home/shlinky/ServeyAILL6/`
2. Create new file: `.htaccess`
3. Add this content:
```apache
DirectoryIndex disabled
RewriteEngine On
RewriteRule ^$ http://127.0.0.1:APP_PORT/ [P,L]
RewriteCond %{REQUEST_FILENAME} !-f
RewriteCond %{REQUEST_FILENAME} !-d
RewriteRule ^(.*)$ http://127.0.0.1:APP_PORT/$1 [P,L]
```
Replace `APP_PORT` with the port shown in your Node.js app (probably 3000)

**Option C: Check logs**
- In Node.js app interface, click "Show logs" or "View logs"
- Look for errors
- Common error: "Port already in use" - change PORT in environment variables

### Issue 4: Port conflicts

If you see "Port 3000 already in use":
1. In environment variables, change PORT to: `3001` or `3002`
2. Restart the app

## Quick Diagnostic

Run through this checklist:

1. **Files uploaded?**
   - cPanel → File Manager → /home/shlinky/ServeyAILL6/
   - Do you see all 5 files?

2. **Node.js app created?**
   - cPanel → Setup Node.js App
   - Do you see your application listed?

3. **NPM installed?**
   - In Node.js app, check for "node_modules" folder indicator
   - Or logs should show "npm install completed"

4. **App running?**
   - Status should be green/running, not stopped/red

5. **Correct URL?**
   - Check "Application URL" in Node.js settings
   - Try that exact path

## If Still Not Working

### Option 1: Use public_html instead

Try placing files in public_html for simpler routing:

1. Move files to: `/home/shlinky/public_html/SurveyAILL6/`
2. Configure Node.js app with Application root: `public_html/SurveyAILL6`
3. Set Application URL: `/SurveyAILL6`

### Option 2: Contact Namecheap Support

Live chat: https://www.namecheap.com/support/live-chat/

Tell them:
> "I'm trying to deploy a Node.js application on my Stellar hosting. I've uploaded files to /home/shlinky/ServeyAILL6/ and need help configuring the Node.js app in cPanel to make it accessible at glowstone.red/SurveyAILL6"

They can:
- Verify Node.js is enabled
- Check app configuration
- Help with routing/proxy setup
- Check for port conflicts

## Next Steps

1. **Go to cPanel now**: https://glowstone.red:2083
2. **Find "Setup Node.js App"**
3. **Create the application** with the settings above
4. **Run NPM Install**
5. **Start the app**
6. **Try accessing again**

The 404 is because static files don't work for Node.js apps - you need to start the Node.js server!

