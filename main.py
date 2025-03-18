from flask import Flask, render_template, request
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = Flask(__name__)

def get_client_ip():
    """Get the client's IP address from various possible headers"""
    if request.headers.get('X-Forwarded-For'):
        ip = request.headers.get('X-Forwarded-For').split(',')[0]
    elif request.headers.get('X-Real-IP'):
        ip = request.headers.get('X-Real-IP')
    else:
        ip = request.remote_addr
    return ip

@app.route('/')
def index():
    try:
        client_ip = get_client_ip()
        logger.debug(f"Detected client IP: {client_ip}")
        return render_template('index.html', ip_address=client_ip)
    except Exception as e:
        logger.error(f"Error detecting IP address: {str(e)}")
        return render_template('index.html', error="Unable to detect IP address")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
