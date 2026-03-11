from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ["DATABASE_URL"]
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

class Message(db.Model):
    __tablename__ = "messages"
    id = db.Column(db.Integer, primary_key=True)
    pseudo = db.Column(db.String(50), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "pseudo": self.pseudo,
            "content": self.content,
            "created_at": str(self.created_at)
        }

with app.app_context():
    db.create_all()

@app.route("/messages", methods=["GET"])
def get_messages():
    messages = Message.query.order_by(Message.created_at.desc()).all()
    return jsonify([m.to_dict() for m in messages])

@app.route("/messages", methods=["POST"])
def post_message():
    data = request.get_json()
    pseudo = data.get("pseudo", "").strip()
    content = data.get("content", "").strip()

    if not pseudo or not content:
        return jsonify({"error": "pseudo et content sont requis"}), 400
    if len(pseudo) > 50:
        return jsonify({"error": "pseudo trop long (max 50 caractères)"}), 400
    if len(content) > 1000:
        return jsonify({"error": "message trop long (max 1000 caractères)"}), 400

    message = Message(pseudo=pseudo, content=content)
    db.session.add(message)
    db.session.commit()
    return jsonify({"id": message.id, "message": "Message publié"}), 201

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)