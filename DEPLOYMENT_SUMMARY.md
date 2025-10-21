# SurveyAI - Ready to Deploy! 🚀

## What You Have Now

### Application Features ✅
- **Survey interface** with 6 AI confidence questions
- **Locked tabs** until user completes survey (Data, Heatmap, Distributions)
- **After submission**: Full access to:
  - Dataset view (read-only for users)
  - Correlation Heatmap (OLS regression coefficients)
  - Distribution charts (variance analysis)
- **Hidden admin panel** at `/84Metashosan` with:
  - Export all data
  - Delete all data
  - View statistics
  - Password protected
- **Centralized database** - All users' responses aggregated

### Files Ready for Deployment
- `index.html` - Main survey application
- `84Metashosan.html` - Admin panel (hidden)
- `server.js` - Node.js backend
- `package.json` - Dependencies
- Deployment scripts (see below)

## Deploy to https://glowstone.red/SurveyAI/

### Fastest Method (Windows PowerShell)

**Step 1:** Edit your SSH username in one of the deployment scripts:
- Open `deploy.php` or `deploy.bat` or `deploy.sh`
- Change `your_username` to your actual SSH username

**Step 2:** Run the deployment:

```powershell
# Using PHP (recommended)
php deploy.php

# Or using batch file
deploy.bat

# Or manual
scp index.html 84Metashosan.html server.js package.json yourusername@glowstone.red:/var/www/SurveyAI/
```

**Step 3:** Complete server setup:

```bash
ssh yourusername@glowstone.red
cd /var/www/SurveyAI
npm install
echo "ADMIN_PASSWORD=YourSecurePassword123" > .env
pm2 restart survey-ai || pm2 start server.js --name survey-ai
```

**Step 4:** Test it!
- Survey: https://glowstone.red/SurveyAI/
- Admin: https://glowstone.red/SurveyAI/84Metashosan

## Deployment Scripts Available

| Script | Platform | Command |
|--------|----------|---------|
| `deploy.php` | All (requires PHP) | `php deploy.php` |
| `deploy.sh` | Linux/Mac | `bash deploy.sh` |
| `deploy.bat` | Windows | `deploy.bat` |
| Manual | All | See `QUICK_DEPLOY.md` |

## Key Features Implementation

### ✅ User Experience
- Users complete survey first
- Tabs show 🔒 until submission
- After submission: automatic redirect to Data tab
- Can view dataset, correlations, and distributions
- Can export CSV (no delete option)
- Data persists across sessions

### ✅ Admin Access
- Hidden page: `/84Metashosan` (not linked anywhere)
- Password protected (default: `admin123` - CHANGE THIS!)
- Can export all data
- Can delete all data (double confirmation required)
- View response statistics

### ✅ Security
- End users cannot delete data
- Admin panel requires password
- No navigation link to admin page
- Data stored server-side (not in browser)
- All responses aggregated centrally

## URLs After Deployment

| Page | URL | Access |
|------|-----|--------|
| Survey | https://glowstone.red/SurveyAI/ | Public |
| Data View | https://glowstone.red/SurveyAI/ (after submission) | Public after survey |
| Heatmap | https://glowstone.red/SurveyAI/ (Heatmap tab) | Public after survey |
| Distributions | https://glowstone.red/SurveyAI/ (Distributions tab) | Public after survey |
| Admin Panel | https://glowstone.red/SurveyAI/84Metashosan | Password protected |

## Important Security Notes

1. **Change the default admin password immediately!**
   ```bash
   ssh yourusername@glowstone.red
   nano /var/www/SurveyAI/.env
   # Change ADMIN_PASSWORD=admin123 to something secure
   pm2 restart survey-ai
   ```

2. **Keep the admin URL secret** - Don't share `/84Metashosan` publicly

3. **Backup your data regularly**
   ```bash
   scp yourusername@glowstone.red:/var/www/SurveyAI/survey-data.json ./backup-$(date +%Y%m%d).json
   ```

## Quick Reference

### Check if it's running
```bash
ssh yourusername@glowstone.red
pm2 status
pm2 logs survey-ai
```

### View current data count
```bash
ssh yourusername@glowstone.red
cat /var/www/SurveyAI/survey-data.json
```

### Restart server
```bash
ssh yourusername@glowstone.red
pm2 restart survey-ai
```

### Update HTML files only (quick)
```bash
scp index.html 84Metashosan.html yourusername@glowstone.red:/var/www/SurveyAI/
ssh yourusername@glowstone.red "pm2 restart survey-ai"
```

## Documentation Files

- **QUICK_DEPLOY.md** - Fastest way to deploy (start here!)
- **DEPLOY_INSTRUCTIONS.md** - Complete deployment guide
- **DEPLOYMENT.md** - Detailed server setup
- **README.md** - Full documentation
- **START.md** - Local testing instructions

## Next Steps

1. ✅ Review deployment scripts
2. ✅ Edit SSH username in script
3. ✅ Run deployment script
4. ✅ Complete server setup
5. ✅ Change admin password
6. ✅ Test the survey
7. ✅ Share survey URL with participants

## Need Help?

Check the documentation files above, or common issues:

- **Can't SSH**: Check username and server access
- **SCP not found**: Install OpenSSH (Windows) or use WinSCP
- **PM2 not found**: `npm install -g pm2`
- **Site not loading**: Check nginx/apache config (see DEPLOYMENT.md)
- **Can't access admin**: Make sure you're using the correct password from `.env`

---

**You're all set!** The application is ready to deploy. Just run one of the deployment scripts and follow the prompts.

