# Deployment Guide for glowstone.red/SurveyAIUIUC

## Quick Start (Local Development)

```bash
cd SurveyAIUIUC
chmod +x install.sh
./install.sh
./start.sh
```

Visit: http://localhost:8000

## Production Deployment on glowstone.red

### Step 1: Upload Files

Upload the entire `SurveyAIUIUC` folder to your server:

```bash
scp -r SurveyAIUIUC user@glowstone.red:/var/www/
```

Or use FTP/SFTP to upload to `/var/www/SurveyAIUIUC`

### Step 2: Install Dependencies

SSH into your server:

```bash
ssh user@glowstone.red
cd /var/www/SurveyAIUIUC
chmod +x install.sh
./install.sh
```

### Step 3: Configure Systemd Service

```bash
# Copy service file
sudo cp surveyai.service /etc/systemd/system/

# Edit if needed (change user, paths)
sudo nano /etc/systemd/system/surveyai.service

# Enable and start service
sudo systemctl daemon-reload
sudo systemctl enable surveyai
sudo systemctl start surveyai

# Check status
sudo systemctl status surveyai
```

### Step 4: Configure Nginx Reverse Proxy

Add to your Nginx configuration:

```nginx
server {
    listen 80;
    server_name glowstone.red;
    
    location /SurveyAIUIUC {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

Reload Nginx:
```bash
sudo nginx -t
sudo systemctl reload nginx
```

### Step 5: Test

Visit: https://glowstone.red/SurveyAIUIUC

## File Structure

```
SurveyAIUIUC/
├── main.py                 # FastAPI backend
├── requirements.txt        # Python dependencies
├── index.html             # Main survey page
├── 84Metashosan.html      # Admin panel
├── survey-data.json       # Data storage
├── install.sh             # Installation script
├── start.sh               # Start script (development)
├── surveyai.service       # Systemd service file
├── .gitignore            # Git ignore rules
├── README.md             # Documentation
└── DEPLOYMENT.md         # This file
```

## Configuration

### Change Admin Password

Edit `main.py`, line 22:

```python
# Generate hash for your password
import hashlib
new_password = "your_secure_password"
ADMIN_PASSWORD_HASH = hashlib.sha256(new_password.encode()).hexdigest()
```

### Change Port

Edit `main.py`, last line:
```python
uvicorn.run(app, host="0.0.0.0", port=8000)  # Change port here
```

Or in `surveyai.service`:
```ini
ExecStart=/usr/bin/uvicorn main:app --host 0.0.0.0 --port 8000
```

### Data Backup

The survey data is stored in `survey-data.json`. Back it up regularly:

```bash
cp survey-data.json survey-data.backup.json
```

## Troubleshooting

### Check Logs

```bash
# Service logs
sudo journalctl -u surveyai -f

# Or run manually to see errors
cd /var/www/SurveyAIUIUC
source venv/bin/activate
python main.py
```

### Permissions

Ensure proper permissions:
```bash
sudo chown -R www-data:www-data /var/www/SurveyAIUIUC
sudo chmod 755 /var/www/SurveyAIUIUC
```

### Port Already in Use

If port 8000 is busy, change it in `main.py` and `surveyai.service`

### Firewall

Ensure port 8000 is open (if accessing directly):
```bash
sudo ufw allow 8000
```

## Monitoring

### Check if Running

```bash
sudo systemctl status surveyai
curl http://localhost:8000/api/responses
```

### Restart Service

```bash
sudo systemctl restart surveyai
```

### View Logs

```bash
sudo journalctl -u surveyai -n 50
```

## Updates

To update the application:

```bash
cd /var/www/SurveyAIUIUC
sudo systemctl stop surveyai
git pull  # or upload new files
source venv/bin/activate
pip install -r requirements.txt
sudo systemctl start surveyai
```

## Security Notes

1. Change the default admin password
2. Use HTTPS (configure SSL in Nginx)
3. Regularly backup `survey-data.json`
4. Keep Python packages updated
5. Monitor access logs

## Support

For issues, check:
- Application logs: `sudo journalctl -u surveyai`
- Nginx logs: `/var/log/nginx/error.log`
- Python errors: Run `python main.py` manually

