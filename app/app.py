from flask import Flask, render_template, request
import json, os, csv, shutil, re, subprocess

app = Flask(__name__)

# ---------------------------------------------------------
# CSV parser (same logic as movies_alpha.py)
# ---------------------------------------------------------
CSV_REGEX = re.compile(r'''
(?:^|,)
(
  "(?:[^"]*)"
  |
  [^,]*
)
''', re.VERBOSE)

def clean_line(line):
    line = line.replace('"""', '"')
    line = line.replace('""', '"')
    return line

def parse_csv_line(line):
    line = clean_line(line).strip()
    fields = CSV_REGEX.findall(line)
    return [f.strip().strip('"') for f in fields]

# ---------------------------------------------------------
# Main page
# ---------------------------------------------------------
@app.route("/")
def index():
    return render_template("index.html")

# ---------------------------------------------------------
# API: return full locations.json
# ---------------------------------------------------------
@app.route("/api/locations")
def get_locations():
    data_path = os.path.join("data", "locations.json")
    with open(data_path, "r", encoding="utf-8") as f:
        return json.load(f)

# ---------------------------------------------------------
# API: get single movie
# ---------------------------------------------------------
@app.route("/api/location/<ean>")
def get_location(ean):
    data_path = os.path.join("data", "locations.json")
    with open(data_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data.get(ean, {"error": "EAN not found"})

# ---------------------------------------------------------
# API: save/update movie
# ---------------------------------------------------------
@app.route("/api/save", methods=["POST"])
def save_movie():
    data_path = os.path.join("data", "locations.json")
    with open(data_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    payload = request.json
    ean = payload["ean"]

    data[ean] = {
        "title": payload["title"],
        "location": payload["location"],
        "dv": payload["dv"],
        "atmos": payload["atmos"],
        "duration": payload.get("duration")
    }

    with open(data_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    return {"status": "ok"}

# ---------------------------------------------------------
# API: add movie
# ---------------------------------------------------------
@app.route("/api/add", methods=["POST"])
def add_movie():
    data_path = os.path.join("data", "locations.json")
    with open(data_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    payload = request.json
    ean = payload["ean"]

    if ean in data:
        return {"error": "EAN already exists"}, 400

    data[ean] = {
        "title": payload["title"],
        "location": payload["location"],
        "dv": payload["dv"],
        "atmos": payload["atmos"],
        "duration": payload.get("duration")
    }

    with open(data_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    return {"status": "ok"}

# ---------------------------------------------------------
# API: delete movie
# ---------------------------------------------------------
@app.route("/api/delete/<ean>", methods=["DELETE"])
def delete_movie(ean):
    data_path = os.path.join("data", "locations.json")
    with open(data_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    if ean not in data:
        return {"error": "EAN not found"}, 404

    del data[ean]

    with open(data_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    return {"status": "deleted"}

# ---------------------------------------------------------
# API: import CSV
# ---------------------------------------------------------
@app.route("/api/import_csv", methods=["POST"])
def import_csv():
    base_dir = os.path.expanduser("~/bluray")
    new_csv_path = os.path.join(base_dir, "collection.csv")

    # Backup rotation
    for i in range(10, 0, -1):
        old_i = os.path.join(base_dir, f"collection.old{i}")
        old_next = os.path.join(base_dir, f"collection.old{i+1}")
        if os.path.exists(old_i):
            shutil.move(old_i, old_next)

    old_path = os.path.join(base_dir, "collection.old")
    if os.path.exists(old_path):
        shutil.move(old_path, os.path.join(base_dir, "collection.old1"))

    if os.path.exists(new_csv_path):
        shutil.move(new_csv_path, old_path)

    uploaded = request.files["file"]
    uploaded.save(new_csv_path)

    data_path = os.path.join("data", "locations.json")
    with open(data_path, "r", encoding="utf-8") as f:
        locations = json.load(f)

    added = 0
    ignored = 0
    errors = 0

    try:
        with open(new_csv_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
            headers = parse_csv_line(lines[0])

            for line in lines[1:]:
                try:
                    row = parse_csv_line(line)
                    if len(row) < 5:
                        continue

                    title = row[0].strip()
                    ean = row[4].strip()

                    if not ean:
                        ignored += 1
                        continue

                    if ean in locations:
                        ignored += 1
                        continue

                    locations[ean] = {
                        "title": title,
                        "location": "",
                        "dv": False,
                        "atmos": False,
                        "duration": None
                    }

                    added += 1

                except Exception:
                    errors += 1

    except Exception:
        return {"error": "CSV parsing failed"}, 500

    with open(data_path, "w", encoding="utf-8") as f:
        json.dump(locations, f, indent=2, ensure_ascii=False)

    return {"added": added, "ignored": ignored, "errors": errors}

# ---------------------------------------------------------
# API: export app JSON to /bluray/locations.json
# ---------------------------------------------------------
@app.route("/api/export", methods=["POST"])
def export_locations():
    app_json_path = os.path.join("data", "locations.json")
    scripts_json_path = os.path.expanduser("~/bluray/locations.json")

    with open(app_json_path, "r", encoding="utf-8") as f:
        app_data = json.load(f)

    export_data = {}

    for ean, info in app_data.items():
        export_data[ean] = {
            "dv": info.get("dv", False),
            "atmos": info.get("atmos", False),
            "level": info.get("location", ""),
            "duration": info.get("duration", None)
        }

    with open(scripts_json_path, "w", encoding="utf-8") as f:
        json.dump(export_data, f, indent=2, ensure_ascii=False)

    return {"status": "exported"}

# ---------------------------------------------------------
# Run TMDB Resolver
# ---------------------------------------------------------
@app.route("/api/run_tmdb_resolver", methods=["POST"])
def run_tmdb_resolver():
    script_path = "/home/<YOUR_PATH>/bluray/tmdb_resolver.py"
    result = subprocess.run(
        ["python3", script_path],
        capture_output=True,
        text=True
    )
    return {
        "returncode": result.returncode,
        "stdout": result.stdout,
        "stderr": result.stderr
    }

# ---------------------------------------------------------
# Run movies_alpha.py
# ---------------------------------------------------------
@app.route("/api/run_movies_alpha", methods=["POST"])
def run_movies_alpha():
    script_path = "/home/<YOUR_PATH>/bluray/movies_alpha.py"
    output_path = "/home/<YOUR_PATH>/bluray/movies_alpha.json"

    result = subprocess.run(
        ["python3", script_path],
        capture_output=True,
        text=True
    )

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(result.stdout)

    return {
        "returncode": result.returncode,
        "stdout": result.stdout[:5000],
        "stderr": result.stderr
    }

# ---------------------------------------------------------
# Run Flask
# ---------------------------------------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
