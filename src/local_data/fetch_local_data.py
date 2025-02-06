import os

import pandas as pd


def fetch_local_data(base_dir: str):
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
        return None  # No CSV files found

    return df


if __name__ == "__main__":
    df = fetch_local_data("/home/lucas/projects/DE-yf-raspi/data")
    print(df.head())
    print(len(df))
