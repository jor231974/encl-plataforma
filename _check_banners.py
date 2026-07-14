# -*- coding: utf-8 -*-
import sys, os
sys.path.insert(0, os.path.dirname(__file__) or '.')
from app import app, db
from models import Banner

with app.app_context():
    banners = Banner.query.order_by(Banner.orden).all()
    print(f'Total banners: {len(banners)}')
    for b in banners:
        file_path = os.path.join(os.path.dirname(__file__) or '.', 'static', 'uploads')
        fname = b.imagen.replace('/uploads/', '') if b.imagen else ''
        full = os.path.join(file_path, fname)
        exists = os.path.exists(full) if fname else False
        size = os.path.getsize(full) if exists else 0
        print(f'  ID {b.id}: "{b.titulo or "sin titulo"}"')
        print(f'    imagen: {b.imagen}')
        print(f'    archivo: {full}')
        print(f'    existe: {exists}, tamano: {size}')
        print(f'    activo: {b.activo}, orden: {b.orden}')
        print()
