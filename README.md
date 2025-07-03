Webhook Receiver Repo
 Overview
This repository (webhook-repo) receives GitHub webhook events from a separate repo (action-repo) and displays them in a minimal, clean UI.

Supported events:

Push

Pull Request

Merge (handled as a merged PR for extra credit)


⚙️ Setup Instructions

1️⃣ Clone the repository

git clone https://github.com/yourusername/webhook-repo.git
cd webhook-repo

2️⃣ Install dependencies

pip install -r requirements.txt

3️⃣ Configure environment

Copy the example environment file:
 cp .env.example .env

Edit .env as needed:

MONGO_URI=mongodb://localhost:27017
DATABASE_NAME=webhook_db
COLLECTION_NAME=events

4️⃣ Start MongoDB
Make sure you have MongoDB running locally (default port: 27017) or use a cloud connection string.

5️⃣ Run the Flask app

python app.py
The app will run by default at: http://localhost:5000

🛰️ Setup GitHub Webhook

1. Go to your action-repo → Settings → Webhooks → Add webhook
2. Payload URL: http://your-server-ip:5000/webhook
3. Content type: application/json
4. Select individual events: Push, Pull Request, Merge (handled as closed merged PR)
5. Save.

Test

1. Push to action-repo
2. Create PR, merge, etc.
3. Open http://localhost:5000 to view UI.



