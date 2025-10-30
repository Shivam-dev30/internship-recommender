# Internship Recommender

Simple Flask app that recommends internships from a CSV based on user skills, sector, location and short bio. Uses rule-based scoring + TF-IDF description similarity.

## Run locally

1. Create virtual env:
   - Linux/Mac:
     ```
     python3 -m venv venv
     source venv/bin/activate
     ```
   - Windows (PowerShell):
     ```
     python -m venv venv
     .\venv\Scripts\Activate.ps1
     ```

2. Install:
pip install -r requirements.txt

3. Run:
python app.py

4. Open: http://127.0.0.1:5000

## Deploy (Render)
1. Push this repo to GitHub.
2. Create a new Web Service on Render, connect your GitHub repo.
3. Set the build command: `pip install -r requirements.txt`
4. Set start command: `gunicorn app:app`
5. (Optional) set environment variable `INTERNS_CSV` to `data/internships.csv` if using custom path.
6. Deploy and open URL.

## Notes
- Update `data/internships.csv` with real listings.
- To improve: add user auth, store feedback to train a re-ranker, integrate company logos, pagination, or filters.

