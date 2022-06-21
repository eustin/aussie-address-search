import os
import dotenv
from elasticsearch import Elasticsearch

dotenv.load_dotenv()

es_client = Elasticsearch(
    "https://localhost:9200",
    ca_certs="ca.crt",
    basic_auth=("elastic", os.environ["ELASTIC_PASSWORD"]),
)

resp = es_client.info()
print(resp)
