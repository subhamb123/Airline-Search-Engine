import os

# Config class for data ingestion either raw or reduced for performance testing
class DataConfig:
    BASE_DIRECTORY = os.path.abspath(os.path.dirname(__file__))

    RAW_DATA_PATH = os.path.join(BASE_DIRECTORY, "../../DataSets/Raw")
    REDUCED_DATA_PATH = os.path.join(BASE_DIRECTORY, "../../DataSets/Reduced")

    PATHS = {
        "airports": {
            True: os.path.join(REDUCED_DATA_PATH, "reducedAirports.csv"),
            False: os.path.join(RAW_DATA_PATH, "airports.csv")
        },
        "airlines": {
            True: os.path.join(REDUCED_DATA_PATH, "reducedAirlines.csv"),
            False: os.path.join(RAW_DATA_PATH, "airlines.csv")
        },
        "routes": {
            True: os.path.join(REDUCED_DATA_PATH, "reducedRoutes.csv"),
            False: os.path.join(RAW_DATA_PATH, "routes.csv")
        }
    }

    @classmethod
    def get_path(cls, name, use_reduced_data):
        return cls.PATHS[name][use_reduced_data]