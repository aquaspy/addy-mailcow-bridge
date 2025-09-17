from flask import Flask, request, jsonify
from os import getenv
from dotenv import load_dotenv
from secrets import token_urlsafe
import requests
from waitress import serve

load_dotenv() 
MAILCOW_DOMAIN = getenv("MAILCOW_DOMAIN")
app = Flask(__name__)

def make_alias(domain: str, bytes: int = 16) -> str:
    """Return a random alias like: aBc3dE5fGh@domain.tld"""
    local = token_urlsafe(bytes)          # url-safe, no + or /
    return f"{local}@{domain}"

@app.route('/<path:destination_email>/api/v1/aliases', methods=['POST']) 
def create_alias(destination_email):
    #Getting data
    data = request.json
    domain = data.get('domain')
    MAILCOW_API_KEY = (request.headers.get("Authorization") or "").removeprefix("Bearer ").strip()
    #Generating the actual alias
    alias = make_alias(domain)

    # Making the actual request

    resp = requests.post(
    f"{MAILCOW_DOMAIN}/api/v1/add/alias",
    headers={
        "Content-Type": "application/json",
        "x-api-key": MAILCOW_API_KEY
    },
    json={
        "active": 1,
        "address": alias,
        "goto": destination_email
    },
    timeout=10
) 
    

    return jsonify({"data": {"email": alias}}), 201

if __name__ == '__main__':
    serve(app, host='0.0.0.0', port=6510)
