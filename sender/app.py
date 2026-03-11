from flask import Flask, render_template, request, redirect, url_for
import requests
import os

app = Flask(__name__)
API_URL = os.environ.get("API_URL", "http://api:5000")

@app.route("/")
def index():
    error = request.args.get("error")
    success = request.args.get("success")
    return render_template("index.html", error=error, success=success)

@app.route("/send", methods=["POST"])
def send():
    pseudo = request.form.get("pseudo", "").strip()
    content = request.form.get("content", "").strip()

    if not pseudo or not content:
        return redirect(url_for("index", error="pseudo et message sont requis"))

    try:
        resp = requests.post(
            f"{API_URL}/messages",
            json={"pseudo": pseudo, "content": content},
            timeout=5
        )
        if resp.status_code == 201:
            return redirect(url_for("index", success="Message publié !"))
        else:
            err = resp.json().get("error", "Erreur inconnue")
            return redirect(url_for("index", error=err))
    except Exception:
        return redirect(url_for("index", error="API inaccessible"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)