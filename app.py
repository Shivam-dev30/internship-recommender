# app.py
from flask import Flask, request, jsonify, render_template
from recommender import Recommender
import os

app = Flask(__name__, static_folder='static', template_folder='templates')

# Initialize recommender with path to CSV
CSV_PATH = os.environ.get('INTERNS_CSV', 'data/internships.csv')
reco = Recommender(csv_path=CSV_PATH)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/recommend', methods=['POST'])
def recommend():
    data = request.json or {}
    # Basic validation/normalization
    user_profile = {
        'skills': data.get('skills', []),
        'sector': data.get('sector', ''),
        'location': data.get('location', ''),
        'bio': data.get('bio', '')
    }
    top_k = int(data.get('top_k', 5))
    try:
        recs = reco.recommend(user_profile, top_k=top_k)
        return jsonify({"status":"ok", "recommendations": recs})
    except Exception as e:
        return jsonify({"status":"error", "message": str(e)}), 500

@app.route('/health')
def health():
    return jsonify({"status":"ok"}), 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    # debug=True for local development; remove in production
    app.run(host='0.0.0.0', port=port, debug=True)
