# Fix cPanel Node.js Installation Error

## Error You're Seeing:
"An error occurred during installation of modules. The operation was performed, but check availability of application has failed."

This means the app was created but can't respond properly yet.

## Quick Fix (Do These Steps)

### Step 1: Ignore the Error (It's Normal!)
- The app IS created, just not fully configured yet
- Click "OK" or close the error
- You should see your application listed in Node.js Apps

### Step 2: Run NPM Install
1. Find your app in the list (ServeyAILL6)
2. Click **"Run NPM Install"** button
3. **Wait 1-2 minutes** for it to complete
4. You should see "Completed" or green checkmark

### Step 3: Add Environment Variables
1. In your app's settings, find **"Environment variables"**
2. Click **"Add Variable"** and add:
   ```
   Name: ADMIN_PASSWORD
   Value: YourSecurePassword123
   ```
3. Add another variable:
   ```
   Name: PORT
   Value: 3000
   ```
4. Click **"Save"**

### Step 4: Edit Application Settings
1. Click **"Edit"** on your application
2. Verify these settings:
   ```
   Application mode: Production
   Application startup file: server.js
   Application root: ServeyAILL6
   ```
3. Click **"Save"**

### Step 5: Restart the Application
1. Click **"Stop App"** (if it's running)
2. Click **"Start App"**
3. Status should show **"Running"** in green

### Step 6: Test
Visit: **https://glowstone.red/SurveyAILL6/**

## Alternative Fix: Create .env File Manually

If environment variables aren't working:

1. Go to **File Manager**
2. Navigate to `/home/shlinky/ServeyAILL6/`
3. Click **"New File"**
4. Name it: `.env`
5. Edit the file and add:
   ```
   ADMIN_PASSWORD=YourSecurePassword123
   PORT=3000
   ```
6. Save the file
7. Go back to Node.js app and **Restart**

## Why This Error Happens

The error occurs because:
1. **No dependencies installed yet** - server.js needs `express`, `cors`, `dotenv`
2. **No environment variables** - server.js expects PORT and ADMIN_PASSWORD
3. **App checking too fast** - cPanel tests the app before npm install completes

This is **NORMAL** for Node.js apps in cPanel!

## Check if It's Working

### Method 1: Check App Status
In Node.js App interface, look for:
- Status: **Running** (green)
- Not: **Stopped** (red)

### Method 2: Check Logs
1. In Node.js app, click **"Show logs"** or **"View Logs"**
2. Look for:
   - ✅ Good: "Survey server running on port 3000"
   - ❌ Bad: "Cannot find module 'express'" = need npm install
   - ❌ Bad: "Port 3000 already in use" = change PORT to 3001

### Method 3: Test URL
Go to: https://glowstone.red/SurveyAILL6/

- ✅ Should see: Purple survey page
- ❌ If 404: App not running or wrong URL
- ❌ If 502: App crashed, check logs

## Still Not Working?

### Solution A: Use Different Port
Some hosting restricts port 3000. Try:

Environment variable:
```
PORT = 3001
```
Or:
```
PORT = 3002
```

Then restart app.

### Solution B: Check Application URL
1. Edit your app
2. Check **"Application URL"** field
3. It should be: `/SurveyAILL6` or `/SurveyAI`
4. Try accessing with that exact path

### Solution C: Reinstall
If all else fails:
1. **Delete** the app (not the files!)
2. **Create** new app with same settings
3. This time, **wait** for npm install before testing

## Common Mistakes

❌ **Wrong startup file**: Must be `server.js` not `index.html`  
❌ **No npm install**: Dependencies must be installed  
❌ **Wrong path**: Application root must be `ServeyAILL6`  
❌ **Port conflict**: Try different port if 3000 doesn't work  

## Success Checklist

Before testing the URL, verify:
- [x] App shows in Node.js Apps list
- [x] NPM Install completed (shows green checkmark or "Completed")
- [x] Environment variables added (ADMIN_PASSWORD, PORT)
- [x] App status is "Running" (green)
- [x] Application URL is set correctly
- [x] Logs show "Survey server running on port..."

## Need More Help?

**Namecheap Support** (24/7):
- Live Chat: https://www.namecheap.com/support/live-chat/
- Tell them: "I'm getting a content-type error when creating Node.js app. The app is created but won't start. Can you help verify the configuration?"

## What to Tell Support

"I'm trying to run a Node.js application. Files are uploaded to /home/shlinky/ServeyAILL6/. I created the Node.js app but getting a content-type error. I've run npm install and set environment variables. Status shows running but URL returns 404. Can you help check the proxy configuration and logs?"

---

**Bottom line**: The error is normal. Just run NPM Install, add environment variables, and restart. It will work!

