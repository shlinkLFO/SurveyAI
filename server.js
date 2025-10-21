require('dotenv').config();
const express = require('express');
const fs = require('fs').promises;
const path = require('path');
const cors = require('cors');

const app = express();
const PORT = process.env.PORT || 3000;
const DATA_FILE = path.join(__dirname, 'survey-data.json');

// Middleware
app.use(cors());
app.use(express.json());
app.use(express.static(__dirname));

// Admin password (in production, use environment variable)
const ADMIN_PASSWORD = process.env.ADMIN_PASSWORD || 'admin123';

console.log('Server configuration:');
console.log('- Port:', PORT);
console.log('- Data file:', DATA_FILE);
console.log('- Admin password:', ADMIN_PASSWORD === 'admin123' ? 'Using default (CHANGE THIS!)' : 'Custom password set');

// Initialize data file if it doesn't exist
async function initDataFile() {
    try {
        await fs.access(DATA_FILE);
    } catch {
        await fs.writeFile(DATA_FILE, JSON.stringify({ responses: [] }));
    }
}

// Read all responses
async function readData() {
    const data = await fs.readFile(DATA_FILE, 'utf8');
    return JSON.parse(data);
}

// Write responses
async function writeData(data) {
    await fs.writeFile(DATA_FILE, JSON.stringify(data, null, 2));
}

// API Routes

// Submit a survey response
app.post('/api/responses', async (req, res) => {
    try {
        const response = req.body;
        
        // Validate response
        if (!response.timestamp) {
            return res.status(400).json({ error: 'Invalid response data' });
        }

        const data = await readData();
        data.responses.push(response);
        await writeData(data);

        res.json({ success: true, count: data.responses.length });
    } catch (error) {
        console.error('Error saving response:', error);
        res.status(500).json({ error: 'Failed to save response' });
    }
});

// Get all responses (for displaying stats)
app.get('/api/responses', async (req, res) => {
    try {
        const data = await readData();
        res.json(data.responses);
    } catch (error) {
        console.error('Error reading responses:', error);
        res.status(500).json({ error: 'Failed to read responses' });
    }
});

// Get response count
app.get('/api/count', async (req, res) => {
    try {
        const data = await readData();
        res.json({ count: data.responses.length });
    } catch (error) {
        console.error('Error reading count:', error);
        res.status(500).json({ error: 'Failed to read count' });
    }
});

// Admin endpoint to clear data (password protected)
app.post('/api/admin/clear', async (req, res) => {
    try {
        const { password } = req.body;
        
        if (password !== ADMIN_PASSWORD) {
            return res.status(403).json({ error: 'Unauthorized' });
        }

        await writeData({ responses: [] });
        res.json({ success: true, message: 'All data cleared' });
    } catch (error) {
        console.error('Error clearing data:', error);
        res.status(500).json({ error: 'Failed to clear data' });
    }
});

// Admin endpoint to export all data (password protected)
app.post('/api/admin/export', async (req, res) => {
    try {
        const { password } = req.body;
        
        if (password !== ADMIN_PASSWORD) {
            return res.status(403).json({ error: 'Unauthorized' });
        }

        const data = await readData();
        res.json(data.responses);
    } catch (error) {
        console.error('Error exporting data:', error);
        res.status(500).json({ error: 'Failed to export data' });
    }
});

// Serve index.html at root
app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'index.html'));
});

// Serve admin page
app.get('/84Metashosan', (req, res) => {
    res.sendFile(path.join(__dirname, '84Metashosan.html'));
});

// Start server
async function start() {
    await initDataFile();
    app.listen(PORT, () => {
        console.log(`Survey server running on port ${PORT}`);
        console.log(`Access the survey at: http://localhost:${PORT}`);
        console.log(`Admin panel at: http://localhost:${PORT}/84Metashosan`);
    });
}

start().catch(console.error);

