# Fix "Cannot GET /SurveyAILL6/" Error

## The Real Problem

The Node.js app IS running, but cPanel's proxy routing isn't configured. Your app is probably accessible at a different URL.

## Try These URLs First:

1. **Check the app's actual URL in cPanel:**
   - Go to "Setup Node.js App"
   - Look at your application
   - There should be an **"OPEN"** link or button next to "Application URL"
   - **Click that link** - it will show you the real URL

2. **Try these alternative URLs:**
   - https://glowstone.red/ (root, no path)
   - http://glowstone.red:3000/ (direct port access - might be blocked)
   - https://YOUR-APP-URL.glowstone.red/ (cPanel might create subdomain)

## Solution 1: Change Application URL to Root

1. **In cPanel Node.js App:**
   - Click "Edit" on your application
   - Change **"Application URL"** from `/SurveyAILL6` to just `/` (root)
   - Click "Save"
   - Restart the app

2. **Then access at:**
   - https://glowstone.red/ (no SurveyAILL6 path)

## Solution 2: Use Subdomain (Recommended)

This is the cleanest approach:

1. **In cPanel, create a subdomain:**
   - Find "Subdomains" (under Domains section)
   - Create: `survey.glowstone.red`
   - Point it to: `/home/shlinky/ServeyAILL6`

2. **Update Node.js App:**
   - Edit your app
   - Change Application URL to match subdomain
   - Restart

3. **Access at:**
   - https://survey.glowstone.red/

## Solution 3: Fix with .htaccess (Advanced)

1. **Go to File Manager:**
   - Navigate to `/home/shlinky/public_html/`
   - Create or edit `.htaccess`

2. **Add this code:**
```apache
<IfModule mod_rewrite.c>
    RewriteEngine On
    
    # Proxy requests to Node.js app
    RewriteCond %{REQUEST_URI} ^/SurveyAILL6
    RewriteRule ^SurveyAILL6/?(.*)$ http://127.0.0.1:3000/$1 [P,L]
    
    # Handle static files
    RewriteCond %{REQUEST_FILENAME} !-f
    RewriteCond %{REQUEST_FILENAME} !-d
    RewriteCond %{REQUEST_URI} ^/SurveyAILL6
    RewriteRule ^SurveyAILL6/?(.*)$ http://127.0.0.1:3000/$1 [P,L]
</IfModule>
```

3. **Save and test**

## Solution 4: Check App Logs

1. **In Node.js App interface:**
   - Find "Show Logs" or "View Logs"
   - Check what the logs say

2. **Look for:**
   - "Survey server running on port 3000" ✅ Good!
   - Any error messages
   - What port it's actually using

## Solution 5: Contact Namecheap (Fastest)

**This is a hosting configuration issue** - Namecheap support can fix it in minutes:

### What to Tell Them:

> "I have a Node.js application running on my Stellar hosting. The app is created and running in the Node.js Selector, but I'm getting 'Cannot GET /SurveyAILL6/' when accessing https://glowstone.red/SurveyAILL6/. 
>
> The app is located at: /home/shlinky/ServeyAILL6/
> Application startup file: server.js
> Desired URL: https://glowstone.red/SurveyAILL6/
>
> Can you help configure the proxy/rewrite rules so the application is accessible at this URL? Or let me know what the correct URL is to access my app?"

**Contact Support:**
- Live Chat: https://www.namecheap.com/support/live-chat/ (fastest!)
- They're available 24/7
- Usually resolve this in 5-10 minutes

## Quick Diagnostic

Run through this checklist:

1. **App Status:**
   - [ ] Shows "Running" in Node.js Selector?

2. **Files Present:**
   - [ ] index.html in /home/shlinky/ServeyAILL6/?
   - [ ] server.js in /home/shlinky/ServeyAILL6/?
   - [ ] package.json present?

3. **Dependencies Installed:**
   - [ ] NPM Install completed?
   - [ ] node_modules folder exists?

4. **Environment Variables:**
   - [ ] ADMIN_PASSWORD set?
   - [ ] PORT set to 3000?

5. **Try Alternative URLs:**
   - [ ] https://glowstone.red/ (root)
   - [ ] Click "OPEN" link in Node.js app
   - [ ] What URL does it show?

## Why This Happens

cPanel Node.js hosting typically works in one of these ways:

**Method A: Subdomain**
- App gets: `https://appname-username.glowstone.red/`
- Clean and isolated

**Method B: Root path**
- App serves at: `https://glowstone.red/`
- Replaces your main website

**Method C: Subdirectory with proxy**
- Needs .htaccess configuration
- Requires mod_proxy enabled
- Server admin might need to configure

Your hosting is using one of these - we just need to find which one!

## Recommended Next Steps

1. **Check Node.js app in cPanel** - look for the actual URL it's using
2. **Try accessing root**: https://glowstone.red/
3. **Contact Namecheap support** - they can configure the routing in 5 minutes

The app itself is working fine - this is purely a routing/proxy configuration issue on the hosting side.

