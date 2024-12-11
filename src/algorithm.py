import itertools

def calculate_remaining_space(bin_dims, orientation):
    """Calculate remaining dimensions after fitting cases."""
    W, D, H = bin_dims
    a, b, c = orientation
    sub_W = W % a
    sub_D = D % b
    sub_H = H % c
    return sub_W, sub_D, sub_H

def calculated_n(bin_dims, orientation):
    """Calculate how many cases fit into the bin for a given orientation."""
    W, D, H = bin_dims
    a, b, c = orientation
    n = (W // a) * (D // b) * (H // c)
    return n

def recursive_computation(bin_dims, orientation_list, used_orientation, total_n):
    """Recursive computation to calculate the total number of cases fitting into the bin."""
    for orientation in orientation_list:
        if orientation in used_orientation:
            continue

        n = calculated_n(bin_dims, orientation)
        print('n:',n, orientation)

        if n < 1:
            # Skip to the next orientation if the current one cannot fit
            continue

        # Add the current orientation to the used list
        total_n += n
        used_orientation.append(orientation)

        # Calculate remaining bin dimensions
        sub_W, sub_D, sub_H = calculate_remaining_space(bin_dims, orientation)
        remaining_bin_dims = (sub_W, sub_D, sub_H)

        # Recursively compute for the remaining space
        total_n = recursive_computation(remaining_bin_dims, orientation_list, used_orientation, total_n)
        
        # Remove the orientation from used list after recursion to allow other paths
        print('used_orientation:',used_orientation, 'and total_n:', total_n)
        used_orientation.pop()
        total_n = 0
        

    return total_n

# Main code
case_dims = (18.9,15.5,14.1)
bin_dims = (40.00,48.00,30.00)
orientation_list = list(itertools.permutations(case_dims))
used_orientation = []
total_n = 0

total_n = recursive_computation(bin_dims, orientation_list, used_orientation, total_n)
