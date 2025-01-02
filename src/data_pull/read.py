import pandas as pd

item = pd.read_json('data/item.json', orient='records', lines=True).set_index('sku_id')


case_dims = tuple(item.loc[123, ['case_width', 'case_length', 'case_height']].values)
print(case_dims)