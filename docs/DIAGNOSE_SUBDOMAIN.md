# Fix: Everything Redirects to /regenai

## The Problem

Your subdomain `survey.glowstone.red` is still being caught by the main domain's redirect rules.

## Diagnosis Steps

### Step 1: Check Subdomain Configuration

**In cPanel → Subdomains:**

Check these details for `survey.glowstone.red`:

✅ **Document Root should be:** `/home/shlinky/ServeyAILL6`  
❌ **NOT:** `/home/shlinky/public_html/survey`  
❌ **NOT:** `/home/shlinky/public_html/`

**If it's wrong:**
1. Click "Manage" or edit icon next to the subdomain
2. Change Document Root to: `/home/shlinky/ServeyAILL6`
3. Save

### Step 2: Check Node.js App Configuration

**In cPanel → Setup Node.js App:**

Check your app settings:
- **Application root:** Should be `ServeyAILL6`
- **Application URL:** Should be empty `/` or `survey.glowstone.red`
- **Status:** Should show "Running"

**If stopped:** Click "Start App"

### Step 3: Check for .htaccess in ServeyAILL6 folder

**In File Manager → `/home/shlinky/ServeyAILL6/`:**

Is there a `.htaccess` file in THIS folder?

**If YES:** Delete it or edit it to ONLY contain:
```apache
DirectoryIndex disabled
```

**If NO:** That's fine, Node.js doesn't need it.

## Solution A: Proper Subdomain Isolation

Create a SEPARATE .htaccess specifically for the subdomain:

**File: `/home/shlinky/ServeyAILL6/.htaccess`**

```apache
# Disable directory indexing
DirectoryIndex disabled

# Stop inheritance from parent .htaccess
RewriteEngine Off
```

This tells Apache to STOP processing any parent directory's .htaccess rules.

## Solution B: Update Main .htaccess More Specifically

**File: `/home/shlinky/public_html/.htaccess`**

Replace the entire file with this:

```apache
RewriteEngine On

# 1) FIRST: Exclude survey subdomain completely
RewriteCond %{HTTP_HOST} ^survey\.glowstone\.red$ [NC]
RewriteRule .* - [L]

# 2) Root -> /regenai/ (ONLY for main domain)
RewriteCond %{HTTP_HOST} ^glowstone\.red$ [NC]
RewriteCond %{REQUEST_URI} ^/?$
RewriteRule ^ https://glowstone.red/regenai/ [R=301,L,NE]

# 3) Drop www for all other paths (any scheme)
RewriteCond %{HTTP_HOST} ^www\.glowstone\.red$ [NC]
RewriteRule ^ https://glowstone.red%{REQUEST_URI} [R=301,L,NE]

# 4) Force HTTPS for main domain only
RewriteCond %{HTTP_HOST} ^glowstone\.red$ [NC]
RewriteCond %{HTTPS} off
RewriteRule ^ https://%{HTTP_HOST}%{REQUEST_URI} [R=301,L,NE]

# 5) HSTS
<IfModule mod_headers.c>
Header always set Strict-Transport-Security "max-age=86400"
</IfModule>
```

Key changes:
- Line 4-6: FIRST rule checks for survey subdomain and stops processing
- Line 9: Added condition to only apply root redirect to main domain
- Line 16: Added condition to only apply HTTPS redirect to main domain

## Solution C: Contact Namecheap Support (Fastest!)

This is a hosting configuration issue. Tell them:

> "I created a subdomain survey.glowstone.red pointing to /home/shlinky/ServeyAILL6 for my Node.js app, but all requests are being redirected to glowstone.red/regenai by the main domain's .htaccess rules. The Node.js app is running. Can you help configure the subdomain to be isolated from the main domain's rewrite rules?"

**Live Chat:** https://www.namecheap.com/support/live-chat/

They can fix this in 5 minutes.

## Quick Test

After making changes, test these URLs:

1. **http://survey.glowstone.red/** - Should show your survey
2. **https://survey.glowstone.red/** - Should show your survey
3. **http://glowstone.red/** - Should redirect to /regenai (as before)

## Most Likely Issue

The subdomain's Document Root is probably pointing to the wrong location. 

**Check this first:**
1. cPanel → Subdomains
2. Find survey.glowstone.red
3. Check Document Root
4. Should be: `/home/shlinky/ServeyAILL6`

If it says anything else, edit it to point there!

## Alternative: Use Different Subdomain Name

If all else fails, try creating a fresh subdomain with a different name:

- Try: `aisurvey.glowstone.red`
- Or: `research.glowstone.red`
- Or: `msba.glowstone.red`

Point it to `/home/shlinky/ServeyAILL6` and test if it works better.

