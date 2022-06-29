from multiprocessing.sharedctypes import Value
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


def create_address(row):
    address_components = []
    add_building_name(row, address_components)
    add_flat_details(row, address_components)
    add_level_details(row, address_components)
    add_number_details(row, address_components)
    add_street_details(row, address_components)
    add_locality(row, address_components)
    add_postcode(row, address_components)
    return "".join(address_components)


def add_building_name(row, address_components):
    address_components.append(row["BUILDING_NAME"])
    if len(row["BUILDING_NAME"]) > 0:
        address_components.append(", ")


def add_flat_details(row, address_components):
    address_components.append(row["FLAT_TYPE_CODE"])

    if len(row["FLAT_TYPE_CODE"]) > 0:
        address_components.append(" ")

    address_components.append(row["FLAT_NUMBER_PREFIX"])
    try:
        address_components.append(str(int(row["FLAT_NUMBER"])))
    except ValueError:
        pass

    address_components.append(row["FLAT_NUMBER_SUFFIX"])
    if len(row["FLAT_TYPE_CODE"]) > 0:
        address_components.append(" ")


def add_level_details(row, address_components):
    if len(row["LEVEL_TYPE_CODE"]):
        address_components.extend([row["LEVEL_TYPE_CODE"], " "])
    address_components.append(row["LEVEL_NUMBER_PREFIX"])

    try:
        address_components.append(str(int(row["LEVEL_NUMBER"])))
    except ValueError:
        pass
    address_components.append(row["LEVEL_NUMBER_SUFFIX"])

    if row["LEVEL_NUMBER"] != "":
        address_components.append(" ")


def add_number_details(row, address_components):
    address_components.append(row["NUMBER_FIRST_PREFIX"])
    try:
        address_components.append(str(int(row["NUMBER_FIRST"])))
    except ValueError:
        pass

    address_components.append(row["NUMBER_FIRST_SUFFIX"])
    if row["NUMBER_LAST_PREFIX"] != "" or row["NUMBER_LAST"] != "" or row["NUMBER_LAST_SUFFIX"] != "":
        address_components.append("-")

    address_components.append(row["NUMBER_LAST_PREFIX"])
    try:
        address_components.append(str(int(row["NUMBER_LAST"])))
    except ValueError:
        pass

    address_components.append(row["NUMBER_LAST_SUFFIX"])
    if row["NUMBER_FIRST"]:
        address_components.append(" ")


def add_street_details(row, address_components):
    if not row["STREET_NAME"] and not row["STREET_TYPE_CODE"]:
        return
    address_components.extend([row["STREET_NAME"],
                              " ", row["STREET_TYPE_CODE"], ", ", ])


def add_locality(row, address_components):
    address_components.append(row["LOCALITY_NAME"])
    if row["LOCALITY_NAME"]:
        address_components.append(", ")


def add_postcode(row, address_components):
    try:
        address_components.append(str(int(row["POSTCODE"])))
    except ValueError:
        logging.error(f'Cannot coerce {row["POSTCODE"]} to number')


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
        # TODO: remove dev code
        if file != "data/address_file_NT.csv":
            continue
        logger.info(f"loading file into elasticsearch: {file}")
        deque(parallel_bulk(es_client, address_generator(file)), maxlen=0)


if __name__ == "__main__":
    main()
