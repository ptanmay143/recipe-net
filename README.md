# RecipeNet

## Project Title

RecipeNet - Recipe Recommendation System

## Overview

A full-stack web application that recommends recipes based on user-selected ingredients using machine learning. The system combines a Node.js Express web server with a Python ML pipeline to match available ingredients against a recipe corpus using TF-IDF vectorization and cosine similarity. Users select ingredients from a multi-select dropdown and receive the recipe with the highest ingredient similarity score.

**Key Algorithm**: Given user ingredient selections, compute cosine similarity between user ingredient vector and pre-computed recipe ingredient vectors to identify the best matching recipe.

## Architecture Overview

The system consists of three integrated components:

```
┌────────────────────────────────┐
│   Browser Frontend             │
│   HTML/Pug + Bootstrap + jQuery│
│   Select2 dropdown component   │
└───────────────┬────────────────┘
                │ HTTP GET
                ├─ POST /recommendation?input=0,5,12
                │
┌───────────────▼────────────────┐
│   Express.js Server (server.js)│
│   ├─ GET /                     │
│   ├─ GET /tool                 │
│   └─ GET /recommendation       │
│       └─ Spawn Python process  │
└───────────────┬────────────────┘
                │ subprocess.spawnSync()
                │ python py-calculate-similarity.py
                │
┌───────────────▼────────────────┐
│   Python ML Pipeline           │
│   ├─ Load vectorizer pickle    │
│   ├─ Load recipe vector matrix │
│   ├─ Compute cosine similarity │
│   └─ Return recipe ID          │
└───────────────┬────────────────┘
                │ stdout: "0042"
                │
┌───────────────▼────────────────┐
│   Express renders results      │
│   ├─ Lookup recipe in JSON     │
│   ├─ Render recommendation.pug │
│   └─ Return HTML to browser    │
└────────────────────────────────┘
```

**Data Processing Pipeline**:
```
Raw Recipe Dataset
(cookstr-recipes.json)
        ↓
py-data-preprocess.py
├─ Extract ingredients
├─ Normalize text (lowercase, replace spaces)
├─ Build vocabulary
└─ Output: cookstr-data.json, cookstr-corpus.json
        ↓
py-calculate-tf-idf.py
├─ Load processed recipes
├─ Compute TF-IDF vectors
├─ Build recipe matrix
└─ Output: tf_idf.pickle, tf_idf_matrix.pickle
        ↓
Ready for Runtime Inference
```

## Installation and Setup

### Prerequisites

- Python 3.6+
- Node.js 12+
- npm (Node Package Manager)
- Git

### Step 1: Clone Repository

```bash
git clone https://github.com/ptanmay143/recipe-net.git
cd recipe-net
```

### Step 2: Install Dependencies

```bash
# Install Node.js dependencies
npm install

# Install Python dependencies
pip install -r requirements.txt
```

**Installed packages:**
- **Node.js**: express, pug, body-parser
- **Python**: scikit-learn (transitive: numpy, scipy, joblib)

### Step 3: Obtain and Place Raw Data

The raw recipe dataset is not included in the repository. You must obtain it separately:

1. Obtain the CookStr dataset (publicly available from research sources)
2. Place file at: `data/cookstr-recipes.json`
3. Verify JSON Lines format (each line is valid JSON object):

```json
{
  "title": "Recipe Name",
  "ingredients_detailed": [{"ingredients": ["ingredient1", "ingredient2"]}],
  "instructions": ["step1", "step2"],
  "url": "https://recipe-url",
  "photo_url": "https://image-url"
}
```

### Step 4: Run Data Processing Pipeline

Execute preprocessing and vectorization (one-time setup):

```bash
# Preprocess recipes
# Extracts ingredients, normalizes text, builds vocabulary
python py-data-preprocess.py

# Generates:
#  - data/cookstr-data.json
#  - data/cookstr-corpus.json

# Compute TF-IDF
# Vectorizes recipes, saves model artifacts
python py-calculate-tf-idf.py

# Generates:
#  - data/tf_idf.pickle (fitted TfidfVectorizer)
#  - data/tf_idf_matrix.pickle (sparse recipe vectors)
```

