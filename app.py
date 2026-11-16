"""
EE308 Software Engineering (FZU-MU) - Address Book
Flask address book: favorite contacts / multiple contact methods / Excel import & export
"""
import os
import sqlite3
from datetime import datetime

from flask import (
    Flask, g, render_template, request, redirect, url_for, flash,
    send_file, abort
)
from openpyxl import Workbook, load_workbook
from io import BytesIO

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.path.join(BASE_DIR, "instance", "address_book.db")

# Contact method type -> display label (shared by templates and Excel headers)
METHOD_TYPES = [
    ("phone", "Phone"),
    ("email", "Email"),
    ("social", "Social"),
    ("address", "Address"),
]
TYPE_LABEL = dict(METHOD_TYPES)

app = Flask(__name__)
app.config["SECRET_KEY"] = "dev-secret-change-before-release"


# ---------- Database ----------

def get_db():
    """Return the database connection shared by the current request."""
    if "db" not in g:
        g.db = sqlite3.connect(DATABASE)
        g.db.row_factory = sqlite3.Row
        g.db.execute("PRAGMA foreign_keys = ON")
    return g.db


@app.teardown_appcontext
def close_db(exc):
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db():
    """Create tables on first run if they do not exist."""
    db = sqlite3.connect(DATABASE)
    db.executescript(
        """
        CREATE TABLE IF NOT EXISTS contact (
            id           INTEGER PRIMARY KEY AUTOINCREMENT,
            name         TEXT NOT NULL,
            note         TEXT DEFAULT '',
            is_favorite  INTEGER NOT NULL DEFAULT 0,
            created_at   TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS contact_method (
            id           INTEGER PRIMARY KEY AUTOINCREMENT,
            contact_id   INTEGER NOT NULL,
            type         TEXT NOT NULL,
            value        TEXT NOT NULL,
            FOREIGN KEY (contact_id) REFERENCES contact (id) ON DELETE CASCADE
        );
        """
    )
    db.commit()
    db.close()


def fetch_methods(db, contact_id):
    """Return all methods of a contact, grouped by type."""
    rows = db.execute(
        "SELECT type, value FROM contact_method WHERE contact_id = ? ORDER BY id",
        (contact_id,),
    ).fetchall()
    grouped = {t: [] for t, _ in METHOD_TYPES}
    for r in rows:
        grouped[r["type"]].append(r["value"])
    return grouped


# ---------- Routes ----------

@app.route("/")
def index():
    """Contact list: favorites on top, the rest by creation time descending."""
    db = get_db()
    contacts = db.execute(
        """
        SELECT * FROM contact
        ORDER BY is_favorite DESC, created_at DESC, id DESC
        """
    ).fetchall()

    result = []
    for c in contacts:
        methods = fetch_methods(db, c["id"])
        result.append({"contact": c, "methods": methods})
    return render_template("index.html", contacts=result, method_types=METHOD_TYPES)


@app.route("/contact/new", methods=["GET", "POST"])
def contact_new():
    if request.method == "POST":
        save_contact_from_form(db=get_db(), contact_id=None)
        flash("Contact added.", "success")
        return redirect(url_for("index"))
    return render_template("form.html", contact=None,
                           methods={t: [] for t, _ in METHOD_TYPES},
                           method_types=METHOD_TYPES)


@app.route("/contact/<int:contact_id>/edit", methods=["GET", "POST"])
def contact_edit(contact_id):
    db = get_db()
    contact = db.execute("SELECT * FROM contact WHERE id = ?", (contact_id,)).fetchone()
    if contact is None:
        abort(404)
    if request.method == "POST":
        save_contact_from_form(db=db, contact_id=contact_id)
        flash("Contact updated.", "success")
        return redirect(url_for("index"))
    methods = fetch_methods(db, contact_id)
    return render_template("form.html", contact=contact, methods=methods,
                           method_types=METHOD_TYPES)


@app.route("/contact/<int:contact_id>/delete", methods=["POST"])
def contact_delete(contact_id):
    db = get_db()
    db.execute("DELETE FROM contact_method WHERE contact_id = ?", (contact_id,))
    db.execute("DELETE FROM contact WHERE id = ?", (contact_id,))
    db.commit()
    flash("Contact deleted.", "info")
    return redirect(url_for("index"))


@app.route("/contact/<int:contact_id>/toggle-favorite", methods=["POST"])
def toggle_favorite(contact_id):
    db = get_db()
    contact = db.execute("SELECT is_favorite FROM contact WHERE id = ?", (contact_id,)).fetchone()
    if contact is None:
        abort(404)
    new_value = 0 if contact["is_favorite"] else 1
    db.execute("UPDATE contact SET is_favorite = ? WHERE id = ?", (new_value, contact_id))
    db.commit()
    return redirect(url_for("index"))


