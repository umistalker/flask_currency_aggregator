from programm import api
from programm.view import HelloWorld, Rate

api.add_resource(HelloWorld, '/')
api.add_resource(Rate, '/rate')