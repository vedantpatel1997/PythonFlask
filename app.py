import os
import logging
import uuid
import pytz
import pandas as pd
import requests
from faker import Faker
from dotenv import load_dotenv
from datetime import datetime
from flask import (
    Flask, redirect, render_template, request,
    send_from_directory, url_for, jsonify
)
from flask_cors import CORS
from jinja2 import Template
from itsdangerous import TimestampSigner
from dateutil import parser

# Load .env config
load_dotenv()

app = Flask(__name__)
CORS(app)
faker = Faker()
signer = TimestampSigner(os.getenv('SIGNER_SECRET', 'dev-secret'))

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
)

# Static example data
df = pd.DataFrame({
    "name": ["Vedant", "Alice", "Bob"],
    "login_time": [datetime.now()] * 3
})

@app.route('/')
def index():
    utc_now = datetime.utcnow().replace(tzinfo=pytz.utc)
    est_now = utc_now.astimezone(pytz.timezone("US/Eastern"))
    parsed_date = parser.parse("2025-08-01T15:30:00Z")
    app.logger.info(f'GET / - UTC: {utc_now}, EST: {est_now}, Parsed: {parsed_date}')
    return render_template('index.html')

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(
        os.path.join(app.root_path, 'static'),
        'favicon.ico', mimetype='image/vnd.microsoft.icon'
    )

@app.route('/hello', methods=['POST'])
def hello():
    name = request.form.get('name', '').strip()
    if name:
        signed_name = signer.sign(name.encode()).decode()
        app.logger.info(f'POST /hello - Name received and signed: {signed_name}')
        return render_template('hello.html', name=name, signed=signed_name)
    else:
        app.logger.warning('POST /hello - No name provided')
        return redirect(url_for('index'))

@app.route('/api/timezones')
def get_timezones():
    return jsonify(df.to_dict(orient='records'))

@app.route('/api/ip')
def get_ip_info():
    try:
        response = requests.get("https://api.ipify.org?format=json", timeout=5)
        return jsonify(response.json())
    except Exception as e:
        app.logger.error(f"IP fetch failed: {e}")
        return jsonify({"error": "Could not retrieve IP info"}), 500

# @app.route('/api/uuid')
# def generate_uuid():
#     uid = str(uuid.uuid4())
#     return jsonify({"uuid": uid})

@app.route('/api/fakeuser')
def fake_user():
    fake_data = {
        "name": faker.name(),
        "email": faker.email(),
        "address": faker.address(),
        "dob": str(faker.date_of_birth())
    }
    return jsonify(fake_data)

@app.route('/api/env')
def show_env():
    return jsonify({
        "SIGNER_SECRET": os.getenv("SIGNER_SECRET"),
        "DEBUG": os.getenv("DEBUG"),
        "PORT": os.getenv("PORT"),
        "WEBSITE_HTTPLOGGING_RETENTION_DAYS": os.getenv("WEBSITE_HTTPLOGGING_RETENTION_DAYS"),
        "SCM_DO_BUILD_DURING_DEPLOYMENT": os.getenv("SCM_DO_BUILD_DURING_DEPLOYMENT")
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8000))
    debug_mode = os.environ.get('DEBUG', 'False').lower() == 'true'
    app.logger.info(f"Starting Flask app on port {port} with debug={debug_mode}")
    app.run(host='0.0.0.0', port=port, debug=debug_mode, threaded=True)




# python -m venv .venv
# .venv\Scripts\Activate
# python.exe -m pip install --upgrade pip
# pip install -r requirements.txt
# pip freeze > requirements.txt
