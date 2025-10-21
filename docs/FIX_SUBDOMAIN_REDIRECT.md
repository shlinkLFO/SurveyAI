# Fix survey.glowstone.red Redirecting to /regenai

## Problem
survey.glowstone.red is being caught by rewrite rules and redirected to glowstone.red/regenai

## Solution: Update /home/shlinky/public_html/.htaccess

You need to EXCLUDE survey.glowstone.red from the redirect rules.

### Find This File:
`/home/shlinky/public_html/.htaccess`

### Add This at the VERY TOP (after RewriteEngine On):

```apache
RewriteEngine On

# IMPORTANT: Skip all redirects for survey subdomain
RewriteCond %{HTTP_HOST} ^survey\.glowstone\.red$ [NC]
RewriteRule ^ - [L]

# ... rest of your existing rules below ...
```

### Full Updated .htaccess Should Look Like:

```apache
# Ensure module on
RewriteEngine On

# EXCLUDE survey subdomain from all redirects
RewriteCond %{HTTP_HOST} ^survey\.glowstone\.red$ [NC]
RewriteRule ^ - [L]

# 1) Root -> /regenai/ (one hop, preserve querystring)
RewriteCond %{REQUEST_URI} ^/?$ 
RewriteRule ^ https://glowstone.red/regenai/ [R=301,L,NE]

# 2) Drop www for all other paths (any scheme)
RewriteCond %{HTTP_HOST} ^www\.glowstone\.red$ [NC]
RewriteRule ^ https://glowstone.red%{REQUEST_URI} [R=301,L,NE]

# 3) Force HTTPS for anything else that's still on http
RewriteCond %{HTTPS} off
RewriteRule ^ https://%{HTTP_HOST}%{REQUEST_URI} [R=301,L,NE]

# 4) HSTS (Stage 1)
<IfModule mod_headers.c>
Header always set Strict-Transport-Security "max-age=86400"
</IfModule>
```

## Key Change:

Lines 5-7 tell Apache:
- "If the request is for survey.glowstone.red"
- "Don't apply ANY other rewrite rules"
- "Just pass it through as-is"

The `[L]` flag means "Last rule" - stop processing other rules for this request.

## Steps to Apply:

1. **Go to cPanel File Manager**
2. **Navigate to:** `/home/shlinky/public_html/`
3. **Find and edit:** `.htaccess`
4. **Add the exclusion rule** at the top (right after RewriteEngine On)
5. **Save**
6. **Test:** http://survey.glowstone.red/

Should now work without redirecting!

## Alternative: Check Subdomain's Document Root

If the above doesn't work, check where the subdomain is pointing:

1. **cPanel → Subdomains**
2. **Find:** survey.glowstone.red
3. **Check Document Root:** Should be `/home/shlinky/ServeyAILL6`

If it's pointing to `/home/shlinky/public_html/survey/` or similar, that's wrong!

**Edit the subdomain and change Document Root to:**
```
/home/shlinky/ServeyAILL6
```

## Why This Happened

When you created the subdomain, it's still being processed by the main domain's .htaccess rules before reaching the subdomain's document root. By adding the exclusion at the top, we tell Apache to skip all those redirects for the survey subdomain.

