import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import ListedColormap
import pandas as pd
# Function to read dataframe from a CSV file and plot the ribbon plots with altar_color using imshow
def plot_ribbon_with_altar_color_imshow(file_path):
    # Read the data from CSV
    df = pd.read_csv(file_path)

    # Calculate mean and standard deviation for each berry fraction across ep_id (assuming multiple ep_id entries)
    df_grouped = df.groupby('step').agg({
        'red_berry_fraction': ['mean', 'std'],
        'green_berry_fraction': ['mean', 'std'],
        'blue_berry_fraction': ['mean', 'std']
    }).reset_index()

    # Flatten column names
    df_grouped.columns = ['step', 'red_mean', 'red_std', 'green_mean', 'green_std', 'blue_mean', 'blue_std']

    # Merge altar_color into the grouped dataframe to have it for plotting
    df_grouped = df_grouped.merge(df[['step', 'altar_color']], on='step', how='left')

    # Replace NaN std values with 0 (if any)
    df_grouped['red_std'].fillna(0, inplace=True)
    df_grouped['green_std'].fillna(0, inplace=True)
    df_grouped['blue_std'].fillna(0, inplace=True)

    # Plotting the ribbon plot for each berry fraction
    fig, ax = plt.subplots(2, 1, figsize=(10, 8), gridspec_kw={'height_ratios': [3, 1]})

    # Red berry fraction ribbon plot
    ax[0].plot(df_grouped['step'], df_grouped['red_mean'], color='red', label='Red Berry Fraction')
    ax[0].fill_between(df_grouped['step'], df_grouped['red_mean'] - df_grouped['red_std'], df_grouped['red_mean'] + df_grouped['red_std'], color='red', alpha=0.3)

    # Green berry fraction ribbon plot
    ax[0].plot(df_grouped['step'], df_grouped['green_mean'], color='green', label='Green Berry Fraction')
    ax[0].fill_between(df_grouped['step'], df_grouped['green_mean'] - df_grouped['green_std'], df_grouped['green_mean'] + df_grouped['green_std'], color='green', alpha=0.3)

    # Blue berry fraction ribbon plot
    ax[0].plot(df_grouped['step'], df_grouped['blue_mean'], color='blue', label='Blue Berry Fraction')
    ax[0].fill_between(df_grouped['step'], df_grouped['blue_mean'] - df_grouped['blue_std'], df_grouped['blue_mean'] + df_grouped['blue_std'], color='blue', alpha=0.3)

    # Labels and title for the first plot
    ax[0].set_xlabel('Step')
    ax[0].set_ylabel('Berry Fraction')
    ax[0].set_title('Berry Fractions with Ribbon Plot')
    ax[0].legend()

    altar_colors = df_grouped[['altar_color']].T.values
    color_map = {1: 'red', 2: 'green', 3: 'blue'}
    altar_color_array = [color_map[val] if val in color_map else 'white' for val in df_grouped['altar_color']]
    
    ax[1].imshow([df_grouped['altar_color']], aspect='auto', cmap=ListedColormap(['red', 'green', 'blue']),
                 extent=[min(df_grouped['step']), max(df_grouped['step']), -1, 1])

    # Labels for the second plot (altar color)
    ax[1].set_xlabel('Step')
    ax[1].set_yticks([])
    ax[1].set_title('Altar Color Over Time')

    # Display the plot
    plt.tight_layout()
    plt.show()

# Example file path (replace with actual file path)
file_path = './comm_df.csv'

# Call the function to read the data from file and plot the ribbons with altar_color bands
plot_ribbon_with_altar_color_imshow(file_path)
