from flask import Flask, render_template
import requests
import os

app = Flask(__name__)
API_URL = os.environ.get("API_URL", "http://api:5000")

@app.route("/")
def index():
    try:
        resp = requests.get(f"{API_URL}/messages", timeout=5)
        messages = resp.json()
    except Exception:
        messages = []
    return render_template("index.html", messages=messages)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)