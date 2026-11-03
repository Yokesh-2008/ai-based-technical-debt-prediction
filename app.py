from flask import Flask, render_template, request, jsonify, send_file
from pathlib import Path
import tempfile, zipfile, io, json
from analyzer import analyze_project

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 25 * 1024 * 1024
ALLOWED = {".py"}

@app.get("/")
def index():
    return render_template("index.html")

@app.post("/api/analyze")
def analyze():
    uploaded = request.files.get("project")
    if not uploaded or not uploaded.filename:
        return jsonify({"error": "Choose a ZIP file containing Python source code."}), 400
    if not uploaded.filename.lower().endswith(".zip"):
        return jsonify({"error": "Please upload a .zip repository."}), 400
    try:
        with zipfile.ZipFile(uploaded.stream) as archive:
            with tempfile.TemporaryDirectory() as tmp:
                root = Path(tmp).resolve()
                for info in archive.infolist():
                    target = (root / info.filename).resolve()
                    if root not in target.parents and target != root:
                        continue
                    if info.is_dir():
                        target.mkdir(parents=True, exist_ok=True)
                    else:
                        target.parent.mkdir(parents=True, exist_ok=True)
                        target.write_bytes(archive.read(info))
                result = analyze_project(root)
        return jsonify(result)
    except zipfile.BadZipFile:
        return jsonify({"error": "The uploaded file is not a valid ZIP archive."}), 400
    except Exception as exc:
        app.logger.exception("Analysis failed")
        return jsonify({"error": f"Analysis failed: {exc}"}), 500

@app.get("/health")
def health():
    return jsonify({"status": "ok"})

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
