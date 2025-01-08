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

def existing_parameter(loc_dims, orientation):
    W, L, H = loc_dims
    a, b, c = orientation

    n_case_stack = H//c
    n_case_row = W//a * H//c

    return n_case_stack, n_case_row

def space_for_new(warehouse_number, location_number, case = case, loc = loc):
    """Iterate all orientation, return the orientation with maximum number of cases"""
    loc_dims = tuple(loc.loc[(warehouse_number, location_number), ['width_inch', 'depth_inch', 'height_inch']].values)
    loc_inventory = loc.loc[(warehouse_number, location_number), 'loc_inventory']
    loc_qty = loc.loc[(warehouse_number, location_number), 'loc_qty']
    
    loc_case_dims = tuple(case.loc[loc_inventory, ['case_width', 'case_length', 'case_height']].values)

    if loc_case_dims[0] * loc_case_dims[1] * loc_case_dims[2] == 0:
        print('Location invenotry SKU has invalid dimension data in the system. Please remeasure for accurate results.')
        return None, None 

    orientation_list = list(itertools.permutations(loc_case_dims))

    maximum_cases  = 0
    for orientation in orientation_list:
        cases = calculate_fit_count(loc_dims, orientation)
        if cases > maximum_cases:
            maximum_cases = cases
            best_orientation = orientation

    n_case_stack, n_case_row = existing_parameter(loc_dims, best_orientation)

    complication = False

    occupied_w2, occupied_l2 = None, None

    # compute existing arrangement
    if loc_qty <= n_case_stack: # within one stack
        occupied_W = best_orientation[0]
        occupied_L = best_orientation[1]
    elif loc_qty <= n_case_row: # within one row
        occupied_W = best_orientation[0] * n_case_row/n_case_stack
        occupied_L = best_orientation[1]
    else: # more than more row
        n_row = loc_qty//n_case_row
        left = loc_qty%n_case_row
        occupied_W = best_orientation[0] * n_case_row/n_case_stack
        occupied_L = best_orientation[1] * n_row
        if left != 0: # row + stack, create irregular space 
            complication = True
            n_stack = left//n_case_stack
            left = left%n_case_stack # number of individual case
            if left != 0:
                n_stack += 1
            occupied_w2 = best_orientation[0] * n_stack
            occupied_l2 = best_orientation[1]
    

    if complication:
        major_space = (loc_dims[0], loc_dims[1] - (occupied_L + occupied_l2), loc_dims[2])
        sub_space = [(loc_dims[0] - occupied_w2, occupied_l2,loc_dims[2]), (loc_dims[0] - occupied_W, occupied_L, loc_dims[2])]
    else:
        major_space = (loc_dims[0], loc_dims[1] - occupied_L, loc_dims[2])
        sub_space = [(loc_dims[0] - occupied_W, occupied_L, loc_dims[2])]
    
    return major_space, sub_space, occupied_W, occupied_L, occupied_w2, occupied_l2, loc_dims, complication

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

        i = 0
        good_sub_lst = []
        good_sub_orient = []
        while i < len(sub_space):
            effective_space = (sub_space[i][0], sub_space[i][1] + remaining_space[1], sub_space[i][2])
            good_sub_case = 0
            sub_orientation = None
            for orientation in orientation_list:
                sub_case = calculate_fit_count(effective_space, orientation)
                if sub_case > good_sub_case: # select the optimized sub_orientation
                    good_sub_case = sub_case
                    sub_orientation = [float(x) for x in orientation]
                    remaining_space = calculate_remaining_space(effective_space, orientation) 
            good_sub_lst.append(good_sub_case)
            good_sub_orient.append(sub_orientation)
            i += 1

        if major_case + sum(good_sub_lst) > opt_cases: # select the optimized total solution
            opt_cases = major_case + sum(good_sub_lst)
            opt_solution['orient'] = [major_orientation, good_sub_orient]
            opt_solution['n_case'] = [float(major_case), good_sub_lst]

    return opt_cases, opt_solution

        
def comprehensive(warehouse_number, location_number, sku_id, case = case, loc = loc):
    major_space, sub_space, occupied_W, occupied_L, occupied_w2, occupied_l2, loc_dims, complication = space_for_new(warehouse_number, location_number, case, loc)
    opt_cases, opt_solution = solution_for_new(sku_id, case, major_space, sub_space)

    if opt_cases:
        return float(opt_cases), opt_solution, occupied_W, occupied_L, occupied_w2, occupied_l2, loc_dims, complication
    else:
        return 'Error: invalid dimensions.'

print(comprehensive(101, 'B03', 37))
