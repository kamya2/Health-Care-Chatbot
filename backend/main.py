from flask import Flask, request
from flask_cors import CORS
from chatbot import HealthCareChatBot
import json
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})
bot = HealthCareChatBot()


@ app.route("/search-answer")
def home():
    user_query = request.args.get('q', '')

    data = {
        "search": user_query,
        "message": bot.get_response(user_query)
    }

    return json.dumps(data)
