#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import json
import bottle
from bottle import HTTPResponse
from ..utils.utils import frame_to_image
from ..models.random_forest_model import RandomForest


def ping_response():
    return HTTPResponse(
        status=200
    )


def start_response(color):
    assert type(color) is str, \
        "Color value must be string"

    return HTTPResponse(
        status=200,
        headers={
            "Content-Type": "application/json"
        },
        body=json.dumps({
            "color": color
        })
    )


def move_response(move):
    assert move in ['up', 'down', 'left', 'right'], \
        "Move must be one of [up, down, left, right]"

    return HTTPResponse(
        status=200,
        headers={
            "Content-Type": "application/json"
        },
        body=json.dumps({
            "move": move
        })
    )


def end_response():
    return HTTPResponse(
        status=200
    )


@bottle.route('/')
def index():
    return '''
    Battlesnake documentation can be found at
       <a href="https://docs.battlesnake.com">https://docs.battlesnake.com</a>.
    '''


@bottle.route('/static/<path:path>')
def static(path):
    return bottle.static_file(path, root='static/')


@bottle.post('/ping')
def ping():
    return ping_response()


@bottle.post('/start')
def start():
    color = "#00FF00"
    return start_response(color)


@bottle.post('/move')
def move():
    data = bottle.request.json

    model = RandomForest()
    model.load("./model.pkl")

    my_id = data["you"]["id"]
    input_values = frame_to_image(data, my_id)
    direction = model.predict(input_values)

    return move_response(direction)


@bottle.post('/end')
def end():
    return end_response()


# Expose WSGI app (so gunicorn can find it)
application = bottle.default_app()


def main():
    bottle.run(
        application,
        host=os.getenv('IP', '0.0.0.0'),
        port=os.getenv('PORT', '8080'),
        debug=os.getenv('DEBUG', True)
    )


if __name__ == '__main__':
    main()
