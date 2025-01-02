# Location Profile Calculator
## Project Description
The Location Profile Calculator is a local HTML-based tool designed to compute the optimized orientation for arranging cases within a specified storage location. By taking into account the actual location dimensions (rather than just volume), it provides realistic and efficient solutions for bin and storage usage.

### Note: 
The actual calculator package is excluded from this repository for confidentiality reasons. To explore the functionality of this calculator, open src/compute_plot.html in your web browser.

### Key Features:
- Optimized case orientation computation.
- Real-time 3D visualization of the arrangement.

## Features
Pre-stored Data Integration: Users can select warehouse numbers, location IDs, or SKU IDs to retrieve dimensions automatically, eliminating manual input.
Optimized Computation: Iteratively evaluates all orientations, including sub-orientations, to maximize space utilization.
3D Visualization: Provides an interactive, clear representation of the optimized arrangement.
Data Security: Fully local execution, requiring no internet connection to protect confidential data.

## How It Works
- Select: Warehouse Number
- Input: Location Number and SKU ID 
- Computation:
    - Calculates the optimal orientation to maximize the number of cases that fit.
    - Iterates over all sub-orientations for efficient space utilization.
- Output:
    - Optimized orientation and total number of cases.
    - SKU name (in Chinese).
    - Total case count, including sub-orientations.
    - Location dimensions (adjusted for an 80% fill rate) and case dimensions.
    - A 3D plot to visualize the arrangement.

## Installation
Clone or download the repository.

Use the following command to clone the project repository:
    *git clone git@github.com:shuting-weee/location_profile.git*

## How to Use
- Open the *html* file in your default web browser.
- Select the warehouse number from the dropdown list.
- Input the location number (e.g., B0102-2-2).
- Input the SKU ID (e.g., 237).
- Click Submit to compute results.
- View the optimized arrangement and 3D visualization.

## Limitations
- Many SKUs lack valid case dimensions in the database (e.g., dimensions listed as 0,0,0), affecting the accuracy of the optimization.
- Sub-orientations may not always be feasible or common in practice.

## Future Enhancements
- Data Quality Improvements: Enhance the quality of SKU case data by resolving invalid entries.
- 3D Interactivity: Add rotation and zoom functionalities for a more dynamic 3D visualization.

## Acknowledgments
Three.js: Utilized for rendering the 3D visualization.

# Contact
For any questions, please email shuting.he@sayweee.com.
