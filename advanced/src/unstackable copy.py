import itertools
import pandas as pd
import numpy as np


""" this method is no good, because only valid for cubic occupied volume, any irregular shapes cannot be calculated eaisly. using the previoud method"""

def read_data(warehouse_number, location_number, sku_id):
    case = pd.read_csv('advanced/data/caseData.csv').set_index('sku_id')
    loc = pd.read_csv('advanced/data/locData.csv').set_index(['warehouse_number', 'location_number'])
    loc_dims = tuple(loc.loc[(warehouse_number, location_number), ['width_inch', 'depth_inch', 'height_inch']].values)
    loc_inventory = loc.loc[(warehouse_number, location_number), 'loc_inventory']
    loc_qty = loc.loc[(warehouse_number, location_number), 'loc_qty']
    loc_case_dims = tuple(case.loc[loc_inventory, ['case_width', 'case_length', 'case_height']].values)
    case_dims = tuple(case.loc[sku_id, ['case_width', 'case_length', 'case_height']].values)
    return loc_dims, loc_qty, loc_case_dims, case_dims

loc_dims, loc_qty, loc_case_dims, case_dims = read_data()

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

def computation_for_new(loc_dims, case_dims, occupied_W, occupied_L, occupied_H):
    orientation_list = list(itertools.permutations(case_dims))

    max_total = 0
    best_solution = {}
    for orientation in orientation_list:
        major_case = int(calculate_fit_count(loc_dims, orientation))
        major_orient = [float(x) for x in orientation]
        remain_space = calculate_remaining_space(loc_dims, orientation)

        occupied_case = int(np.ceil(occupied_W/orientation[0]) * np.ceil(occupied_L/orientation[1]) * np.ceil(occupied_H/orientation[2]))

        major_case -= occupied_case

        best_sub = 0
        sub_orient = None
        for orientation in orientation_list:
            sub_case =int(calculate_fit_count(remain_space, orientation))
            if sub_case > best_sub:
                best_sub = sub_case
                sub_orient = orientation
        
        total_case = major_case + best_sub
        if total_case > max_total:
            max_total = total_case
            best_solution['orientations'] = [major_orient, sub_orient]
            best_solution['num_case'] = [major_case, best_sub]
        return max_total, best_solution

def space_for_new(loc_dims, loc_qty, loc_case_dims, case_dims, compact_existing = False, stackable = False):
    """Iterate all orientation, return the orientation with maximum number of cases"""
    if loc_case_dims[0] * loc_case_dims[1] * loc_case_dims[2] == 0:
        print('Location invenotry SKU has invalid dimension data in the system. Please remeasure for accurate results.')
        return None, None 
    
    if case_dims[0] * case_dims[1] *case_dims[2] == 0:
        print('New SKU has invalid dimension data in the system. Please remeasure for accurate results.')
        return None, None 

    orientation_list = list(itertools.permutations(loc_case_dims))

    # best orientation of existing sku
    maximum_cases  = 0
    for orientation in orientation_list:
        cases = calculate_fit_count(loc_dims, orientation)
        if cases > maximum_cases:
            maximum_cases = cases
            best_orientation = orientation

    # check whether existing SKU has occupied all space, assume only reach to the maximum existing triggers this 
    max_existing, _ = computation_for_new(loc_dims, case_dims, occupied_W = 0, occupied_L = 0, occupied_H = 0)
    if loc_qty >= max_existing:
        print("Existing SKU of the inventory seems occupied the whole space of the location, double check the location's availability")
        return None, None

    if compact_existing: # optimize existing SKU's arrangement by layer them and make them more compact
        n_stack = np.ceil((loc_qty * best_orientation[2])/loc_dims[2])
        occupied_W = best_orientation[0]*n_stack # assume existing SKU arranged horizontally, hence length is not changed.
        occupied_L = best_orientation[1]
    else: # assume existing inventories are not layered properly
        number_onelayer = loc_dims[0]//best_orientation[0] * loc_dims[1]//best_orientation[1]
        if loc_qty >= number_onelayer and not stackable:
            print('The existing SKUs have utilized all available space. To use this location, optimize the current SKUs or make them stackable with different SKUs.')
            return None, None
        else: 
            occupied_W = best_orientation[0]*loc_qty
            occupied_L = best_orientation[1]*loc_qty
        
    if stackable:
        # need to care the height, maximum height
        occupied_H = loc_dims[2]//
        max_total, best_solution = computation_for_new(loc_dims, case_dims, occupied_W, occupied_L, occupied_H)
    else:
        # no need to care height
        occupied_H = loc_dims[2] 
        max_total, best_solution = computation_for_new(loc_dims, case_dims, occupied_W, occupied_L, occupied_H)


    return max_total, best_solution 

        




def comprehensive(warehouse_number, location_number, sku_id, case = case, loc = loc, optimize = False):
    major_space, sub_space = space_for_new(warehouse_number, location_number, case, loc, optimize)
    opt_cases, opt_solution = solution_for_new(sku_id, case, major_space, sub_space)

    if opt_cases:
        return float(opt_cases), pd.DataFrame(opt_solution)
    else:
        return 'Error: invalid dimensions.'


print(comprehensive(101, 'B03', 37, optimize= True))