from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Define the URLs for the microservices
AUTH_SERVICE_URL = 'http://127.0.0.1:6000'  # Replace with actual URL and port for authentication service
TODO_SERVICE_URL = 'http://127.0.0.1:7000'  # Replace with actual URL and port for todo service

# Helper function to route requests
def forward_request(service_url):
    response = requests.request(
        method=request.method,
        url=f"{service_url}{request.path}",
        headers={key: value for (key, value) in request.headers if key != 'Host'},
        data=request.get_data(),
        params=request.args
    )
    return (response.content, response.status_code, response.headers.items())

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH'])
def gateway(path):
    if path.startswith('auth') or path.startswith('login') or path.startswith('register'):
        return forward_request(AUTH_SERVICE_URL)
    elif path.startswith('todo'):
        return forward_request(TODO_SERVICE_URL)
    else:
        return jsonify({'error': 'Service not found'}), 404

if __name__ == "__main__":
    app.run(debug=True, port=5000)
