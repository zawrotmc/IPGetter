from flask import render_template, request
from app import app, db
from models import Visit

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
        # Save visit to database
        visit = Visit(ip_address=client_ip)
        db.session.add(visit)
        db.session.commit()
        return render_template('index.html', ip_address=client_ip)
    except Exception as e:
        app.logger.error(f"Error handling visit: {str(e)}")
        return render_template('index.html', error="Unable to detect IP address")

@app.route('/admin/visits')
def admin_visits():
    visits = Visit.query.order_by(Visit.visit_time.desc()).all()
    return render_template('admin/visits.html', visits=visits)
