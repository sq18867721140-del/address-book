# Collaboration and Delivery Guide (Two-Person Team)

## 1. Git Workflow

1. The team lead forks the course repository to their own GitHub, creates a repository `address-book`, and adds the teammate as a collaborator.
2. Clone locally:
   ```bash
   git clone <repository-url>
   cd address-book
   ```
3. Agree on a branch strategy: `main` is the working trunk; develop each feature on a `feature/xxx` branch, then open a Pull Request to merge back into `main`.
4. Code style: consistent naming (snake_case), English commit messages (e.g. `add favorite feature`), and commit after each feature is done.
5. **At least 3 commits**, with both members having commit records; Section 2 of the blog needs the commit history screenshot and per-member commit counts.

## 2. Run Locally

```bash
python -m pip install -r requirements.txt
python app.py
# Open http://127.0.0.1:5000 in the browser
```

## 3. Suggested Division (adjust as needed)

| Member | Suggested Responsibilities |
| --- | --- |
| Member A | Data model, contact CRUD, favorite feature, backend routes |
| Member B | Multi-method form, Excel import/export, page style, deployment and blog materials |

## 4. Optional Cloud Deployment (+15 points)

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

## 5. Pre-Submission Checklist

- [ ] The repository can be built and run directly (`pip install -r requirements.txt`, then `python app.py`)
- [ ] Favorite / unfavorite works, favorites pinned on top
- [ ] One contact can hold multiple methods of different types
- [ ] Exported Excel columns are correct; importing a file in the same format populates the database
- [ ] Page style is clean
- [ ] At least 3 commits, both members have commits
- [ ] Release tag created and Pull Request opened
- [ ] Blog includes description table, TOC, project links, commit screenshots, implementation approach, screenshots and full video, division and contribution, PSP table
- [ ] Blog published early and pending review; do not wait until the deadline day
- [ ] Deadline: 2026-11-17 23:59
