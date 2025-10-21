# Quick Deployment Guide

## For glowstone.red/SurveyAI

### 1. First Time Setup

```bash
# SSH into your server
ssh user@glowstone.red

# Create directory
sudo mkdir -p /var/www/SurveyAI
sudo chown $USER:$USER /var/www/SurveyAI

# Exit and upload files from local machine
exit

# From your local machine (in the SurveyAI directory)
scp index.html 84Metashosan.html server.js package.json README.md user@glowstone.red:/var/www/SurveyAI/

# SSH back in
ssh user@glowstone.red
cd /var/www/SurveyAI

# Install dependencies
npm install

# Set admin password
echo "ADMIN_PASSWORD=YourSecurePassword123" > .env
echo "PORT=3000" >> .env

# Start with PM2
pm2 start server.js --name survey-ai
pm2 save
pm2 startup
```

### 2. Configure Reverse Proxy

#### For Nginx:

```bash
# Create nginx config
sudo nano /etc/nginx/sites-available/survey

# Paste this configuration:
```

```nginx
server {
    listen 80;
    server_name glowstone.red;

    location /SurveyAI {
        proxy_pass http://localhost:3000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
        
        rewrite ^/SurveyAI/?(.*)$ /$1 break;
    }
}
```

```bash
# Enable and restart
sudo ln -s /etc/nginx/sites-available/survey /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

#### For Apache:

```bash
# Enable proxy modules
sudo a2enmod proxy
sudo a2enmod proxy_http

# Edit Apache config
sudo nano /etc/apache2/sites-available/000-default.conf

# Add inside <VirtualHost>:
    ProxyPass /SurveyAI http://localhost:3000
    ProxyPassReverse /SurveyAI http://localhost:3000

# Restart Apache
sudo systemctl restart apache2
```

### 3. Enable HTTPS (Recommended)

```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d glowstone.red
```

### 4. Test

Visit:
- Survey: https://glowstone.red/SurveyAI/
- Admin: https://glowstone.red/SurveyAI/84Metashosan (hidden page, no link on main site)

### 5. Update Application Later

```bash
ssh user@glowstone.red
cd /var/www/SurveyAI

# Upload new files (from local machine)
scp index.html 84Metashosan.html user@glowstone.red:/var/www/SurveyAI/

# Restart (on server)
pm2 restart survey-ai
```

## Useful Commands

```bash
# Check status
pm2 status

# View logs
pm2 logs survey-ai

# Monitor
pm2 monit

# Restart
pm2 restart survey-ai

# Stop
pm2 stop survey-ai

# Backup data
cp survey-data.json ~/backups/survey-data-$(date +%Y%m%d).json
```

## Default Admin Password

**admin123** - CHANGE THIS in the .env file!

## Troubleshooting

**Can't access the site:**
- Check PM2 status: `pm2 status`
- Check nginx/apache is running: `sudo systemctl status nginx`
- Check firewall: `sudo ufw status`

**Responses not saving:**
- Check server logs: `pm2 logs survey-ai`
- Check file permissions: `ls -la survey-data.json`
- Test API directly: `curl http://localhost:3000/api/count`

**Admin panel not working:**
- Verify password in .env file
- Check browser console for errors
- Restart server: `pm2 restart survey-ai`

