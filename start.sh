#!/bin/bash
# Initialize database and seed data
python -c "
from app import app, db
with app.app_context():
    db.create_all()
"
python seed.py
# Start gunicorn
exec gunicorn app:app --bind 0.0.0.0:${PORT:-10000} --workers 2
