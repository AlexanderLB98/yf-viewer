import os

import pandas as pd
from collections import defaultdict

def fetch_index_dict(base_dir: str) -> dict:
    """
    This function returns a dictionary where keys are folder names (indexes), 
    and values are lists of all subfolder names inside them.
    """
    index_dict = defaultdict(list)
    
    if not os.path.exists(base_dir):
        raise FileNotFoundError(f"Directory {base_dir} does not exist")
    
    for index_folder in os.listdir(base_dir):
        index_folder_path = os.path.join(base_dir, index_folder)
        if os.path.isdir(index_folder_path):
            subfolders = [subfolder for subfolder in os.listdir(index_folder_path) if os.path.isdir(os.path.join(index_folder_path, subfolder))]
            index_dict[index_folder] = subfolders
    
    return dict(index_dict)

def fetch_local_data(base_dir: str)-> pd.DataFrame: 
    """
    This function returns a df with all the data from the config path
    """
    all_dfs = []

    if not os.path.exists(base_dir):
        raise FileNotFoundError(f"Directory {base_dir} does not exist")

    for main_folder in os.listdir(base_dir):
        main_folder_path = os.path.join(base_dir, main_folder)
        if os.path.isdir(main_folder_path):  # Ensure it's a directory
            for subfolder in os.listdir(main_folder_path):
                subfolder_path = os.path.join(main_folder_path, subfolder)
                if os.path.isdir(subfolder_path):
                    csv_file = os.path.join(subfolder_path, f"{subfolder}.csv")
                    if os.path.exists(csv_file):
                        df = pd.read_csv(csv_file)
                        df["source"] = subfolder  # Add a column to track origin
                        all_dfs.append(df)

    if all_dfs:
        final_df = pd.concat(all_dfs, ignore_index=True)
        return final_df
    else:
        return pd.DataFrame()



if __name__ == "__main__":
    df = fetch_local_data("/home/lucas/projects/DE-yf-raspi/data")
    print(df.head())
    print(len(df))
    test_dict = fetch_index_dict("/home/lucas/projects/DE-yf-raspi/data")
    print(test_dict)
