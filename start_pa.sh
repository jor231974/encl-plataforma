#!/bin/bash
cd ~/encl-plataforma
python seed.py
exec gunicorn app:app
