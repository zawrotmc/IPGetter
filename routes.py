from flask import render_template, request, redirect, session, url_for, flash, jsonify
from app import app, db
from models import Visit
from datetime import datetime
import requests
import logging
import os
from dotenv import load_dotenv

load_dotenv()

def get_admin_password():
    admin_password = os.getenv("PASSWORD")
    if not admin_password or admin_password.strip() == "":
        return "password"
    return admin_password.strip()

def get_client_ip():
    if request.headers.get('X-Forwarded-For'):
        ip = request.headers.get('X-Forwarded-For').split(',')[0]
    elif request.headers.get('X-Real-IP'):
        ip = request.headers.get('X-Real-IP')
    else:
        ip = request.remote_addr
    return ip

def get_geolocation(ip):
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

def record_visit(client_ip):
    try:
        visit = Visit.query.filter_by(ip_address=client_ip).first()
        if visit:
            visit.visit_count += 1
            visit.last_visit = datetime.utcnow()
        else:
            geo_data = get_geolocation(client_ip)
            visit = Visit(ip_address=client_ip,
                          country=geo_data.get('country'),
                          city=geo_data.get('city'),
                          region=geo_data.get('region'),
                          latitude=geo_data.get('latitude'),
                          longitude=geo_data.get('longitude'))
        db.session.add(visit)
        db.session.commit()
        return True
    except Exception as e:
        app.logger.error(f"Error recording visit: {str(e)}")
        return False

@app.route('/')
def index():
    try:
        client_ip = get_client_ip()
        record_visit(client_ip)
        return render_template('index.html', ip_address=client_ip)
    except Exception as e:
        app.logger.error(f"Error handling visit: {str(e)}")
        return render_template('index.html', error="Unable to detect IP address")

@app.route('/youtube')
def youtube():
    try:
        record_visit(get_client_ip())
    except Exception as e:
        app.logger.error(f"Error recording IP: {str(e)}")
    return redirect("https://youtube.com")

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    error = None
    admin_password = get_admin_password()
    if request.method == 'POST':
        if request.form['password'] == admin_password:
            session['admin_logged_in'] = True
            return redirect(url_for('admin_visits'))
        else:
            error = 'Incorrect Password!'
    return render_template('admin/login.html', error=error)

@app.route('/admin/logout')
def admin_logout():
    session.pop('admin_logged_in', None)
    return redirect(url_for('admin_login'))

@app.route('/admin/visits')
def admin_visits():
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))
    visits = Visit.query.order_by(Visit.last_visit.desc()).all()
    return render_template('admin/visits.html', visits=visits)

@app.route('/admin/delete-visits', methods=['POST'])
def admin_delete_visits():
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))
    selected_visits = request.form.getlist('selected_visits')
    if not selected_visits:
        return redirect(url_for('admin_visits'))
    try:
        deleted_count = 0
        for visit_id in selected_visits:
            visit = Visit.query.get(visit_id)
            if visit:
                db.session.delete(visit)
                deleted_count += 1
        db.session.commit()
        flash(f'Usunięto {deleted_count} wybranych wpisów.', 'success')
    except Exception as e:
        db.session.rollback()
        app.logger.error(f"Error deleting visits: {str(e)}")
        flash('Wystąpił błąd podczas usuwania wpisów.', 'danger')
    return redirect(url_for('admin_visits'))

@app.route('/keep-alive', methods=['POST'])
def keep_alive():
    return jsonify({"status": "ok"})