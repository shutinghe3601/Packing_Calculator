function calculateRemainingSpace(locDims, orientation) {
    const [W, L, H] = locDims;
    const [a, b, c] = orientation;
    return [W % a, L % b, H % c];
}

// Function to calculate how many cases fit into the location
function calculateFitCount(locDims, orientation) {
    const [W, L, H] = locDims;
    const [a, b, c] = orientation;
    return Math.floor(W / a) * Math.floor(L / b) * Math.floor(H / c);
}

// Function to determine existing parameters
function existingParameter(locDims, orientation) {
    const [W, L, H] = locDims;
    const [a, b, c] = orientation;
    const nCaseStack = Math.floor(H / c);
    const nCaseRow = Math.floor(W / a) * nCaseStack;
    return [nCaseStack, nCaseRow];
}

// Main function to compute space for new cases
function spaceForNew(warehouseNumber, locationNumber) {
    const loc = locData.find(
        (l) => l.warehouse_number.toString() === warehouseNumber && l.location_number.toString() === locationNumber
    );
    // const loc = locData.find(
    //     (l) => l.warehouse_number === parseInt(warehouseNumber) && l.location_number === locationNumber
    // );
    if (!loc) throw new Error('there are something wrong with loc')

    const locDims = [loc.width_inch, loc.depth_inch, loc.height_inch]

    const locQty = loc.loc_qty
    if (!locQty) throw new Error('there are something wrong with loc_QTY')

    const loc_inv = caseData.find(
        (i) => i.sku_id === loc.loc_inventory.toString()
    );
    
    const locCaseDims = [loc_inv.case_width, loc_inv.case_length, loc_inv.case_height];

    if (!loc_inv) {
        locCaseDims = [0, 0, 0]
    }

    const orientations = permute(locCaseDims);
    let maxCases = 0;
    let bestOrientation = null;

    orientations.forEach(orientation => {
        const cases = calculateFitCount(locDims, orientation);
        if (cases > maxCases) {
            maxCases = cases;
            bestOrientation = orientation;
        }
    });

    const [nCaseStack, nCaseRow] = existingParameter(locDims, bestOrientation);
    let occupiedW = 0, occupiedL = 0, occupiedW2 = 0, occupiedL2 = 0;
    let complication = false;

    if (locQty <= nCaseStack) {
        occupiedW = bestOrientation[0];
        occupiedL = bestOrientation[1];
    } else if (locQty <= nCaseRow) {
        occupiedW = bestOrientation[0] * (nCaseRow / nCaseStack);
        occupiedL = bestOrientation[1];
    } else {
        complication = true;
        const nRows = Math.floor(locQty / nCaseRow);
        const remainder = locQty % nCaseRow;
        occupiedW = bestOrientation[0] * (nCaseRow / nCaseStack);
        occupiedL = bestOrientation[1] * nRows;

        if (remainder > 0) {
            const nStacks = Math.floor(remainder / nCaseStack);
            const leftover = remainder % nCaseStack;
            occupiedW2 = bestOrientation[0] * (leftover > 0 ? nStacks + 1 : nStacks);
            occupiedL2 = bestOrientation[1];
        }
    }

    const majorSpace = complication ? [locDims[0], locDims[1] - (occupiedL + occupiedL2), locDims[2]] : [locDims[0], locDims[1] - occupiedL, locDims[2]];
    const subSpaces = complication ? [
        [locDims[0] - occupiedW2, occupiedL2, locDims[2]],
        [locDims[0] - occupiedW, occupiedL, locDims[2]]
    ] : [
        [locDims[0] - occupiedW, occupiedL, locDims[2]]
    ];
    
    return {majorSpace, subSpaces, occupiedW, occupiedL, occupiedW2, occupiedL2, complication, locDims };
}

// Helper function to generate permutations
function permute(arr) {
    if (arr.length <= 1) return [arr];
    const result = [];
    arr.forEach((val, i) => {
        const rest = arr.slice(0, i).concat(arr.slice(i + 1));
        permute(rest).forEach(permutation => {
            result.push([val].concat(permutation));
        });
    });
    return result;
}

// Comprehensive function to compute all necessary results
function comprehensive(warehouseNumber, locationNumber, skuId) {
    const spaceData = spaceForNew(warehouseNumber, locationNumber);
    const { majorSpace, subSpaces, occupiedW, occupiedL, occupiedW2, occupiedL2, complication, locDims: dims } = spaceData;

    const item = caseData.find((i) => i.sku_id.toString() === skuId);
    if (!item) throw new Error('Item not found for the given SKU ID.');

    const newCaseDims = [item.case_width, item.case_length, item.case_height];

    const orientations = permute(newCaseDims);
    let optCases = 0;
    let optSolution = { orient: [], n_case: [] };

    orientations.forEach(orientation => {
        const majorFit = calculateFitCount(majorSpace, orientation);
        const remainingSpace = calculateRemainingSpace(majorSpace, orientation);

        const subFits = subSpaces.map(space => {
            const effectiveSpace = [space[0], space[1] + remainingSpace[1], space[2]];
            let bestFit = 0;
            let bestSubOrientation = null;

            orientations.forEach(subOrientation => {
                const fit = calculateFitCount(effectiveSpace, subOrientation);
                if (fit > bestFit) {
                    bestFit = fit;
                    bestSubOrientation = subOrientation;
                }
            });

            return { cases: bestFit, orientation: bestSubOrientation };
        });

        const totalCases = majorFit + subFits.reduce((sum, subFit) => sum + subFit.cases, 0);
        if (totalCases > optCases) {
            optCases = totalCases;
            optSolution.orient = [orientation, subFits.map(sub => sub.orientation || null)];
            optSolution.n_case = [majorFit, subFits.map(sub => sub.cases || 0)];
        }
    });

    return {optCases, optSolution, occupiedW, occupiedL, occupiedW2, occupiedL2, dims, complication, newCaseDims};
}