# Deploy SurveyAI to glowstone.red - Web-Based Deployment

## No SSH Access - Alternative Deployment Methods

Since glowstone.red only has SSL (HTTPS) and no SSH, here are your deployment options:

## Option 1: FTP/SFTP Upload (Recommended)

### Using FileZilla (Free)

1. **Download FileZilla**: https://filezilla-project.org/

2. **Connect to your server:**
   - Host: `ftp.glowstone.red` or `glowstone.red`
   - Protocol: Try SFTP first, then FTP if that fails
   - Port: 21 (FTP) or 990 (FTPS) or 22 (SFTP)
   - Username: `shlinky`
   - Password: (your hosting password)

3. **Navigate to:** `/var/www/ServeyAILL6/` or `/public_html/ServeyAILL6/`

4. **Upload these files:**
   - index.html
   - 84Metashosan.html
   - server.js
   - package.json
   - .gitignore

### Using WinSCP (Free)

1. **Download WinSCP**: https://winscp.net/

2. **Connect:**
   - File protocol: FTP or SFTP
   - Host name: `glowstone.red`
   - User name: `shlinky`
   - Password: (your password)

3. **Upload files** to `/var/www/ServeyAILL6/`

## Option 2: cPanel / Control Panel

### If you have cPanel:

1. **Log into cPanel**: https://glowstone.red:2083 or https://glowstone.red/cpanel

2. **File Manager:**
   - Navigate to `/public_html/ServeyAILL6/` or `/var/www/ServeyAILL6/`
   - Click "Upload"
   - Select and upload all 5 files

3. **Terminal (if available in cPanel):**
   ```bash
   cd /var/www/ServeyAILL6
   npm install
   echo "ADMIN_PASSWORD=YourSecurePassword123" > .env
   pm2 start server.js --name survey-ai
   ```

### If you have Plesk:

1. **Log into Plesk**: https://glowstone.red:8443

2. **File Manager:**
   - Go to your domain
   - Navigate to the correct directory
   - Upload files

3. **Node.js Application Setup:**
   - Go to "Node.js" section
   - Set Document Root: `/var/www/ServeyAILL6`
   - Application Startup File: `server.js`
   - Add environment variable: `ADMIN_PASSWORD=YourSecurePassword`

## Option 3: Git Deployment (If Available)

If your host supports Git deployment:

1. **Create a Git repository** (GitHub, GitLab, Bitbucket)

2. **Push your code:**
   ```powershell
   cd C:\Users\mason\SurveyAI
   git init
   git add index.html 84Metashosan.html server.js package.json .gitignore
   git commit -m "Initial commit"
   git remote add origin https://github.com/yourusername/surveyai.git
   git push -u origin main
   ```

3. **In your hosting control panel:**
   - Find "Git Version Control" or "Git Deployment"
   - Connect your repository
   - Deploy to `/var/www/ServeyAILL6/`

## Option 4: Hosting Provider's Method

Contact your hosting provider (glowstone.red support) and ask:

1. **"How do I deploy a Node.js application?"**
   - They may have a specific process
   - May need to enable Node.js hosting first

2. **"Do you support Node.js apps?"**
   - If not, you may need to:
     - Upgrade hosting plan
     - Use a different hosting service (Heroku, Vercel, DigitalOcean)

3. **"What's the correct path for web applications?"**
   - Might be `/public_html/` or `/var/www/` or `/home/shlinky/`

## Option 5: Use a Node.js-Friendly Host

If glowstone.red doesn't support Node.js applications, consider these alternatives:

### Free/Easy Options:
- **Vercel** (free): https://vercel.com
- **Netlify** (free): https://netlify.com
- **Railway** (free tier): https://railway.app
- **Render** (free tier): https://render.com

### Quick Deploy to Vercel (5 minutes):

```powershell
# Install Vercel CLI
npm install -g vercel

# Deploy
cd C:\Users\mason\SurveyAI
vercel

# Follow prompts, your site will be live at: https://your-project.vercel.app
```

## What You Need to Know

### Questions to Ask Your Host:

1. **Does glowstone.red support Node.js applications?**
   - If yes: What's the deployment process?
   - If no: Can they enable it or recommend alternatives?

2. **What's my FTP/SFTP login information?**
   - Host
   - Port
   - Username (probably `shlinky`)
   - Password

3. **Can I run custom applications with npm?**
   - Node.js apps need npm to install dependencies
   - Need ability to run `node server.js`

4. **Is PM2 or another process manager available?**
   - To keep the app running 24/7

## Files Ready to Upload

Located in `C:\Users\mason\SurveyAI\`:
- ✅ **index.html** (38 KB) - Main survey page
- ✅ **84Metashosan.html** (12 KB) - Admin panel
- ✅ **server.js** (4 KB) - Backend server
- ✅ **package.json** (1 KB) - Dependencies
- ✅ **.gitignore** (1 KB) - Git ignore rules

## After Upload - What's Needed on Server

Your hosting needs to run:
```bash
cd /var/www/ServeyAILL6
npm install  # Installs express, cors, dotenv
node server.js  # Starts the server
```

Or with PM2 (process manager):
```bash
pm2 start server.js --name survey-ai
```

## Static HTML Version (Backup Plan)

If Node.js isn't available, I can convert this to a static HTML version that:
- Works without Node.js
- Saves data to browser localStorage only
- No admin panel needed
- Just upload and works immediately

Let me know if you need this version!

## Quick Test - Check Your Hosting Type

Run this to check what's available:
```powershell
# Check if you have FTP access
Test-NetConnection glowstone.red -Port 21

# Check if you have FTPS access  
Test-NetConnection glowstone.red -Port 990
```

## Next Step: Contact Your Host

**Email/Support Ticket to send:**

> Hi,
> 
> I have a Node.js application I need to deploy to my account (username: shlinky).
> 
> Questions:
> 1. Does my hosting plan support Node.js applications?
> 2. What's the best way to upload files? (FTP, cPanel, Git?)
> 3. How do I run a Node.js server on port 3000?
> 4. Is PM2 available for process management?
> 5. What's the correct directory path for web apps?
> 
> The app files are: index.html, server.js, package.json
> 
> Thank you!

## I Can Help With:

1. **Converting to static HTML** (no server needed)
2. **Deploying to alternative hosts** (Vercel, Netlify, etc.)
3. **Setting up on VPS** if you have one
4. **Creating Docker container** for deployment

Let me know what you'd like to do!

