# Correct .htaccess File Locations

## Understanding the Directory Structure

You have TWO different .htaccess files in different locations:

1. **`/home/shlinky/.htaccess`** - Home directory (the one you showed me)
   - Controls root domain behavior
   - Handles redirects for main site

2. **`/home/shlinky/public_html/.htaccess`** - Web root
   - This is where web content is served from
   - This is where you need to add proxy rules

3. **`/home/shlinky/ServeyAILL6/`** - Your Node.js app
   - Outside of public_html
   - Needs to be proxied TO from public_html

## Solution 1: Create Subdomain (Still Recommended!)

Since your app is in `/home/shlinky/ServeyAILL6/` (outside public_html), the subdomain approach is actually PERFECT:

### Steps:
1. **cPanel → Subdomains**
2. **Create:**
   ```
   Subdomain: survey
   Domain: glowstone.red
   Document Root: /home/shlinky/ServeyAILL6
   ```
3. This creates: `survey.glowstone.red` → points directly to your app folder
4. No .htaccess needed!
5. Access: **http://survey.glowstone.red/**

**This bypasses all the main domain redirects automatically!**

## Solution 2: Add Proxy Rules to public_html/.htaccess

If you want to use the path `/SurveyAILL6` on the main domain:

### File: `/home/shlinky/public_html/.htaccess`

Add these lines at the BOTTOM (after all existing rules):

```apache
# Proxy SurveyAILL6 to Node.js app
<IfModule mod_rewrite.c>
    # Don't apply other redirects to this path
    RewriteCond %{REQUEST_URI} ^/SurveyAILL6 [NC]
    RewriteRule ^SurveyAILL6/?(.*)$ http://127.0.0.1:3000/$1 [P,L]
</IfModule>
```

### Important Notes:
- Add this to `/home/shlinky/public_html/.htaccess` (NOT /home/shlinky/.htaccess)
- Place at the END of the file (after all other rules)
- This proxies requests to your Node.js app running on port 3000

## Understanding Your Current Setup

Your `/home/shlinky/.htaccess` rules:
- Line 6-7: Redirect root to /regenai/
- Line 10-11: Remove www
- Line 14-15: Force HTTPS

These apply to the MAIN site, not to subdirectories/subdomains.

**Your Node.js app is in a separate directory**, so:
- Option A: Use subdomain (survey.glowstone.red) - bypasses all main site rules ✅
- Option B: Proxy from public_html/.htaccess to your app

## Recommended: Use Subdomain

**Why?**
1. Your app is already OUTSIDE public_html
2. Subdomain bypasses all main domain redirects
3. No .htaccess conflicts
4. Both HTTP and HTTPS work automatically
5. Clean URL: survey.glowstone.red

**Steps:**
1. cPanel → Subdomains
2. Subdomain: `survey`, Domain: `glowstone.red`
3. Document Root: `/home/shlinky/ServeyAILL6`
4. Create
5. Node.js App → Verify Application URL
6. Access: http://survey.glowstone.red/

## If You Want /SurveyAILL6 Path Instead

**Edit this file:** `/home/shlinky/public_html/.htaccess`

**Add at the bottom:**
```apache
# Proxy to Node.js app
RewriteCond %{REQUEST_URI} ^/SurveyAILL6 [NC]
RewriteRule ^SurveyAILL6/?(.*)$ http://127.0.0.1:3000/$1 [P,L]
```

**Then access:** https://glowstone.red/SurveyAILL6/

---

## Quick Decision Guide

**Choose Subdomain if:**
- ✅ You want survey.glowstone.red
- ✅ You want the simplest setup
- ✅ You want to avoid .htaccess complexity

**Choose /SurveyAILL6 path if:**
- ✅ You want glowstone.red/SurveyAILL6
- ✅ You're comfortable editing .htaccess in public_html
- ✅ You don't mind adding proxy rules

**I strongly recommend the subdomain approach!**

