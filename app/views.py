from flask import render_template, redirect, url_for

from app import app
from app.lib.games import Game

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/new-game", methods=["POST"])
def new_game():
    app.game = Game()
    app.game.setup_game()

    return redirect(url_for("run_game"))

@app.route("/run-game", methods=["GET", "POST"])
def run_game():
    if app.game is None:
        app.game = Game()
        app.game.setup_game()

    game = app.game
    game_display = game.get_game_display()

    return render_template("game.html",
        game_display="\n".join(game_display))
