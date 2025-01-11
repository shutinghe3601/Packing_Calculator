# Location Profile Calculator

## Project Description
**Packing Calculator** is an HTML-based tool for determining the optimal orientation to arrange cases within a given storage location. Unlike traditional volume-based methods, it considers actual dimensions, existing inventory, and assumes items are unstackable, ensuring compact and efficient arrangements. Its local setup also prevents data leakage.

This tool showcases demo usage and algorithm logic, supports further development. All data in this repository is synthetic and generated for demonstration purposes.

## Features
- **Pre-Stored Data Integration**: 
  - Retrieve dimensions automatically by selecting warehouse numbers, location IDs, or SKU IDs, eliminating manual data entry.
- **Optimized Computation**: 
  - Evaluates all possible orientations, including sub-orientations, to maximize space utilization.
- **3D Visualization**: 
  - Visual representation of the optimized arrangement.
- **Data Security**: 
  - Fully local execution ensures confidentiality, as no internet connection is required.

## How It Works
1. **Select**: Choose the Warehouse Number, Location Number and SKU ID.
2. **Computation**:
   - Divide remaining space into multiple sub-spaces.
   - Iterate over all possible orientations to fit items into each sub-space.
   - Identify the arrangement yielding the maximum number of cases.
3. **Output**:
   - Optimized orientation and total case count.
   - SKU name and total case count.
   - Location dimensions (adjusted for an 80% fill rate) and case dimensions.
   - A 3D visualization of the arrangement, showcasing:
     - Inventory blocks of existing SKUs.
     - Main orientation and sub-orientations for the new SKU.

## Installation
Clone or download the repository using the following command:

```bash
git clone git@github.com:shutinghe3601/Packing_Calculator.git 
```

## How to Use
1. Open the advanced/calculator.html file in your default web browser.
2. Select the warehouse number from the dropdown menu.
3. Select the location number from the dropdown menu.
4. Select the SKU ID from the dropdown menu.
5. Click Submit to compute the packing solution.
6. Review the optimized arrangement and 3D visualization.

## Limitations 
- **Unstackable Assumption**: Existing SKUs are treated as unstackable.
- **Data Gaps**: Some SKUs lack valid case dimensions in the database (e.g., dimensions listed as 0,0,0), affecting optimization accuracy.

## Future Enhancements
- **Data Quality Improvements**: Address invalid SKU case data for better accuracy.
- **Stackable Solutions**: Develop packing solutions for stackable cases.

## Acknowledgments
**Three.js**: Utilized for rendering the 3D visualization.

## License
This project is licensed under the [MIT License](LICENSE.txt).  
You are free to use, modify, and distribute this software as long as you include the original license notice.








