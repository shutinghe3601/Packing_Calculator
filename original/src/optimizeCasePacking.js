function optimizeCasePacking(warehouseNumber, locationNumber, skuId, locData, caseData) {
    const loc = locData.find(
        (l) => l.warehouse_number.toString() === warehouseNumber && l.location_number.toString() === locationNumber
    );
    if (!loc) throw new Error('Location not found for the given warehouse and location number.');

    const locDims = [loc.width_inch, loc.depth_inch, loc.height_inch];

    const item = caseData.find((i) => i.sku_id.toString() === skuId);
    if (!item) throw new Error('Item not found for the given SKU ID.');

    const caseDims = [item.case_width, item.case_length, item.case_height];

    const orientationList = generatePermutations(caseDims);
    let totalCases = 0;
    const packingOrientations = [];

    while (true) {
        let bestOrientation = null;
        let maxCases = 0;
        let remainingLocDims = null;

        for (const orientation of orientationList) {
            const cases = calculateFitCount(locDims, orientation);
            if (cases > maxCases) {
                maxCases = cases;
                bestOrientation = orientation;
                remainingLocDims = calculateRemainingSpace(locDims, orientation);
            }
        }

        if (maxCases === 0) break;

        totalCases += maxCases;
        packingOrientations.push({ orientation: bestOrientation, count: maxCases });
        locDims[0] = remainingLocDims[0];
        locDims[1] = remainingLocDims[1];
        locDims[2] = remainingLocDims[2];
    }

    return { totalCases, packingOrientations };
}

function calculateRemainingSpace(locDims, orientation) {
    const [W, D, H] = locDims;
    const [a, b, c] = orientation;
    return [W % a, D % b, H % c];
}

function calculateFitCount(locDims, orientation) {
    const [W, D, H] = locDims;
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