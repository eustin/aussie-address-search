# aussie-address-search
A (maybe) Python + React project (probably) using Elasticsearch to search the [Geocoded National Address File](https://data.gov.au/dataset/ds-dga-19432f89-dc3a-4ef3-b943-5326ef1dbecc/details).

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

## How to run the stack

In the root of this repo:

1. Run `cp .env.template .env`
2. In the `.env` file, fill out the `ELASTIC_PASSWORD` and `KIBANA_PASSWORD` environment variables
3. (optional) Set `vm.max_map_count` to a higher value (see the Troubleshooting section, below)
4. (optional) If running Windows, make sure your `KIBANA_PORT` is available
4.  Run `docker-compose up`

Once Kibana starts running, visit `localhost:${KIBANA_PORT}` and login with the username `elastic` and password `${ELASTIC_PASSWORD}` as defined in your `.env` file. 

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




