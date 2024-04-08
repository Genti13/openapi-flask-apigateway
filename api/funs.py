from flask import jsonify, request

def hello():
    return jsonify({"message": "Hello, world!"})
