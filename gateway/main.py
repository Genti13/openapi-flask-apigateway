from flask import Flask, jsonify, request, abort
import requests
from werkzeug.security import safe_join

app = Flask(__name__)


@app.errorhandler(405)
def error_405(e):
    return jsonify({"error": "Method Not Allowed"}), 405


@app.errorhandler(500)
def error_500(e):
    return jsonify({"error": f"Error in the request {str(e)}"}), 500

@app.errorhandler(400)
def error_400(e):
    return jsonify({"error": "Invalid path"}), 400



@app.route("/api/<path:path>", methods=["GET", "POST"])
def gateway(path):

    try:
        path = safe_join("", path)
    except (ValueError, TypeError):
        return abort(400)

    query = request.args if request.method == "GET" else request.json if request.is_json else request.form

    try:
        response = requests.request(
            method=request.method,
            url=f"http://127.0.0.1:33667/{path}",
            json=query if request.method == "POST" else None,
            params=query if request.method == "GET" else None,
            headers={'Content-Type': 'application/json'}
        )
    except:
        abort(500)

    if response.status_code == 405:
        abort(405)

    return response.json(), response.status_code


if __name__ == '__main__':
    app.run(debug=True)
