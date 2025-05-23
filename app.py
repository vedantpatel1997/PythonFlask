import os
import logging
from flask import (
    Flask, redirect, render_template, request,
    send_from_directory, url_for
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
)

app = Flask(__name__)

@app.route('/')
def index():
    app.logger.info('GET / - index page requested')
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
        app.logger.info(f'POST /hello - Name received: {name}')
        return render_template('hello.html', name=name)
    else:
        app.logger.warning('POST /hello - No name provided, redirecting to index')
        return redirect(url_for('index'))

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug_mode = os.environ.get('DEBUG', 'False').lower() == 'true'
    
    app.logger.info(f"Starting Flask app on port {port} with debug={debug_mode}")
    app.run(host='0.0.0.0', port=port, debug=debug_mode, threaded=True)
