import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
# Function to read dataframe from a CSV file and plot the ribbon plots
def plot_ribbon_from_file(file_path):
    # Read the data from CSV
    df = pd.read_csv(file_path)

    # Calculate mean and standard deviation for each berry fraction across ep_id (assuming multiple ep_id entries)
    df_grouped = df.groupby('step').agg({
        'red_zone_fraction': ['mean', 'std'],
        'green_zone_fraction': ['mean', 'std'],
        'blue_zone_fraction': ['mean', 'std']
    }).reset_index()

    # Flatten column names
    df_grouped.columns = ['step', 'red_mean', 'red_std', 'green_mean', 'green_std', 'blue_mean', 'blue_std']

    # Replace NaN std values with 0 (if any)
    df_grouped['red_std'].fillna(0, inplace=True)
    df_grouped['green_std'].fillna(0, inplace=True)
    df_grouped['blue_std'].fillna(0, inplace=True)

    # Plotting the ribbon plot for each berry fraction
    plt.figure(figsize=(10, 6))

    # Red berry fraction ribbon plot
    plt.plot(df_grouped['step'], df_grouped['red_mean'], color='red', label='Red Berry Fraction')
    plt.fill_between(df_grouped['step'], df_grouped['red_mean'] - df_grouped['red_std'], df_grouped['red_mean'] + df_grouped['red_std'], color='red', alpha=0.3)

    # Green berry fraction ribbon plot
    plt.plot(df_grouped['step'], df_grouped['green_mean'], color='green', label='Green Berry Fraction')
    plt.fill_between(df_grouped['step'], df_grouped['green_mean'] - df_grouped['green_std'], df_grouped['green_mean'] + df_grouped['green_std'], color='green', alpha=0.3)

    # Blue berry fraction ribbon plot
    plt.plot(df_grouped['step'], df_grouped['blue_mean'], color='blue', label='Blue Berry Fraction')
    plt.fill_between(df_grouped['step'], df_grouped['blue_mean'] - df_grouped['blue_std'], df_grouped['blue_mean'] + df_grouped['blue_std'], color='blue', alpha=0.3)

    # Labels and title
    plt.xlabel('Step')
    plt.ylabel('Berry Fraction')
    plt.title('Berry Fractions with Ribbon Plot for Red, Green, and Blue Berries')
    plt.legend()

    # Display the plot
    plt.show()

# Example file path (replace with actual file path)
file_path = './all_df.csv'

# Call the function to read the data from file and plot the ribbons
plot_ribbon_from_file(file_path)
