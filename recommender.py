# recommender.py
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import os

class Recommender:
    def __init__(self, csv_path='data/internships.csv'):
        if not os.path.exists(csv_path):
            raise FileNotFoundError(f"{csv_path} not found.")
        self.df = pd.read_csv(csv_path)
        # Ensure id is int
        if 'id' in self.df.columns:
            self.df['id'] = self.df['id'].astype(int)
        # Prepare text for TF-IDF
        self.df['description'] = self.df['description'].fillna('')
        self.tfidf = TfidfVectorizer(stop_words='english', max_features=4000)
        self.tfidf_matrix = self.tfidf.fit_transform(self.df['description'])

    def _count_skill_matches(self, job_skills, user_skills):
        job_set = set([s.strip().lower() for s in job_skills.split(';') if s.strip()])
        user_set = set([s.strip().lower() for s in user_skills if s.strip()])
        return len(job_set & user_set)

    def recommend(self, user_profile: dict, top_k: int = 5):
        """
        user_profile: {
            'skills': ['python', 'pandas'],
            'sector': 'Data Science',
            'location': 'Delhi',
            'bio': 'I like data cleaning and visualization'
        }
        returns: list of dicts with recommendation and explanation
        """
        # default safe values
        skills = user_profile.get('skills', []) or []
        sector = (user_profile.get('sector') or '').strip().lower()
        location = (user_profile.get('location') or '').strip().lower()
        bio = user_profile.get('bio', '') or ''

        # TF-IDF vector for bio
        user_vec = self.tfidf.transform([bio])
        sim_scores = cosine_similarity(user_vec, self.tfidf_matrix).flatten()  # len = n_jobs

        recs = []
        for idx, row in self.df.iterrows():
            score = 0.0
            explanations = []

            # Sector match (binary)
            job_sector = str(row.get('sector', '')).strip().lower()
            if job_sector and sector and job_sector == sector:
                score += 5.0
                explanations.append("Sector match")

            # Location match (binary)
            job_loc = str(row.get('location', '')).strip().lower()
            if job_loc and location and job_loc == location:
                score += 2.0
                explanations.append("Location match")

            # Skills matches
            job_skills = str(row.get('skills', '')).lower()
            skill_matches = self._count_skill_matches(job_skills, skills)
            if skill_matches > 0:
                score += 3.0 * skill_matches
                explanations.append(f"{skill_matches} skill match{'es' if skill_matches>1 else ''}")

            # TF-IDF similarity adds a small continuous boost
            tfidf_sim = float(sim_scores[idx])
            score += 0.6 * tfidf_sim
            if tfidf_sim > 0.1:
                explanations.append("Description similarity")

            # small tie-breaker: prefer shorter durations (optional)
            # not used now, but could be added.

            recs.append({
                "id": int(row['id']),
                "title": row.get('title',''),
                "company": row.get('company',''),
                "description": row.get('description','')[:250],
                "skills": row.get('skills',''),
                "sector": row.get('sector',''),
                "location": row.get('location',''),
                "duration": row.get('duration',''),
                "apply_link": row.get('apply_link',''),
                "score": round(float(score), 4),
                "explanation": "; ".join(explanations) if explanations else "Based on description similarity"
            })

        # sort by score descending
        recs_sorted = sorted(recs, key=lambda x: x['score'], reverse=True)
        return recs_sorted[:top_k]


# Quick test when run directly
if __name__ == "__main__":
    r = Recommender()
    user = {
        "skills": ["python", "pandas"],
        "sector": "Data Science",
        "location": "Delhi",
        "bio": "I enjoy data cleaning, EDA, machine learning"
    }
    results = r.recommend(user, top_k=5)
    for res in results:
        print(res['id'], res['title'], res['score'], res['explanation'])
