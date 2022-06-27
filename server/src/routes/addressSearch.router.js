const express = require("express");

const addressSearchRouter = express.Router();

addressSearchRouter.post("/", (req, res) => {
  return res.status(200).json({
    message: "success!"
  })
});

module.exports = addressSearchRouter;
