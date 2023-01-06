import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path


def load_data(file_path, file_name):
    """
    load_data: this function load data from a user-specified
    file path and file name

    Args:
        file_path (Path): path to data file list of variables to be recoded (specified by user)
        file_name (str): name of data file
    Returns:
        (DataFrame): dataframe of imported data
    """
    data_path = Path(file_path, file_name)

    if data_path.is_file():
        return pd.read_csv(data_path)
    else:
        raise Exception(f"Raw data file not found at {data_path}!")


def save_fig(
    fig_id, tight_layout=True, image_directory=None, fig_extension="png", resolution=300
):
    if image_directory is not None:
        file_name = f"{fig_id}.{fig_extension}"
        path = Path(image_directory, file_name)

        print("Saving figure", fig_id)

        if tight_layout:
            plt.tight_layout()

        plt.savefig(path, format=fig_extension, dpi=resolution)

    else:
        print("No image directory is provided, image is not saved.")
