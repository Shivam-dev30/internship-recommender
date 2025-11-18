from flask import Flask, request, jsonify, render_template
from recommender import Recommender
import os

app = Flask(__name__, static_folder='static', template_folder='templates')

# CSV path (Vercel allows reading project files)
CSV_PATH = os.path.join(os.path.dirname(__file__), 'data', 'internships.csv')

# Initialize recommender
reco = Recommender(csv_path=CSV_PATH)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/recommend', methods=['POST'])
def recommend():
    data = request.json or {}
    user_profile = {
        'skills': data.get('skills', []),
        'sector': data.get('sector', ''),
        'location': data.get('location', ''),
        'bio': data.get('bio', '')
    }
    top_k = int(data.get('top_k', 5))

    try:
        recs = reco.recommend(user_profile, top_k=top_k)
        return jsonify({"status": "ok", "recommendations": recs})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/health')
def health():
    return jsonify({"status": "ok"}), 200

# ❌ IMPORTANT: Do NOT include app.run() for Vercel
