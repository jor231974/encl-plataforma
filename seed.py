from app import app, db
from models import *
from werkzeug.security import generate_password_hash
from datetime import datetime, timedelta
import random

def seed_database():
    with app.app_context():
        db.create_all()

        if User.query.first():
            print("Database already seeded")
            return

        admin = User(
            username='admin',
            email='admin@encl.edu.mx',
            password_hash=generate_password_hash('admin123'),
            role='admin',
            nombre='Administrador',
            apellidos='Sistema ENCL',
            activo=True
        )
        db.session.add(admin)

        superadmin = User(
            username='superadmin',
            email='superadmin@encl.edu.mx',
            password_hash=generate_password_hash('superadmin123'),
            role='superadmin',
            nombre='Super',
            apellidos='Administrador',
            activo=True
        )
        db.session.add(superadmin)

        estados_data = [
            'Aguascalientes', 'Baja California', 'Baja California Sur', 'Campeche',
            'Chiapas', 'Chihuahua', 'Ciudad de México', 'Coahuila', 'Colima',
            'Durango', 'Estado de México', 'Guanajuato', 'Guerrero', 'Hidalgo',
            'Jalisco', 'Michoacán', 'Morelos', 'Nayarit', 'Nuevo León', 'Oaxaca',
            'Puebla', 'Querétaro', 'Quintana Roo', 'San Luis Potosí', 'Sinaloa',
            'Sonora', 'Tabasco', 'Tamaulipas', 'Tlaxcala', 'Veracruz', 'Yucatán', 'Zacatecas'
        ]

        for e in estados_data:
            estado = Estado(nombre=e)
            db.session.add(estado)
        db.session.flush()

        for estado in Estado.query.all():
            for i in range(1, 4):
                muni = Municipio(nombre=f'{estado.nombre} - Municipio {i}', estado_id=estado.id)
                db.session.add(muni)
        db.session.flush()

        for muni in Municipio.query.all():
            for i in range(1, 3):
                dist = Distrito(nombre=f'Distrito {i:02d}', codigo=f'D-{muni.id:02d}-{i:02d}', municipio_id=muni.id)
                db.session.add(dist)
        db.session.flush()

        for dist in Distrito.query.all():
            for i in range(1, 3):
                grupo = Grupo(nombre=f'Grupo {i}', codigo=f'G-{dist.id:02d}-{i:02d}', distrito_id=dist.id)
                db.session.add(grupo)

        categorias_data = [
            ('Idiomas', 'fa-language'),
            ('Tecnología', 'fa-laptop-code'),
            ('Administración', 'fa-building'),
            ('Desarrollo Profesional', 'fa-user-tie'),
            ('Capacitación Social', 'fa-hand-holding-heart'),
            ('Capacitación Técnica', 'fa-tools'),
            ('Emprendimiento', 'fa-rocket')
        ]

        for nom, icon in categorias_data:
            cat = Categoria(nombre=nom, icono=icon)
            db.session.add(cat)
        db.session.flush()

        instructores = []
        instr_names = ['Jacky', 'María', 'José', 'Ana', 'Miguel', 'Sofía', 'Roberto', 'Laura', 'Fernando', 'Diana']
        instr_last = ['Jordain', 'García', 'Martínez', 'López', 'Hernández', 'González', 'Pérez', 'Rodríguez', 'Flores', 'Morales']

        i = 0
        for name, last in zip(instr_names, instr_last):
            instr = User(
                username=f'instructor{i+1}',
                email=f'instructor{i+1}@encl.edu.mx',
                password_hash=generate_password_hash('instructor123'),
                role='instructor',
                nombre=name,
                apellidos=last,
                foto=f'instructor-{i+1}.jpg',
                telefono=f'555{i+1:04d}',
                activo=True
            )
            db.session.add(instr)
            instructores.append(instr)
            i += 1

        cursos_data = {
            1: [
                ('Inglés Básico', 'Aprende los fundamentos del inglés para comunicación diaria.', 'Iniciación'),
                ('Inglés Intermedio', 'Mejora tu nivel de inglés con gramática y conversación.', 'Intermedio'),
                ('Inglés Avanzado', 'Domina el inglés con expresiones complejas y fluidez.', 'Avanzado'),
                ('Inglés Conversacional', 'Practica conversaciones en inglés para situaciones reales.', 'Intermedio'),
                ('Inglés Empresarial', 'Inglés para negocios y entorno corporativo.', 'Avanzado'),
            ],
            2: [
                ('Computación Básica', 'Introducción a la computación y manejo de PC.', 'Principiante'),
                ('Office Profesional', 'Domina Word, Excel, PowerPoint y Outlook.', 'Intermedio'),
                ('Excel Avanzado', 'Fórmulas, tablas dinámicas, macros y análisis de datos.', 'Avanzado'),
                ('Inteligencia Artificial', 'Fundamentos de IA, machine learning y aplicaciones.', 'Intermedio'),
                ('Marketing Digital', 'Estrategias digitales, SEO, SEM y redes sociales.', 'Intermedio'),
                ('Diseño Gráfico', 'Principios de diseño, Photoshop, Illustrator y Canva.', 'Principiante'),
                ('Redes y Telecomunicaciones', 'Fundamentos de redes, TCP/IP y telecomunicaciones.', 'Intermedio'),
                ('Ciberseguridad', 'Protección de datos, ethical hacking y seguridad informática.', 'Avanzado'),
            ],
            3: [
                ('Administración Pública', 'Gestión y administración de entidades gubernamentales.', 'Intermedio'),
                ('Administración Empresarial', 'Principios de administración de empresas modernas.', 'Intermedio'),
                ('Recursos Humanos', 'Gestión del talento humano y desarrollo organizacional.', 'Intermedio'),
                ('Planeación Estratégica', 'Desarrollo de planes estratégicos empresariales.', 'Avanzado'),
                ('Gestión de Proyectos', 'Metodologías ágiles, PMP y gestión de proyectos.', 'Avanzado'),
            ],
            4: [
                ('Liderazgo', 'Desarrollo de habilidades de liderazgo efectivo.', 'Intermedio'),
                ('Comunicación Efectiva', 'Técnicas de comunicación oral y escrita profesional.', 'Principiante'),
                ('Atención Ciudadana', 'Servicio de calidad y atención al ciudadano.', 'Principiante'),
                ('Ventas', 'Técnicas de ventas y negociación comercial.', 'Intermedio'),
                ('Negociación', 'Estrategias de negociación efectiva.', 'Avanzado'),
                ('Oratoria', 'Hablar en público con confianza y persuasión.', 'Intermedio'),
                ('Desarrollo Personal', 'Crecimiento personal y productividad.', 'Principiante'),
            ],
            5: [
                ('Liderazgo Comunitario', 'Desarrollo de líderes comunitarios.', 'Intermedio'),
                ('Gestión Social', 'Gestión de proyectos de impacto social.', 'Intermedio'),
                ('Participación Ciudadana', 'Mecanismos de participación democrática.', 'Principiante'),
                ('Desarrollo Comunitario', 'Desarrollo y fortalecimiento comunitario.', 'Intermedio'),
                ('Elaboración de Proyectos Sociales', 'Diseño de proyectos con impacto social.', 'Avanzado'),
            ],
            6: [
                ('Instalación CCTV', 'Instalación y configuración de sistemas CCTV.', 'Intermedio'),
                ('Alarmas', 'Instalación de sistemas de alarma residencial y comercial.', 'Intermedio'),
                ('Control de Acceso', 'Sistemas de control de acceso electrónico.', 'Intermedio'),
                ('Redes', 'Configuración y administración de redes.', 'Intermedio'),
                ('Fibra Óptica', 'Instalación y mantenimiento de fibra óptica.', 'Avanzado'),
                ('Electricidad Básica', 'Fundamentos de electricidad residencial.', 'Principiante'),
                ('Domótica', 'Automatización y hogar inteligente.', 'Avanzado'),
            ],
            7: [
                ('Creación de Empresas', 'Pasos para crear tu propia empresa.', 'Principiante'),
                ('Finanzas Personales', 'Educación financiera y administración del dinero.', 'Principiante'),
                ('Comercio Electrónico', 'Vender productos y servicios en línea.', 'Intermedio'),
                ('Administración de Negocios', 'Gestión eficiente de negocios PyME.', 'Intermedio'),
                ('Ventas Digitales', 'Estrategias de ventas en canales digitales.', 'Intermedio'),
            ]
        }

        levels = ['Principiante', 'Intermedio', 'Avanzado']
        for cat_id, cursos_list in cursos_data.items():
            for titulo, desc, nivel in cursos_list:
                instr = random.choice(instructores)
                curso = Curso(
                    titulo=titulo,
                    slug=titulo.lower().replace(' ', '-').replace('á','a').replace('é','e').replace('í','i').replace('ó','o').replace('ú','u').replace('ñ','n'),
                    descripcion_corta=desc,
                    descripcion_larga=f'{desc} Curso completo con materiales, ejercicios y certificación avalada por la ENCL.',
                    categoria_id=cat_id,
                    instructor_id=instr.id,
                    nivel=nivel,
                    duracion_horas=random.randint(10, 60),
                    precio=random.choice([0, 0, 0, 499, 799, 999, 1499]),
                    activo=True,
                    tiene_certificado=True,
                    temario={'modulos': [f'Módulo {i}: {titulo}' for i in range(1, 6)]}
                )
                db.session.add(curso)
        db.session.flush()

        cursos = Curso.query.all()
        for curso in cursos:
            for i in range(1, 9):
                clase = Clase(
                    curso_id=curso.id,
                    titulo=f'{curso.titulo} - Clase {i}',
                    descripcion=f'Clase {i} del curso {curso.titulo}',
                    tipo=random.choice(['grabada', 'grabada', 'grabada', 'vivo']),
                    duracion_minutos=random.randint(15, 60),
                    activo=True
                )
                db.session.add(clase)

            examen = Examen(
                curso_id=curso.id,
                titulo=f'Evaluación - {curso.titulo}',
                descripcion=f'Examen final del curso {curso.titulo}',
                tiempo_limite_minutos=30,
                calificacion_minima=6.0
            )
            db.session.add(examen)
            db.session.flush()

            preguntas_data = [
                ("¿Cuál es el objetivo principal de este curso?", ["Aprender teoría", "Desarrollar habilidades prácticas", "Memorizar conceptos", "Solo lectura"], 1),
                ("¿Qué nivel se requiere para tomar este curso?", ["Ninguno", "Básico", "Intermedio", "Avanzado"], 0),
                ("¿Cuánto dura el curso aproximadamente?", ["1 semana", "1 mes", "3 meses", "Variable"], 3),
                ("¿El curso incluye certificación?", ["Sí", "No", "Solo si se aprueba", "Bajo costo adicional"], 2),
                ("¿Qué materiales se proporcionan?", ["Solo videos", "Videos y PDF", "Videos, PDF y ejercicios", "Todo incluido"], 3)
            ]
            for texto, opciones, correcta in preguntas_data:
                pregunta = Pregunta(
                    examen_id=examen.id,
                    texto=texto,
                    opciones=opciones,
                    respuesta_correcta=correcta
                )
                db.session.add(pregunta)

        db.session.flush()

        alumnos_data = [
            ('alumno1', 'alumno1@encl.edu.mx', 'Juan', 'Pérez García', '55510001'),
            ('alumno2', 'alumno2@encl.edu.mx', 'María', 'López Hernández', '55510002'),
            ('alumno3', 'alumno3@encl.edu.mx', 'Pedro', 'González Ruiz', '55510003'),
        ]
        estados_ids = [e.id for e in Estado.query.all()]
        grupos_ids = [g.id for g in Grupo.query.all()]

        for username, email, nombre, apellidos, telefono in alumnos_data:
            estado_id = random.choice(estados_ids)
            munis = Municipio.query.filter_by(estado_id=estado_id).all()
            muni_id = random.choice(munis).id if munis else None
            dists = Distrito.query.filter_by(municipio_id=muni_id).all()
            dist_id = random.choice(dists).id if dists else None
            grps = Grupo.query.filter_by(distrito_id=dist_id).all()
            grupo_id = random.choice(grps).id if grps else None

            alumno = User(
                username=username,
                email=email,
                password_hash=generate_password_hash('alumno123'),
                role='alumno',
                nombre=nombre,
                apellidos=apellidos,
                telefono=telefono,
                estado_id=estado_id,
                municipio_id=muni_id,
                distrito_id=dist_id,
                grupo_id=grupo_id,
                nivel=random.choice(levels),
                progreso_general=random.uniform(10, 90),
                activo=True
            )
            db.session.add(alumno)
        db.session.flush()

        alumnos = User.query.filter_by(role='alumno').all()
        for alumno in alumnos:
            cursos_inscritos = random.sample(cursos, min(3, len(cursos)))
            for curso in cursos_inscritos:
                insc = Inscripcion(
                    alumno_id=alumno.id,
                    curso_id=curso.id,
                    progreso=random.uniform(0, 100),
                    completado=random.choice([True, False, False])
                )
                db.session.add(insc)

                certificados = Certificado(
                    folio=f'ENCL-{alumno.id:04d}-{curso.id:04d}',
                    alumno_id=alumno.id,
                    curso_id=curso.id,
                    instructor_id=curso.instructor_id,
                    codigo_qr=f'https://encl.edu.mx/validar/ENCL-{alumno.id:04d}-{curso.id:04d}',
                    valido=True
                )
                db.session.add(certificados)

        patrocinadores_data = [
            ('Gobierno de México', 'Comprometidos con la educación y el desarrollo de México.', 'Secretaría de Educación', 'La educación es el arma más poderosa para cambiar el mundo.'),
            ('Fundación Telmex', 'Impulsando la educación digital en México.', 'Director General', 'La tecnología al servicio de la educación.'),
            ('Microsoft México', 'Transformando la educación con tecnología innovadora.', 'Director de Educación', 'Empoderando a cada persona y organización en el planeta.'),
            ('Grupo Bimbo', 'Alimentando un mundo mejor a través de la educación.', 'Director de RSE', 'Educación y nutrición para el desarrollo.'),
            ('Santander Universidades', 'Apoyando la educación superior y la capacitación profesional.', 'Director Ejecutivo', 'Invertir en educación es invertir en el futuro.'),
        ]

        for nombre, lema, cargo, descripcion in patrocinadores_data:
            pat = Patrocinador(
                nombre=nombre,
                cargo=cargo,
                lema=lema,
                activo=True
            )
            db.session.add(pat)

        from datetime import date
        becas_data = [
            {'nombre': 'Beca Excelencia Académica', 'descripcion': 'Apoyo para alumnos con alto rendimiento en cursos de tecnología y desarrollo profesional.', 'tipo': 'porcentaje', 'valor': 50, 'requisitos': 'Estar inscrito en al menos un curso. No tener adeudos. Promedio mínimo de 8.', 'cupo_maximo': 20},
            {'nombre': 'Beca Impulso Social', 'descripcion': 'Apoyo económico para estudiantes de comunidades vulnerables.', 'tipo': 'monto_fijo', 'valor': 500, 'requisitos': 'Comprobante de residencia en zona prioritaria. Carta de exposición de motivos.', 'cupo_maximo': 50},
            {'nombre': 'Beca Mujeres en Tecnología', 'descripcion': 'Fomenta la participación femenina en cursos de tecnología e innovación.', 'tipo': 'porcentaje', 'valor': 75, 'requisitos': 'Ser mujer mexicana mayor de 18 años. Inscribirse a un curso de tecnología.', 'cupo_maximo': 30},
            {'nombre': 'Beca Jóvenes Emprendedores', 'descripcion': 'Apoyo integral para jóvenes que deseen desarrollar su propio negocio.', 'tipo': 'porcentaje', 'valor': 40, 'requisitos': 'Tener entre 18 y 29 años. Presentar un plan de negocio básico.', 'cupo_maximo': 25},
            {'nombre': 'Beca Capacitación Continua', 'descripcion': 'Descuento para profesionales que deseen actualizar sus habilidades.', 'tipo': 'porcentaje', 'valor': 30, 'requisitos': 'Comprobante de empleo activo. Carta de recomendación laboral.', 'cupo_maximo': 0},
        ]
        for bd in becas_data:
            if not Beca.query.filter_by(nombre=bd['nombre']).first():
                beca = Beca(nombre=bd['nombre'], descripcion=bd['descripcion'], tipo=bd['tipo'], valor=bd['valor'], requisitos=bd['requisitos'], cupo_maximo=bd['cupo_maximo'], activo=True, fecha_inicio=date.today())
                db.session.add(beca)

        config_defaults = {
            'site_name': 'ESCUELA NACIONAL DE CAPACITACIÓN Y CURSOS EN LÍNEA',
            'site_subtitle': 'Transformando personas, fortaleciendo comunidades y desarrollando talento para el futuro.',
            'hero_title': 'ESCUELA NACIONAL DE CAPACITACIÓN Y CURSOS EN LÍNEA',
            'hero_subtitle': 'Transformando personas, fortaleciendo comunidades y desarrollando talento para el futuro.',
            'about_text': 'Somos una institución nacional dedicada a la capacitación profesional, desarrollo social y formación continua. Nuestra misión es transformar personas, fortalecer comunidades y desarrollar talento para el futuro de México.',
            'mision_text': 'Proporcionar capacitación profesional de excelencia, accesible y certificada que impulse el desarrollo personal y profesional de los mexicanos.',
            'vision_text': 'Ser la plataforma de capacitación líder en México, reconocida por su calidad educativa, innovación tecnológica y contribución al desarrollo nacional.',
            'contact_email': 'contacto@encl.edu.mx',
            'contact_phone': '55 5555 5555',
            'contact_address': 'Av. Educación Nacional 1000, Ciudad de México',
            'primary_color': '#0d6efd',
            'secondary_color': '#6c757d',
        }

        for clave, valor in config_defaults.items():
            conf = Configuracion(clave=clave, valor=valor)
            db.session.add(conf)

        db.session.commit()
        print("Database seeded successfully!")

if __name__ == '__main__':
    seed_database()
