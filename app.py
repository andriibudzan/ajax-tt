import json

from flask import Flask, jsonify
from flask_httpauth import HTTPTokenAuth
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash

import pandas as pd

app = Flask(__name__)
auth = HTTPBasicAuth()

# Sample Bearer token for demonstration purposes
token = 'mytoken1'

users = {
    "user1": generate_password_hash("Password1"),
    "user2": generate_password_hash("password2")
    }


def load_data():
    df = pd.read_csv('./data/gold/employees_detailed.csv')
    df = (
        df
        .astype({'id': 'Int64', 'reports': 'Int64'})
        .drop(labels=['token'], axis=1)
    )
    return df


# Verify Bearer token
@auth.verify_password
def verify_password(username, password):
    if username in users and check_password_hash(users.get(username), password):
        return username


# Endpoint to get all users (requires Bearer token authentication)
@app.route('/users', methods=['GET'])
@auth.login_required
def get_users():
    df = load_data()
    return json.dumps(df.to_dict(orient='records'), ensure_ascii=False), 200


# Endpoint to get a specific user by ID (requires Bearer token authentication)
@app.route('/users/<int:user_id>', methods=['GET'])
@auth.login_required
def get_user(user_id):
    df = load_data()
    if user_id in df['id'].values:
        return json.dumps(
                df[df['id'] == user_id].to_dict(orient='records'),
                ensure_ascii=False), 200
    else:
        return jsonify({'error': 'Employee not found'}), 404


if __name__ == '__main__':
    app.run(debug=True)
