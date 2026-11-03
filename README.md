# AI-Based Technical Debt Prediction

A beginner-friendly academic prototype based on the supplied project specification.

## Features
- Upload a ZIP containing Python source files.
- Scan Python files using the built-in Abstract Syntax Tree (AST).
- Measure lines of code, branching complexity, functions, classes and repeated lines.
- Flag long functions, large classes, low comment ratio and other simple code smells.
- Calculate a transparent 0–100 heuristic risk score and classify Low / Medium / High.
- View prioritized results and recommendations in a browser dashboard.
- Export the analysis as JSON.

## Important scope note
This version is a working prototype, not a fully trained AI model. The uploaded specification calls for historical repository activity, dependency analysis, trained ML prediction, confidence levels, alerts and continuous monitoring. Those require additional repository history/data, dependency parsers, a labeled training dataset and deployment integrations. This prototype deliberately labels its score as a heuristic so it is not mistaken for a validated ML prediction. It currently scans Python `.py` files only.

## Requirements
- Python 3.10+
- pip

## Run locally

### Windows
```bash
cd ai_technical_debt_prediction
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

### macOS / Linux
```bash
cd ai_technical_debt_prediction
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m pip install -r requirements.txt
python app.py
```

Open http://127.0.0.1:5000 in your browser. Create a ZIP of a Python project and upload it.

## ZIP upload notes
- Upload a `.zip` archive containing `.py` files.
- The analyzer ignores `.git`, virtual environments, `node_modules` and Python cache directories.
- The demo has a 25 MB upload limit.
- The uploaded files are extracted to a temporary folder and removed after analysis.

## Example test project
Create `sample_project.py`:
```python
def process_records(records):
    result = []
    for record in records:
        if record.get("active"):
            if record.get("score", 0) > 50:
                if record.get("verified"):
                    result.append(record)
    return result
```
Zip the file and upload it.

## API
- `GET /` — dashboard
- `GET /health` — health check
- `POST /api/analyze` — multipart upload field named `project`, a ZIP file

## GitHub upload instructions
1. Create a GitHub account or sign in.
2. Select **New repository** on GitHub.
3. Name it `ai-based-technical-debt-prediction`.
4. Choose Public or Private, then create the repository.
5. Extract this project ZIP on your computer.
6. Open the extracted folder in VS Code or a terminal.
7. Run:
   ```bash
   git init
   git add .
   git commit -m "Initial AI technical debt prediction project"
   git branch -M main
   git remote add origin https://github.com/YOUR-USERNAME/ai-based-technical-debt-prediction.git
   git push -u origin main
   ```
8. Replace `YOUR-USERNAME` with your GitHub username.
9. Refresh the repository page to confirm the files are uploaded.

### Suggested `.gitignore`
```gitignore
.venv/
__pycache__/
*.pyc
.env
.DS_Store
```

## Suggested future enhancements
- GitHub API integration for commits, branches and pull requests.
- Dependency checks for requirements files.
- Historical training dataset and evaluation (precision, recall, F1).
- Random Forest / XGBoost model trained on labeled historical examples.
- Confidence calibration, scheduled scans and configurable alerts.
- Authentication, role-based access and persistent database storage.
