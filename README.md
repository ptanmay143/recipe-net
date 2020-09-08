# Recipe Net

This is a website that will recommend the closest recipe that a user can make using the ingredients that are available. It provides a way for the user to select the ingredients that are available.

It uses Node.js to serve the website and uses Python for the backend.

## Requirements

- Python
- Node.js

## Usage

- Preprocess the dataset.

  ```shell
  python py-data-preprocess.py
  ```

- Calculate the term frequency and inverse document frequency scores.

  ```shell
  python py-calculate-tf-idf.py
  ```

- Start the webserver.

  ```shell
  node server.js
  ```

- Access the website on port `9876`.
