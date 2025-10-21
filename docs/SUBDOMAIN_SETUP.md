# Setup survey.glowstone.red Subdomain

## Option 1: Create Subdomain in cPanel (Recommended)

### Step 1: Create Subdomain

1. **In cPanel, find "Subdomains"** (under Domains section)

2. **Create new subdomain:**
   ```
   Subdomain: survey
   Domain: glowstone.red
   Document Root: /home/shlinky/ServeyAILL6
   ```
   (Note: It may auto-fill document root - that's fine)

3. **Click "Create"**

### Step 2: Update Node.js App Configuration

1. **Go to "Setup Node.js App"**

2. **Edit your application:**
   ```
   Application URL: survey.glowstone.red (or just leave as /)
   Application root: ServeyAILL6
   ```

3. **Save and Restart**

### Step 3: Access Your Survey

- **HTTP**: http://survey.glowstone.red/
- **HTTPS**: https://survey.glowstone.red/

Both should work!

---

## Option 2: Update .htaccess (Alternative)

If you want to keep using the /SurveyAILL6 path on main domain:

### Updated .htaccess Content:

I've created `new_htaccess.txt` with the updated rules.

**Key changes:**
- Line 6-8: Allows survey.glowstone.red to bypass redirects
- Line 25-29: Proxies /SurveyAILL6 to your Node.js app

### To Apply:

1. **Go to File Manager** → `/home/shlinky/public_html/`
2. **Edit `.htaccess`**
3. **Replace content** with the content from `new_htaccess.txt`
4. **Save**
5. **Test:** https://glowstone.red/SurveyAILL6/

---

## Which Option to Choose?

**Use Option 1 (Subdomain)** if:
- ✅ You want a clean URL: survey.glowstone.red
- ✅ You want to allow both HTTP and HTTPS
- ✅ Easier to manage and maintain
- ✅ Better for sharing with survey participants

**Use Option 2 (.htaccess)** if:
- ✅ You want to keep: glowstone.red/SurveyAILL6
- ✅ You don't want to create a subdomain
- ✅ You're comfortable editing .htaccess

---

## Recommended: Option 1 (Subdomain)

**Why?**
- Clean, professional URL
- No .htaccess conflicts
- Works with both HTTP and HTTPS automatically
- Easier for cPanel to route

**Steps:**
1. cPanel → Subdomains
2. Create: `survey.glowstone.red` → points to `/home/shlinky/ServeyAILL6`
3. Node.js App → Update Application URL if needed
4. Restart app
5. Access: http://survey.glowstone.red/ or https://survey.glowstone.red/

---

## After Setup, Your URLs Will Be:

**Survey (Public):**
- http://survey.glowstone.red/
- https://survey.glowstone.red/

**Admin (Hidden):**
- http://survey.glowstone.red/84Metashosan
- https://survey.glowstone.red/84Metashosan

**GitHub Repo:**
- https://github.com/shlinkLFO/SurveyAI

---

## Need Help?

The subdomain approach is much simpler and recommended. If you run into issues, contact Namecheap support and say:

> "I need to create a subdomain survey.glowstone.red that points to my Node.js application at /home/shlinky/ServeyAILL6. Can you help me configure this?"

