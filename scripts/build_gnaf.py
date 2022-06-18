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


def main():
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
    address_detail_files = glob(
        (gnaf_standard_dir / "*_ADDRESS_DETAIL_psv.psv").as_posix()
    )
    street_locality_files = glob(
        (gnaf_standard_dir / "*_STREET_LOCALITY_psv.psv").as_posix()
    )
    locality_files = glob((gnaf_standard_dir / "*LOCALITY_psv.psv").as_posix())
    locality_files = [x for x in locality_files if "STREET" not in x]
    level_type_file = glob(
        (gnaf_auth_code_dir / "Authority_Code_LEVEL_TYPE_AUT_psv.psv").as_posix()
    )

    # create hashmaps for smaller datasets to keep them in memory
    logger.info("creating Authority Code LEVEL_TYPE hashmap")
    level_type_df = pd.read_csv(level_type_file.pop(), delimiter="|")
    level_type_dict = {row.CODE: row.NAME for i, row in level_type_df.iterrows()}

    def build_hashmap(fpath_list, state_territory_pattern, primary_key):
        hashmap = {}
        for file in fpath_list:
            logging.info(f"creating hashmap for {file}")
            try:
                state_or_territory = re.search(state_territory_pattern, file).group()
            except AttributeError:
                logging.error(
                    f"Could not match a state or territory name from file {file}"
                )
                raise

            this_df = pd.read_csv(file, delimiter="|")
            this_df.set_index(primary_key, inplace=True)
            hashmap[state_or_territory] = this_df.to_dict(orient="index")
        return hashmap

    street_locality_dict = build_hashmap(
        street_locality_files,
        "(?<=\/)[A-Z]+(?=_STREET_LOCALITY_psv.psv)",
        "STREET_LOCALITY_PID",
    )
    locality_dict = build_hashmap(
        locality_files, "(?<=\/)[A-Z]+(?=_LOCALITY_psv.psv)", "LOCALITY_PID"
    )


if __name__ == "__main__":
    main()
