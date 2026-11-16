# EE308 Address Book

Course: Software Engineering (FZU–MU) · Extreme Programming Assignment

## Features

- Create, edit, and delete contacts
- Favorite / unfavorite contacts; favorites are pinned to the top
- Multiple contact methods per contact (phone, email, social, address)
- Excel export: one row per contact, columns for Name / Phone / Email / Social / Address / Note / Favorite
- Excel import: read a file in the same format and append contacts
- (Optional) Cloud server deployment

## Tech Stack

- Python 3 + Flask
- SQLite (stdlib `sqlite3`, no separate database install)
- Bootstrap 5 (CDN)
- openpyxl (Excel read/write)

## Run Locally

```bash
# 1. Install dependencies
python -m pip install -r requirements.txt

# 2. Start the server (database is created automatically on first run)
python app.py

# 3. Open in the browser
# http://127.0.0.1:5000
```

## Directory Structure

```
address-book/
├── app.py                  # Backend routes and business logic
├── requirements.txt        # Python dependencies
├── .gitignore
├── instance/               # SQLite database (generated at runtime)
├── static/
│   └── style.css
└── templates/
    ├── base.html           # Shared layout
    ├── index.html          # Contact list
    └── form.html           # Create / edit form
```

## Team Division (two-person team)

> Fill in the actual division before submitting code.

| Member | Responsible Modules |
| --- | --- |
| Member A |  |
| Member B |  |
