"""End-to-end smoke test: create / favorite / multiple methods / export / import."""
import os
import sys

BASE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE)
os.chdir(BASE)
import app as address_app

app = address_app.app
address_app.init_db()

client = app.test_client()

# 1. Create a contact (with two phone numbers and one email)
resp = client.post("/contact/new", data={
    "name": "Alice Smith",
    "note": "Classmate",
    "is_favorite": "on",
    "phone": ["13800000001", "13800000002"],
    "email": ["alice@example.com"],
    "social": [],
    "address": "Fuzhou, Fujian",
}, follow_redirects=True)
assert resp.status_code == 200, resp.status_code
print("Create contact OK")

# 2. List page shows the name and the favorite star
body = resp.get_data(as_text=True)
assert "Alice Smith" in body and "9733" in body, "Contact or favorite marker missing in list"
print("List + favorite pinned OK")

# 3. Export Excel
resp = client.get("/export")
assert resp.status_code == 200
assert resp.data[:2] == b"PK", "Exported file is not xlsx"
with open("instance/export_sample.xlsx", "wb") as f:
    f.write(resp.data)
print("Export Excel OK, size:", len(resp.data), "bytes")

# 4. Re-import the exported file
resp = client.post("/import", data={"file": (open("instance/export_sample.xlsx", "rb"), "contacts.xlsx")},
                   follow_redirects=True)
assert resp.status_code == 200
body = resp.get_data(as_text=True)
assert "Successfully imported" in body, body
print("Import Excel OK")

# 5. Verify counts (1 original + 1 imported = 2 contacts)
db = address_app.sqlite3.connect(address_app.DATABASE)
count = db.execute("SELECT COUNT(*) FROM contact").fetchone()[0]
method_count = db.execute("SELECT COUNT(*) FROM contact_method").fetchone()[0]
db.close()
print(f"Contacts in DB: {count}, methods: {method_count}")
assert count == 2, count
print("All smoke tests passed")
