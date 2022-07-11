from survey_analysis.processing.data_manager import load_dataset
from survey_analysis import config
import pandas as pd


def main():
    data = load_dataset(file_name=config.app_config.training_data_file)
    print(data.sample(5))





if __name__=="__main__":
    main()