def save_contact_from_form(db, contact_id):
    """Read the form and persist (create or update), rebuilding the methods."""
    name = request.form.get("name", "").strip()
    note = request.form.get("note", "").strip()
    is_favorite = 1 if request.form.get("is_favorite") else 0
    if not name:
        raise ValueError("Name cannot be empty")

    if contact_id is None:
        cur = db.execute(
            "INSERT INTO contact (name, note, is_favorite, created_at) VALUES (?, ?, ?, ?)",
            (name, note, is_favorite, datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
        )
        contact_id = cur.lastrowid
    else:
        db.execute(
            "UPDATE contact SET name = ?, note = ?, is_favorite = ? WHERE id = ?",
            (name, note, is_favorite, contact_id),
        )
        # On edit, clear old methods first, then rebuild from the form
        db.execute("DELETE FROM contact_method WHERE contact_id = ?", (contact_id,))

    for type_key, _ in METHOD_TYPES:
        values = request.form.getlist(type_key)
        for v in values:
            v = v.strip()
            if v:
                db.execute(
                    "INSERT INTO contact_method (contact_id, type, value) VALUES (?, ?, ?)",
                    (contact_id, type_key, v),
                )
    db.commit()


# ---------- Excel import & export ----------

HEADERS = ["Name", "Phone", "Email", "Social", "Address", "Note", "Favorite"]
TYPE_BY_HEADER = {"Phone": "phone", "Email": "email", "Social": "social", "Address": "address"}
FAVORITE_TRUE = ("Yes", "Y", "y", "1", "true", "是")


@app.route("/export")
def export_excel():
    db = get_db()
    contacts = db.execute("SELECT * FROM contact ORDER BY id").fetchall()

    wb = Workbook()
    ws = wb.active
    ws.title = "contacts"
    ws.append(HEADERS)

    for c in contacts:
        methods = fetch_methods(db, c["id"])
        row = [
            c["name"],
            "\n".join(methods["phone"]),
            "\n".join(methods["email"]),
            "\n".join(methods["social"]),
            "\n".join(methods["address"]),
            c["note"],
            "Yes" if c["is_favorite"] else "No",
        ]
        ws.append(row)

    buf = BytesIO()
    wb.save(buf)
    buf.seek(0)
    return send_file(
        buf,
        as_attachment=True,
        download_name="contacts.xlsx",
        mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )


@app.route("/import", methods=["POST"])
def import_excel():
    file = request.files.get("file")
    if file is None or file.filename == "":
        flash("Please choose an Excel file to import.", "danger")
        return redirect(url_for("index"))

    try:
        wb = load_workbook(file, data_only=True)
        ws = wb.active
        rows = list(ws.iter_rows(values_only=True))
        if not rows:
            flash("The Excel file is empty.", "danger")
            return redirect(url_for("index"))

        header = [str(h).strip() if h is not None else "" for h in rows[0]]
        # Locate columns by header name, independent of column order
        col_index = {name: header.index(name) if name in header else None for name in HEADERS}

        db = get_db()
        imported = 0
        for raw in rows[1:]:
            if raw is None or all(cell is None or str(cell).strip() == "" for cell in raw):
                continue

            def cell(name):
                idx = col_index[name]
                if idx is None or idx >= len(raw):
                    return ""
                return "" if raw[idx] is None else str(raw[idx]).strip()

            name = cell("Name")
            if not name:
                continue  # Skip rows without a name

            note = cell("Note")
            fav = 1 if cell("Favorite") in FAVORITE_TRUE else 0
            cur = db.execute(
                "INSERT INTO contact (name, note, is_favorite, created_at) VALUES (?, ?, ?, ?)",
                (name, note, fav, datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
            )
            contact_id = cur.lastrowid

            for header_name, type_key in TYPE_BY_HEADER.items():
                value = cell(header_name)
                if value:
                    # Line breaks inside a cell separate multiple methods of the same type
                    for v in value.splitlines():
                        v = v.strip()
                        if v:
                            db.execute(
                                "INSERT INTO contact_method (contact_id, type, value) VALUES (?, ?, ?)",
                                (contact_id, type_key, v),
                            )
            imported += 1

        db.commit()
        flash(f"Successfully imported {imported} contact(s).", "success")
    except Exception as e:  # Show a message on failure instead of crashing
        flash(f"Import failed: {e}", "danger")
    return redirect(url_for("index"))


if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000, debug=True)
