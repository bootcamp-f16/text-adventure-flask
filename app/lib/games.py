from random import randint
from os import environ
import requests

from app.lib.rooms import rooms_builder
from app.lib.requests import Request
from app.lib.responses import Response
from app.lib.actions import Action
from app.lib.io_utils import clear_screen, draw, prompt, exit
from app.lib.players import Player

import app.lib.game_actions as game_actions

class Game():
    def __init__(self):
        super().__init__()
        self.current_room = None
        self.repo = None
        self.should_exit = False
        self.actions = [
            Action('echo', take_action=game_actions.echo_action),
            Action('help', take_action=game_actions.help_action),
            Action('exit', 'game', take_action=game_actions.exit_action),
        ]

    def setup_game(self, rooms_builder=rooms_builder, requests=requests, environ=environ):
        auth = (
            environ.get("GITHUB_USER"),
            environ.get("GITHUB_PASSWORD")
        )
        r = requests.get("https://api.github.com/orgs/bootcamp-f16/repos")
        repos = r.json()
        self.repo = repos[randint(0, len(repos) - 1)]
        self.current_room = rooms_builder()
        self.player = Player()
        self.tries_left = 3

    def set_exit(self):
        self.should_exit = True

    def get_game_display(self):
        game_display = []
        game_display.append("GITHUB ADVENTURES")
        game_display.append("="*60)
        game_display.append(self.current_room.draw())
        game_display.append("")
        game_display.append("HEALTH: {}      GUESSES LEFT: {}".format(self.player.health, self.tries_left))
        game_display.append("="*60)

        return game_display

    def run(self):

        response = Response()

        draw("GITHUB ADVENTURES")
        draw("="*60)
        draw(self.current_room.draw())
        draw("")
        draw("HEALTH: {}      GUESSES LEFT: {}".format(self.player.health, self.tries_left))
        draw("="*60)
        draw(response.draw())

        # Check if we are exiting before prompting the user
        if self.should_exit:
            return exit()

        user_input = prompt()
        request = Request(user_input)
        response = Response()

        for action in self.actions:
            if(action.should_take_action(request)):
                action.take_action(request, response, self)

        for action in self.current_room.actions:
            if(action.should_take_action(request)):
                action.take_action(request, response, self)

        if self.current_room.npc is not None:
            npc = self.current_room.npc
            for action in npc.actions:
                if(action.should_take_action(request)):
                    action.take_action(request, response, self)

        if self.current_room.clue is not None:
            clue = self.current_room.clue
            for action in clue.actions:
                if(action.should_take_action(request)):
                    action.take_action(request, response, self)

        if not request.action_taken:
            response.addOutput("Invalid input")

        self.check_conditions(request, response)

    def check_conditions(self, request, response):
        health = self.player.health
        if health <= 0 or self.tries_left <= 0:
            self.set_exit()
            response.addOutput("SORRY YOU LOSE!")
