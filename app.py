import os
import logging
import pytz
import pandas as pd
import requests
from dotenv import load_dotenv
from datetime import datetime
from flask import (
    Flask, redirect, render_template, request,
    send_from_directory, url_for, jsonify
)
from jinja2 import Template
from itsdangerous import TimestampSigner
from dateutil import parser

# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
)

app = Flask(__name__)
signer = TimestampSigner(os.getenv('SIGNER_SECRET', 'default-secret'))

# Simulated dataset (pandas usage)
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
        app.logger.warning('POST /hello - No name provided, redirecting to index')
        return redirect(url_for('index'))

@app.route('/api/timezones')
def get_timezones():
    # Return DataFrame content as JSON
    return jsonify(df.to_dict(orient='records'))

@app.route('/api/ip')
def get_ip_info():
    try:
        response = requests.get("https://api.ipify.org?format=json", timeout=5)
        ip_info = response.json()
        return jsonify(ip_info)
    except Exception as e:
        app.logger.error(f"Failed to get IP info: {e}")
        return jsonify({"error": "Could not retrieve IP info"}), 500

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
