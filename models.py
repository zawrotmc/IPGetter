from datetime import datetime
from app import db

class Visit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ip_address = db.Column(db.String(45), unique=True, nullable=False)  # IPv6 can be up to 45 chars
    visit_count = db.Column(db.Integer, default=1, nullable=False)
    first_visit = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    last_visit = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    # Geolocation data
    country = db.Column(db.String(100))
    city = db.Column(db.String(100))
    region = db.Column(db.String(100))
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)

    def __repr__(self):
        return f'<Visit {self.ip_address} ({self.visit_count} visits)>'