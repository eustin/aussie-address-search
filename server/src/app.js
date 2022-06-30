const path = require("path");
const express = require("express");
const cors = require("cors");
const addressSearchRouter = require("./routes/addressSearch.router");

const app = express();
app.use(express.json());
app.use(express.static(path.join(__dirname, "..", "public")));
app.use(cors({ origin: "http://localhost:8000" }));

app.use("/search", addressSearchRouter);
app.get("/*", (req, res) => {
  res.sendFile(path.join(__dirname, "..", "public", "index.html"));
});

module.exports = app;
