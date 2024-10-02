
# Data Processing and Plot Generation for Allelopathy and Commons Harvest

This repository contains scripts to process data from text files into pandas DataFrames and generate visualizations for the allelopathic and commons harvests.

## 1. Data Processing

To convert the text file into a pandas DataFrame for each harvest type, you need to run the following scripts:

- **Allelopathic Harvest**: 
  Run `parse_data_allelopathy.py` to process the data for the allelopathic harvest.

- **Commons Harvest**: 
  Run `parse_data_commons.py` to process the data for the commons harvest.

### Output:

After running these scripts, two CSV files will be generated:

- `allelopathy_df.csv`: Data frame for the allelopathic harvest.
- `commons_df.csv`: Data frame for the commons harvest.

## 2. Plot Generation

### Allelopathic Harvest:
To generate plots for the allelopathic harvest data, run:

```bash
python generate_plot_allelopathy.py
```

This will create and display visualizations based on the `allelopathy_df.csv` data.

### Commons Harvest:
To generate a plot for the commons harvest data, run:

```bash
python generate_plot_commons.py
```

*Note*: The metric for the commons harvest plot is still under consideration, so the current metric used might not be fully meaningful.
