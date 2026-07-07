"""
Contenido de demostración para presentación del proyecto.
Identificado con tag [DEMO] para fácil reemplazo posterior.
Ejecutar: python3 seed_demo.py
"""
from app import app, db
from models import *
from werkzeug.security import generate_password_hash
from datetime import datetime, timedelta, date
import random

def seed_demo():
    with app.app_context():
        db.create_all()
        print("=== INICIANDO CARGA DE CONTENIDO DEMO [DEMO] ===")

        cat = Categoria.query.filter_by(nombre='Tecnología').first()
        if not cat:
            cat = Categoria(nombre='Tecnología', icono='fa-laptop-code')
            db.session.add(cat)
            db.session.flush()

        # === INSTRUCTOR ===
        instructor = User.query.filter_by(username='jorge.flores').first()
        if not instructor:
            instructor = User(
                username='jorge.flores', email='jorge.flores@encl.edu.mx',
                password_hash=generate_password_hash('instructor123'),
                role='instructor', nombre='Jorge', apellidos='Flores',
                foto='instructor-jorge.jpg', telefono='55559999', activo=True
            )
            db.session.add(instructor); db.session.flush()
            print('[DEMO] Instructor creado: Jorge Flores')
        else:
            print('[DEMO] Instructor ya existe')

        # === CREAR/TOMAR CURSO DEMO ===
        create_all = False
        curso = Curso.query.filter_by(slug='herramientas-digitales-e-informatica').first()
        if not curso:
            create_all = True
            curso = Curso(
                titulo='Herramientas Digitales e Informática [DEMO]',
                slug='herramientas-digitales-e-informatica',
                descripcion_corta='Curso de demostración sobre herramientas digitales, informática básica y transformación tecnológica.',
                descripcion_larga='Curso demo de la presentación. Cubre fundamentos de herramientas digitales, informática y transformación tecnológica. Contiene materiales, ejercicios, examen y certificación.',
                categoria_id=cat.id, instructor_id=instructor.id,
                nivel='Principiante', duracion_horas=40, precio=0,
                modalidad='En línea', activo=True, tiene_certificado=True,
                temario={'modulos': ['Módulo 1: Introducción a la Informática', 'Módulo 2: Herramientas Digitales Básicas', 'Módulo 3: Internet y Comunicación Digital', 'Módulo 4: Seguridad Digital', 'Módulo 5: Transformación Tecnológica']}
            )
            db.session.add(curso); db.session.flush()
            print('[DEMO] Curso creado: Herramientas Digitales e Informática [DEMO]')

        # === CLASES (solo si curso nuevo) ===
        if create_all:
            for titulo, desc, tipo, duracion in [
                ('Introducción a la Informática [DEMO]', 'Conceptos básicos de informática, hardware y software.', 'grabada', 25),
                ('Sistemas Operativos [DEMO]', 'Conoce los principales sistemas operativos y su funcionamiento.', 'grabada', 30),
                ('Suite de Oficina [DEMO]', 'Uso de procesador de texto, hoja de cálculo y presentaciones.', 'grabada', 35),
                ('Navegación en Internet [DEMO]', 'Uso seguro y eficiente de navegadores web.', 'grabada', 20),
                ('Correo Electrónico [DEMO]', 'Gestión profesional del correo electrónico.', 'grabada', 25),
                ('Herramientas de Colaboración [DEMO]', 'Plataformas de trabajo colaborativo en la nube.', 'vivo', 40),
                ('Seguridad Digital [DEMO]', 'Buenas prácticas de seguridad informática.', 'grabada', 30),
                ('Transformación Digital [DEMO]', 'El impacto de la tecnología en la sociedad y el trabajo.', 'vivo', 35),
            ]:
                db.session.add(Clase(curso_id=curso.id, titulo=titulo, descripcion=desc, tipo=tipo,
                    url_video='https://www.youtube.com/embed/dQw4w9WgXcQ' if tipo == 'grabada' else '',
                    duracion_minutos=duracion, activo=True))
            db.session.flush()
            print('[DEMO] 8 clases creadas')

        # === MATERIAL (agregar si no existe) ===
        if not MaterialClase.query.filter(MaterialClase.clase_id == Clase.id).join(Clase).filter(Clase.curso_id == curso.id).first():
            primera = Clase.query.filter_by(curso_id=curso.id).first()
            if primera:
                db.session.add(MaterialClase(clase_id=primera.id, titulo='Guía de Herramientas Digitales [DEMO]',
                    tipo='PDF', archivo_url='/uploads/demo_guia_herramientas_digitales.pdf'))
                print('[DEMO] Material PDF agregado')

        # === TAREA (agregar si no existe) ===
        if not Tarea.query.filter_by(curso_id=curso.id).first():
            db.session.add(Tarea(curso_id=curso.id,
                titulo='Ejercicio práctico: Diagnóstico digital [DEMO]',
                descripcion='Realiza un diagnóstico de tus habilidades digitales actuales y elabora un plan de mejora.',
                fecha_entrega=datetime.utcnow() + timedelta(days=30), activo=True))
            print('[DEMO] Tarea creada')

        # === EXAMEN (agregar si no existe) ===
        examen = Examen.query.filter_by(curso_id=curso.id).first()
        if not examen:
            examen = Examen(curso_id=curso.id, titulo='Evaluación - Herramientas Digitales [DEMO]',
                descripcion='Examen de demostración: opción múltiple y verdadero/falso.',
                tiempo_limite_minutos=30, calificacion_minima=6.0, activo=True)
            db.session.add(examen); db.session.flush()

            preguntas = [
                ('¿Qué es un sistema operativo?', ['Un programa de correo', 'Software que gestiona el hardware', 'Un navegador web', 'Una hoja de cálculo'], 1),
                ('¿Cuál de los siguientes es un navegador web?', ['Microsoft Word', 'Google Chrome', 'Adobe Photoshop', 'Windows 10'], 1),
                ('¿Qué significa URL?', ['Universal Resource Link', 'Uniform Resource Locator', 'Unified Remote Language', 'Universal Reference List'], 1),
                ('¿Qué herramienta de Office se usa para presentaciones?', ['Word', 'Excel', 'PowerPoint', 'Outlook'], 2),
                ('¿Qué es la nube?', ['Almacenamiento local', 'Servicios por internet', 'Un antivirus', 'Un sistema operativo'], 1),
                ('El correo electrónico es comunicación asíncrona.', ['Verdadero', 'Falso'], 0),
                ('La contraseña "123456" es segura.', ['Verdadero', 'Falso'], 1),
                ('Una red LAN conecta dispositivos en área extensa.', ['Verdadero', 'Falso'], 1),
                ('El phishing es un ataque cibernético.', ['Verdadero', 'Falso'], 0),
                ('La transformación digital solo es comprar tecnología.', ['Verdadero', 'Falso'], 1),
            ]
            for texto, opciones, correcta in preguntas:
                db.session.add(Pregunta(examen_id=examen.id, texto=texto, opciones=opciones, respuesta_correcta=correcta))
            print(f'[DEMO] Examen creado con {len(preguntas)} preguntas')

        # === ALUMNOS DEMO (agregar si no existen) ===
        existing_demos = User.query.filter(User.username.like('demo.alumno%')).count()
        if existing_demos == 0:
            for username, email, nombre, apellidos, telefono in [
                ('demo.alumno1', 'demo1@encl.edu.mx', 'Carlos', 'Martínez López', '55530001'),
                ('demo.alumno2', 'demo2@encl.edu.mx', 'Ana', 'García Hernández', '55530002'),
                ('demo.alumno3', 'demo3@encl.edu.mx', 'Luis', 'Rodríguez Pérez', '55530003'),
                ('demo.alumno4', 'demo4@encl.edu.mx', 'Sofía', 'Ramírez Cruz', '55530004'),
                ('demo.alumno5', 'demo5@encl.edu.mx', 'Miguel', 'Torres Díaz', '55530005'),
            ]:
                alumno = User(username=username, email=email, password_hash=generate_password_hash('demo123'),
                    role='alumno', nombre=nombre, apellidos=apellidos, telefono=telefono,
                    nivel='Principiante', progreso_general=100.0, activo=True)
                db.session.add(alumno); db.session.flush()

                db.session.add(Inscripcion(alumno_id=alumno.id, curso_id=curso.id, progreso=100.0, completado=True))

                # Asistencia a todas las clases
                for cl in Clase.query.filter_by(curso_id=curso.id).all():
                    db.session.add(Asistencia(clase_id=cl.id, alumno_id=alumno.id,
                        presente=True,
                        fecha=datetime.utcnow() - timedelta(days=random.randint(1, 14))))

                # Entrega de tarea
                tarea = Tarea.query.filter_by(curso_id=curso.id).first()
                if tarea:
                    db.session.add(EntregaTarea(tarea_id=tarea.id, alumno_id=alumno.id,
                        comentario='Tarea entregada y completada.',
                        calificacion=random.randint(8, 10),
                        fecha_entrega=datetime.utcnow() - timedelta(days=1)))

                # Certificado para todos
                db.session.add(Certificado(folio=f'DEMO-ENCL-{alumno.id:04d}-{curso.id:04d}',
                    alumno_id=alumno.id, curso_id=curso.id, instructor_id=instructor.id,
                    codigo_qr=f'https://encl.edu.mx/validar/DEMO-ENCL-{alumno.id:04d}-{curso.id:04d}', valido=True))

            print(f'[DEMO] 5 alumnos demo creados con inscripciones, asistencias y progreso')
        else:
            print(f'[DEMO] Alumnos demo ya existen ({existing_demos})')

        db.session.commit()
        print("=== CONTENIDO DEMO CARGADO EXITOSAMENTE ===")

if __name__ == '__main__':
    seed_demo()
