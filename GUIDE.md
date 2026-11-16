# Delivery Guide (Individual Project)

## 1. Git Workflow

1. Create a repository `address-book` on GitHub and clone it locally:
   ```bash
   git clone <repository-url>
   cd address-book
   ```
2. Keep `main` as the working trunk; commit each feature separately with an English message (e.g. `add favorite feature`).
3. **At least 3 commits** spread across development; Section 2 of the blog needs the commit history screenshot and total commit count.

## 2. Run Locally

```bash
python -m pip install -r requirements.txt
python app.py
# Open http://127.0.0.1:5000 in the browser
```

## 3. Optional Cloud Deployment (+15 points)

> A localhost link does not count; a publicly accessible URL is required.

1. Get a Huawei Cloud / Alibaba Cloud lightweight server and open port 80.
2. Install Python 3 and dependencies on the server, upload the code.
3. Run Flask with Gunicorn:
   ```bash
   pip install gunicorn
   gunicorn -w 4 -b 0.0.0.0:8000 app:app
   ```
4. Reverse proxy port 80 to 8000 with Nginx; open the corresponding port in the firewall.
5. Put the public URL into Section 1 of the blog.
6. Before going live, replace `SECRET_KEY` in `app.py` with a random string and set `debug` to `False`.

## 4. Pre-Submission Checklist

- [ ] The repository can be built and run directly (`pip install -r requirements.txt`, then `python app.py`)
- [ ] Favorite / unfavorite works, favorites pinned on top
- [ ] One contact can hold multiple methods of different types
- [ ] Exported Excel columns are correct; importing a file in the same format populates the database
- [ ] Page style is clean
- [ ] At least 3 commits
- [ ] Release tag created and Pull Request opened
- [ ] Blog includes description table, TOC, project links, commit screenshots, implementation approach, screenshots and full video, PSP table
- [ ] Blog published early and pending review; do not wait until the deadline day
- [ ] Deadline: 2026-11-17 23:59
