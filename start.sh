#!/bin/bash
# Initialize database and seed data
python -c "
from app import app, db
with app.app_context():
    db.create_all()
    from models import User
    if not User.query.first():
        exec(open('seed.py').read())
        print('Database seeded successfully')
    else:
        print('Database already has data, skipping seed')
"
# Start gunicorn
exec gunicorn app:app --bind 0.0.0.0:${PORT:-10000} --workers 2
