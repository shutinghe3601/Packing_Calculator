"""
This scripts pulls the item case dimension and warehouse location dimensions, and convert to txt files that ready to convert to javascript files.
"""

import hidden 
import connect
import pandas as pd

item_case = """
select item_number as sku_id, name, case_length ,case_width, case_height
from dwd.wms_item
where status  = 'A'
"""

loc_dims = """
select loc.warehouse_number, loc.location_no, size.width_inch * size.fill_rate as loc_width, size.height_inch * size.fill_rate as loc_height, size.depth_inch * size.fill_rate as loc_depth
from dwd.wh_storage_location loc 
left join dwd.wms_wh_location_size size on loc.size_id  = size.size_id 
where loc.location_type  = 3
"""

cursor,conn = connect.connection(3, hidden.secrets())
# item_case = connect.execute_query(cursor, sample)
loc_data = connect.exeute(cursor, loc_dims)
item_data = connect.exeute(cursor, item_case)



connect.closure(cursor, conn)


text = 'var locData = '
end = ';'
with open('data/sample_locData.txt','w') as file:
    file.write(text)
    file.writelines(str(loc_data[:10]))
    file.write(end)

text2 = 'var itemData = '
with open('data/sample_itemData.txt', 'w') as file:
    file.write(text2)
    file.writelines(str(item_data[:10]))
    file.write(end)

print('txt file done.')

# data.to_csv('data/inventory_20241211_wh37.csv', index = False)

# # Sample DataFrame
# data = {
#     "Warehouse Number": [101, 102, 103],
#     "Location Number": [1, 2, 3],
#     "SKU ID": ["A123", "B456", "C789"]
# }
# df = pd.DataFrame(data)

# # Convert DataFrame to JSON and save to a file
# json_file_path = 'output.json'
# df.to_json(json_file_path, orient='records', lines=True)

# print(f"JSON data file saved to {json_file_path}")