**Verification**: Check `data/` directory contains:
- cookstr-data.json (processed recipes)
- cookstr-corpus.json (ingredient vocabulary)
- tf_idf.pickle (vectorizer model)
- tf_idf_matrix.pickle (recipe vectors)

### Step 5: Start Web Server

```bash
npm start
# Or directly: node server.js
```

Expected output: Server listening on port 9876

### Step 6: Access Application

Open browser to: **http://localhost:9876**

1. **Home Page** - Overview and navigation
2. **Tool Page** - Ingredient selector with dropdown
3. **Recommendation Page** - Display best matching recipe

## Configuration

### Current Hard-Coded Settings

| Setting | Value | Location |
|---------|-------|----------|
| Server Port | 9876 | server.js line 5 |
| Data Directory | ./data/ | All Python scripts |
| Python Executable | python | server.js line 26 |

### To Customize

**Change Server Port**:
```javascript
// server.js, line 5
app.listen(9876);  // Change this number
```

**Change Data Directory**:
1. Update file paths in py-data-preprocess.py
2. Update file paths in py-calculate-tf-idf.py
3. Update file paths in py-calculate-similarity.py
4. Update file paths in server.js

**Use Environment Variables** (Recommended):
```bash
# Create .env file
PORT=9876
DATA_DIR=./data
PYTHON_PATH=python
```

## Usage

### User Workflow

```
1. User opens http://localhost:9876
2. Clicks "Go to Tool" button
3. Dropdown shows ~5,000+ ingredients (from corpus)
4. User selects ingredients (e.g., tomato, basil, garlic)
5. Clicks "Get Recommendation!"
6. Browser navigates to: /recommendation?input=342,118,502
   (ingredient IDs, comma-separated)
7. Express route:
   a. Receives query parameters
   b. Validates ingredient IDs
   c. Spawns Python subprocess
   d. Python calculates similarity
   e. Looks up recipe in JSON
   f. Renders results page
8. User sees recipe: title, ingredients, instructions, photo link
```

### Data Processing

1. User Input: Ingredient IDs (comma-separated)
2. Python script loads:
   - Vectorizer from tf_idf.pickle
   - Recipe matrix from tf_idf_matrix.pickle
   - Ingredient corpus from cookstr-corpus.json
3. Creates user ingredient vector from IDs
4. Computes cosine similarity with all recipes
5. Returns recipe ID with maximum similarity
6. Express looks up recipe details in cookstr-data.json
7. Renders recommendation page with recipe details

## Dependencies

### Node.js Runtime

```json
{
  "dependencies": {
    "express": "^4.17.1",      // Web framework
    "pug": "^3.0.1",           // Template engine
    "body-parser": "^1.19.0"   // Middleware (unused)
  }
}
```

### Python Runtime

```
scikit-learn >= 0.20.0  // TF-IDF, cosine similarity
                        // Transitive: numpy, scipy, joblib
```

### Frontend CDN

- Bootstrap 4.4.1 - Responsive UI
- jQuery 3.4.1 - DOM manipulation
- Select2 4.0.13 - Multi-select dropdown
- Popper.js 1.16.0 - Positioning library

## Development and Testing

### Code Organization

**server.js** (43 lines):
- GET / → render home page
- GET /tool → render ingredient selector
- GET /recommendation → spawn Python, lookup recipe, render results

**py-data-preprocess.py** (63 lines):
- `read_raw_data()` - Load JSON lines
- `feature_selection()` - Extract ingredients from recipes
- `load_into_corpus_list()` - Build ingredient vocabulary
- `main()` - Orchestrate preprocessing

**py-calculate-tf-idf.py** (32 lines):
- `read_json_data()` - Load processed recipes
- `load_into_ingredients_list()` - Extract ingredient lists
- `calculate_tf_idf()` - Vectorize and serialize
- `main()` - Orchestrate

**py-calculate-similarity.py** (38 lines):
- `data_pre_processing()` - Parse arguments, load corpus
- `calculate_cos_sim()` - Load pickles, compute similarity
- `main()` - Orchestrate

### Code Quality Observations

