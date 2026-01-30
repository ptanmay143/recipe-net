# recipe-net

> Find recipes based on ingredients you have at home

RecipeNet is a web application that recommends recipes using machine learning. Select your available ingredients from a dropdown, and the system finds the best matching recipe using TF-IDF vectorization and cosine similarity.

## Usage

**Quick Start:**

```bash
npm start
# Server listening on port 9876
```

Open `http://localhost:9876` in your browser:

1. Click "Go to Tool"
2. Select ingredients from the dropdown (e.g., tomato, basil, garlic)
3. Click "Get Recommendation!"
4. View the best matching recipe with ingredients, instructions, and photo

**Example:**
```
User selects: tomato, basil, garlic, olive oil
         ↓
System matches against 5000+ recipes
         ↓
Returns: "Tomato Basil Pasta" with full details
```

## Installation

**Prerequisites:**
- Node.js 12+
- Python 3.6+
- Git

**Steps:**

```bash
# Clone repository
git clone https://github.com/ptanmay143/recipe-net.git
cd recipe-net

# Install dependencies
npm install
pip install -r requirements.txt

# Obtain the CookStr dataset
# Place the dataset at: data/cookstr-recipes.json
# (Publicly available from research sources)

# Process the data (one-time setup)
python py-data-preprocess.py
python py-calculate-tf-idf.py

# Start the server
npm start
```

Visit `http://localhost:9876` to use the application.

## API

### Routes

**`GET /`**
- Returns the home page

**`GET /tool`**
- Returns the ingredient selection page
- Dropdown populated with ~5000 ingredients from corpus

**`GET /recommendation?input=<ids>`**
- Returns recipe recommendation page
- Parameters:
  - `input` (string): Comma-separated ingredient IDs (e.g., "0,5,12")
- Spawns Python subprocess to compute similarity
- Renders recipe with title, ingredients, instructions, and photo

### Python Scripts

**`py-data-preprocess.py`**
- Reads `data/cookstr-recipes.json`
- Extracts and normalizes ingredients
- Outputs: `cookstr-data.json`, `cookstr-corpus.json`

**`py-calculate-tf-idf.py`**
- Vectorizes recipes using TF-IDF
- Outputs: `tf_idf.pickle`, `tf_idf_matrix.pickle`

**`py-calculate-similarity.py <ingredient_ids>`**
- Takes comma-separated ingredient IDs as argument
- Computes cosine similarity with all recipes
- Returns recipe ID with highest similarity score

## How It Works

The system uses a three-layer architecture:

1. **Browser Frontend** (Pug templates + Bootstrap)
   - Multi-select dropdown for ingredient selection
   - Sends selected ingredient IDs to server

2. **Express Server** (Node.js)
   - Serves web pages
   - Spawns Python subprocess for similarity computation
   - Looks up and renders recipe details

3. **ML Pipeline** (Python + scikit-learn)
   - Loads pre-computed TF-IDF vectors
   - Calculates cosine similarity between user ingredients and recipes
   - Returns best matching recipe ID

**Algorithm:** Given user ingredient selections, compute cosine similarity between user ingredient vector and pre-computed recipe ingredient vectors to identify the best matching recipe.

## Background

RecipeNet was created to solve a common problem: "What can I cook with the ingredients I have?" Traditional recipe search requires knowing what dish you want to make. This system flips that approach by starting with ingredients and finding the best matching recipes.

The system uses **TF-IDF (Term Frequency-Inverse Document Frequency)** to represent recipes as vectors in ingredient space, then uses **cosine similarity** to find recipes that best match the user's available ingredients. This approach is computationally efficient and provides good results for ingredient-based matching.

## Configuration

**Server Port:** Default is 9876. Change in `server.js`:
```javascript
app.listen(9876);  // Change this number
```

**Data Directory:** Default is `./data/`. Update paths in Python scripts and `server.js` if needed.

**Production Deployment:**
```bash
# Using pm2
npm install -g pm2
pm2 start server.js --name recipe-net

# Using Docker
docker build -t recipe-net .
docker run -p 9876:9876 recipe-net
```

## Development

### Code Structure

- `server.js` (37 lines) - Express server with 3 routes
- `py-data-preprocess.py` (62 lines) - Extract and normalize ingredients
- `py-calculate-tf-idf.py` (47 lines) - Compute TF-IDF vectors
- `py-calculate-similarity.py` (48 lines) - Calculate cosine similarity
- `views/` - Pug templates for frontend
- `public/` - Static assets

### Dependencies

**Node.js:**
- express - Web framework
- pug - Template engine  
- body-parser - Request parsing

**Python:**
- scikit-learn - TF-IDF and cosine similarity

**Frontend (CDN):**
- Bootstrap 4.4.1
- jQuery 3.4.1
- Select2 4.0.13

### Testing

```bash
# Test data preprocessing
python py-data-preprocess.py
# Verify: cookstr-data.json and cookstr-corpus.json created

# Test TF-IDF computation
python py-calculate-tf-idf.py
# Verify: tf_idf.pickle and tf_idf_matrix.pickle created

# Test similarity calculation
python py-calculate-similarity.py "0,5,10"
# Expected: 4-digit recipe ID

# Test web server
npm start
# Open http://localhost:9876
```

## Known Issues

- **Security:** Command injection risk in subprocess spawning (needs input validation)
- **Performance:** Spawns Python process per request (consider caching or microservice)
- **Limitation:** Output parsing assumes recipe ID < 10000
- **Error handling:** Minimal validation and error messages

See [Issues](https://github.com/ptanmay143/recipe-net/issues) for planned improvements.

## Contributing

1. Fork the repository
2. Create feature branch: `git checkout -b feature-name`
3. Make changes and test with `npm start`
4. Submit pull request

## License

MIT © Tanmay Pachpande

See [LICENSE](LICENSE) file for details.
