<h1 align="center">
   <a href="https://github.com/ptanmay143/recipe-net">
      <img src="docs/images/logo.svg" alt="Logo" width="100" height="100">
   </a>
</h1>

<div align="center">
   Recipe Net
   <br />
   <a href="#about"><strong>Explore the screenshots »</strong></a>
   <br />
   <br />
   <a href="https://github.com/ptanmay143/recipe-net/issues/new?assignees=&labels=bug&template=01_BUG_REPORT.md&title=bug%3A+">Report a Bug</a>
   ·
   <a href="https://github.com/ptanmay143/recipe-net/issues/new?assignees=&labels=enhancement&template=02_FEATURE_REQUEST.md&title=feat%3A+">Request a Feature</a>
   ·
   <a href="https://github.com/ptanmay143/recipe-net/issues/new?assignees=&labels=question&template=04_SUPPORT_QUESTION.md&title=support%3A+">Ask a Question</a>
</div>

<div align="center">
<br />

[![Project license](https://img.shields.io/github/license/ptanmay143/recipe-net.svg?style=flat-square)](LICENSE)
[![Pull Requests welcome](https://img.shields.io/badge/PRs-welcome-ff69b4.svg?style=flat-square)](https://github.com/ptanmay143/recipe-net/issues?q=is%3Aissue+is%3Aopen+label%3A%22help+wanted%22)
[![code with love by ptanmay143](https://img.shields.io/badge/%3C%2F%3E%20with%20%E2%99%A5%20by-ptanmay143-ff1414.svg?style=flat-square)](https://github.com/ptanmay143)

</div>

<details open="open">
<summary>Table of Contents</summary>

- [About](#about)
  - [Built With](#built-with)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [Usage](#usage)
- [Roadmap](#roadmap)
- [Support](#support)
- [Project Assistance](#project-assistance)
- [Contributing](#contributing)
- [Authors & contributors](#authors--contributors)
- [Security](#security)
- [License](#license)
- [Acknowledgements](#acknowledgements)

</details>

---

## About

Recipe Net is an ingredient-driven recipe recommendation web application. Instead of searching by dish name, users choose ingredients they currently have, and the system ranks recipes based on semantic similarity between selected ingredients and a preprocessed recipe corpus.

The application targets practical cooking discovery with minimal interaction complexity: open the site, pick ingredients, and receive one high-confidence recommended recipe including title, ingredient list, instructions, and image.

At runtime, the Node.js/Express server handles page routing and orchestrates recommendation requests. For each recommendation call, it executes a Python similarity script (`py-calculate-similarity.py`) that loads previously generated TF-IDF artifacts and computes cosine similarity against all recipe vectors.

The recommendation quality depends on a preprocessing pipeline that converts raw Cookstr data into normalized ingredients (`cookstr-data.json`), corpus mapping (`cookstr-corpus.json`), and serialized vectorization assets (`tf_idf.pickle`, `tf_idf_matrix.pickle`). This batch step is intended as one-time setup or refresh whenever source data changes.

<details>
<summary>Screenshots</summary>
<br>

Add screenshots under `docs/images/` and update this table for visual documentation.

|                               Home Page                               |                               Recommendation                               |
| :-------------------------------------------------------------------: | :------------------------------------------------------------------------: |
| <img src="docs/images/screenshot.png" title="Home Page" width="100%"> | <img src="docs/images/screenshot.png" title="Recommendation" width="100%"> |

</details>

### Built With

- **Node.js + Express** — web server and route handling.
- **Pug** — server-side templating for `index`, `tool`, and `recommendation` views.
- **Python 3** — data preprocessing and similarity scoring scripts.
- **scikit-learn** — TF-IDF vectorization and cosine similarity.
- **NumPy** — argmax selection of top similarity result.
- **Bootstrap / jQuery / Select2** — front-end styling and ingredient selection UI.

---

## Getting Started

Setup includes both JavaScript and Python dependencies plus one-time data artifact generation. Once artifacts exist, normal development requires only starting the Node server.

### Prerequisites

- **Node.js** — compatible with this project’s dependency set (`express@4`, `pug@3`, `body-parser@1`).
- **Python 3** — required for preprocessing and runtime recommendation scripts.
- **pip** — to install `scikit-learn`.
- **Cookstr raw dataset file** — `data/cookstr-recipes.json` is expected by preprocessing script.

### Installation

1. Clone the repository.

```bash
git clone https://github.com/ptanmay143/recipe-net.git
```

2. Enter the project folder.

```bash
cd recipe-net
```

3. Install Node dependencies.

```bash
npm install
```

4. Install Python dependencies.

```bash
pip install -r requirements.txt
```

5. Place raw data file.

```text
Expected path: data/cookstr-recipes.json
```

6. Generate processed dataset and corpus.

```bash
python py-data-preprocess.py
```

7. Generate TF-IDF artifacts.

```bash
python py-calculate-tf-idf.py
```

8. Start the web server.

```bash
npm start
```

9. Verify setup.

```text
Open http://localhost:9876 and navigate to /tool, select ingredients,
then confirm recommendation page renders recipe details.
```

### Environment Variables

No environment variables are read in current source.

| Variable | Required | Default | Description                                         | Example Value |
| -------- | -------- | ------- | --------------------------------------------------- | ------------- |
| None     | No       | N/A     | Configuration currently uses hard-coded paths/port. | N/A           |

---

## Usage

Start server:

```bash
npm start
```

Open application:

```text
http://localhost:9876
```

Important user-facing routes:

- `GET /` — landing page.
- `GET /tool` — ingredient selection interface.
- `GET /recommendation?input=<comma-separated-ingredient-ids>` — renders selected best-match recipe.

Example recommendation request:

```text
GET /recommendation?input=0,5,10
```

Pipeline command usage examples:

```bash
python py-data-preprocess.py
python py-calculate-tf-idf.py
python py-calculate-similarity.py 0,5,10
```

Expected similarity script output:

```text
A zero-padded 4-digit recipe ID (e.g., 0123)
```

Runtime data flow:

```text
Browser ingredient IDs -> Express /recommendation -> spawnSync Python script
-> cosine similarity against TF-IDF matrix -> best recipe ID -> lookup in cookstr-data.json
-> render recommendation.pug
```

Operational notes:

- Server listens on port `9876` (`app.listen(9876)`).
- Recommendation endpoint uses shell-enabled child process invocation.
- Output parsing currently slices first 4 characters, implying an implicit recipe ID formatting assumption.

---

## Roadmap

See the [open issues](https://github.com/ptanmay143/recipe-net/issues) for a full list of proposed features and known bugs.

- [Top Feature Requests](https://github.com/ptanmay143/recipe-net/issues?q=label%3Aenhancement+is%3Aopen+sort%3Areactions-%2B1-desc) (Add your votes using the 👍 reaction)
- [Top Bugs](https://github.com/ptanmay143/recipe-net/issues?q=is%3Aissue+is%3Aopen+label%3Abug+sort%3Areactions-%2B1-desc) (Add your votes using the 👍 reaction)
- [Newest Bugs](https://github.com/ptanmay143/recipe-net/issues?q=is%3Aopen+is%3Aissue+label%3Abug)

Likely next improvements include input validation and safer process invocation for `/recommendation`, performance optimization to avoid per-request Python process spawning, and richer recommendation outputs (top-N results rather than single best match).

---

## Support

Reach out to the maintainer at one of the following places:

- [GitHub issues](https://github.com/ptanmay143/recipe-net/issues/new?assignees=&labels=question&template=04_SUPPORT_QUESTION.md&title=support%3A+)
- Contact options listed on [this GitHub profile](https://github.com/ptanmay143)

---

## Project Assistance

If you want to say **thank you** or support active development of Recipe Net:

- Add a [GitHub Star](https://github.com/ptanmay143/recipe-net) to the project.
- Share benchmark results or dataset improvements with maintainers.
- Publish usage demos showing real ingredient-to-recipe scenarios.

Together, we can make Recipe Net **better**!

---

## Contributing

First off, thanks for taking the time to contribute! Contributions are what make the open-source community such an amazing place to learn, inspire, and create.

Recommended workflow:

1. Fork and create a feature branch.
2. Apply focused changes to either server, preprocessing, or UI layers.
3. Rebuild data artifacts if your change impacts corpus/vectorization.
4. Validate route behavior locally.
5. Open a pull request with reproducible steps.

No dedicated `docs/CONTRIBUTING.md` is currently present.

---

## Authors & Contributors

The original setup of this repository is by [Tanmay Pachpande](https://github.com/ptanmay143).

For a full list of all authors and contributors, see [the contributors page](https://github.com/ptanmay143/recipe-net/contributors).

---

## Security

Recipe Net follows good practices of security, but 100% security cannot be assured. Recipe Net is provided **"as is"** without any **warranty**. Use at your own risk.

Known security-sensitive area in current implementation: `/recommendation` uses shell-enabled process execution with user-provided query input; validate and sanitize before production exposure.

---

## License

This project is licensed under the **MIT License**.

See [LICENSE](LICENSE) for more information.

---

## Acknowledgements

- scikit-learn community for mature text vectorization tooling.
- Express and Pug maintainers for simple full-stack web composition.
- Cookstr data source and open recipe-data ecosystem.

<!-- Generated by README_GENERATOR_PROMPT v0.1 -->
