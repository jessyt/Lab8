from flask import Flask, request, jsonify
from service import GameApp
from models import Schema
import json
app = Flask(__name__)

@app.after_request
def add_headers(response):
    response.headers['Access-Control-Allow-Origin'] = "*"
    response.headers['Access-Control-Allow-Headers'] = "Content-Type, Access-Control-Allow-Headers, Authorization, X-Requested-With"
    response.headers['Access-Control-Allow-Methods']= "POST, GET, PUT, DELETE, OPTIONS"
    return response

@app.route("/")
def hello():
    return "Cribbage Game App!"

@app.route("/getgamebyid/<game_id>", methods=["GET"])
def get_game_by_id(game_id):
    return jsonify(GameApp().get_game_by_id(game_id))

@app.route("/createGame", methods=["POST"])
def create_game():
    return jsonify(GameApp().create_game(request.get_json()))

@app.route("/getallgames", methods=["GET"])
def get_all_games():
    return jsonify(GameApp().get_games())

@app.route("/incrementPlayersPoints", methods=["POST"])
def update_players_points():
    return jsonify(GameApp().update_Points(request.get_json()))
    
#########################
## PLAYER INFORMATION
#########################
@app.route("/createplayer", methods=["POST"])
def create_player():
    jsonData = request.get_json()
    name = jsonData.get("name")
    return jsonify(GameApp().create_player(name))

@app.route("/getallplayers", methods=["GET"])
def get_all_players():
    return jsonify(GameApp().get_players())

@app.route("/incrementplayerwins", methods=["POST"])
def increment_players_wins():
    return jsonify(GameApp().increment_wins(request.get_json()))

@app.route("/incrementplayerlosses", methods=["POST"])
def increment_players_losses():
    return jsonify(GameApp().increment_losses(request.get_json()))


if __name__ == "__main__":
    Schema()
    app.run(host='0.0.0.0', port=5000)
