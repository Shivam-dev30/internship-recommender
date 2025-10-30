// script.js

function clearForm(){
  document.getElementById('skills').value = '';
  document.getElementById('sector').value = '';
  document.getElementById('location').value = '';
  document.getElementById('bio').value = '';
  document.getElementById('results').innerHTML = '';
}

async function submitProfile(){
  const skillsRaw = document.getElementById('skills').value.trim();
  const skills = skillsRaw ? skillsRaw.split(',').map(s => s.trim()).filter(Boolean) : [];
  const sector = document.getElementById('sector').value.trim();
  const location = document.getElementById('location').value.trim();
  const bio = document.getElementById('bio').value.trim();

  const payload = {
    skills, sector, location, bio, top_k: 5
  };

  // UI: show loading
  const resultsEl = document.getElementById('results');
  resultsEl.innerHTML = '<div class="card"><em>Loading recommendations…</em></div>';

  try {
    const res = await fetch('/recommend', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify(payload)
    });
    const data = await res.json();
    if(data.status !== 'ok'){
      resultsEl.innerHTML = `<div class="card">Error: ${data.message || 'Unknown'}</div>`;
      return;
    }
    const recs = data.recommendations || [];
    if(recs.length === 0){
      resultsEl.innerHTML = `<div class="card">No matches found. Try broader skills or remove location filter.</div>`;
      return;
    }
    // Build cards
    resultsEl.innerHTML = '';
    recs.forEach(r => {
      const card = document.createElement('div'); card.className = 'card';
      const title = document.createElement('h3');
      title.textContent = r.title + ' ';
      const badge = document.createElement('span'); badge.className = 'score-badge';
      badge.textContent = r.score;
      title.appendChild(badge);
      card.appendChild(title);

      const meta = document.createElement('div'); meta.className = 'meta small';
      meta.textContent = `${r.company} • ${r.location} • ${r.duration}`;
      card.appendChild(meta);

      const desc = document.createElement('div'); desc.className = 'explain';
      desc.textContent = r.description;
      card.appendChild(desc);

      const expl = document.createElement('div'); expl.className = 'small';
      expl.textContent = `Why: ${r.explanation}`;
      card.appendChild(expl);

      const actions = document.createElement('div'); actions.className = 'actions';
      const apply = document.createElement('a'); apply.className = 'apply';
      apply.href = r.apply_link || '#'; apply.target = '_blank'; apply.textContent = 'Apply';
      actions.appendChild(apply);

      // optional: feedback buttons
      const good = document.createElement('button'); good.textContent = 'Useful';
      good.onclick = () => { good.disabled = true; good.textContent = 'Thanks'; };
      actions.appendChild(good);

      card.appendChild(actions);
      resultsEl.appendChild(card);
    });
  } catch (err) {
    resultsEl.innerHTML = `<div class="card">Network error: ${err.message}</div>`;
  }
}
