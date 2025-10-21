# Deploy to glowstone.red - Manual Steps

## Server Details
- **Server**: glowstone.red (68.65.122.141)
- **Username**: shlinky
- **Path**: /var/www/ServeyAILL6

## Issue: SSH Port 22 Timed Out

The default SSH port (22) is timing out. Here are solutions:

### Solution 1: Check if SSH is on a Different Port

Try connecting with different ports:

```powershell
# Try common alternative SSH ports
ssh -p 2222 shlinky@glowstone.red
# or
ssh -p 2200 shlinky@glowstone.red
# or
ssh -p 22222 shlinky@glowstone.red
```

If one works, use that port for SCP:
```powershell
scp -P 2222 index.html 84Metashosan.html server.js package.json shlinky@glowstone.red:/var/www/ServeyAILL6/
```

### Solution 2: Check VPN/Network Access

You may need to:
1. Connect to a VPN if the server requires it
2. Whitelist your IP address on the server
3. Check with your server administrator

### Solution 3: Use a Control Panel (if available)

If glowstone.red has cPanel, Plesk, or another control panel:

1. Log into the control panel
2. Use the File Manager to upload files:
   - index.html
   - 84Metashosan.html
   - server.js
   - package.json
   - .gitignore

3. Use Terminal/SSH in the control panel to run:
```bash
cd /var/www/ServeyAILL6
npm install
echo "ADMIN_PASSWORD=YourSecurePassword123" > .env
echo "PORT=3000" >> .env
pm2 start server.js --name survey-ai
pm2 save
```

### Solution 4: Use SFTP Client (GUI)

Download and use **WinSCP** or **FileZilla**:

**WinSCP** (Recommended): https://winscp.net/

1. Download and install WinSCP
2. Create new connection:
   - Host: glowstone.red
   - User: shlinky
   - Try different ports if 22 doesn't work
3. Drag and drop these files to `/var/www/ServeyAILL6/`:
   - index.html
   - 84Metashosan.html
   - server.js
   - package.json
   - .gitignore

### Solution 5: Test SSH Connection First

Run this to see what's happening:

```powershell
# Test basic SSH connection
ssh -v shlinky@glowstone.red

# The -v flag will show verbose output and help identify the issue
```

## Files Ready to Upload

These files are ready in `C:\Users\mason\SurveyAI\`:
- ✅ index.html
- ✅ 84Metashosan.html
- ✅ server.js
- ✅ package.json
- ✅ .gitignore

## After Upload - Run on Server

Once files are uploaded, SSH into server and run:

```bash
cd /var/www/ServeyAILL6
npm install
echo "ADMIN_PASSWORD=YourSecurePassword123" > .env
echo "PORT=3000" >> .env
pm2 restart survey-ai || pm2 start server.js --name survey-ai
pm2 save
```

## Access Your Application

After deployment:
- **Survey**: https://glowstone.red/SurveyAI/ or https://glowstone.red/ServeyAILL6/
- **Admin**: https://glowstone.red/SurveyAI/84Metashosan or https://glowstone.red/ServeyAILL6/84Metashosan

## Next Steps

1. **Find out the correct SSH port** - Contact your server admin or check your hosting dashboard
2. **Try WinSCP** - Easier GUI for Windows users
3. **Check if VPN is needed** - Some servers require VPN access
4. **Verify you have SSH access** - You may need to set up SSH keys

## Need Help?

Common issues:
- **"Connection timed out"** = Firewall/wrong port/need VPN
- **"Permission denied"** = Wrong username or need SSH key
- **"Host key verification failed"** = Need to accept host key

Contact your hosting provider for:
- Correct SSH port number
- VPN requirements
- IP whitelist requirements
- SSH access credentials

