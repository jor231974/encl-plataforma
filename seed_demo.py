"""
Contenido de demostración para presentación del proyecto.
Identificado con tag [DEMO] para fácil reemplazo posterior.
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

        # === CATEGORÍA ===
        cat = Categoria.query.filter_by(nombre='Tecnología').first()
        if not cat:
            cat = Categoria(nombre='Tecnología', icono='fa-laptop-code')
            db.session.add(cat)
            db.session.flush()

        # === INSTRUCTOR JORGE FLORES ===
        instructor = User.query.filter_by(username='jorge.flores').first()
        if not instructor:
            instructor = User(
                username='jorge.flores',
                email='jorge.flores@encl.edu.mx',
                password_hash=generate_password_hash('instructor123'),
                role='instructor',
                nombre='Jorge',
                apellidos='Flores',
                cargo='Instructor de Herramientas Digitales e Informática',
                foto='instructor-jorge.jpg',
                telefono='55559999',
                activo=True
            )
            db.session.add(instructor)
            db.session.flush()
            print(f'[DEMO] Instructor creado: {instructor.nombre} {instructor.apellidos}')

        # === CURSO DEMO ===
        curso = Curso.query.filter_by(slug='herramientas-digitales-e-informatica').first()
        if not curso:
            curso = Curso(
                titulo='Herramientas Digitales e Informática [DEMO]',
                slug='herramientas-digitales-e-informatica',
                descripcion_corta='Curso de demostración sobre herramientas digitales, informática básica y transformación tecnológica.',
                descripcion_larga='Este curso de demostración cubre los fundamentos de herramientas digitales, informática y transformación tecnológica. Está diseñado para la presentación del proyecto ante directivos. Contiene materiales, ejercicios, examen y certificación demo.',
                categoria_id=cat.id,
                instructor_id=instructor.id,
                nivel='Principiante',
                duracion_horas=40,
                precio=0,
                modalidad='En línea',
                activo=True,
                tiene_certificado=True,
                temario={'modulos': [
                    'Módulo 1: Introducción a la Informática',
                    'Módulo 2: Herramientas Digitales Básicas',
                    'Módulo 3: Internet y Comunicación Digital',
                    'Módulo 4: Seguridad Digital',
                    'Módulo 5: Transformación Tecnológica'
                ]}
            )
            db.session.add(curso)
            db.session.flush()
            print(f'[DEMO] Curso creado: {curso.titulo}')

            # === CLASES ===
            clases_data = [
                ('Introducción a la Informática [DEMO]', 'Conceptos básicos de informática, hardware y software.', 'grabada', 25),
                ('Sistemas Operativos [DEMO]', 'Conoce los principales sistemas operativos y su funcionamiento.', 'grabada', 30),
                ('Suite de Oficina [DEMO]', 'Uso de procesador de texto, hoja de cálculo y presentaciones.', 'grabada', 35),
                ('Navegación en Internet [DEMO]', 'Uso seguro y eficiente de navegadores web.', 'grabada', 20),
                ('Correo Electrónico [DEMO]', 'Gestión profesional del correo electrónico.', 'grabada', 25),
                ('Herramientas de Colaboración [DEMO]', 'Plataformas de trabajo colaborativo en la nube.', 'vivo', 40),
                ('Seguridad Digital [DEMO]', 'Buenas prácticas de seguridad informática.', 'grabada', 30),
                ('Transformación Digital [DEMO]', 'El impacto de la tecnología en la sociedad y el trabajo.', 'vivo', 35),
            ]
            for titulo, desc, tipo, duracion in clases_data:
                c = Clase(
                    curso_id=curso.id,
                    titulo=titulo,
                    descripcion=desc,
                    tipo=tipo,
                    url_video='https://www.youtube.com/embed/dQw4w9WgXcQ' if tipo == 'grabada' else '',
                    url_reunion='' if tipo == 'vivo' else '',
                    duracion_minutos=duracion,
                    activo=True
                )
                db.session.add(c)
            print(f'[DEMO] 8 clases creadas')

            # === MATERIAL DESCARGABLE ===
            material = MaterialClase(
                curso_id=curso.id,
                titulo='Guía de Herramientas Digitales [DEMO]',
                tipo='PDF',
                archivo_url='/uploads/demo_guia_herramientas_digitales.pdf'
            )
            db.session.add(material)
            print(f'[DEMO] Material PDF agregado')

            # === EJERCICIO ===
            ejercicio = Tarea(
                curso_id=curso.id,
                titulo='Ejercicio práctico: Diagnóstico digital [DEMO]',
                descripcion='Realiza un diagnóstico de tus habilidades digitales actuales y elabora un plan de mejora. Descarga la plantilla incluida en los materiales.',
                fecha_entrega=datetime.utcnow() + timedelta(days=30),
                activo=True
            )
            db.session.add(ejercicio)
            print(f'[DEMO] Ejercicio descargable creado')

            # === EXAMEN CON 10 PREGUNTAS ===
            examen = Examen(
                curso_id=curso.id,
                titulo='Evaluación - Herramientas Digitales [DEMO]',
                descripcion='Examen de demostración que combina opción múltiple y verdadero/falso.',
                tiempo_limite_minutos=30,
                calificacion_minima=6.0,
                activo=True
            )
            db.session.add(examen)
            db.session.flush()

            preguntas = [
                # Opción múltiple
                ('¿Qué es un sistema operativo?',
                 ['Un programa de correo', 'Software que gestiona el hardware y software', 'Un navegador web', 'Una hoja de cálculo'], 1),
                ('¿Cuál de los siguientes es un navegador web?',
                 ['Microsoft Word', 'Google Chrome', 'Adobe Photoshop', 'Windows 10'], 1),
                ('¿Qué significa URL?',
                 ['Universal Resource Link', 'Uniform Resource Locator', 'Unified Remote Language', 'Universal Reference List'], 1),
                ('¿Qué herramienta de Office se usa para crear presentaciones?',
                 ['Word', 'Excel', 'PowerPoint', 'Outlook'], 2),
                ('¿Qué es la nube (cloud computing)?',
                 ['Un servicio de almacenamiento local', 'Servicios de computación a través de internet', 'Un tipo de antivirus', 'Un sistema operativo'], 1),
                # Verdadero/Falso
                ('El correo electrónico es una herramienta de comunicación asíncrona.', ['Verdadero', 'Falso'], 0),
                ('La contraseña "123456" es segura.', ['Verdadero', 'Falso'], 1),
                ('Una red LAN conecta dispositivos en un área geográfica extensa.', ['Verdadero', 'Falso'], 1),
                ('El phishing es un tipo de ataque cibernético.', ['Verdadero', 'Falso'], 0),
                ('La transformación digital solo implica comprar tecnología nueva.', ['Verdadero', 'Falso'], 1),
            ]
            for texto, opciones, correcta in preguntas:
                p = Pregunta(
                    examen_id=examen.id,
                    texto=texto,
                    opciones=opciones,
                    respuesta_correcta=correcta
                )
                db.session.add(p)
            print(f'[DEMO] Examen creado con {len(preguntas)} preguntas')

            # === ALUMNOS DEMO ===
            demo_alumnos = [
                ('demo.alumno1', 'demo1@encl.edu.mx', 'Carlos', 'Martínez López', '55530001', 45.0),
                ('demo.alumno2', 'demo2@encl.edu.mx', 'Ana', 'García Hernández', '55530002', 78.5),
                ('demo.alumno3', 'demo3@encl.edu.mx', 'Luis', 'Rodríguez Pérez', '55530003', 92.0),
                ('demo.alumno4', 'demo4@encl.edu.mx', 'Sofía', 'Ramírez Cruz', '55530004', 30.0),
                ('demo.alumno5', 'demo5@encl.edu.mx', 'Miguel', 'Torres Díaz', '55530005', 100.0),
            ]
            for username, email, nombre, apellidos, telefono, progreso in demo_alumnos:
                alumno = User(
                    username=username,
                    email=email,
                    password_hash=generate_password_hash('demo123'),
                    role='alumno',
                    nombre=nombre,
                    apellidos=apellidos,
                    telefono=telefono,
                    nivel='Principiante',
                    progreso_general=progreso,
                    activo=True
                )
                db.session.add(alumno)
                db.session.flush()

                # Inscripción
                insc = Inscripcion(
                    alumno_id=alumno.id,
                    curso_id=curso.id,
                    progreso=progreso,
                    completado=progreso >= 100
                )
                db.session.add(insc)

                # Asistencias (simular 3 clases con asistencia)
                clases_curso = Clase.query.filter_by(curso_id=curso.id).all()
                for cl in clases_curso[:3]:
                    asis = Asistencia(
                        clase_id=cl.id,
                        alumno_id=alumno.id,
                        presente=random.choice([True, True, False]),
                        fecha=datetime.utcnow() - timedelta(days=random.randint(1, 14))
                    )
                    db.session.add(asis)

                # Si completó, generar certificado
                if progreso >= 100:
                    cert = Certificado(
                        folio=f'DEMO-ENCL-{alumno.id:04d}-{curso.id:04d}',
                        alumno_id=alumno.id,
                        curso_id=curso.id,
                        instructor_id=instructor.id,
                        codigo_qr=f'https://encl.edu.mx/validar/DEMO-ENCL-{alumno.id:04d}-{curso.id:04d}',
                        valido=True
                    )
                    db.session.add(cert)

            print(f'[DEMO] 5 alumnos demo creados con inscripciones, asistencias y progreso')

        else:
            print(f'[DEMO] El curso ya existe, saltando creación')

        db.session.commit()
        print("=== CONTENIDO DEMO CARGADO EXITOSAMENTE ===")
        print("=== Para eliminar: ejecuta seed_demo_clean.py ===")

if __name__ == '__main__':
    seed_demo()
