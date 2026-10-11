# Deploy the live demo to GitHub Pages
GitHub Pages hosts static files only, so it serves the in-browser demo in `site/`. The FastAPI backend needs a server
(Render, Railway, Fly.io, or any VPS) - see the end of this file.

1. Create a new **public** repo named `questionnaire-ai` on GitHub (no README).
2. Push this project:
   ```bash
   git init && git add . && git commit -m "Attestra master release"
   git branch -M main
   git remote add origin https://github.com/Nikhil-creat/questionnaire-ai.git
   git push -u origin main
   ```
3. Repo **Settings > Pages > Build and deployment > Source: GitHub Actions**.
4. The `pages` workflow runs on every push to `main`. Watch it under the **Actions** tab.
5. Your site: https://nikhil-creat.github.io/questionnaire-ai/
6. Add the link to the repo's About box, your LinkedIn Featured section, and resume.

Troubleshooting: workflow failing on deploy means step 3 was skipped. A 404 usually means the first run hasn't finished.

## Hosting the API (optional)
Deploy `apps/api` with its Dockerfile on Render/Railway, set `ANTHROPIC_API_KEY` as a secret, and add authentication
(see `ROADMAP.md`) before sharing the URL.
