function create3DPlot(caseDims, locDims) {
    // Retrieve the plot container
    const plotContainer = document.getElementById('plotContainer');

    // Clear any previous canvas
    while (plotContainer.firstChild) {
        plotContainer.removeChild(plotContainer.firstChild);
    }

    // Create scene, camera, and renderer
    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(75, 2, 0.1, 1000);
    const renderer = new THREE.WebGLRenderer({ antialias: true });
    renderer.setSize(600, 300); // Fixed canvas size
    renderer.setClearColor(0xf5f5dc); // Beige white background
    plotContainer.appendChild(renderer.domElement);

    // Add 3D space (bounding box mesh)
    const [locWidth, locDepth, locHeight] = locDims;
    const spaceGeometry = new THREE.BoxGeometry(locWidth, locHeight, locDepth);
    const spaceMaterial = new THREE.MeshBasicMaterial({
        color: 0x87ceeb, // Light blue
        wireframe: true,
        transparent: true,
        opacity: 0.5,
    });
    const spaceMesh = new THREE.Mesh(spaceGeometry, spaceMaterial);
    spaceMesh.position.set(locWidth / 2, locHeight / 2, locDepth / 2); // Center the space
    scene.add(spaceMesh);

    // Add object inside the 3D space
    const scaleFactor = 1; // Scale the object
    const [objWidth, objDepth, objHeight] = caseDims.map(dim => dim * scaleFactor);
    const objGeometry = new THREE.BoxGeometry(objWidth, objHeight, objDepth);

    // Material for the object
    const objMaterial = new THREE.MeshBasicMaterial({ color: 0xffa500 }); // Orange
    const objectMesh = new THREE.Mesh(objGeometry, objMaterial);
    objectMesh.position.set(objWidth / 2, objHeight / 2, objDepth / 2); // Place on the floor
    scene.add(objectMesh);

    // Add edges for the object for better visibility
    const edges = new THREE.EdgesGeometry(objGeometry);
    const edgeMaterial = new THREE.LineBasicMaterial({ color: 0x000000 }); // Black for edges
    const edgeLines = new THREE.LineSegments(edges, edgeMaterial);
    objectMesh.add(edgeLines);

    // Add axes for reference
    const axisLength = Math.max(...locDims);
    addAxis(scene, [0, 0, 0], [axisLength, 0, 0], 0xff0000); // X-axis (red)
    addAxis(scene, [0, 0, 0], [0, axisLength, 0], 0x00ff00); // Y-axis (green)
    addAxis(scene, [0, 0, 0], [0, 0, axisLength], 0x0000ff); // Z-axis (blue)

    
    // Add 'Front' label
    const loader = new THREE.FontLoader();
    loader.load('https://threejs.org/examples/fonts/droid/droid_sans_regular.typeface.json', function (font) {
        const textGeometry = new THREE.TextGeometry('Front', {
            font: font,
            size: locHeight * 0.2, // Scale size relative to bounding box
            height: 0.5,
        });
        const textMaterial = new THREE.MeshBasicMaterial({ color: 0x7a7a7a }); // Grey color
        const textMesh = new THREE.Mesh(textGeometry, textMaterial);

        // Position the text at the front-center of the box
        textMesh.position.set(locWidth / 3, 0, locDepth + locHeight * 0.3); 
        textMesh.rotation.x = -Math.PI / 2; // Rotate 90 degrees clockwise along the X-axis

        scene.add(textMesh);
    });               

    // Set camera position and angle
    camera.position.set(locWidth * 1.5, locHeight * 1.2, locDepth * 1.5); // Adjust for top-left view
    camera.lookAt(locWidth / 2, locHeight / 2, locDepth / 2);

    // Animation loop to render the scene
    function animate() {
        requestAnimationFrame(animate);
        renderer.render(scene, camera);
    }

    animate(); // Start the rendering loop
}


function addAxis(scene, start, end, color) {
    const material = new THREE.LineBasicMaterial({ color: color });
    const geometry = new THREE.BufferGeometry().setFromPoints([
        new THREE.Vector3(...start),
        new THREE.Vector3(...end),
    ]);
    const axis = new THREE.Line(geometry, material);
    scene.add(axis);
}