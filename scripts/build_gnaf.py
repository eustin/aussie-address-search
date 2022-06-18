import logging
from glob import glob
from pathlib import Path
import re
from time import time
import numpy as np
import pandas as pd

STATES_TERRITORIES = ["ACT", "NSW", "NT", "QLD", "SA", "TAS", "VIC", "WA"]

logging.basicConfig(level="INFO")
logger = logging.getLogger(__name__)


# validate dirs exist
def check_dirs_exist(parent_path, child_dir):
    try:
        dir_to_check = parent_path / child_dir
        print(dir_to_check)
        assert dir_to_check.exists()
        return dir_to_check
    except AssertionError:
        logging.error(f"{dir_to_check.as_posix()} doesn't exist")
        raise


try:
    gnaf_dir = Path(glob("data/G-NAF/G-NAF*").pop())
except IndexError:
    logging.error("GNAF data directory doesn't exist")
    raise

gnaf_standard_dir = check_dirs_exist(gnaf_dir, "Standard")
gnaf_auth_code_dir = check_dirs_exist(gnaf_dir, "Authority Code")

# build file lists
address_detail_files = glob((gnaf_standard_dir / "*_ADDRESS_DETAIL_psv.psv").as_posix())
street_locality_files = glob(
    (gnaf_standard_dir / "*_STREET_LOCALITY_psv.psv").as_posix()
)
locality_files = glob((gnaf_standard_dir / "*_LOCALITY_psv.psv").as_posix())
level_type_file = glob(
    (gnaf_auth_code_dir / "Authority_Code_LEVEL_TYPE_AUT_psv.psv").as_posix()
)

# create hashmaps for smaller datasets to keep them in memory
street_locality_dict = {}
for file in street_locality_files:
    logging.info(f"creating street locality hashmap for {file}")
    try:
        state_or_territory = re.search(
            "(?<=\/)[A-Z]+(?=_STREET_LOCALITY_psv.psv)", file
        ).group()
    except AttributeError:
        logging.error(f"Could not match a state or territory name from file {file}")

    street_locality_df = pd.read_csv(file, delimiter="|")
    street_locality_df.set_index("STREET_LOCALITY_PID", inplace=True)
    street_locality_dict[state_or_territory] = street_locality_df.to_dict(
        orient="index"
    )
