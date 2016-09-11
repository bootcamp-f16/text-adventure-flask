from flask import request, render_template, redirect, url_for

from app import app
from app.lib.games import Game
from app.forms import GameForm

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
    form = GameForm(request.form)

    if request.method == "POST" and form.validate():
        action_result = game.process(form.user_input.data)
    else:
        action_result=""

    game_display = game.get_game_display()

    return render_template("game.html",
        game_display="\n".join(game_display),
        game_form=form,
        action_result=action_result,
        should_exit=game.should_exit)
