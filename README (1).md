# Vibe Marketing Platform Starter
A deliberately tiny project showcase site built with Flask.
## Features
- View a gallery of team projects (title, description, link, image)
- Add a new project via a simple form
- Disco ball hover effect on each project card (pure CSS animation, no images)
- Keep temporary data in an in-memory Python list
## Run it
```bash
cd vibemarketinghult
pip install -r requirements.txt
python app.py
```
Then open http://127.0.0.1:5000

Live version: [add your Render URL here]
## Important limitation
The starter app stores data only in memory while the server is running. A server restart (or Render's free tier spinning down after inactivity) will wipe any projects that were added.
That is intentional for the first version. Once the interface feels right, replace the in-memory `projects` list and the logic inside `add_project` with Supabase queries.
## Suggested next steps
1. Add Supabase persistence.
2. Give each project its own detail page.
3. Pull projects automatically from GitHub instead of manual entry.
4. Add more form fields (tags, submitted-by name, tech stack used).
5. Add login so only team members can submit projects.
6. Deploy with a custom domain.
# vibemarketinghult