✓ Separation of concerns (preprocessing, ML, web serving)
✓ Reusable Python pipeline (independent of web server)
✓ Server-side template rendering (Pug)
✓ Minimal dependencies

⚠ Minimal error handling
⚠ No input validation on ingredient IDs
⚠ Hard-coded file paths and port
⚠ No logging
⚠ Assumes recipe ID < 10000 (output truncation)

### Testing

**Manual Tests**:
```bash
# Test data preprocessing
python py-data-preprocess.py
# Verify: cookstr-data.json and cookstr-corpus.json created

# Test TF-IDF computation
python py-calculate-tf-idf.py
# Verify: tf_idf.pickle and tf_idf_matrix.pickle created

# Test similarity script
python py-calculate-similarity.py "0,5,10"
# Expected output: 4-digit recipe ID (e.g., "0042")

# Test web server
npm start
# Open http://localhost:9876
```

**Recommended Test Framework**: pytest (Python), Jest/Mocha (Node.js)

## Deployment

### Development

```bash
npm start
```

### Production

**Environment Configuration**:
```bash
# Create .env file
PORT=9876
DATA_DIR=./data
PYTHON_PATH=python
```

**Docker** (Recommended):
```dockerfile
FROM node:14-slim
RUN apt-get update && apt-get install -y python3 python3-pip
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY requirements.txt ./
RUN pip install -r requirements.txt
COPY . .
EXPOSE 9876
CMD ["npm", "start"]
```

**Process Manager** (pm2):
```bash
npm install -g pm2
pm2 start server.js --name recipe-net
pm2 save
```

**Performance Optimization**:
1. Pre-load pickle files at server startup
2. Cache recommendation results
3. Move Python subprocess to separate microservice
4. Implement request rate limiting
5. Add response compression

## Limitations and Future Improvements

### Limitations

| Issue | Impact | Severity |
|-------|--------|----------|
| Output string truncation (assumes ID < 10000) | Breaks for large recipe sets | High |
| No file validation | Server crashes if pickles missing | High |
| Process spawning per request | Slow response, CPU overhead | High |
| No input validation | XSS/injection vulnerability | High |
| Bare `except` in Python | Silent failures during preprocessing | Medium |
| Recipe matching on ingredients only | Limited personalization | Medium |
| Static corpus per deployment | Cannot update without full retraining | Medium |
| No error handling in Node server | Unclear failure messages | Medium |

### Known Issues

1. **Command Injection Risk** (server.js line 28):
   - Current: Uses `shell: true` with user input
   - Fix: Use array form without shell

2. **Missing Input Validation** (server.js):
   - Add regex check: `/^\d+(,\d+)*$/` before spawning

3. **Output Parsing Issue** (server.js line 34):
   - Current: `output.slice(0, 4)` assumes ID ≤ 9999
   - Fix: Parse as integer with padding

4. **Missing Error Handling**:
   - Add checks for python.error and python.status

### Future Improvements

**Short Term (High Value)**:
- [ ] Add input validation and error handling
- [ ] Fix command injection vulnerability
- [ ] Implement configuration file (.env)
- [ ] Add structured logging
- [ ] Write unit tests for Python scripts
- [ ] Add caching layer

**Medium Term**:
- [ ] Move ML inference to separate service
- [ ] Add multiple recommendations with ranking
- [ ] Implement ingredient substitution suggestions
- [ ] Add user favorites & recipe ratings
- [ ] Database integration for recipe storage

**Long Term**:
- [ ] Advanced filtering (cuisine, prep time, difficulty)
- [ ] User authentication and ratings
- [ ] REST API for third-party integrations
- [ ] Mobile app
- [ ] Neural network-based recommendations

## Contribution Guidelines

1. Fork the repository
2. Create feature branch: `git checkout -b feature/your-feature`
3. Make focused changes
4. Test thoroughly with `npm start`
5. Submit pull request with clear description

## License

MIT License - See [LICENSE](LICENSE) file for complete terms.

**Copyright**: Tanmay Pachpande

**Permissions**: Commercial use, modification, distribution, private use

**Conditions**: License and copyright notice must be included

**Limitations**: No liability or warranty
