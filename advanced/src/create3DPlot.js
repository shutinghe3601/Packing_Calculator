function create3DPlot(computation_result) {
    const plotContainer = document.getElementById('plotContainer');

    const locDims = computation_result.dims;
    const occupiedW = computation_result.occupiedW;
    const occupiedL = computation_result.occupiedL;
    const occupiedW2 = computation_result.occupiedW2;
    const occupiedL2 = computation_result.occupiedL2;
    const complication = computation_result.complication; 
    const optSolution = computation_result.optSolution;

    // Clear any previous canvas
    while (plotContainer.firstChild) {
        plotContainer.removeChild(plotContainer.firstChild);
    }

    // Create scene, camera, and renderer
    const scene = new THREE.Scene();
    // const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
    const camera = new THREE.PerspectiveCamera(75, 2, 0.1, 1000);
    const renderer = new THREE.WebGLRenderer({ antialias: true });
    // renderer.setSize(window.innerWidth, window.innerHeight);
    renderer.setSize(600, 300); // Fixed canvas size
    renderer.setClearColor(0xf5f5dc); // Beige background
    plotContainer.appendChild(renderer.domElement);

    // Add cubic 3D space (bounding box)
    const [locWidth, locDepth, locHeight] = locDims;
    const spaceGeometry = new THREE.BoxGeometry(locWidth, locHeight, locDepth);
    const spaceMaterial = new THREE.MeshBasicMaterial({
        color: 0x87ceeb, // Light blue
        wireframe: true,
        transparent: true,
        opacity: 0.5,
    });
    const spaceMesh = new THREE.Mesh(spaceGeometry, spaceMaterial);
    spaceMesh.position.set(locWidth / 2, locHeight / 2, locDepth / 2);
    scene.add(spaceMesh);

    // Function to add a box to the scene
    function addBox(x, y, z, w, h, d, color, opacity = 0.7) {
        const geometry = new THREE.BoxGeometry(w, h, d);
        const material = new THREE.MeshBasicMaterial({ color, transparent: true, opacity });
        const mesh = new THREE.Mesh(geometry, material);
        mesh.position.set(x + w / 2, z + h / 2, y + d / 2);

        // Add edges for better visibility
        const edges = new THREE.EdgesGeometry(geometry);
        const edgeMaterial = new THREE.LineBasicMaterial({ color: 0x000000 });
        const edgeLines = new THREE.LineSegments(edges, edgeMaterial);
        mesh.add(edgeLines);

        scene.add(mesh);
    }

    // Add existing SKU block (unstackable)
    addBox(0, 0, 0, occupiedW, locHeight, occupiedL, 0xff0000,0.7); // Red box

    // Add main orientation block
    const [w1, l1, h1] = optSolution.orient[0];
    if (complication) {
        addBox(0, occupiedL + occupiedL2, 0, w1, h1, l1, 0x00ff00); // Green box attached to the stack
    } else {
        addBox(0, occupiedL, 0, w1, h1, l1, 0x00ff00); // Green box
    }

    // Add sub-orientation block if present
    if (optSolution.orient[1][0] != null) {
        const [w2, l2, h2] = optSolution.orient[1][0];

        if (optSolution.orient[1] != [null] && complication) {
            addBox(occupiedW2, occupiedL2, 0, w2, h2, l2, 0x0000ff); // Blue box
        } else if (optSolution.orient[1] != [null] ) { // && optSolution.orient[1].length === 1
            addBox(occupiedW, 0, 0, w2, h2, l2, 0x0000ff); // Blue box attached to the first row
        }
    }

    // Add complication block if needed
    if (complication) {
        addBox(0, occupiedL, 0, occupiedW2, locHeight, occupiedL2, 0xff0000, 0.7); // Additional red block

        if (optSolution.orient[1].length > 1 && optSolution.orient[1][1] != null) {
            const [w3, l3, h3] = optSolution.orient[1][1];
            addBox(occupiedW, 0, 0, w3, h3, l3, 0xffc0cb); // Another blue block
        }
    }

    // Add 'Front' label
    const loader = new THREE.FontLoader();
    loader.load('https://threejs.org/examples/fonts/droid/droid_sans_regular.typeface.json', function (font) {
        const textGeometry = new THREE.TextGeometry('Width (Front)', {
            font: font,
            size: locHeight * 0.1, // Scale size relative to bounding box
            height: 0.5,
        });
        const textMaterial = new THREE.MeshBasicMaterial({ color: 0x7a7a7a }); // Grey color
        const textMesh = new THREE.Mesh(textGeometry, textMaterial);

        // Position the text at the front-center of the box
        textMesh.position.set(locWidth / 3, 0, locDepth + locHeight * 0.3); 
        textMesh.rotation.x = -Math.PI / 2; // Rotate 90 degrees clockwise along the X-axis

        scene.add(textMesh);
    }); 

    // Position and angle the camera
    camera.position.set(locWidth * 1.5, locHeight * 2.5, locDepth * 1.5);
    camera.lookAt(locWidth / 2, locHeight / 2, locDepth / 2);

    // Animation loop to render the scene
    function animate() {
        requestAnimationFrame(animate);
        renderer.render(scene, camera);
    }
    animate();
}

function createLegend(plotContainer) {
    // Create a container for the legend
    const legendContainer = document.createElement('div');
    legendContainer.style.textAlign = 'center';
    legendContainer.style.marginBottom = '10px';

    // Define legend items
    const legendItems = [
        { color: 'green', text: 'Main Orientation' },
        { color: 'blue', text: 'Sub-Orientation 1' },
        { color: 'pink', text: 'Sub-Orientation 2' },
        { color: 'red', text: 'Inventory Blocks' },
    ];

    // Generate legend rows
    legendItems.forEach((item) => {
        const legendRow = document.createElement('div');
        legendRow.style.display = 'inline-block';
        legendRow.style.margin = '0 10px';
        legendRow.style.fontSize = '12px';

        // Create a color box
        const colorBox = document.createElement('span');
        colorBox.style.display = 'inline-block';
        colorBox.style.width = '10px';
        colorBox.style.height = '10px';
        colorBox.style.backgroundColor = item.color;
        colorBox.style.marginRight = '5px';

        // Create the text for the legend item
        const legendText = document.createElement('span');
        legendText.textContent = item.text;

        // Append the color box and text to the row
        legendRow.appendChild(colorBox);
        legendRow.appendChild(legendText);
        legendContainer.appendChild(legendRow);
    });

    // Insert the legendContainer into the plotContainer at the top
    plotContainer.prepend(legendContainer);
}


