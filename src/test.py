"""
This script extract daily inventory data, and verify whether it's need to have a secondary orientation.
"""

import hidden 
import connect
import pandas as pd
import numpy as np

query = """
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

cursor,conn = connect.connection(3, hidden.secrets())
data = connect.execute_query(cursor, query)
connect.closure(cursor, conn)

data.to_csv('data/inventory_20241211_wh37.csv', index = False)



