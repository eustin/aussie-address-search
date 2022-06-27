const express = require("express");
const cors = require("cors");
const addressSearchRouter = require("./routes/addressSearch.router");

const app = express();
app.use(express.json());
app.use(cors({ origin: "http://localhost3000" }));

app.use("/search", addressSearchRouter);

module.exports = app;
