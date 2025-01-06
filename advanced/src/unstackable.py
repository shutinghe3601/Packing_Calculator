import itertools
import pandas as pd
import numpy as np

def read_data():
    case = pd.read_csv('advanced/data/caseData.csv').set_index('sku_id')
    loc = pd.read_csv('advanced/data/locData.csv').set_index(['warehouse_number', 'location_number'])
    return case, loc

case, loc = read_data()

def calculate_remaining_space(loc_dims, orientation):
    """Calculate remaining dimensions after fitting cases."""
    W, L, H = loc_dims
    a, b, c = orientation
    sub_W = W % a
    sub_L = L % b
    sub_H = H % c
    return sub_W, sub_L, sub_H

def calculate_fit_count(loc_dims, orientation):
    """Calculate how many cases fit into the loc for a given orientation."""
    W, L, H = loc_dims
    a, b, c = orientation
    return (W // a) * (L // b) * (H // c)

def space_for_new(warehouse_number, location_number, case = case, loc = loc, optimize = False):
    """Iterate all orientation, return the orientation with maximum number of cases"""
    loc_dims = tuple(loc.loc[(warehouse_number, location_number), ['width_inch', 'depth_inch', 'height_inch']].values)
    loc_inventory = loc.loc[(warehouse_number, location_number), 'loc_inventory']
    loc_qty = loc.loc[(warehouse_number, location_number), 'case_qty']
    
    case_dims = tuple(case.loc[loc_inventory, ['case_width', 'case_length', 'case_height']].values)

    if case_dims[0] * case_dims[1] * case_dims[2] == 0:
        print('Location invenotry SKU has invalid dimension data in the system. Please remeasure for accurate results.')
        return None, None 


    orientation_list = list(itertools.permutations(case_dims))

    maximum_cases  = 0
    for orientation in orientation_list:
        cases = calculate_fit_count(loc_dims, orientation)
        if cases > maximum_cases:
            maximum_cases = cases
            best_orientation = orientation


    if optimize: # optimize meaning stack all existing loc inventory together
        n_stack = np.ceil((loc_qty * best_orientation[2])/loc_dims[2])
        occupied_W = best_orientation[0]*n_stack
        occupied_D = best_orientation[1]*n_stack
    else: # assume existing loc inventories are placed on the floor horizontally
        occupied_W = best_orientation[0]*loc_qty
        occupied_D = best_orientation[1]*loc_qty    
    
    print(occupied_W, occupied_D)
    major_space = tuple([loc_dims[0], loc_dims[1] - occupied_D, loc_dims[2]])
    sub_space = tuple([loc_dims[0] - occupied_W, occupied_D, loc_dims[2]])

    return major_space, sub_space

def solution_for_new(sku_id, case, major_space, sub_space):
    case_dims = tuple(case.loc[sku_id, ['case_width', 'case_length', 'case_height']].values)

    if case_dims[0] * case_dims[1] *case_dims[2] == 0:
        print('New SKU has invalid dimension data in the system. Please remeasure for accurate results.')
        return None, None 

    orientation_list = list(itertools.permutations(case_dims))

    opt_cases  = 0
    opt_solution = {}
    for orientation in orientation_list:
        major_case = calculate_fit_count(major_space, orientation)
        major_orientation = [float(x) for x in orientation]
        remaining_space = calculate_remaining_space(major_space, orientation)

        effective_space = (sub_space[0], sub_space[1], sub_space[2] + remaining_space[2])

        good_sub_case = 0
        sub_orientation = None
        for orientation in orientation_list:
            sub_case = calculate_fit_count(effective_space, orientation)
            if sub_case > good_sub_case: # select the optimized sub_orientation
                good_sub_case = sub_case
                sub_orientation = [float(x) for x in orientation]

        if major_case + good_sub_case > opt_cases: # select the optimized total solution
            opt_cases = major_case + good_sub_case
            opt_solution['orient'] = [major_orientation, sub_orientation]
            opt_solution['n_case'] = [float(major_case), float(good_sub_case)]

    return opt_cases, opt_solution

        
def comprehensive(warehouse_number, location_number, sku_id, case = case, loc = loc, optimize = False):
    major_space, sub_space = space_for_new(warehouse_number, location_number, case, loc, optimize)
    opt_cases, opt_solution = solution_for_new(sku_id, case, major_space, sub_space)

    if opt_cases:
        return float(opt_cases), pd.DataFrame(opt_solution)
    else:
        return 'Error: invalid dimensions.'


print(comprehensive(101, 'B03', 37, optimize= True))