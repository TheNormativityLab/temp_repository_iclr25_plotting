import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Function to convert RGB fractions to barycentric coordinates in an equilateral triangle
def barycentric_coordinates(red, green, blue):
    # Vertex positions of the equilateral triangle
    vertex_red = np.array([1, 0])
    vertex_green = np.array([0, 0])
    vertex_blue = np.array([0.5, np.sqrt(3) / 2])
    
    # Barycentric coordinates as a weighted sum of vertices
    return red * vertex_red + green * vertex_green + blue * vertex_blue

def plot_triangle_for_step(df, step_numbers):
    # Define the color map for altar_color
    color_map = {1: 'red', 2: 'green', 3: 'blue'}
    
    # Determine the number of rows and columns (5 columns per row)
    n_cols = 5
    n_rows = int(np.ceil(len(step_numbers) / n_cols))
    
    # Create a figure with n_rows and n_cols for subplots
    fig, axs = plt.subplots(n_rows, n_cols, figsize=(5 * n_cols, 5 * n_rows))
    
    # Flatten axs array if there's more than one row
    axs = axs.flatten() if n_rows > 1 else [axs]
    
    # Define the triangle vertices for red, green, and blue
    triangle_vertices = np.array([[1, 0], [0, 0], [0.5, np.sqrt(3) / 2]])
    
    for i, step_number in enumerate(step_numbers):
        ax = axs[i]
        
        # Filter the dataframe for the specific step and sample 100 entries
        df_step = df[df['step'].isin([step_number])].sample(n=100, random_state=42)

        # Plot the triangle in the current subplot
        ax.plot([1, 0.5, 0, 1], [0, np.sqrt(3)/2, 0, 0], 'k-', lw=2)
        
        # Plot the labels for the triangle vertices
        ax.text(1.05, 0, 'R', color='red', fontsize=12, ha='center')
        ax.text(-0.05, 0, 'G', color='green', fontsize=12, ha='center')
        ax.text(0.5, np.sqrt(3)/2 + 0.05, 'B', color='blue', fontsize=12, ha='center')
        
        # Normalize the ep_id to adjust brightness (opacity) between 0.1 and 1
        min_ep_id = df_step['ep_id'].min()
        max_ep_id = df_step['ep_id'].max()
        
        # Plot each point with the corresponding color and brightness based on ep_id
        for _, row in df_step.iterrows():
            coords = barycentric_coordinates(row['red_berry_fraction'], row['green_berry_fraction'], row['blue_berry_fraction'])
            brightness = 0.05 + 0.85 * (row['ep_id'] - min_ep_id) / (max_ep_id - min_ep_id)  # Scale between 0.1 and 1
            ax.scatter(coords[0], coords[1], color=color_map[row['altar_color']], alpha=brightness)
        
        # Set limits
        ax.set_xlim(-0.1, 1.1)
        ax.set_ylim(-0.1, np.sqrt(3)/2 + 0.1)
        ax.set_aspect('equal', adjustable='box')
        ax.set_axis_off()
    
    # Hide any unused subplots (if step_numbers < total subplots created)
    for j in range(i + 1, len(axs)):
        axs[j].set_visible(False)
    
    # Adjust layout and display the plot
    plt.tight_layout()
    plt.show()



# Example dataframe creation (replace with actual data loading)
# For demonstration purposes, here's how you could create the dataframe from CSV or from provided data
df = pd.read_csv('./allelopathy_df.csv')  # Replace with actual path to the CSV file

# Call the function to plot the triangle for step 498
plot_triangle_for_step(df, df['step'].unique().tolist()[1:])
