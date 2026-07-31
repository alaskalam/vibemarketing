"""
Vibe Marketing Platform — bare bones starter
----------------------------------------------
A tiny Flask app that lets people paste in a project (title, description,
link, optional image URL) and see everything in a card gallery.

Storage is just an in-memory Python list for now — restarting the server
wipes it. That's fine for a v1; swap in SQLite or a JSON file later once
this is working the way you like.

Run it with:
    pip install flask
    python app.py
Then open http://127.0.0.1:5000
"""

from flask import Flask, render_template_string, request, redirect, url_for

app = Flask(__name__)

# --- "Database" (in-memory list, resets on restart) ------------------------
projects = [
    {
        "title": "Sample Project",
        "description": "This is a placeholder — add your own above!",
        "link": "https://example.com",
        "image": "",
    }
]

# --- Templates (kept inline so this is a single-file app) ------------------
BASE_STYLE = """
<style>
  * { box-sizing: border-box; }
  body {
    font-family: -apple-system, Segoe UI, Roboto, sans-serif;
    background: #0f0f1a;
    color: #f1f1f1;
    margin: 0;
    padding: 0 20px 60px;
  }
  header {
    text-align: center;
    padding: 50px 20px 30px;
  }
  header h1 {
    font-size: 2.5rem;
    margin: 0;
    background: linear-gradient(90deg, #7f5af0, #2cb67d);
    -webkit-background-clip: text;
    background-clip: text;
    color: transparent;
  }
  header p { color: #a0a0b0; }
  .add-btn {
    display: inline-block;
    margin-top: 15px;
    padding: 10px 22px;
    background: #7f5af0;
    color: white;
    text-decoration: none;
    border-radius: 8px;
    font-weight: 600;
  }
  .grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
    gap: 20px;
    max-width: 1100px;
    margin: 30px auto;
  }

  .card {
    position: relative;
    background: #1a1a2e;
    border: 1px solid #2a2a40;
    border-radius: 12px;
    overflow: visible;
    display: flex;
    flex-direction: column;
    transition: transform 0.2s ease;
  }
  .card:hover {
    transform: translateY(-4px);
  }

  /* --- Disco ball hover effect --------------------------------------- */
  .disco-ball {
    position: absolute;
    top: -34px;
    left: 50%;
    transform: translateX(-50%) scale(0.4);
    width: 40px;
    height: 40px;
    border-radius: 50%;
    
 
    background:
      repeating-linear-gradient(45deg, #2cb67d 0 4px, #1e8c5f 4px 8px),
      repeating-linear-gradient(-45deg, transparent 0 4px, rgba(0,0,0,0.15) 4px 8px);
    box-shadow: 0 0 12px 2px rgba(44,182,125,0.6), 0 0 24px 6px rgba(127,90,240,0.4);


    opacity: 0;
    pointer-events: none;
    transition: opacity 0.2s ease, transform 0.2s ease;
    animation: discoSpin 1.4s linear infinite;
    animation-play-state: paused;
    z-index: 5;
  }
  .card:hover .disco-ball {
    opacity: 1;
    transform: translateX(-50%) scale(1);
    animation-play-state: running;
  }
  @keyframes discoSpin {
    from { background-position: 0 0, 0 0; }
    to { background-position: 40px 0, -40px 0; }
  }
  .disco-ball::before,
  .disco-ball::after {
    content: "";
    position: absolute;
    width: 3px;
    height: 3px;
    border-radius: 50%;
    background: #fff;
    box-shadow: 0 0 6px 2px #fff;
    opacity: 0;
  }
  .card:hover .disco-ball::before {
    top: -6px;
    left: 6px;
    animation: sparkle 1s ease-in-out infinite;
  }
  .card:hover .disco-ball::after {
    top: 4px;
    right: -8px;
    animation: sparkle 1s ease-in-out 0.4s infinite;
  }
  @keyframes sparkle {
    0%, 100% { opacity: 0; }
    50% { opacity: 1; }
  }

  
  
  .card img {
    width: 100%;
    height: 150px;
    object-fit: cover;
    background: #24243a;
  }
  .card-body { padding: 16px; flex: 1; display: flex; flex-direction: column; }
  .card h3 { margin: 0 0 8px; }
  .card p { color: #b8b8c8; font-size: 0.92rem; flex: 1; }
  .card a.visit {
    margin-top: 10px;
    color: #2cb67d;
    text-decoration: none;
    font-weight: 600;
  }
  form {
    max-width: 500px;
    margin: 40px auto;
    background: #1a1a2e;
    padding: 24px;
    border-radius: 12px;
    border: 1px solid #2a2a40;
  }
  form label { display: block; margin-top: 14px; margin-bottom: 6px; font-size: 0.9rem; color: #b8b8c8; }
  form input, form textarea {
    width: 100%;
    padding: 10px;
    border-radius: 6px;
    border: 1px solid #333;
    background: #0f0f1a;
    color: white;
    font-family: inherit;
  }
  form button {
    margin-top: 20px;
    padding: 10px 20px;
    background: #2cb67d;
    color: #0f0f1a;
    border: none;
    border-radius: 8px;
    font-weight: 700;
    cursor: pointer;
  }
  .back { display: block; text-align: center; margin-top: 10px; color: #a0a0b0; }
</style>
"""

GALLERY_TEMPLATE = BASE_STYLE + """
<header>
  <h1>Our Project Showcase</h1>
  <p>Cool stuff the team has built, all in one place.</p>
  <a class="add-btn" href="{{ url_for('add_project') }}">+ Add a project</a>
</header>

<div class="grid">
  {% for p in projects %}
    <div class="card">
    <div class="disco-ball"></div>
    {% if p.image %}
      <img src="{{ p.image }}" alt="{{ p.title }}">
    {% endif %}
    <div class="card-body">
      <h3>{{ p.title }}</h3>
      <p>{{ p.description }}</p>
      <a class="visit" href="{{ p.link }}" target="_blank" rel="noopener">Visit project →</a>
    </div>
  </div>
  {% endfor %}
</div>
"""

ADD_TEMPLATE = BASE_STYLE + """
<header>
  <h1>Add a Project</h1>
  <p>Paste in the details and it'll show up on the gallery.</p>
</header>

<form method="POST">
  <label>Project title</label>
  <input type="text" name="title" required>

  <label>Description</label>
  <textarea name="description" rows="3" required></textarea>

  <label>Link (URL)</label>
  <input type="url" name="link" required>

  <label>Image URL (optional)</label>
  <input type="url" name="image">

  <button type="submit">Add project</button>
</form>
<a class="back" href="{{ url_for('gallery') }}">← back to gallery</a>
"""


# --- Routes ------------------------------------------------------------
@app.route("/")
def gallery():
    return render_template_string(GALLERY_TEMPLATE, projects=projects)


@app.route("/add", methods=["GET", "POST"])
def add_project():
    if request.method == "POST":
        projects.append({
            "title": request.form.get("title", "").strip(),
            "description": request.form.get("description", "").strip(),
            "link": request.form.get("link", "").strip(),
            "image": request.form.get("image", "").strip(),
        })
        return redirect(url_for("gallery"))
    return render_template_string(ADD_TEMPLATE)


if __name__ == "__main__":
    app.run(debug=True)
