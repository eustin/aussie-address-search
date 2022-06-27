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

def main():
    es_client = Elasticsearch(
        "https://localhost:9200",
        ca_certs="ca.crt",
        basic_auth=("elastic", os.environ["ELASTIC_PASSWORD"]),
    )

    address_files = glob("data/address_file_*.csv")

    def address_generator(file_path):
        csv_reader = csv.DictReader(open(file_path))
        for row in csv_reader:
            yield {
                "_id": row["ADDRESS_DETAIL_PID"],
                "_index": "addresses",
                "body": f'{row["STREET_NAME"]} {row["STREET_TYPE_CODE"]}, {row["LOCALITY_NAME"]}' 
            }

    for file in address_files:
        logger.info(f"loading file into elasticsearch: {file}")    
        deque(parallel_bulk(es_client, address_generator(file)), maxlen=0)

if __name__ == "__main__":
    main()
