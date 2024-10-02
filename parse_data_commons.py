import pandas as pd
import ast
import re

def save_dataframe_to_file(df, output_file_path):
    df.to_csv(output_file_path, index=False)

def clean_and_parse_line(line):
    # Replace `array(X, dtype=int32)` with just `X`
    cleaned_line = re.sub(r'array\((\d+), dtype=int32\)', r'\1', line)
    cleaned_line = cleaned_line.replace('None', 'None')  # Ensure 'None' is handled properly
    return cleaned_line

# Function to read and parse the raw data from a file
def parse_csv_as_dict(file_path):
    data = []
    ep_id_index_map = {}  # A dictionary to track index for each ep_id
    idx = 0
    # Reading the file contents
    with open(file_path, 'r') as file:
        for line in file:
            # Clean the line to remove complex constructs like 'array()'
            cleaned_line = clean_and_parse_line(line.strip())
            
            try:
                # Using ast.literal_eval to safely evaluate the cleaned dictionary-like string
                line_data = ast.literal_eval(cleaned_line)
            except Exception as e:
                print(f"Error parsing line: {line}\nError: {e}")
                continue
            
            ep_id = line_data['ep_id']
            steps = line_data['step']
            altar_colors = [None if x is None else int(x) for x in line_data['altar_color']]
            red_zone_fractions = line_data['red_zone_count']
            green_zone_fractions = line_data['green_zone_count']
            blue_zone_fractions = line_data['blue_zone_count']
            
            # Initialize index for this ep_id if it hasn't been encountered before
            if ep_id not in ep_id_index_map:
                idx+=1
            ep_id_index_map[ep_id] = 1

            
            # Zip all values together to create rows
            for step, altar_color, red_zone, green_zone, blue_zone in zip(steps, altar_colors, red_zone_fractions, green_zone_fractions, blue_zone_fractions):
                data.append({
                    'index': idx,  # Index unique to each ep_id
                    'ep_id': ep_id,
                    'step': step,
                    'altar_color': altar_color,
                    'red_zone_fraction': red_zone,
                    'green_zone_fraction': green_zone,
                    'blue_zone_fraction': blue_zone
                })
                
    
    return pd.DataFrame(data)

# Replace 'data.txt' with your actual file path
file_path = './commons_150am.txt'  # Example file path

# Parse the data
df = parse_csv_as_dict(file_path)
output_file_path = 'commons_150am_df.csv'

# Save the dataframe to a CSV file
save_dataframe_to_file(df, output_file_path)
