const searchAddress = require("../models/addressSearch.model");

async function httpSearchForAddress(req, res) {
  const address = req.body;

  if (!address.searchInput) {
    return res.status(400).json({
      error: "Missing searchInput property",
    });
  }

  const results = await searchAddress(address.searchInput);
  const hits = results.hits?.hits;

  const suggestions = hits
    ? hits.map((hit) => ({
        id: hit._id,
        suggestion: hit._source.body,
      }))
    : [];

  return res.status(200).json({ suggestions });
}

module.exports = httpSearchForAddress;
