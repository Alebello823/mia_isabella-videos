import os, uuid, subprocess, threading, time
from flask import Flask, request, jsonify, send_file

app = Flask(__name__)
DOWNLOAD_DIR = "downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

def auto_delete():
    while True:
        time.sleep(600)
        now = time.time()
        for f in os.listdir(DOWNLOAD_DIR):
            path = os.path.join(DOWNLOAD_DIR, f)
            if os.path.getmtime(path) < now - 1800:
                try: os.remove(path)
                except: pass
threading.Thread(target=auto_delete, daemon=True).start()

@app.route("/download", methods=["POST"])
def download():
    url = request.json.get("url")
    file_id = str(uuid.uuid4())
    filename = f"{file_id}.mp4"
    filepath = os.path.join(DOWNLOAD_DIR, filename)
    try:
        # Comando optimizado para mejor calidad
        subprocess.run(['yt-dlp', '-f', 'bestvideo+bestaudio/best', '--merge-output-format', 'mp4', '-o', filepath, url], check=True)
        return jsonify({"status": "ok", "file_id": filename, "size": os.path.getsize(filepath)})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route("/file/<filename>")
def get_file(filename):
    return send_file(os.path.join(DOWNLOAD_DIR, filename), as_attachment=True)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

