import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats
import numpy as np

# Assuming your data is in a CSV file named 'data.csv'
df = pd.read_csv('./commons_150am_df.csv')

# Group by ep_id and check if any of the zone fractions is 0
def check_zero(group):
    red_zero = (group['red_zone_fraction'] > 0).all().astype(int)
    green_zero = (group['green_zone_fraction'] > 0).all().astype(int)
    blue_zero = (group['blue_zone_fraction'] > 0).all().astype(int)
    return pd.Series({
        'red_zero': red_zero,
        'green_zero': green_zero,
        'blue_zero': blue_zero
    })

# Define a function to calculate the metric
def calculate_metric(group):
    '''
    return (int(group['green_zone_fraction'].eq(0).any()) +
            int(group['blue_zone_fraction'].eq(0).any()) +
            int(group['red_zone_fraction'].eq(0).any())) / 3
    '''
    return group.shape[0]

# Sample 1000 random rows from the DataFrame
sampled_df = df

# Apply the metric calculation to each group and create a new column
#grouped_df = sampled_df.groupby('ep_id').apply(calculate_metric).reset_index(name='metric')
new_df = df.groupby('index').apply(check_zero).reset_index()
#grouped_df = df.groupby('index').size().reset_index(name='metric')
#grouped_df.sort_values(by='index', inplace=True)
# Display the new DataFrame
#print(grouped_df.head(20))
# Adding a new column 'metric' that is the average of 'red_zero', 'green_zero', and 'blue_zero'
new_df['metric'] = new_df[['red_zero', 'green_zero', 'blue_zero']].mean(axis=1)

grouped_df = new_df
sampled_indices = np.linspace(grouped_df['index'].min(), grouped_df['index'].max(), num=1000, dtype=int)
grouped_df = grouped_df[grouped_df['index'].isin(sampled_indices)]

# Normalize the 'ep_id' column to be between 0 and 1
min_ep_id = grouped_df['index'].min()
max_ep_id = grouped_df['index'].max()
grouped_df['normalized_ep_id'] = (grouped_df['index'] - min_ep_id) / (max_ep_id - min_ep_id)

slope, intercept, r_value, p_value, std_err = stats.linregress(grouped_df['normalized_ep_id'], grouped_df['metric'])

# Create the plot
plt.figure(figsize=(10, 6))
plt.scatter(grouped_df['normalized_ep_id'], grouped_df['metric'])

# Add the regression line
plt.plot(grouped_df['normalized_ep_id'], slope * grouped_df['normalized_ep_id'] + intercept, color='red', label=f'y={slope:.2f}x+{intercept:.2f}')

plt.xlabel('Normalized Episode ID')
plt.ylabel('Depletion Metric')
plt.title('Metric vs. Normalized Episode ID with Linear Regression')
plt.legend()
plt.show()