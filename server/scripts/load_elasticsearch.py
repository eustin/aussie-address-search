import os
import dotenv
from glob import glob
import logging
import csv
from collections import deque
from elasticsearch import Elasticsearch
from elasticsearch.helpers import parallel_bulk

dotenv.load_dotenv()
logging.basicConfig(level="INFO")
logger = logging.getLogger(__name__)


def convert_string_float_to_string_int(float_string):
    if not float_string:
        return ""
    error_message = f"Error converting {float_string} to int"
    try:
        num = float(float_string)
        return str(int(num))
    except ValueError as e:
        logging.info(error_message, e)
        raise
    except TypeError as e:
        logging.info(error_message, e)
        raise


def create_address(row):
    address_components = []
    address_components = add_building_name(row, list(address_components))
    address_components = add_flat_details(row, list(address_components))
    address_components = add_level_details(row, list(address_components))
    address_components = add_number_details(row, list(address_components))
    address_components = add_street_details(row, list(address_components))
    address_components = add_locality(row, list(address_components))
    address_components = add_postcode(row, list(address_components))
    return "".join(list(address_components))


def add_building_name(row, address_components):
    address_components.append(row["BUILDING_NAME"])
    if len(row["BUILDING_NAME"]) > 0:
        address_components.append(", ")
    return address_components


def add_flat_details(row, address_components):
    address_components.append(row["FLAT_TYPE_CODE"])

    if len(row["FLAT_TYPE_CODE"]) > 0:
        address_components.append(" ")

    address_components.append(row["FLAT_NUMBER_PREFIX"])
    try:
        flat_number = convert_string_float_to_string_int(row["FLAT_NUMBER"])
        address_components.append(flat_number)
    except ValueError:
        pass
    
    address_components.append(row["FLAT_NUMBER_SUFFIX"])
    if len(row["FLAT_TYPE_CODE"]) > 0:
        address_components.append(" ")

    return address_components


def add_level_details(row, address_components):
    if len(row["LEVEL_TYPE_CODE"]):
        address_components.extend([row["LEVEL_TYPE_CODE"], " "])
    address_components.append(row["LEVEL_NUMBER_PREFIX"])

    try:
        level_number = convert_string_float_to_string_int(row["LEVEL_NUMBER"])
        address_components.append(level_number)
    except ValueError:
        pass
    address_components.append(row["LEVEL_NUMBER_SUFFIX"])

    if row["LEVEL_NUMBER"] != "":
        address_components.append(" ")
    
    return address_components



def add_number_details(row, address_components):
    address_components.append(row["NUMBER_FIRST_PREFIX"])
    try:
        level_number = convert_string_float_to_string_int(row["NUMBER_FIRST"])
        address_components.append(level_number)
    except ValueError as e:
        logging.info("Error adding NUMBER_FIRST", e)

    address_components.append(row["NUMBER_FIRST_SUFFIX"])
    if row["NUMBER_LAST_PREFIX"] != "" or row["NUMBER_LAST"] != "" or row["NUMBER_LAST_SUFFIX"] != "":
        address_components.append("-")

    address_components.append(row["NUMBER_LAST_PREFIX"])
    try:
        number_last = convert_string_float_to_string_int(row["NUMBER_LAST"])
        address_components.append(number_last)
    except ValueError:
        pass

    address_components.append(row["NUMBER_LAST_SUFFIX"])
    if row["NUMBER_FIRST"]:
        address_components.append(" ")

    return address_components


def add_street_details(row, address_components):
    if not row["STREET_NAME"] and not row["STREET_TYPE_CODE"]:
        return address_components
    address_components.append(row["STREET_NAME"])
    if row["STREET_TYPE_CODE"]:
        address_components.extend([" ", row["STREET_TYPE_CODE"]])
    address_components.append(", ")

    return address_components


def add_locality(row, address_components):
    address_components.append(row["LOCALITY_NAME"])
    if row["LOCALITY_NAME"]:
        address_components.append(", ")

    return address_components


def add_postcode(row, address_components):
    try:
        postcode = convert_string_float_to_string_int(row["POSTCODE"])
        address_components.append(postcode)
    except ValueError:
        logging.error(f'Cannot coerce {row["POSTCODE"]} to number')

    return address_components


def address_generator(file_path):
    csv_reader = csv.DictReader(open(file_path))
    for row in csv_reader:
        address_string = create_address(row)

        yield {
            "_id": row["ADDRESS_DETAIL_PID"],
            "_index": "addresses",
            "body": address_string,
            "type": "completion"
        }


def create_elastic_client():
    return Elasticsearch(
        f'https://localhost:{os.environ["ES_PORT"]}',
        ca_certs="ca.crt",
        basic_auth=(os.environ["ELASTIC_USER"],
                    os.environ["ELASTIC_PASSWORD"]),
    )


def main():
    es_client = create_elastic_client()
    address_files = glob("data/address_file_*.csv")

    for file in address_files:
        logger.info(f"loading file into elasticsearch: {file}")
        deque(parallel_bulk(es_client, address_generator(file)), maxlen=0)


if __name__ == "__main__":
    main()
