import logging
from glob import glob
from pathlib import Path
import re
import pandas as pd

STATES_TERRITORIES = ["ACT", "NSW", "NT", "QLD", "SA", "TAS", "VIC", "WA"]

ADDRESS_DETAIL_TARGET_FIELDS = [
    "ADDRESS_DETAIL_PID",
    "BUILDING_NAME",
    "LOT_NUMBER_PREFIX",
    "LOT_NUMBER",
    "LOT_NUMBER_SUFFIX",
    "FLAT_TYPE_CODE",
    "FLAT_NUMBER_PREFIX",
    "FLAT_NUMBER",
    "FLAT_NUMBER_SUFFIX",
    "LEVEL_TYPE_CODE",
    "LEVEL_NUMBER_PREFIX",
    "LEVEL_NUMBER",
    "LEVEL_NUMBER_SUFFIX",
    "NUMBER_FIRST_PREFIX",
    "NUMBER_FIRST",
    "NUMBER_FIRST_SUFFIX",
    "NUMBER_LAST_PREFIX",
    "NUMBER_LAST",
    "NUMBER_LAST_SUFFIX",
    "STREET_LOCALITY_PID",
    "LOCALITY_PID",
    "POSTCODE",
]

STREET_LOCALITY_TARGET_FIELDS = [
    "STREET_LOCALITY_PID",
    "STREET_NAME",
    "STREET_TYPE_CODE",
    "STREET_SUFFIX_CODE",
]

LOCALITY_TARGET_FIELDS = ["LOCALITY_PID", "LOCALITY_NAME"]

logging.basicConfig(level="INFO")
logger = logging.getLogger(__name__)


def create_file_map(fpath_list, sate_pattern):
    states_list = [re.search(sate_pattern, x).group() for x in fpath_list]
    return {k: v for k, v in zip(states_list, fpath_list)}

def check_dirs_exist(parent_path, child_dir):
    try:
        dir_to_check = parent_path / child_dir
        assert dir_to_check.exists()
        return dir_to_check
    except AssertionError:
        logging.error(f"{dir_to_check.as_posix()} doesn't exist")
        raise

def df_from_pipe_delimited_file(fpath):
    return pd.read_csv(fpath, delimiter="|")

def create_locality_dict(gnaf_standard_dir):
    locality_files = glob((gnaf_standard_dir / "*LOCALITY_psv.psv").as_posix())
    locality_files = [x for x in locality_files if "STREET" not in x]
    locality_dict = create_file_map(locality_files, "(?<=\/)[A-Z]+(?=_LOCALITY_psv.psv)")
    return locality_dict

def create_street_locality_detail_dict(gnaf_standard_dir):
    street_locality_files = glob((gnaf_standard_dir / "*_STREET_LOCALITY_psv.psv").as_posix())
    street_locality_dict = create_file_map(street_locality_files, "(?<=\/)[A-Z]+(?=_STREET_LOCALITY_psv.psv)")
    return street_locality_dict

def create_address_detail_dict(gnaf_standard_dir):
    address_detail_files = glob((gnaf_standard_dir / "*_ADDRESS_DETAIL_psv.psv").as_posix())
    address_detail_dict = create_file_map(address_detail_files, "(?<=\/)[A-Z]+(?=_ADDRESS_DETAIL_psv.psv)")
    return address_detail_dict

def create_level_type_df(gnaf_auth_code_dir):
    level_type_file = glob((gnaf_auth_code_dir / "Authority_Code_LEVEL_TYPE_AUT_psv.psv").as_posix()).pop()
    level_type_df = pd.read_csv(level_type_file, delimiter="|").drop(columns="DESCRIPTION")
    return level_type_df

def create_address_df(details_df, street_locality_df, locality_df):
    logging.info(f"merging files")
    try:
        address_df = pd.merge(details_df, street_locality_df, on="STREET_LOCALITY_PID", how="inner")
        address_df = pd.merge(address_df, locality_df, on="LOCALITY_PID", how="inner")
        assert address_df.shape[0] == details_df.shape[0]
        return address_df
    except AssertionError:
        logging.error("Number of rows in address dataframe rows don't match number of rows in address detail")
        raise


def main():
    try:
        gnaf_dir = Path(glob("data/G-NAF/G-NAF*").pop())
    except IndexError:
        logging.error("GNAF data directory doesn't exist")
        raise

    gnaf_standard_dir = check_dirs_exist(gnaf_dir, "Standard")
    gnaf_auth_code_dir = check_dirs_exist(gnaf_dir, "Authority Code")

    address_detail_dict = create_address_detail_dict(gnaf_standard_dir)
    street_locality_dict = create_street_locality_detail_dict(gnaf_standard_dir)
    locality_dict = create_locality_dict(gnaf_standard_dir)
    level_type_df = create_level_type_df(gnaf_auth_code_dir)

    for state, details_fpath in address_detail_dict.items():
        logging.info(f"processing {state}")
        street_locality_fpath = street_locality_dict[state]
        locality_fpath = locality_dict[state]

        logging.info(f"reading details file: {details_fpath}")
        details_df = df_from_pipe_delimited_file(details_fpath)[
            ADDRESS_DETAIL_TARGET_FIELDS
        ]

        logging.info(f"reading street locality file: {street_locality_fpath}")
        street_locality_df = df_from_pipe_delimited_file(street_locality_fpath)[
            STREET_LOCALITY_TARGET_FIELDS
        ]

        logging.info(f"reading locality file: {locality_fpath}")
        locality_df = df_from_pipe_delimited_file(locality_fpath)[
            LOCALITY_TARGET_FIELDS
        ]

        address_df = create_address_df(details_df, street_locality_df, locality_df)

        out_path = f"data/address_file_{state}.csv"
        logging.info(f"saving CSV file to {out_path}")
        address_df.to_csv(out_path, index=False)


if __name__ == "__main__":
    main()
