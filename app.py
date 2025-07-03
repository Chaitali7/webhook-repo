from flask import Flask, request, jsonify, render_template
from pymongo import MongoClient
from utils import format_timestamp
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
DATABASE_NAME = os.getenv("DATABASE_NAME", "webhook_db")
COLLECTION_NAME = os.getenv("COLLECTION_NAME", "events")

client = MongoClient(MONGO_URI)
db = client[DATABASE_NAME]
collection = db[COLLECTION_NAME]

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/events', methods=['GET'])
def get_events():
    events = list(collection.find().sort("timestamp", -1))
    result = []
    for event in events:
        result.append({
            "author": event["author"],
            "action_type": event["action_type"],
            "from_branch": event.get("from_branch"),
            "to_branch": event["to_branch"],
            "timestamp": format_timestamp(event["timestamp"].strftime("%Y-%m-%dT%H:%M:%SZ"))
        })
    return jsonify(result)

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    action_type = None
    author = data.get("pusher", {}).get("name")
    from_branch = None
    to_branch = None

    if "pull_request" in data:
        action_type = "pull_request"
        author = data["pull_request"]["user"]["login"]
        from_branch = data["pull_request"]["head"]["ref"]
        to_branch = data["pull_request"]["base"]["ref"]
    elif "pusher" in data and "ref" in data:
        action_type = "push"
        to_branch = data["ref"].split("/")[-1]
    elif data.get("action") == "closed" and data.get("pull_request", {}).get("merged"):
        action_type = "merge"
        author = data["pull_request"]["user"]["login"]
        from_branch = data["pull_request"]["head"]["ref"]
        to_branch = data["pull_request"]["base"]["ref"]

    if action_type:
        event_doc = {
            "author": author,
            "action_type": action_type,
            "from_branch": from_branch,
            "to_branch": to_branch,
            "timestamp": datetime.utcnow()
        }
        collection.insert_one(event_doc)
        return "Event stored", 200
    else:
        return "Unsupported event", 400

if __name__ == "__main__":
    app.run(debug=True)
