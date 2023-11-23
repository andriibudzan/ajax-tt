import json

from flask import Flask, jsonify
from flask_httpauth import HTTPTokenAuth

import pandas as pd

app = Flask(__name__)
auth = HTTPTokenAuth(scheme='Bearer')

# Sample Bearer token for demonstration purposes
token = 'mytoken1'


def load_data():
    df = pd.read_csv('./data/gold/employees_detailed.csv')
    df = (
        df
        .astype({'id': 'Int64', 'reports': 'Int64'})
        .drop(labels=['token'], axis=1)
    )
    return df

# Verify Bearer token
@auth.verify_token
def verify_token(given_token):
    return given_token == token


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
        return jsonify({'error': 'User not found'}), 404


if __name__ == '__main__':
    app.run(debug=True)
