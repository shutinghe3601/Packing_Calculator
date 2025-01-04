import itertools
import pandas as pd

def calculate_remaining_space(loc_dims, orientation):
    """Calculate remaining dimensions after fitting cases."""
    W, D, H = loc_dims
    a, b, c = orientation
    sub_W = W % a
    sub_D = D % b
    sub_H = H % c
    return sub_W, sub_D, sub_H

def calculate_fit_count(loc_dims, orientation):
    """Calculate how many cases fit into the loc for a given orientation."""
    W, D, H = loc_dims
    a, b, c = orientation
    return (W // a) * (D // b) * (H // c)

def best_orientation(warehouse_number, location_number, sku_id):
    """Iterate all orientation, return the orientation with maximum number of cases"""
    case = pd.read_csv('v2.1_easy_senario/data/caseData.csv').set_index('sku_id')
    loc = pd.read_csv('v2.1_easy_senario/data/locData.csv').set_index(['warehouse_number', 'location_number'])
    loc_dims = tuple(loc.loc[(warehouse_number, location_number), ['width_inch', 'depth_inch', 'height_inch']].values)
    case_dims = tuple(case.loc[sku_id, ['case_width', 'case_length', 'case_height']].values)

    orientation_list = list(itertools.permutations(case_dims))

    maximum_cases  = 0
    for orientation in orientation_list:
        cases = calculate_fit_count(loc_dims, orientation)
        if cases > maximum_cases:
            maximum_cases = cases
            main_orientation = orientation
            remaining_loc_dims = calculate_remaining_space(loc_dims, orientation)
    return main_orientation, maximum_cases, remaining_loc_dims, orientation_list

main_orientation, maximum_cases, remaining_loc_dims, orientation_list = best_orientation(101, 'B20', 60)
main_orientation = [float(x) for x in main_orientation]

def available_space(maximum_cases, warehouse_number, location_number):
    loc = pd.read_csv('v2.1_easy_senario/data/locData.csv').set_index(['warehouse_number', 'location_number'])
    existing_case = loc.loc[(warehouse_number, location_number),'inventory_cases']
    return maximum_cases - existing_case, existing_case

available_case, existing_case = available_space(maximum_cases, 101, 'B20')

def sub_orientation(remaining_loc_dims, orientation_list):
    sub_cases = 0
    suborientation = None
    for orientation in orientation_list:
        cases = calculate_fit_count(remaining_loc_dims, orientation)
        if cases > maximum_cases:
            sub_cases = cases
            suborientation = orientation
    return suborientation, sub_cases

suborientation, sub_cases = sub_orientation(remaining_loc_dims, orientation_list)

def output(main_orientation, maximum_cases, suborientation, sub_cases):
    return pd.DataFrame(data = {'note': ['main_orientation','sub_orientation'], 'orientation':[main_orientation,suborientation], 'num_cases':[maximum_cases, sub_cases]})

print('Optimal arrangement:')
print(output(main_orientation, maximum_cases, suborientation, sub_cases))
if available_case != 0: 
    print(f'Existing number of cases {existing_case}, leaving space for {available_case} with orientation {main_orientation}')
else:
    print('No space for available_case.')