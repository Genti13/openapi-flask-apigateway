from flask import Flask, Blueprint, jsonify, json, request
from openapi_routing import ROUTES

with open('openapi.json', 'r') as f:
    swagger_data = json.load(f)

app = Flask(__name__)
sample_api = Blueprint('sample_api', __name__)

# Función para registrar las rutas basadas en el JSON
def register_paths(swagger_data, blueprint):
    paths = swagger_data.get('paths')
    for path, methods in paths.items():
        for method, details in methods.items():
            operation_id = details.get('operationId')
            if operation_id:
                blueprint.add_url_rule(path, view_func=ROUTES[operation_id], methods=[method])

# Registrar las rutas basadas en el JSON
register_paths(swagger_data, sample_api)

# Registrar el Blueprint con la aplicación Flask
app.register_blueprint(sample_api)

if __name__ == '__main__':
    app.run(debug=True, port=33667)