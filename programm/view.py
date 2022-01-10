import json

import bs4
import jinja2
import requests
from flask import render_template, Response
from flask_restful import Resource
from werkzeug.utils import redirect

from programm import controllers, app


class HelloWorld(Resource):
    def get(self):
        return {'message': "Hello World"}, 200


class Rate(Resource):
    def get(self):
        name = 'Mark'
        context = {'context': name}
        return render_template('rate.html', context=name)


@app.route('/ar')
def route():
    return render_template('rate.html', context='Mark')
