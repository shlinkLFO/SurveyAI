# Fix Blank Page on survey.glowstone.red

## Good News!
✅ No more redirect to /regenai! The .htaccess fix worked!
❌ Node.js app isn't serving content

## Quick Diagnostic Checklist

### 1. Check Node.js App Status
**In cPanel → Setup Node.js App:**
- [ ] Is the app showing as "Running" (green)?
- [ ] If stopped or red, click "Start App" or "Restart"

### 2. Check Application Logs
**In the Node.js App interface:**
1. Find "View Logs" or "Show Logs" button
2. Click it
3. Look for:
   - ✅ Good: "Survey server running on port 3000"
   - ❌ Bad: Error messages
   - ❌ Bad: "Cannot find module 'express'"
   - ❌ Bad: Port errors

### 3. Verify NPM Install Completed
Did you run "Run NPM Install"?
- [ ] Yes, and it showed success/completed
- [ ] No, go back and run it now
- [ ] Not sure, check for "node_modules" folder in /home/shlinky/ServeyAILL6/

### 4. Check Subdomain Document Root
**In cPanel → Subdomains:**
1. Find survey.glowstone.red
2. Check "Document Root"
3. Should be: `/home/shlinky/ServeyAILL6`
4. NOT: `/home/shlinky/public_html/survey`

### 5. Verify Files Are There
**In File Manager → /home/shlinky/ServeyAILL6/:**
- [ ] index.html
- [ ] 84Metashosan.html
- [ ] server.js
- [ ] package.json
- [ ] .env
- [ ] node_modules folder (created by npm install)

## Most Likely Causes

### Cause 1: App Not Running
**Fix:** Go to Node.js App and click "Start App" or "Restart"

### Cause 2: NPM Install Never Ran
**Fix:** 
1. Node.js App → "Run NPM Install"
2. Wait for completion
3. Restart app

### Cause 3: Wrong Document Root
**Fix:**
1. Subdomains → Edit survey.glowstone.red
2. Change Document Root to: `/home/shlinky/ServeyAILL6`
3. Save

### Cause 4: App Crashed
**Fix:** Check logs for error message, then:
- Verify .env file exists with PORT=3000
- Check if port 3000 is available
- Look for syntax errors in logs

## Step-by-Step Fix

### Step 1: Restart the App
1. Go to "Setup Node.js App"
2. Find your app
3. Click "Stop App"
4. Click "Start App"
5. Wait 10 seconds
6. Refresh survey.glowstone.red

### Step 2: Check Logs
1. In Node.js app, click "View Logs"
2. Look at the most recent entries
3. Should see: "Survey server running on port 3000"

### Step 3: If Still Blank
Try accessing with HTTP specifically:
- http://survey.glowstone.red/ (not https)

### Step 4: Browser Console Check
1. On the blank page, press F12
2. Go to Console tab
3. Look for any errors
4. Screenshot or copy errors

### Step 5: Test the App Directly
Try accessing the main domain root:
- https://glowstone.red/

If that also shows blank (not /regenai redirect), there's a deeper Apache config issue.

## Quick Terminal Test (in cPanel)

If cPanel has Terminal access:
```bash
cd /home/shlinky/ServeyAILL6
ls -la
# Should see all your files plus node_modules

# Check if app is running
ps aux | grep node
# Should see server.js process

# Test if port 3000 responds
curl http://localhost:3000/
# Should return HTML
```

## Contact Namecheap Support

If still blank after all checks:

> "My Node.js app at survey.glowstone.red shows a blank page. The app is running (status green), NPM install completed, all files are uploaded to /home/shlinky/ServeyAILL6/, and logs show 'Survey server running on port 3000'. The subdomain points to the correct document root. Can you help check why the app isn't serving content?"

**Live Chat:** https://www.namecheap.com/support/live-chat/

