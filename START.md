# Quick Start - Local Testing

## Test the application locally before deploying

### 1. Install Dependencies

```bash
npm install
```

### 2. Start the Server

```bash
npm start
```

You should see:
```
Server configuration:
- Port: 3000
- Data file: C:\Users\mason\SurveyAI\survey-data.json
- Admin password: Using default (CHANGE THIS!)
Survey server running on port 3000
Access the survey at: http://localhost:3000
```

### 3. Test the Survey

Open your browser to:
- **Survey**: http://localhost:3000/
- **Admin Panel**: http://localhost:3000/84Metashosan.html

### 4. Test Functionality

1. Notice that Data, Heatmap, and Distributions tabs are locked (🔒)
2. Fill out the survey and click "Submit Response"
3. After submission, you're automatically taken to the "Data" tab
4. The locked tabs should now be accessible
5. View the dataset, correlation heatmap, and distributions
6. Try exporting the data as CSV (no delete option for users)
7. Visit hidden admin panel at http://localhost:3000/84Metashosan.html
8. Login with password: **admin123**
9. View admin dashboard with export and delete capabilities

### 5. Verify Data Persistence

1. Submit a response
2. Close the browser
3. Restart the server
4. Open browser again - your data should still be there
5. Check that `survey-data.json` file was created

### Success!

If everything works, you're ready to deploy to glowstone.red!

See **DEPLOYMENT.md** for server deployment instructions.

