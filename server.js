const express = require('express');
const path = require('path');

const app = express();
const port = 3000;

// Serve static files like images, styles, and JS
app.use(express.static(path.join(__dirname, 'public')));

// Serve the main HTML file
app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'index.html'));
});

// Handle the search functionality
app.get('/search', (req, res) => {
    const query = req.query.search;
    // You can add logic here to search from a database or an API
    if (query) {
        res.send(`<h1>Search Results for "${query}"</h1>`);
    } else {
        res.send('<h1>No search query provided</h1>');
    }
});

// Start the server
app.listen(port, () => {
    console.log(`Server running at http://localhost:${port}`);
});
