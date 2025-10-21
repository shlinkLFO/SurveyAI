# AI Confidence Survey

A web application for collecting AI confidence survey data with centralized storage and analytics.

## Features

- 6-question confidence survey with slider inputs (-1 to +1 scale)
- Centralized data storage across all users
- Locked tabs until survey completion
- After submission: access to dataset, correlation heatmap, and distributions
- Hidden admin panel for data management
- Password-protected admin access

## Live Application

- **Survey**: https://survey.glowstone.red/
- **Admin**: https://survey.glowstone.red/84Metashosan (hidden, password required)
- **GitHub**: https://github.com/shlinkLFO/SurveyAI

## Files

### Application Files
- `index.html` - Main survey interface
- `84Metashosan.html` - Hidden admin panel
- `server.js` - Node.js/Express backend API
- `package.json` - Dependencies
- `.gitignore` - Git ignore rules

### Documentation
See `/docs` folder for detailed deployment and troubleshooting guides.

## Quick Start (Local Development)

```bash
# Install dependencies
npm install

# Create .env file
echo "ADMIN_PASSWORD=your_password" > .env
echo "PORT=3000" >> .env

# Start server
npm start

# Access at: http://localhost:3000
```

## Deployment

Deployed on Namecheap cPanel with Node.js hosting.

**Requirements:**
- Node.js 16.x or higher
- Express, CORS, dotenv packages

**Quick Deploy:**
1. Upload all files to `/home/shlinky/ServeyAILL6/`
2. Create Node.js app in cPanel
3. Set environment variables: `ADMIN_PASSWORD`, `PORT`
4. Run NPM Install
5. Start app

See `/docs/NAMECHEAP_DEPLOY.md` for detailed instructions.

## Technology Stack

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

## API Endpoints

- `POST /api/responses` - Submit survey response
- `GET /api/responses` - Get all responses
- `GET /api/count` - Get response count
- `POST /api/admin/clear` - Clear all data (admin only)
- `POST /api/admin/export` - Export data (admin only)

## Security

- Admin panel hidden (not linked from main page)
- Password-protected admin endpoints
- Users cannot delete data
- All responses stored server-side

## Data Storage

Survey responses stored in `survey-data.json` on server (not in repository).

**Backup:** Regularly backup this file from the server.

## License

MIT

## Research

UIUC MS Business Analytics Research Project
