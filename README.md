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
