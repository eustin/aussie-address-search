const express = require("express");
const httpSearchForAddress = require("./addressSearch.controller");

const addressSearchRouter = express.Router();

addressSearchRouter.post("/", httpSearchForAddress);

module.exports = addressSearchRouter;
