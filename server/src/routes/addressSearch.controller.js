const searchAddress = require("../models/addressSearch.model");

async function httpSearchForAddress(req, res) {
  const address = req.body;
  if (!address.searchInput) {
    return res.status(400).json({
      error: "Missing searchInput property",
    });
  }

  const results = await searchAddress(address.searchInput);

  return res.status(200).json({
    message: results,
  });
}

module.exports = httpSearchForAddress;
