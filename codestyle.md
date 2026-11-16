# Code Style Guide

## Language and Format

- Backend: Python 3, following PEP 8.
- Frontend: HTML5, CSS3, vanilla JavaScript (ES2015+).
- All user-facing strings and comments in the source are written in English.

## Naming

- Variables and functions: `snake_case` (e.g. `fetch_methods`, `contact_new`).
- Classes: `PascalCase` (none in this project yet).
- Constants: `UPPER_SNAKE_CASE` (e.g. `METHOD_TYPES`, `HEADERS`).
- HTML ids / CSS classes: `kebab-case` (e.g. `method-group`, `remove-method`).

## Python Rules

- One responsibility per function; route handlers stay thin and delegate to helpers.
- Use parameterized SQL (`?`) to avoid injection; never concatenate user input into queries.
- Keep line length reasonable; wrap long queries and lists over multiple lines.
- Imports are grouped: standard library, third-party, local.

## Templates

- Reuse the shared `base.html` layout; avoid repeating navigation or head markup.
- Loop over `method_types` instead of hard-coding each contact method.

## Commit Messages

- Format: `<type>: <short summary>`
- Types: `feat` (new feature), `fix` (bug fix), `docs` (documentation), `style` (formatting), `refactor`, `test`.
- Summary in English, imperative mood, e.g. `feat: add contact search filter`.

## Project Layout

- `app.py`: routes and business logic.
- `templates/`: Jinja2 views.
- `static/`: CSS and static assets.
- `smoke_test.py`: end-to-end self-test script.
