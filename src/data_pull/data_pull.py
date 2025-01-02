"""
This scripts returns the query that pulls the warehouse location dimensions and item case dimensions from the database.
"""

import hidden 
import connect
import pandas as pd

sample = """
select inv.item_number, inv.location_no, loc.size_id, 
	loc_size.value, loc_size.width_inch as loc_width, loc_size.depth_inch as loc_depth, loc_size.height_inch as loc_height,
	item.case_width, item.case_length, item.case_height 
from dwd.wms_wh_inventory_transaction inv
left join dwd.wms_storage_location loc on loc.location_no = inv.location_no
	and loc.warehouse_number  = inv.warehouse_number 
left join dwd.wms_wh_location_size loc_size on loc_size.size_id  = loc.size_id 
left join dwd.wms_item item on item.item_number = inv.item_number 
where inv.warehouse_number = 37 and inv.location_no != 'D-adjust'
    and loc.size_id is not null
"""

item_case = """
select item_number, name, case_width, case_length, case_height
from dwd.wms_item
where status = 'A'
"""

bin_dims = """
select warehouse_number, location_no, size_id, value, width_inch, depth_inch, height_inch
"""

cursor,conn = connect.connection(3, hidden.secrets())
data = connect.execute_query(cursor, sample)
connect.closure(cursor, conn)

data.to_csv('data/inventory_20241211_wh37.csv', index = False)

# Sample DataFrame
data = {
    "Warehouse Number": [101, 102, 103],
    "Location Number": [1, 2, 3],
    "SKU ID": ["A123", "B456", "C789"]
}
df = pd.DataFrame(data)

# Convert DataFrame to JSON and save to a file
json_file_path = 'output.json'
df.to_json(json_file_path, orient='records', lines=True)

print(f"JSON data file saved to {json_file_path}")


