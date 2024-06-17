from flask import Flask, jsonify, send_from_directory, request
from flask_swagger_ui import get_swaggerui_blueprint
import requests

app = Flask(__name__)

# Swagger UI configuration
SWAGGER_URL = '/swagger'
API_URL = '/swagger.json'

swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={'app_name': "Dynamic Swagger API"}
)

app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

@app.route('/')
def home():
    return "Hello, World!"

# Route to call an external API and return JSON response
@app.route('/fetch-data', methods=['GET'])
def fetch_data():
    external_api_url = 'https://api.coindesk.com/v1/bpi/currentprice.json'  # Example API
    response = requests.get(external_api_url)
    data = response.json()
    return jsonify(data)

# Route to serve Swagger JSON dynamically based on the fetched data
@app.route('/swagger.json')
def swagger_json():
    swagger_template = {
        "swagger": "2.0",
        "info": {
            "title": "Dynamic API",
            "description": "API description in Markdown.",
            "version": "1.0.0"
        },
        "host": request.host,
        "schemes": ["http"],
        "paths": {
            "/fetch-data": {
                "get": {
                    "summary": "Fetch data from an external API",
                    "responses": {
                        "200": {
                            "description": "Successful response",
                            "schema": {
                                "type": "object"
                            }
                        }
                    }
                }
            }
        }
    }
    return jsonify(swagger_template)

if __name__ == "__main__":
    app.run(debug=True)
