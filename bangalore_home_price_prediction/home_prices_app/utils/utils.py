# Helper functions that I will use in my server backend.
import json
from pathlib import Path
import numpy as np

__locations = None


def get_possible_locations():
    global __locations

    locations_path = Path("utils", "artifacts", "possible_locations.json")

    # get the possible locations from json
    with open(locations_path, "r") as f:
        __locations = json.load(f)["possible_locations"]

    return __locations


# Dictionaries to map values of area_type and availability:
# From values on html.app form to levels expected by our ML model
area_type_map = [
    np.nan,
    "Super_built_up_Area",
    "Built_up_Area",
    "Plot_Area",
    "Carpet_Area",
]

availability_map = [np.nan, "Ready To Move", "Not Ready To Move"]


if __name__ == "__main__":
    print(get_possible_locations()[:10])
    print(area_type_map)
