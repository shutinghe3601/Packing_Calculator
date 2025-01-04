const fs = require('fs'); 
// Data array
var caseData = [
    {'sku_id': '22', 'name': 'blahblah', 'case_length': 0.0, 'case_width': 0.0, 'case_height': 0.0}, 
    {'sku_id': '14', 'name': 'blahblah', 'case_length': 11.0, 'case_width': 4.0, 'case_height': 13.0}, 
    {'sku_id': '23', 'name': 'blahblahblahblah', 'case_length': 10.0, 'case_width': 19.2, 'case_height': 12.6}, 
    {'sku_id': '37', 'name': 'blahblahblahblah', 'case_length': 11.7, 'case_width': 17.0, 'case_height': 8.5}, 
    {'sku_id': '60', 'name': 'blahblah', 'case_length': 23.1, 'case_width': 15.8, 'case_height': 4.6}
];

var locData = [
    {'warehouse_number': 101, 'location_number': 'B03', 'width_inch': 32.0, 'height_inch': 20.0, 'depth_inch': 36, 'inventory_cases':2}, 
    {'warehouse_number': 101, 'location_number': 'B07', 'width_inch': 32.0, 'height_inch': 24.0, 'depth_inch': 38.4, 'inventory_cases':3}, 
    {'warehouse_number': 101, 'location_number': 'B08', 'width_inch': 40.0, 'height_inch': 20.0, 'depth_inch': 36, 'inventory_cases':6}, 
    {'warehouse_number': 101, 'location_number': 'B18', 'width_inch': 32.0, 'height_inch': 20.0, 'depth_inch': 38.4, 'inventory_cases':1}, 
    {'warehouse_number': 101, 'location_number': 'B20', 'width_inch': 40.0, 'height_inch': 24.0, 'depth_inch': 36, 'inventory_cases':9}
];

// Convert JSON array to CSV
function jsonToCsv(data) {
    const headers = Object.keys(data[0]).join(","); // Extract column headers
    const rows = data.map(row => Object.values(row).join(",")); // Extract rows
    return [headers, ...rows].join("\n"); // Combine headers and rows
}

// Save CSV to file
function saveCsv(data, filename = "output.csv") {
    const csvContent = jsonToCsv(data);
    fs.writeFileSync(filename, csvContent);
    console.log(`CSV file saved as ${filename}`);
}

// Generate and save CSV
saveCsv(locData);
