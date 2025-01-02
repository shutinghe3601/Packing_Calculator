// Import THREE.js (Include this script in your HTML or use a module bundler)
// <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/110/three.min.js"></script>
<script src="./three.min.js"></script>

function create3DVisualization(binDims, optimizedOrientation) {
    const [binWidth, binDepth, binHeight] = binDims;
    const [caseX, caseY, caseZ] = optimizedOrientation;

    // Create the scene
    const scene = new THREE.Scene();

    // Create the camera
    const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
    camera.position.set(60, 80, 100);
    camera.lookAt(0, 0, 0);

    // Create the renderer
    const renderer = new THREE.WebGLRenderer();
    renderer.setSize(window.innerWidth, window.innerHeight);
    document.body.appendChild(renderer.domElement);

    // Create the bin (wireframe cube)
    const binGeometry = new THREE.BoxGeometry(binWidth, binDepth, binHeight);
    const binEdges = new THREE.EdgesGeometry(binGeometry);
    const binMaterial = new THREE.LineBasicMaterial({ color: 0x0000ff, linewidth: 1 });
    const binWireframe = new THREE.LineSegments(binEdges, binMaterial);
    binWireframe.position.set(binWidth / 2, binDepth / 2, binHeight / 2); // Center the bin
    scene.add(binWireframe);

    // Create the optimized case (filled cube)
    const caseGeometry = new THREE.BoxGeometry(caseX, caseY, caseZ);
    const caseMaterial = new THREE.MeshBasicMaterial({ color: 0xffa500, transparent: true, opacity: 0.7 });
    const caseMesh = new THREE.Mesh(caseGeometry, caseMaterial);
    caseMesh.position.set(caseX / 2, caseY / 2, caseZ / 2); // Position the case
    scene.add(caseMesh);

    // Add edges to the case
    const caseEdges = new THREE.EdgesGeometry(caseGeometry);
    const caseEdgeMaterial = new THREE.LineBasicMaterial({ color: 0x000000 });
    const caseWireframe = new THREE.LineSegments(caseEdges, caseEdgeMaterial);
    caseWireframe.position.set(caseX / 2, caseY / 2, caseZ / 2); // Align edges with the case
    scene.add(caseWireframe);

    // Add axes for reference
    const axesHelper = new THREE.AxesHelper(50);
    scene.add(axesHelper);

    // Render the scene
    function animate() {
        requestAnimationFrame(animate);
        renderer.render(scene, camera);
    }
    animate();
}

// Example Usage
const binDims = [40.0, 48.0, 30.0]; // Bin dimensions (Width, Depth, Height)
const optimizedOrientation = [18.9, 15.5, 14.1]; // Optimized case dimensions (x, y, z)
create3DVisualization(binDims, optimizedOrientation);
