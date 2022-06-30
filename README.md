# Aussie Address Search
A React + Express + Python project using Elasticsearch to search the [Geocoded National Address File](https://data.gov.au/dataset/ds-dga-19432f89-dc3a-4ef3-b943-5326ef1dbecc/details).

## Motivation

For some applications, you don't need the Rolls-Royce of address data. One would hope that a database of `15.2 million addresses` that are `independently examined and validated` would be good enough! 

There are several address search providers out there that you have to pay a lot for per search request. I hope that this project gives you enough to get started in creating your own (cheaper) address search service! 

## The G-NAF End User Licence Agreement

Please refer to the EULA found [here](https://data.gov.au/dataset/ds-dga-19432f89-dc3a-4ef3-b943-5326ef1dbecc/distribution/dist-dga-09f74802-08b1-4214-a6ea-3591b2753d30/details?q=). At the time of writing, the G-NAF data set is covered by the Creative Commons Attribution 4.0 International license. 

The main usage restriction is this:

```
You must not use the Licensed Material for the generation of an
address or a compilation of addresses for the sending of mail unless You have
verified that each address to be used for the sending of mail is capable of receiving
mail by reference to a secondary source of information other than the Licensed
Material. 
```

## Current state

<img src="https://user-images.githubusercontent.com/6435319/176627680-80ce7e4a-3b71-433b-bc86-a44209ae38b5.gif" width=1000>

### Done

* Elasticsearch running in Docker
* Bash and Python sripts to download and process G-NAF data located in `server/scripts`
* Node.js server + Express app as backend
* React frontend 
* Beautiful Wombat image credit goes to <a href="https://www.vecteezy.com/free-vector/nature">Nature Vectors by Vecteezy</a>

### To do

* Throttle API requests to search endpoint
* Styling
* Backend API tests
* Backend API logging
* Node HTTPS webserver
* Serve React app build from Node server 
* Create Elasticsearch cluster
* Tune Elasticsearch suggestions performance 
* Dockerise and deploy!


## How to run this project

These Makefile targets have been deliberately split up so that you can run specific parts of it at your will.

### 1. Set up env vars

In the root of this repo:

1. `make .envs`. This will create `.env` files in `client/` and `server/`
2. In `server/.env` Fill out `ELASTIC_PASSWORD` and `KIBANA_PASSWORD`.

### 2. Download and build G-NAF files

`make setup-gnaf`

### 3. Optional steps to take before setting up Elasticsearch and Kibana

    1. Set `vm.max_map_count` to a higher value (see the Troubleshooting section, below)
    2. If running Windows, make sure your `KIBANA_PORT` is available (see Troubleshooting section, below)

### 4. Set up and load data into Elasticsearch index

Run `make setup-elastic`

Once Kibana starts running and you want to check it out, visit `localhost:${KIBANA_PORT}` and login with the username `elastic` and password `${ELASTIC_PASSWORD}` as defined in your `.env` file. 

### 5. Install server and React app

Run `make install`

### 6. Run the stack

Run `make deploy`

This will start the Node server on `http://localhost:8000`.

## Bringing down the stack

Run `make down`

## Making requests to the Elasticsearch using Postman

The base URL to make POST requests to when developing locally is this:

`https://localhost:{ELASTIC_SEARCH_PORT}/addresses/_search`

Before making requests to the above endpoint, you will need to:
* load the CA certificate into Postman at `Settings -> Certificates`
* pass your credentials in `Authorization -> Basic Auth`

Here is an example request you can make to the above endpoint:

```
{
    "query": {
        "match": {
            "body": "SUNSHINE PARADE"
        }
    }
}
```

## Notes on the `docker-compose` file

Most of the `docker-compose.yml` file comes from [this link](https://www.elastic.co/guide/en/elasticsearch/reference/current/docker.html).

## Troubleshooting

### vm.max_map_count is too low

After issuing `docker-compose up`, you might see an error like this: 

```max virtual memory areas vm.max_map_count [65530] is too low, increase to at least [262144]```

See [this link](https://www.elastic.co/guide/en/elasticsearch/reference/current/vm-max-map-count.html) on how to resolve it. 

### An attempt was made to access a socket in a way forbidden by its access permissions

Another error you might see after running `docker-compose up` is something like this:

```Ports are not available: exposing port TCP 0.0.0.0:5601 -> 0.0.0.0:0: listen tcp 0.0.0.0:5601: bind: An attempt was made to access a socket in a way forbidden by its access permissions```

If you're running Windows with WSL2 like I am, run this command to see port exclusion ranges:

```netsh int ipv4 show excludedportrange protocol=tcp```

Choose a port that falls outside of these ranges and update the `KIBANA_PORT` environment variable in your `.env` file. 
