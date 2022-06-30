const fs = require("fs");
const path = require("path");
const https = require("https");
const axios = require("axios");

const ES_URL = `https://${process.env.ES_URL}:${process.env.ES_PORT}`;
const SEARCH_ENDPOINT_URL = `${ES_URL}/${process.env.ES_INDEX_NAME}/_search`;

const httpsAgent = new https.Agent({
  ca: fs.readFileSync(path.join(__dirname, "../../ca.crt")),
});

const axiosInstance = axios.create({
  baseURL: SEARCH_ENDPOINT_URL,
  httpsAgent: httpsAgent,
  headers: {
    Authorization: `Basic ${Buffer.from(
      process.env.ELASTIC_USER + ":" + process.env.ELASTIC_PASSWORD
    ).toString("base64")}`,
  },
});

async function searchAddress(searchText) {
  const response = await axiosInstance.post("/", {
    from: 0,
    size: 5,
    query: {
      match: {
        body: searchText,
      },
    },
  });
  return response.data;
}

module.exports = searchAddress;
