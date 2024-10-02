import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats

# Assuming your data is in a CSV file named 'data.csv'
df = pd.read_csv('./commons_df.csv')

# Define a function to calculate the metric
def calculate_metric(group):
    return (int(group['green_zone_fraction'].eq(0).any()) +
            int(group['blue_zone_fraction'].eq(0).any()) +
            int(group['red_zone_fraction'].eq(0).any())) / 3

# Sample 1000 random rows from the DataFrame
sampled_df = df.sample(n=1000)

# Apply the metric calculation to each group and create a new column
grouped_df = sampled_df.groupby('ep_id').apply(calculate_metric).reset_index(name='metric')

# Normalize the 'ep_id' column to be between 0 and 1
min_ep_id = grouped_df['ep_id'].min()
max_ep_id = grouped_df['ep_id'].max()
grouped_df['normalized_ep_id'] = (grouped_df['ep_id'] - min_ep_id) / (max_ep_id - min_ep_id)

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