from flask import Flask, jsonify, render_template, request, session
import redis
import json
from pymongo import MongoClient
from flask_session import Session
from funcs_db import check_blacklist, check_whitelist, add_to_blacklist, add_to_whitelist  # Import your SQLite functions

# Config
server = Flask(__name__)
redisPort = 6379
redisClient = redis.Redis("localhost", redisPort)

server.config["SESSION_PERMANENT"] = False
server.config["SESSION_TYPE"] = "filesystem"
Session(server)

client = MongoClient("Enter_MongoDB_Connection_Link_here")
data_base = client["test"]

# Supplementary functions
def check_in_history(input_url):
    try:
        result = -1
        details = data_base.history.find({"url":input_url})[0]
        print(details)
        if details:
            result = details["status"]
        return result
    except:
        return -1

def add_to_history(url, status):
    status = (int)(status)
    data_base.history.insert_one({'url': url, 'status': status})

# Endpoints
@server.route("/", methods=["GET"])
def home():
    session.clear() 
    session["ans"] = "unknown"
    return render_template("home.html")

@server.route("/view_history", methods=["GET"])
def dashboard():
    details = data_base.history.find()
    return render_template("view_history.html",details = details)

@server.route("/url_detect", methods=["POST"])
def submitURL():
    data = request.get_json()
    if 'url' not in data:
        return jsonify({'error': 'no url provided'}), 400
    url = data['url']
    
    # Check if the URL is in the whitelist
    if check_whitelist("blacklist_whitelist.db",url):
        result = "legit"
        session["ans"] = "legit"
        redisClient.hset("url_predictions", url, result)
        return jsonify({'message': 'URL found in whitelist. Marked as legit.'})
    
    # Check if the URL is in the blacklist
    if check_blacklist("blacklist_whitelist.db",url):
        result = "phishing"
        session["ans"] = "phishing"
        redisClient.hset("url_predictions", url, result)
        return jsonify({'message': 'URL found in blacklist. Marked as phishing.'})
    
    res2 = check_in_history(url)
    if (res2 == 1):
        session["ans"] = "phishing"
        redisClient.hset("url_predictions", url, "phishing")
        return jsonify({'url': url, 'prediction': "phishing", 'message': 'History Detection'})
    elif (res2 == 0):
        session["ans"] = "legit"
        redisClient.hset("url_predictions", url, "legit")
        return jsonify({'url': url, 'prediction': "legit", 'message': 'History Detection'})

    
    # If the URL is not found in either list, add it to the Redis queue
    url_data = {"url": url}
    redisClient.rpush("UrlQueue", json.dumps(url_data))
    
    return jsonify({'message': 'URL submitted successfully. Please check back later for the result.'})

@server.route("/result", methods=["GET"])
def get_result():
    url = request.args.get('url')
    if not url:
        return jsonify({'error': 'no url provided'}), 400

    # Retrieve the prediction result from the Redis hash
    prediction = redisClient.hget("url_predictions", url)
    if not prediction:
        return jsonify({'message': 'Prediction is still being processed, please check again later.'}), 202
    

    # Optionally delete the result after retrieval
    redisClient.hdel("url_predictions", url)
    if (prediction.decode('utf-8') == "phishing"):
        add_to_history(url, 1)
    elif (prediction.decode('utf-8') == "legit"):
        add_to_history(url, 0)
    return jsonify({'url': url, 'prediction': prediction.decode('utf-8')})

if __name__ == "__main__":
    server.run(debug=True)
