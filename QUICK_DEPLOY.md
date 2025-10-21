# Quick Deploy to glowstone.red/SurveyAI

## Before You Start

1. **Edit the deployment script** with your SSH username:
   - `deploy.php` - Change line 8: `$username = 'your_username';`
   - `deploy.sh` - Change line 9: `USERNAME="your_username"`
   - `deploy.bat` - Change line 7: `set USERNAME=your_username`

2. **Have SSH access** to glowstone.red with your username

## Deploy Now!

### Windows (PowerShell or CMD)

```powershell
# Option 1: Use PHP script
php deploy.php

# Option 2: Use batch script
deploy.bat

# Option 3: Manual command
scp index.html 84Metashosan.html server.js package.json your_username@glowstone.red:/var/www/SurveyAI/
```

### Linux/Mac

```bash
# Option 1: Use bash script
bash deploy.sh

# Option 2: Use PHP script
php deploy.php

# Option 3: Manual command
scp index.html 84Metashosan.html server.js package.json your_username@glowstone.red:/var/www/SurveyAI/
```

## After Upload

SSH into server and complete setup:

```bash
ssh your_username@glowstone.red
cd /var/www/SurveyAI
npm install
echo "ADMIN_PASSWORD=YourSecurePassword123" > .env
pm2 restart survey-ai || pm2 start server.js --name survey-ai
```

## Test Your Deployment

Visit these URLs:
- **Survey**: https://glowstone.red/SurveyAI/
- **Admin**: https://glowstone.red/SurveyAI/84Metashosan (password: what you set in .env)

## Quick Updates

### Just changed HTML?

```bash
# Upload HTML files only
scp index.html 84Metashosan.html your_username@glowstone.red:/var/www/SurveyAI/

# Restart
ssh your_username@glowstone.red "cd /var/www/SurveyAI && pm2 restart survey-ai"
```

### Changed backend code?

```bash
# Upload backend
scp server.js package.json your_username@glowstone.red:/var/www/SurveyAI/

# Install and restart
ssh your_username@glowstone.red "cd /var/www/SurveyAI && npm install && pm2 restart survey-ai"
```

## Troubleshooting

**"scp: command not found"** (Windows)
- Install OpenSSH: Settings > Apps > Optional Features > OpenSSH Client
- Or use [WinSCP](https://winscp.net/) GUI tool

**"Permission denied"**
```bash
ssh your_username@glowstone.red
sudo chown -R $USER:$USER /var/www/SurveyAI
```

**"PM2 not found"**
```bash
ssh your_username@glowstone.red
npm install -g pm2
```

**Site not loading**
- Check nginx/apache config (see DEPLOYMENT.md)
- Check PM2 status: `pm2 status`
- Check logs: `pm2 logs survey-ai`

## Need More Help?

See detailed documentation:
- `DEPLOY_INSTRUCTIONS.md` - Complete deployment guide
- `DEPLOYMENT.md` - Server configuration
- `README.md` - Full documentation

