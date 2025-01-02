import pandas as pd


item = {
    "sku_id": ["123", "456", "789"],
    "case_width": [1, 2, 3],
    "case_length": [4, 5, 6],
    "case_height": [7, 7, 7]
}

bin = {
    "warehouse_number": [101, 102, 103],
    "location_number": ['C1', 'C2', 'C3'],
    "width_inch": [10, 20, 30],
    "depth_inch": [40, 40, 40],
    "height_inch": [80, 80, 80]
}

item_df = pd.DataFrame(item)
bin_df = pd.DataFrame(bin)

print(item_df)
print(bin_df)


item_df.to_json('data/item.json', orient='records', lines=True)
bin_df.to_json('data/bin.json', orient='records', lines=True)