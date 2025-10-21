# Debug Survey App Not Working

## Immediate Actions

### Step 1: Check the Application Logs

**MOST IMPORTANT - Do this first!**

1. In the Node.js App interface, look for **"Show Logs"** or **"View Logs"** button
2. Click it
3. Look at the most recent entries

**What to look for:**
- ✅ "Survey server running on port 3000" = Good!
- ❌ "Error: Cannot find module 'express'" = npm install didn't work
- ❌ "EADDRINUSE" = Port already in use
- ❌ ".env" errors = Environment file issue
- ❌ Any other error messages

**TELL ME WHAT THE LOGS SAY!** This is the key to fixing it.

### Step 2: Verify App Status

Is it actually running?
- Should show "Running" in GREEN
- Not "Stopped" in RED
- Not "Error" in ORANGE

### Step 3: Check stderr.log File

In File Manager:
1. Go to `/home/shlinky/ServeyAILL6/`
2. Look for `stderr.log` file
3. Click to view it
4. Copy any error messages

## Common Issues & Fixes

### Issue 1: Port Mismatch

**Check in File Manager:**
- `/home/shlinky/ServeyAILL6/.env`
- Should contain: `PORT=3000`

If file doesn't exist or is wrong, create/fix it with:
```
ADMIN_PASSWORD=bub2step-433
PORT=3000
```

### Issue 2: cPanel Using Different Port

Sometimes cPanel assigns a different port automatically.

**Fix:**
1. In Node.js app, look for what port it's actually using
2. Might show "Port: 3001" or similar
3. If different, update .env file to match

### Issue 3: Application Entry Point Wrong

**Verify in Node.js App:**
- Application startup file: `server.js` (not index.js, not app.js)

### Issue 4: Document Root vs Application Root Mismatch

**Check two places:**

1. **Subdomains** → survey.glowstone.red → Document Root: `/home/shlinky/ServeyAILL6`
2. **Node.js App** → Application root: `ServeyAILL6`

They must match!

### Issue 5: .env File Not Being Read

cPanel might not read .env files properly. Try adding Environment Variables in the Node.js App interface instead:

1. Click "Add Variable"
2. Add:
   - Name: `ADMIN_PASSWORD`, Value: `bub2step-433`
   - Name: `PORT`, Value: `3000`
3. Save and restart

### Issue 6: Node Version Issue

Try changing Node.js version:
- Currently: 18.20.8
- Try: 20.x or 16.x
- Save and restart

## Alternative Test: Direct Port Access

Try accessing the port directly (if firewall allows):
- http://glowstone.red:3000/

This tests if the Node app itself is working, bypassing the subdomain routing.

## Check App Is Actually Serving

SSH or cPanel Terminal:
```bash
cd /home/shlinky/ServeyAILL6
curl http://localhost:3000/
```

Should return HTML, not connection refused.

## Nuclear Option: Fresh Start

If nothing works, let's try a different approach:

### Option A: Use Main Domain Path Instead

Change Node.js app configuration:
- Application URL: `/survey` (use a path instead of subdomain)
- Then access: https://glowstone.red/survey/

### Option B: Use Passenger

Some hosts use Passenger instead of direct Node.js:
1. Create `passenger_wsgi.py` (for Python)
2. Or configure Passenger for Node.js

### Option C: Deploy on Different Service

If Namecheap's Node.js isn't working:
- Vercel (5 minutes, free): vercel.com
- Railway (free): railway.app  
- Render (free): render.com

I can help you deploy there instead!

## What I Need From You

**Please check and tell me:**

1. **What do the logs say?** (Most important!)
2. What is the app status? (Running/Stopped/Error)
3. Does stderr.log file exist? What's in it?
4. Can you access: http://survey.glowstone.red/ vs https://survey.glowstone.red/
5. Does it show blank page or error page?

The logs will tell us exactly what's wrong!

