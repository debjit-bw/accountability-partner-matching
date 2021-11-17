import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "./keys/keyfile.json"

if "PORT" in os.environ:
    PORT = os.environ["PORT"]
else:
    PORT = 8080

from flask import Flask, request
from flask_cors import CORS
from packages.flask_firebase_admin import FirebaseAdmin
from database.database import db_manager
from core.matcher.main import matcher

algo = matcher(
    [
        -1.141253420905099,
        0.4110048023788764,
        0.2493821256254638,
        1.8826022654166499,
        4.397295230211623,
    ]
) # Parameters from optimization

app = Flask(__name__)

# CORS allowance
CORS(app, resources={r"/*": {"origins": "*"}})
app.config["CORS_HEADERS"] = "Content-Type"

# Database setup
firebase = FirebaseAdmin(app)  # uses GOOGLE_APPLICATION_CREDENTIALS
db = db_manager(firebase)

# Routing here
@app.route("/get_matches", methods=["GET", "POST"])
@firebase.jwt_required
def get_matches():
    interested_users = db.get_interested_users(is_test = False)
    seeking_user_id = request.jwt_payload["user_id"]
    if seeking_user_id in interested_users:
        # seeking_user = interested_users[seeking_user_id]
        suggestions = algo.get_suggestions(seeking_user_id, interested_users)
        return suggestions
    else:
        return {
            "msg": "User not found in interested_users document",
        }, 404


# Unprotected route for testing
@app.route("/d/get_matches/<user_id>", methods=["GET", "POST"])
def d_get_matches(user_id):
    interested_users = db.get_interested_users(is_test = True)
    seeking_user_id = str(user_id)
    if seeking_user_id in interested_users:
        # seeking_user = interested_users[seeking_user_id]
        suggestions = algo.get_suggestions(seeking_user_id, interested_users)
        return {"matches": suggestions}
    else:
        return {
            "msg": "User not found in interested_users document",
        }, 404


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=PORT)
