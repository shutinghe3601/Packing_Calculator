const fs = require('fs'); 

function readJsonFile(filePath) {
    // Read and parse JSON file, handling multiple JSON objects if necessary
    const fileContent = fs.readFileSync(filePath, 'utf8');
    try {
        return JSON.parse(fileContent);
    } catch (e) {
        // If JSON.parse fails, try splitting the file content by lines and parsing each line
        return fileContent
            .split('\n')
            .filter((line) => line.trim()) // Ignore empty lines
            .map((line) => JSON.parse(line));
    }
}

function calculateRemainingSpace(binDims, orientation) {
    const [W, D, H] = binDims;
    const [a, b, c] = orientation;
    const subW = W % a;
    const subD = D % b;
    const subH = H % c;
    return [subW, subD, subH];
}

function calculateFitCount(binDims, orientation) {
    const [W, D, H] = binDims;
    const [a, b, c] = orientation;
    return Math.floor(W / a) * Math.floor(D / b) * Math.floor(H / c);
}

function generatePermutations(array) {
    if (array.length === 0) return [[]];
    const result = [];
    for (let i = 0; i < array.length; i++) {
        const rest = array.slice(0, i).concat(array.slice(i + 1));
        const permutations = generatePermutations(rest);
        for (const perm of permutations) {
            result.push([array[i], ...perm]);
        }
    }
    return result;
}

function optimizeCasePacking(warehouseNumber, locationNumber, skuId) {
    const bin = binData.find(
        (b) => b.warehouse_number === warehouseNumber && b.location_number === locationNumber
    );
    if (!bin) throw new Error('Bin not found for the given warehouse and location number.');

    const binDims = [bin.width_inch, bin.depth_inch, bin.height_inch];

    const item = itemData.find((i) => i.sku_id === skuId);
    if (!item) throw new Error('Item not found for the given SKU ID.');

    const caseDims = [item.case_width, item.case_length, item.case_height];

    const orientationList = generatePermutations(caseDims);
    let totalCases = 0;
    const packingOrientations = [];

    while (true) {
        let bestOrientation = null;
        let maxCases = 0;
        let remainingBinDims = null;

        for (const orientation of orientationList) {
            const cases = calculateFitCount(binDims, orientation);
            if (cases > maxCases) {
                maxCases = cases;
                bestOrientation = orientation;
                remainingBinDims = calculateRemainingSpace(binDims, orientation);
            }
        }

        if (maxCases === 0) break;

        totalCases += maxCases;
        packingOrientations.push({ orientation: bestOrientation, count: maxCases });
        binDims[0] = remainingBinDims[0];
        binDims[1] = remainingBinDims[1];
        binDims[2] = remainingBinDims[2];
    }

    return { totalCases, packingOrientations };
}

module.exports = { optimizeCasePacking };


// function optimizeCasePacking(binData, itemData, warehouseNumber, locationNumber, skuId) {
//     const bin = binData.find(
//         (b) => b.warehouse_number.toString() === warehouseNumber && b.location_number.toString() === locationNumber
//     );
//     if (!bin) throw new Error('Bin not found for the given warehouse and location number.');

//     const binDims = [bin.width_inch, bin.depth_inch, bin.height_inch];

//     const item = itemData.find((i) => i.sku_id.toString() === skuId);
//     if (!item) throw new Error('Item not found for the given SKU ID.');

//     const caseDims = [item.case_width, item.case_length, item.case_height];

//     const orientationList = generatePermutations(caseDims);
//     let totalCases = 0;
//     const packingOrientations = [];

//     while (true) {
//         let bestOrientation = null;
//         let maxCases = 0;
//         let remainingBinDims = null;

//         for (const orientation of orientationList) {
//             const cases = calculateFitCount(binDims, orientation);
//             if (cases > maxCases) {
//                 maxCases = cases;
//                 bestOrientation = orientation;
//                 remainingBinDims = calculateRemainingSpace(binDims, orientation);
//             }
//         }

//         if (maxCases === 0) break;

//         totalCases += maxCases;
//         packingOrientations.push({ orientation: bestOrientation, count: maxCases });
//         binDims[0] = remainingBinDims[0];
//         binDims[1] = remainingBinDims[1];
//         binDims[2] = remainingBinDims[2];
//     }

//     return { totalCases, packingOrientations };
// }


// // Example usage
// const warehouseNumber = 101;
// const locationNumber = 'C2';
// const skuId = "765";

// try {
//     const result = optimizeCasePacking(warehouseNumber, locationNumber, skuId);
//     console.log('Optimized Total Cases:', result.totalCases);
//     console.log('Packing Orientations:', result.packingOrientations);
// } catch (error) {
//     console.error('Error:', error.message);
// }
