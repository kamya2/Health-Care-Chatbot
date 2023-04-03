import datetime
from flask import Flask, request, jsonify, session
from flask_cors import CORS, cross_origin
from chatbot import HealthCareChatBot
import json
from flask_pymongo import PyMongo
import bcrypt
from pymongo import MongoClient
from bson.objectid import ObjectId

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)


bot = HealthCareChatBot()

app.secret_key = 'your_secret_key_here'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/chatbot_db'
mongo = PyMongo(app)
mongo_client = MongoClient('mongodb://localhost:27017/chatbot_db')
mongo_db = mongo_client['chatbot_db']
users_collection = mongo_db.get_collection('users')
conversations_collection = mongo_db.get_collection('conversations')


@ app.route("/search-answer", methods=['POST'])
@cross_origin(supports_credentials=True)
def search_answer():

    username = request.cookies.get('username')
    email = request.cookies.get('email')
    if username and email:
        pass
    else:
        return jsonify({'success': False, 'message': 'User not logged in'}), 400

    user_query = request.json['q']
    conversation_id = request.json['conversation_id']

    returned_answer = bot.get_response(user_query)
    data = {
        "search": user_query,
        "message": returned_answer
    }

    user_message = {
        'type': 'text',
        'message': user_query,
        'sender': 'user',
        'direction': 'outgoing',
    }

    bot_message = {
        'type': 'text',
        'message': returned_answer,
        'sender': 'bot',
        'direction': 'incoming',
    }

    messages = [user_message, bot_message]

    conversations_collection.update_one({'_id': ObjectId(conversation_id)}, {
                                        '$push': {'messages': {'$each': messages}}})

    return json.dumps(data)


@app.route('/register', methods=['POST'])
@cross_origin(supports_credentials=True)
def register():
    try:
        username = request.json['first_name'] + ' ' + request.json['last_name']
        password = request.json['password']
        email = request.json['email']
        hashed_password = bcrypt.hashpw(
            password.encode('utf-8'), bcrypt.gensalt())
        user_id = users_collection.insert_one(
            {'username': username, 'password': hashed_password, 'email': email})
        response = jsonify(
            {'success': True, 'data': {'user_id': str(user_id)}})
        response.set_cookie('username', username, max_age=604800)
        response.set_cookie('email', email, max_age=604800)
        return response, 201
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 400


@app.route('/login', methods=['POST'])
@cross_origin(supports_credentials=True)
def login():
    try:
        password = request.json['password']
        email = request.json['email']
        user = users_collection.find_one({'email': email})
        if user and bcrypt.checkpw(password.encode('utf-8'), user['password']):
            username = user['username']
            email = user['email']
            response = jsonify({'success': True})
            response.set_cookie('username', username, max_age=604800)
            response.set_cookie('email', email, max_age=604800)
            return response, 200
        else:
            return jsonify({'success': False, 'message': 'Invalid username or password'}), 401
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 400


@app.route('/validate_session', methods=['GET'])
@cross_origin(supports_credentials=True)
def validate_session():
    try:
        username = request.cookies.get('username')
        email = request.cookies.get('email')
        if username and email:
            return jsonify({'success': True}), 200
        else:
            return jsonify({'success': False, 'message': 'User not logged in'}), 400
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 400


@app.route('/logout', methods=['POST'])
@cross_origin(supports_credentials=True)
def logout():
    try:
        response = jsonify({'success': True})
        response.delete_cookie('username')
        response.delete_cookie('email')
        return response, 200
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 400


@app.route('/conversation', methods=['POST'])
@cross_origin(supports_credentials=True)
def create_conversation():
    try:
        username = request.cookies.get('username')
        email = request.cookies.get('email')
        if username and email:
            pass
        else:
            return jsonify({'success': False, 'message': 'User not logged in'}), 400

        conversation_title = 'Conversation ' + \
            str(conversations_collection.count_documents({}) + 1)
        result = conversations_collection.insert_one(
            {'title': conversation_title, 'messages': []})

        return jsonify({'success': True, 'data': {'conversation_id': str(result.inserted_id)}}), 201
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 400


@app.route('/conversation', methods=['GET'])
@cross_origin(supports_credentials=True)
def get_conversations():
    try:
        username = request.cookies.get('username')
        email = request.cookies.get('email')
        if username and email:
            pass
        else:
            return jsonify({'success': False, 'message': 'User not logged in'}), 400

        conversation_list = []

        for conversation in conversations_collection.find():

            conversation_list.append({'conversation_id': str(conversation['_id']),
                                      'title': str(conversation['title']) or ''})
        return jsonify({'success': True, 'data': {'conversations': conversation_list}}), 200
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 400


@app.route('/message/<conversation_id>', methods=['GET'])
@cross_origin(supports_credentials=True)
def get_messages(conversation_id):
    try:
        print('get_messages(conversation_id):')
        username = request.cookies.get('username')
        email = request.cookies.get('email')
        if username and email:
            pass
        else:
            return jsonify({'success': False, 'message': 'User not logged in'}), 400
        print(conversation_id)
        conversation = conversations_collection.find_one(
            {'_id': ObjectId(conversation_id)})
        print(conversation)
        if conversation:
            return jsonify({'success': True, 'data': {'messages': conversation['messages'], 'conversation_id': conversation_id, 'conversation_title': conversation['title']}}), 200
        else:
            return jsonify({'success': False, 'message': 'Conversation not found'}), 404
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 400


@app.route('/conversation/<conversation_id>', methods=['DELETE'])
@cross_origin(supports_credentials=True)
def delete_conversation(conversation_id):
    try:
        username = request.cookies.get('username')
        email = request.cookies.get('email')
        if username and email:
            pass
        else:
            return jsonify({'success': False, 'message': 'User not logged in'}), 400

        result = conversations_collection.delete_one({'_id': ObjectId(conversation_id)})
        if result.deleted_count == 1:
            return jsonify({'success': True, 'message': 'Conversation deleted'}), 200
        else:
            return jsonify({'success': False, 'message': 'Conversation not found'}), 404
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 400
