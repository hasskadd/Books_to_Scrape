import pandas as pd

# read DataFrame
data = pd.read_csv("products.csv")

for (Category), group in data.groupby(['category']):
    group.to_csv(f'categories/{Category}.csv', index=False)
