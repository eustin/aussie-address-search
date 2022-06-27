require("dotenv").config();
const http = require("http");
const app = require("./app");

const PORT = process.env.NODE_PORT || 8000;

const server = http.createServer(app);

server.listen(PORT, () => {
  console.log(`Listening on port ${PORT}`);
});
