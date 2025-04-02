from flask import render_template, request, redirect
from app import app, db
from models import Visit
from datetime import datetime
import requests
import logging

def get_client_ip():
    """Get the client's IP address from various possible headers"""
    if request.headers.get('X-Forwarded-For'):
        ip = request.headers.get('X-Forwarded-For').split(',')[0]
    elif request.headers.get('X-Real-IP'):
        ip = request.headers.get('X-Real-IP')
    else:
        ip = request.remote_addr
    return ip

def get_geolocation(ip):
    """Get geolocation data for an IP address"""
    try:
        response = requests.get(f'http://ip-api.com/json/{ip}')
        if response.status_code == 200:
            data = response.json()
            if data.get('status') == 'success':
                return {
                    'country': data.get('country'),
                    'city': data.get('city'),
                    'region': data.get('regionName'),
                    'latitude': data.get('lat'),
                    'longitude': data.get('lon')
                }
    except Exception as e:
        app.logger.error(f"Error getting geolocation: {str(e)}")
    return {}

@app.route('/')
def index():
    """Redirect to allpvp.pl but record the IP first"""
    try:
        # Record the visit
        record_visit(get_client_ip())
        # Redirect to allpvp.pl
        return redirect("http://is.allpvp.pl")
    except Exception as e:
        app.logger.error(f"Error handling redirect: {str(e)}")
        return redirect("http://is.allpvp.pl")

@app.route('/checkip')
def checkip():
    """Show visitor their IP address"""
    try:
        client_ip = get_client_ip()
        # Record the visit
        record_visit(client_ip)
        return render_template('index.html', ip_address=client_ip)
    except Exception as e:
        app.logger.error(f"Error handling visit: {str(e)}")
        return render_template('index.html', error="Unable to detect IP address")

def record_visit(client_ip):
    """Record or update a visit in the database"""
    try:
        # Check if IP exists
        visit = Visit.query.filter_by(ip_address=client_ip).first()

        if visit:
            # Update existing visit
            visit.visit_count += 1
            visit.last_visit = datetime.utcnow()
        else:
            # Create new visit and get geolocation
            geo_data = get_geolocation(client_ip)
            visit = Visit(
                ip_address=client_ip,
                country=geo_data.get('country'),
                city=geo_data.get('city'),
                region=geo_data.get('region'),
                latitude=geo_data.get('latitude'),
                longitude=geo_data.get('longitude')
            )

        db.session.add(visit)
        db.session.commit()
        return True
    except Exception as e:
        app.logger.error(f"Error recording visit: {str(e)}")
        return False

@app.route('/admin/visits')
def admin_visits():
    visits = Visit.query.order_by(Visit.last_visit.desc()).all()
    return render_template('admin/visits.html', visits=visits)