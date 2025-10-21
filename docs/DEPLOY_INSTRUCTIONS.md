# How to Deploy SurveyAI to glowstone.red

## Quick Deploy

### Option 1: Using the PHP Script

```bash
php deploy.php
```

**Before running:**
1. Open `deploy.php` and change `$username` to your SSH username
2. Run the script
3. Follow the interactive prompts

### Option 2: Using the Bash Script

```bash
bash deploy.sh
```

**Before running:**
1. Open `deploy.sh` and change `USERNAME` to your SSH username
2. Make the script executable: `chmod +x deploy.sh`
3. Run the script
4. Follow the interactive prompts

### Option 3: Manual Deployment (Windows PowerShell)

```powershell
# 1. Upload files via SCP
scp index.html 84Metashosan.html server.js package.json your_username@glowstone.red:/var/www/SurveyAI/

# 2. SSH into server
ssh your_username@glowstone.red

# 3. On the server, run:
cd /var/www/SurveyAI
npm install
echo "ADMIN_PASSWORD=YourSecurePassword123" > .env
echo "PORT=3000" >> .env
pm2 restart survey-ai || pm2 start server.js --name survey-ai
```

## What Gets Deployed

- `index.html` - Main survey interface
- `84Metashosan.html` - Hidden admin panel
- `server.js` - Backend API server
- `package.json` - Dependencies
- `.gitignore` - Git ignore rules

## After Deployment

### 1. Verify it's running

Visit:
- Survey: https://glowstone.red/SurveyAI/
- Admin: https://glowstone.red/SurveyAI/84Metashosan

### 2. Check server status

```bash
ssh your_username@glowstone.red
pm2 status
pm2 logs survey-ai
```

### 3. Update admin password

```bash
ssh your_username@glowstone.red
cd /var/www/SurveyAI
nano .env
# Change ADMIN_PASSWORD value
pm2 restart survey-ai
```

## Quick Updates

### Update HTML only (no server restart needed)

```bash
scp index.html 84Metashosan.html your_username@glowstone.red:/var/www/SurveyAI/
ssh your_username@glowstone.red
cd /var/www/SurveyAI
pm2 restart survey-ai
```

### Update backend (requires npm install)

```bash
scp server.js package.json your_username@glowstone.red:/var/www/SurveyAI/
ssh your_username@glowstone.red
cd /var/www/SurveyAI
npm install
pm2 restart survey-ai
```

## Troubleshooting

### Can't connect via SSH

```bash
# Test SSH connection
ssh your_username@glowstone.red

# If that fails, check:
# - Username is correct
# - Server is reachable: ping glowstone.red
# - SSH service is running on server
```

### SCP command not found (Windows)

Install OpenSSH:
1. Settings > Apps > Optional Features
2. Add OpenSSH Client
3. Restart terminal

Or use WinSCP GUI: https://winscp.net/

### PM2 not found on server

```bash
ssh your_username@glowstone.red
npm install -g pm2
```

### Server not accessible at URL

Check nginx/apache proxy configuration (see DEPLOYMENT.md)

### Permission denied errors

```bash
ssh your_username@glowstone.red
sudo chown -R $USER:$USER /var/www/SurveyAI
```

## Rollback

If something goes wrong, restore from backup:

```bash
ssh your_username@glowstone.red
cd /var/www/SurveyAI
cp ~/backups/survey-data-YYYYMMDD.json survey-data.json
pm2 restart survey-ai
```

## Security Notes

1. **Change default password** - The default `admin123` password must be changed
2. **Keep 84Metashosan secret** - Don't share the admin URL publicly
3. **Backup data regularly** - Set up automated backups of `survey-data.json`
4. **Use HTTPS** - Ensure SSL is configured (see DEPLOYMENT.md)
5. **Keep dependencies updated** - Run `npm update` periodically

## Need Help?

Check these files for more information:
- `START.md` - Local testing instructions
- `DEPLOYMENT.md` - Detailed server setup
- `README.md` - Complete documentation

