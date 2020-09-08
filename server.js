const express = require("express");
const app = express();
app.set("view engine", "pug");
app.use(express.static(__dirname + "/public"));
app.listen(9876);

// routes
app.get("/", (req, res) => {
  res.render("index", {
    page: "index",
    title: "Home",
  });
});
app.get("/tool", (req, res) => {
  res.render("tool", {
    page: "tool",
    title: "Tool",
  });
});
app.get("/recommendation", (req, res) => {
  const dataset = require("./data/cookstr-data.json");
  const childProcess = require("child_process");
  const command = "python py-calculate-similarity.py";
  console.log("Input:", req.query.input);
  const python = childProcess.spawnSync(command, [req.query.input], {
    shell: true,
  });
  output = python.stdout.toString();
  output = output.slice(0, 4);
  console.log("Output:", output);
  const recipe = dataset.find((p) => p.id === +output);
  res.render("recommendation", {
    page: "recommendation",
    title: "Recommendation",
    recipe: recipe,
  });
});
