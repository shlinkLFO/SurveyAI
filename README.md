# AI Confidence Survey - Deployment Guide

## Overview
This is a web application for collecting AI confidence survey data with a Node.js backend. All responses are stored centrally and aggregated across all users.

## Features
- 6-question confidence survey with slider inputs (-1 to +1 scale)
- Centralized data storage across all users
- Data export to CSV
- Correlation heatmap visualization
- Response distribution charts
- Admin panel for data management
- End users cannot delete data

## Files
- `index.html` - Main survey application (public)
- `84Metashosan.html` - Hidden admin dashboard for managing data
- `server.js` - Node.js/Express backend API
- `package.json` - Node.js dependencies
- `survey-data.json` - Data storage (created automatically)

## Quick Start

### 1. Install Dependencies

```bash
npm install
```

### 2. Configure Admin Password (Optional)

Create a `.env` file or set environment variable:
```bash
# Option 1: Create .env file
echo "ADMIN_PASSWORD=your_secure_password" > .env

# Option 2: Use default password (admin123)
```

### 3. Start the Server

```bash
npm start
```

The server will start on `http://localhost:3000`

### 4. Access the Application

- **Survey**: `http://localhost:3000/`
- **Admin Panel**: `http://localhost:3000/84Metashosan.html`

## Deployment to glowstone.red/ServeyAILL6

### Prerequisites
- Node.js 14+ installed on server
- Nginx or Apache for reverse proxy
- PM2 for process management (recommended)

### Step 1: Upload Files to Server

```bash
# Option A: Using SCP
scp -r * user@glowstone.red:/var/www/ServeyAILL6/

# Option B: Using Git
ssh user@glowstone.red
cd /var/www
git clone <your-repo-url> ServeyAILL6
cd ServeyAILL6
```

### Step 2: Install Dependencies on Server

```bash
ssh user@glowstone.red
cd /var/www/ServeyAILL6
npm install
```

### Step 3: Set Admin Password

```bash
# Create .env file with secure password
echo "ADMIN_PASSWORD=YourSecurePassword123" > .env
echo "PORT=3000" >> .env
```

### Step 4: Start the Application with PM2

```bash
# Install PM2 globally (if not installed)
npm install -g pm2

# Start the application
pm2 start server.js --name survey-ai

# Save PM2 configuration
pm2 save

# Set PM2 to start on boot
pm2 startup
```

### Step 5: Configure Nginx Reverse Proxy

Create nginx configuration at `/etc/nginx/sites-available/survey`:

```nginx
server {
    listen 80;
    server_name glowstone.red;

    location /ServeyAILL6 {
        proxy_pass http://localhost:3000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_cache_bypass $http_upgrade;
        
        # Handle trailing slashes
        rewrite ^/ServeyAILL6/?(.*)$ /$1 break;
    }
}
```

Enable the site and restart nginx:
```bash
sudo ln -s /etc/nginx/sites-available/survey /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### Step 6: Enable HTTPS (Recommended)

```bash
# Install certbot
sudo apt install certbot python3-certbot-nginx

# Get SSL certificate
sudo certbot --nginx -d glowstone.red
```

### Alternative: Using Apache

If using Apache instead of Nginx:

```apache
<VirtualHost *:80>
    ServerName glowstone.red
    
    ProxyPreserveHost On
    ProxyPass /ServeyAILL6 http://localhost:3000
    ProxyPassReverse /ServeyAILL6 http://localhost:3000
</VirtualHost>
```

Enable required modules and restart:
```bash
sudo a2enmod proxy
sudo a2enmod proxy_http
sudo systemctl restart apache2
```

## Verification

After deployment:

1. **Survey Interface**: `https://glowstone.red/SurveyAI/`
2. **Admin Panel**: `https://glowstone.red/SurveyAI/84Metashosan` (hidden, no link from main page)

You should see:
- Purple-themed survey interface
- Locked data tabs until survey is submitted
- After submission: access to dataset, correlation heatmap, and distributions
- Response counter showing total from all users
- No "Clear Data" button for end users
- Hidden admin page with export and delete capabilities

## Data Management

- **Storage**: All data stored centrally in `survey-data.json` on server
- **Aggregation**: All users' responses are combined in one dataset
- **Export**: End users can download CSV of all responses
- **Admin**: Only admin can clear data via admin panel
- **Backup**: Recommended to backup `survey-data.json` regularly

## Admin Panel

Access: `https://glowstone.red/SurveyAI/84Metashosan` (hidden page)

Default password: `admin123` (change via environment variable)

Features:
- View total response count
- See recent responses
- Export all data to CSV
- Clear all data (with double confirmation)
- Refresh dashboard
- No link from main survey page (security through obscurity)

**Important**: 
1. Change the default admin password before deploying!
2. The admin page path (84Metashosan) is not linked anywhere on the public site
3. Only share this URL with authorized administrators

## Managing the Application

```bash
# View logs
pm2 logs survey-ai

# Restart application
pm2 restart survey-ai

# Stop application
pm2 stop survey-ai

# View status
pm2 status

# Monitor
pm2 monit
```

## Backup Data

```bash
# Backup survey data
cp /var/www/ServeyAILL6/survey-data.json ~/backups/survey-data-$(date +%Y%m%d).json

# Automate with cron (daily at 2 AM)
0 2 * * * cp /var/www/ServeyAILL6/survey-data.json ~/backups/survey-data-$(date +\%Y\%m\%d).json
```

## Technical Details

**Frontend:**
- React 18 (CDN)
- Recharts for visualizations
- Tailwind CSS
- Babel Standalone for JSX

**Backend:**
- Node.js + Express
- JSON file storage
- RESTful API
- CORS enabled

**API Endpoints:**
- `POST /api/responses` - Submit survey response
- `GET /api/responses` - Get all responses
- `GET /api/count` - Get response count
- `POST /api/admin/clear` - Clear all data (admin only)
- `POST /api/admin/export` - Export data (admin only)

## Security Considerations

1. **Change admin password**: Set `ADMIN_PASSWORD` environment variable
2. **Use HTTPS**: Enable SSL with certbot
3. **Firewall**: Ensure port 3000 is not exposed publicly
4. **Backup**: Regularly backup `survey-data.json`
5. **Updates**: Keep Node.js and dependencies updated

## Troubleshooting

**Server won't start:**
```bash
# Check if port is in use
sudo lsof -i :3000

# Check PM2 logs
pm2 logs survey-ai
```

**Can't submit responses:**
- Check server is running: `pm2 status`
- Check nginx/apache proxy configuration
- Check browser console for errors

**Admin panel won't authenticate:**
- Verify `ADMIN_PASSWORD` is set correctly
- Check server logs for authentication attempts

## Browser Requirements

- Modern browser with ES6+ support
- JavaScript enabled
- Fetch API support
- Recommended: Chrome, Firefox, Safari, Edge (latest versions)

