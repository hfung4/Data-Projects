from pathlib import Path
import src.config as config
import pickle

# Save model
def save_model(clf, fold=None):
    if fold is None:
        fold_name = "full"
    else:
        fold_name = f"fold_{fold}"

    model_out_path = Path(config.MODEL_DIR, fold_name)
    # Make directory if not exist
    model_out_path.mkdir(parents=True, exist_ok=True)
    with open(Path(model_out_path, f"{fold_name}_best_clf.pkl"), "wb") as f:
        pickle.dump(clf, f)


# Save processed data
# Save model
def save_processed_data(fold=None, **kwargs):
    if fold is None:
        fold_name = "full"
    else:
        fold_name = f"fold_{fold}"

    # Create file path to saved processed data, create the directory if not exist
    data_out_path = Path(config.PROCESSED_DATA_DIR, fold_name)
    # Make directory if not exist
    data_out_path.mkdir(parents=True, exist_ok=True)

    for k, v in kwargs.items():
        with open(Path(data_out_path, f"{fold_name}_{k}.pkl"), "wb") as f:
            pickle.dump(v, f)
