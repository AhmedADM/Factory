from crypt import methods
from flask import  jsonify, request
from flask_restx import Resource






class Home(Resource):

    def get(self):
        return jsonify({
            "message": "Factory API"
        })






