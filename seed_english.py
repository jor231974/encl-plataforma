# -*- coding: utf-8 -*-
"""
Seed: English for Opportunity - Nivel A1 (12 semanas, 36 sesiones)
Ejecutar: python3 seed_english.py
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__) or '.')
from app import app, db
from models import *

WEEKS = [
    (1, 'Presentaciones', 'Presentarse, saludar e intercambiar información personal'),
    (2, 'Uno mismo y otros', 'Hablar sobre uno mismo y otras personas'),
    (3, 'La familia', 'Hablar sobre la familia'),
    (4, 'Rutinas', 'Describir rutinas diarias'),
    (5, 'Gustos', 'Expresar gustos y preferencias'),
    (6, 'Lugares', 'Describir lugares y dar direcciones'),
    (7, 'Compras y alimentos', 'Desenvolverse en situaciones de compra y alimentación'),
    (8, 'Acciones en progreso', 'Describir acciones en curso'),
    (9, 'Pasado', 'Hablar de eventos pasados'),
    (10, 'Futuro', 'Expresar planes e intenciones futuras'),
    (11, 'Inglés laboral', 'Comunicarse en entornos profesionales'),
    (12, 'Integración', 'Integrar y aplicar todos los conocimientos'),
]

SESSIONS = {
    1: [
        (1, 'Bienvenida e introducción', '• Presentación del curso\n• Cómo aprender inglés\n• Pronunciación básica\n• Alfabeto\n• Saludos'),
        (2, 'Información personal', '• Presentaciones\n• Nombre\n• Países y nacionalidades\n• Edad\n• Profesiones'),
        (3, 'Consolidación', '• Presentación completa\n• Deletrear\n• Conversaciones básicas'),
    ],
    2: [
        (4, 'Verbo To Be', '• Afirmativo\n• Negativo\n• Preguntas\n• Pronombres'),
        (5, 'Descripciones', '• Apariencia\n• Personalidad\n• Colores\n• Adjetivos'),
        (6, 'Integración', '• Describirse\n• Describir personas\n• Entrevistas'),
    ],
    3: [
        (7, 'Familia', '• Miembros\n• This is\n• These are'),
        (8, 'Posesivos', '• My, your, his, her, our, their\n• Possessive\'s'),
        (9, 'Conversación', '• Árbol genealógico\n• Describir familiares'),
    ],
    4: [
        (10, 'Simple Present', '• Rutinas\n• Verbos frecuentes\n• Horarios'),
        (11, 'Tiempo', '• Hora\n• Días\n• Meses\n• Fechas'),
        (12, 'Conversación', '• Rutina diaria\n• Role play'),
    ],
    5: [
        (13, 'Likes', '• Like\n• Love\n• Hate\n• Enjoy'),
        (14, 'Hobbies', '• Deportes\n• Música\n• Viajes\n• Películas'),
        (15, 'Integración', '• Encuestas\n• Conversaciones'),
    ],
    6: [
        (16, 'Places', '• Lugares de la ciudad'),
        (17, 'There is/are', '• Singular\n• Plural\n• Some\n• Any'),
        (18, 'Directions', '• Left\n• Right\n• Next to\n• Between'),
    ],
    7: [
        (19, 'Food', '• Comidas\n• Bebidas\n• Frutas\n• Verduras'),
        (20, 'Restaurant', '• Ordenar\n• Menú\n• Cuenta'),
        (21, 'Role play', '• Restaurante\n• Cafetería\n• Supermercado'),
    ],
    8: [
        (22, 'Present Continuous', '• Verbo+ing\n• Preguntas\n• Negaciones'),
        (23, 'Actividades', '• Trabajar\n• Leer\n• Conducir\n• Estudiar'),
        (24, 'Conversación', '• ¿Qué estás haciendo?\n• Descripción de imágenes'),
    ],
    9: [
        (25, 'Simple Past', '• Was/Were\n• Verbos regulares'),
        (26, 'Expresiones de tiempo', '• Yesterday\n• Last week\n• Ago'),
        (27, 'Conversación', '• Fin de semana\n• Vacaciones'),
    ],
    10: [
        (28, 'Going to', '• Planes\n• Intenciones'),
        (29, 'Vocabulario', '• Tomorrow\n• Next week\n• Next year'),
        (30, 'Conversación', '• Metas\n• Vacaciones'),
    ],
    11: [
        (31, 'Oficina', '• Vocabulario\n• Reuniones\n• Teléfono'),
        (32, 'Conversaciones profesionales', '• Presentaciones\n• Small talk'),
        (33, 'Role plays', '• Atención al cliente\n• Reuniones'),
    ],
    12: [
        (34, 'Repaso', '• Gramática\n• Vocabulario\n• Pronunciación'),
        (35, 'Proyecto final', '• Presentación integral'),
        (36, 'Evaluación', '• Speaking\n• Listening\n• Retroalimentación'),
    ],
}

def seed():
    with app.app_context():
        cat = Categoria.query.filter_by(nombre='Idiomas').first()
        if not cat:
            cat = Categoria(nombre='Idiomas', icono='fa-language')
            db.session.add(cat)
            db.session.flush()

        instructor = User.query.filter_by(username='marifer').first()
        if not instructor:
            from werkzeug.security import generate_password_hash
            instructor = User(
                username='marifer', email='marifer@encl.edu.mx',
                password_hash=generate_password_hash('instructor123'),
                role='instructor', nombre='María Fernanda', apellidos='Instructor',
                activo=True
            )
            db.session.add(instructor)
            db.session.flush()
            print('Instructor marifer creado')

        curso = Curso.query.filter_by(slug='english-for-opportunity-a1').first()
        if not curso:
            curso = Curso(
                titulo='English for Opportunity – Nivel A1',
                slug='english-for-opportunity-a1',
                descripcion_corta='Curso de inglés básico (A1) de 12 semanas. Desarrolla habilidades de comunicación oral y escrita para situaciones cotidianas y laborales.',
                descripcion_larga='Programa diseñado para desarrollar la capacidad de comunicarse en inglés en situaciones cotidianas y laborales, alcanzando un nivel A1 con transición a A2 inicial, priorizando la comunicación oral. Incluye 36 sesiones de 60 minutos con actividades interactivas, ejercicios prácticos y evaluación continua.',
                categoria_id=cat.id, instructor_id=instructor.id,
                nivel='Principiante', duracion_horas=36, precio=0,
                modalidad='En línea', activo=True, tiene_certificado=True,
                temario={'semanas': 12, 'sesiones': 36, 'duracion_sesion': 60}
            )
            db.session.add(curso)
            db.session.flush()
            print(f'Curso creado: {curso.titulo}')

            for num, titulo, objetivo in WEEKS:
                sem = CursoSemana(curso_id=curso.id, numero=num, titulo=titulo, objetivo=objetivo, orden=num)
                db.session.add(sem)
                db.session.flush()

                for s_num, s_titulo, s_contenidos in SESSIONS.get(num, []):
                    ses = SemanaSesion(semana_id=sem.id, numero=s_num, titulo=s_titulo, contenidos=s_contenidos, orden=s_num)
                    db.session.add(ses)

            print('12 semanas y 36 sesiones creadas')
        else:
            print(f'Curso ya existe (ID {curso.id})')

        db.session.commit()
        print()
        print('=== ENGLISH FOR OPPORTUNITY - NIVEL A1 ===')
        print(f'Instructor: marifer / instructor123')
        print(f'Semanas: {CursoSemana.query.filter_by(curso_id=curso.id).count()}')
        print(f'Sesiones: {SemanaSesion.query.join(CursoSemana).filter(CursoSemana.curso_id == curso.id).count()}')
        print('DONE.')

if __name__ == '__main__':
    seed()
