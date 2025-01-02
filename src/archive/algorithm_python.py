import itertools
import pandas as pd

def calculate_remaining_space(bin_dims, orientation):
    """Calculate remaining dimensions after fitting cases."""
    W, D, H = bin_dims
    a, b, c = orientation
    sub_W = W % a
    sub_D = D % b
    sub_H = H % c
    return sub_W, sub_D, sub_H

def calculate_fit_count(bin_dims, orientation):
    """Calculate how many cases fit into the bin for a given orientation."""
    W, D, H = bin_dims
    a, b, c = orientation
    return (W // a) * (D // b) * (H // c)

def optimize_case_packing(warehouse_number, location_number, sku_id):
    """Optimize the packing of cases into a bin."""
    item = pd.read_json('data/item.json', orient='records', lines=True).set_index('sku_id')
    bin = pd.read_json('data/bin.json', orient='records', lines=True).set_index(['warehouse_number', 'location_number'])
    bin_dims = tuple(bin.loc[(warehouse_number, location_number), ['width_inch', 'depth_inch', 'height_inch']].values)
    case_dims = tuple(item.loc[sku_id, ['case_width', 'case_length', 'case_height']].values)

    orientation_list = list(itertools.permutations(case_dims))
    total_cases = 0
    packing_orientations = []

    while True:
        best_orientation = None
        max_cases = 0
        remaining_bin_dims = None

        # Find the best orientation for the current bin dimensions
        for orientation in orientation_list:
            cases = calculate_fit_count(bin_dims, orientation)
            if cases > max_cases:
                max_cases = cases
                best_orientation = orientation
                remaining_bin_dims = calculate_remaining_space(bin_dims, orientation)
        
        if max_cases == 0:  # No more cases can fit
            break

        # Update total cases and bin dimensions for remaining space
        total_cases += max_cases
        packing_orientations.append((best_orientation, max_cases))
        print(packing_orientations)
        bin_dims = remaining_bin_dims

    return total_cases, packing_orientations

# Main code
case_dims = (18.9, 15.5, 14.1)
bin_dims = (40.00, 48.00, 30.00)

total_cases, packing_orientations = optimize_case_packing(bin_dims, case_dims)

orientations= packing_orientations[0][0]
count = packing_orientations[0][1]

# # print(f"Optimized total cases: {total_cases}")
# print("Optimized orientations and counts:")
# for orientation, count in packing_orientations:
#     print(f"Orientation: {orientation}, Count: {count}")


import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import numpy as np

# Dimensions of the bin and optimized orientation
bin_dims = (40.00, 48.00, 30.00)  # Bin dimensions: (Width, Depth, Height)
optimized_orientation = (18.9, 15.5, 14.1)  # Optimized case dimensions (x, y, z)

# Extract bin and optimized orientation dimensions
bin_width, bin_depth, bin_height = bin_dims
case_x, case_y, case_z = optimized_orientation

# Create figure and 3D axes
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Draw the bin as a transparent wireframe cube
bin_corners = np.array([
    [0, 0, 0],
    [bin_width, 0, 0],
    [bin_width, bin_depth, 0],
    [0, bin_depth, 0],
    [0, 0, bin_height],
    [bin_width, 0, bin_height],
    [bin_width, bin_depth, bin_height],
    [0, bin_depth, bin_height]
])
bin_lines = [
    (0, 1), (1, 2), (2, 3), (3, 0),  # Bottom face
    (4, 5), (5, 6), (6, 7), (7, 4),  # Top face
    (0, 4), (1, 5), (2, 6), (3, 7)   # Vertical edges
]
for start, end in bin_lines:
    ax.plot(
        [bin_corners[start, 0], bin_corners[end, 0]],
        [bin_corners[start, 1], bin_corners[end, 1]],
        [bin_corners[start, 2], bin_corners[end, 2]],
        color='blue',
        alpha=0.3
    )

# Draw the optimized case as a filled cube
case_corners = np.array([
    [0, 0, 0],
    [case_x, 0, 0],
    [case_x, case_y, 0],
    [0, case_y, 0],
    [0, 0, case_z],
    [case_x, 0, case_z],
    [case_x, case_y, case_z],
    [0, case_y, case_z]
])
case_faces = [
    [case_corners[i] for i in [0, 1, 5, 4]],  # Front face
    [case_corners[i] for i in [1, 2, 6, 5]],  # Right face
    # [case_corners[i] for i in [2, 3, 7, 6]],  # Back face
    # [case_corners[i] for i in [3, 0, 4, 7]],  # Left face
    [case_corners[i] for i in [4, 5, 6, 7]],  # Top face
    # [case_corners[i] for i in [0, 1, 2, 3]]   # Bottom face
]
# Add faces and edges
for face in case_faces:
    ax.add_collection3d(Poly3DCollection([face], color='orange', alpha=0.7))
    for i in range(len(face)):
        start = face[i]
        end = face[(i + 1) % len(face)]  # Loop back to the first vertex
        ax.plot(
            [start[0], end[0]],
            [start[1], end[1]],
            [start[2], end[2]],
            color='black', alpha = 1, linewidth=1
        )

# Set plot limits
ax.set_xlim([0, bin_width])
ax.set_ylim([0, bin_depth])
ax.set_zlim([0, bin_height])

# Set labels
ax.set_xlabel('Width (X)')
ax.set_ylabel('Depth (Y)')
ax.set_zlabel('Height (Z)')

# Show plot
plt.title('3D Visualization of Bin and Optimized Orientation')
plt.show()