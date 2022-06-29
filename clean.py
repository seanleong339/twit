import pandas as pd

df = pd.read_json(r'test.json')

print(df['News'])

df['News'] = True
print(df['News'])

#df.to_json('test.json', orient='records',date_format= 'iso', force_ascii=False)