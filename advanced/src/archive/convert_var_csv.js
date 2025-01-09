const fs = require('fs'); 

// Convert JSON array to CSV
function jsonToCsv(data) {
    const headers = Object.keys(data[0]).join(","); // Extract column headers
    const rows = data.map(row => Object.values(row).join(",")); // Extract rows
    return [headers, ...rows].join("\n"); // Combine headers and rows
}

// Save CSV to file
function saveCsv(data, filename = "locData.csv") {
    const csvContent = jsonToCsv(data);
    fs.writeFileSync(filename, csvContent);
    console.log(`CSV file saved as ${filename}`);
}

// Generate and save CSV
saveCsv(locData);
