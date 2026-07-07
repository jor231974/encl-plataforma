"""
Carga contenido inicial de la plataforma: instructor, curso, alumnos y evaluaciones.
Ejecutar: python3 seed_demo.py
"""
from app import app, db
from models import *
from werkzeug.security import generate_password_hash
from datetime import datetime, timedelta, date
import random
import os

try:
    from reportlab.lib.pagesizes import letter
    from reportlab.lib.units import inch
    from reportlab.lib.colors import HexColor
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.enums import TA_CENTER, TA_LEFT
    HAS_REPORTLAB = True
except ImportError:
    HAS_REPORTLAB = False
    print('reportlab no instalado, PDF básico')


def _generar_pdf(pdf_path):
    if not HAS_REPORTLAB:
        with open(pdf_path, 'wb') as f:
            f.write(b'%PDF-1.4\n1 0 obj<</Type/Catalog/Pages 2 0 R>>endobj\n2 0 obj<</Type/Pages/Kids[3 0 R]/Count 1>>endobj\n3 0 obj<</Type/Page/Parent 2 0 R/MediaBox[0 0 612 792]/Contents 4 0 R/Resources<</Font<</F1 5 0 R>>>>>>endobj\n4 0 obj<</Length 44>>stream\nBT /F1 18 Tf 50 700 Td (Guia de Herramientas Digitales) Tj ET\nendstream\nendobj\n5 0 obj<</Type/Font/Subtype/Type1/BaseFont/Helvetica>>endobj\nxref\n0 6\n0000000000 65535 f \n0000000009 00000 n \n0000000058 00000 n \n0000000115 00000 n \n0000000266 00000 n \n0000000362 00000 n \ntrailer<</Size 6/Root 1 0 R>>\nstartxref\n419\n%%EOF')
        return

    doc = SimpleDocTemplate(pdf_path, pagesize=letter,
                            leftMargin=50, rightMargin=50,
                            topMargin=50, bottomMargin=50)
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle('CoverTitle', parent=styles['Title'],
                fontSize=28, leading=34, textColor=HexColor('#1a237e'),
                spaceAfter=12, alignment=TA_CENTER))
    styles.add(ParagraphStyle('CoverSub', parent=styles['Normal'],
                fontSize=14, leading=18, textColor=HexColor('#666666'),
                alignment=TA_CENTER))
    styles.add(ParagraphStyle('ModTitle', parent=styles['Heading2'],
                fontSize=16, textColor=HexColor('#1a237e'),
                spaceBefore=16, spaceAfter=6))
    styles.add(ParagraphStyle('ModBody', parent=styles['Normal'],
                fontSize=10, leading=14, spaceAfter=6))
    styles.add(ParagraphStyle('ExerTitle', parent=styles['Heading2'],
                fontSize=14, textColor=HexColor('#c62828'),
                spaceBefore=12, spaceAfter=8))
    styles.add(ParagraphStyle('ExerQ', parent=styles['Normal'],
                fontSize=10, leading=14, spaceAfter=4))

    story = []

    # Portada
    story.append(Spacer(1, 2.5 * inch))
    story.append(Paragraph('GUÍA DE HERRAMIENTAS DIGITALES', styles['CoverTitle']))
    story.append(Paragraph('Escuela Nacional de Capacitación en Línea', styles['CoverSub']))
    story.append(Spacer(1, 0.3 * inch))
    story.append(Paragraph(
        'Escuela Nacional de Capacitación en Línea<br/>'
        'Material didáctico de apoyo para el curso<br/>'
        '<b>Herramientas Digitales e Informática</b>',
        styles['CoverSub']))
    story.append(Spacer(1, 0.5 * inch))
    story.append(Paragraph(
        'Resumen de los 5 módulos del curso con contenido teórico<br/>'
        'y un ejercicio de Verdadero / Falso para reforzar el aprendizaje.',
        ParagraphStyle('small', parent=styles['Normal'], fontSize=9,
                        textColor=HexColor('#999999'), alignment=TA_CENTER)))
    story.append(PageBreak())

    # Contenido
    modulos = [
        ('Módulo 1: Introducción a la Informática',
         'La informática es la ciencia que estudia el tratamiento automático de la información. '
         'En este módulo se abordan los conceptos fundamentales: hardware (componentes físicos como '
         'CPU, memoria RAM, disco duro, monitor, teclado) y software (programas y sistemas operativos). '
         'Se explica la diferencia entre software de sistema (Windows, Linux, macOS) y software de '
         'aplicación (Office, navegadores, editores). También se introduce el concepto de algoritmo '
         'como secuencia lógica de pasos para resolver un problema.'),
        ('Módulo 2: Herramientas Digitales Básicas',
         'Las herramientas digitales básicas incluyen las suites de ofimática (Microsoft Office, '
         'Google Workspace, LibreOffice). Se estudia el procesador de textos (Word) para crear '
         'documentos profesionales, la hoja de cálculo (Excel) para organizar y analizar datos, '
         'y el software de presentaciones (PowerPoint) para comunicar ideas visualmente. '
         'Se abordan funciones esenciales como formato de texto, tablas, fórmulas básicas, '
         'gráficos y transiciones.'),
        ('Módulo 3: Internet y Comunicación Digital',
         'Internet es una red global de computadoras interconectadas. Este módulo cubre '
         'conceptos como navegadores web, motores de búsqueda, URL, HTTP/HTTPS, y correo '
         'electrónico. Se explica la diferencia entre comunicación síncrona (videollamadas, '
         'chat en vivo) y asíncrona (correo electrónico, foros). También se introducen '
         'herramientas de colaboración en la nube como Google Drive, Dropbox y Microsoft Teams, '
         'que permiten trabajar en equipo desde cualquier lugar.'),
        ('Módulo 4: Seguridad Digital',
         'La seguridad digital protege la integridad y privacidad de la información. '
         'Se cubren temas como contraseñas seguras (combinación de letras, números y símbolos, '
         'mínimo 8 caracteres), autenticación de dos factores, phishing (correos fraudulentos), '
         'malware (virus, troyanos, ransomware), y redes seguras (VPN, HTTPS). Se enfatiza '
         'la importancia de mantener el software actualizado y realizar copias de seguridad '
         'periódicas.'),
        ('Módulo 5: Transformación Tecnológica',
         'La transformación digital es la integración de tecnología en todas las áreas de una '
         'organización, cambiando cómo opera y entrega valor. Se analizan tendencias como '
         'inteligencia artificial, Internet de las Cosas (IoT), Big Data, y computación en '
         'la nube. Se discute el impacto en el mercado laboral y la importancia de la '
         'capacitación continua. La transformación digital no es solo comprar tecnología, '
         'sino cambiar la cultura organizacional y los procesos.'),
    ]
    for titulo, cuerpo in modulos:
        story.append(Paragraph(titulo, styles['ModTitle']))
        story.append(Paragraph(cuerpo, styles['ModBody']))
        story.append(Spacer(1, 0.1 * inch))

    story.append(PageBreak())

    # Ejercicio de Falso y Verdadero
    story.append(Paragraph('Ejercicio de Verdadero / Falso', styles['ExerTitle']))
    story.append(Paragraph(
        'Instrucciones: Lee cada afirmación y escribe "V" si es verdadera o "F" si es falsa.',
        styles['ModBody']))
    story.append(Spacer(1, 0.15 * inch))

    ejercicios = [
        ('1. El hardware se refiere a los programas de una computadora.',
         'Falso — El hardware son los componentes físicos; los programas son software.'),
        ('2. Google Chrome es un navegador web.',
         'Verdadero — Google Chrome es un navegador para acceder a internet.'),
        ('3. URL significa "Universal Reference Language".',
         'Falso — URL significa Uniform Resource Locator.'),
        ('4. PowerPoint se utiliza para crear hojas de cálculo.',
         'Falso — PowerPoint es para presentaciones; Excel es para hojas de cálculo.'),
        ('5. El correo electrónico es un ejemplo de comunicación asíncrona.',
         'Verdadero — No requiere que emisor y receptor estén conectados simultáneamente.'),
        ('6. Una contraseña segura puede ser "123456".',
         'Falso — "123456" es débil y fácil de adivinar.'),
        ('7. El phishing es un tipo de ataque cibernético mediante engaño.',
         'Verdadero — El phishing usa mensajes falsos para robar información.'),
        ('8. Una red LAN conecta dispositivos en un área geográfica extensa.',
         'Falso — LAN cubre áreas locales; WAN cubre áreas extensas.'),
        ('9. La nube permite almacenar y acceder a datos por internet.',
         'Verdadero — La computación en la nube ofrece servicios bajo demanda vía internet.'),
        ('10. La transformación digital solo significa comprar tecnología nueva.',
         'Falso — Implica cambiar procesos, cultura y estrategia, no solo adquirir tecnología.'),
    ]
    data = [['Afirmación', 'V/F', 'Respuesta Correcta']]
    for afir, resp in ejercicios:
        data.append([afir, '_____', resp])

    t = Table(data, colWidths=[3.2 * inch, 0.6 * inch, 3.2 * inch])
    t.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 8),
        ('BACKGROUND', (0, 0), (-1, 0), HexColor('#1a237e')),
        ('TEXTCOLOR', (0, 0), (-1, 0), HexColor('#ffffff')),
        ('ALIGN', (1, 0), (2, -1), 'CENTER'),
        ('GRID', (0, 0), (-1, -1), 0.5, HexColor('#cccccc')),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    story.append(t)
    story.append(Spacer(1, 0.2 * inch))
    story.append(Paragraph(
        '<i>Nota: Las respuestas se muestran en la columna derecha para facilitar la revisión. '
        'En una evaluación en línea, el alumno debe seleccionar su respuesta sin ver la solución.</i>',
        ParagraphStyle('nota', parent=styles['Normal'], fontSize=8,
                        textColor=HexColor('#999999'))))

    doc.build(story)
    print('PDF generado con reportlab (%d páginas)' % (len(modulos) + 3))


def seed_demo():
    with app.app_context():
        db.create_all()
        print("=== CARGANDO CONTENIDO INICIAL ===")

        upload_dir = os.path.join(os.path.dirname(__file__), 'static', 'uploads')
        os.makedirs(upload_dir, exist_ok=True)

        # Limpiar tag   de registros existentes y actualizar descripciones viejas
        for c in Curso.query.filter(Curso.titulo.like('% %')).all():
            c.titulo = c.titulo.replace('  ', '').strip()
            if 'demostración' in c.descripcion_corta or 'demostración' in c.descripcion_larga:
                c.descripcion_corta = 'Aprende herramientas digitales, informática básica y transformación tecnológica para potenciar tu desarrollo profesional.'
                c.descripcion_larga = 'Curso completo que cubre los fundamentos de herramientas digitales, informática y transformación tecnológica. Incluye materiales de estudio, ejercicios prácticos, examen de certificación y acompañamiento de instructor especializado.'
        for c in Clase.query.filter(Clase.titulo.like('% %')).all():
            c.titulo = c.titulo.replace('  ', '').strip()
        for m in MaterialClase.query.filter(MaterialClase.titulo.like('% %')).all():
            m.titulo = m.titulo.replace('  ', '').strip()
        for t in Tarea.query.filter(Tarea.titulo.like('% %')).all():
            t.titulo = t.titulo.replace('  ', '').strip()
        for e in Examen.query.filter(Examen.titulo.like('% %')).all():
            e.titulo = e.titulo.replace('  ', '').strip()
        db.session.commit()

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
            print('Instructor creado: Jorge Flores')
        else:
            print('Instructor ya existe')

        # Foto del instructor
        foto_path = os.path.join(upload_dir, 'instructor-jorge.jpg')
        if not os.path.exists(foto_path):
            try:
                from PIL import Image, ImageDraw, ImageFont
                img = Image.new('RGB', (400, 400), '#1a237e')
                draw = ImageDraw.Draw(img)
                try:
                    font = ImageFont.truetype('arial.ttf', 140)
                except Exception:
                    font = ImageFont.load_default()
                bbox = draw.textbbox((0, 0), 'JF', font=font)
                tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
                draw.text(((400 - tw) // 2, (400 - th) // 2 - 10), 'JF',
                          fill='white', font=font)
                img.save(foto_path, 'JPEG', quality=85)
                print('Foto instructor creada')
            except ImportError:
                print('PIL no disponible, sin foto')

        # === CREAR/TOMAR CURSO DEMO ===
        create_all = False
        curso = Curso.query.filter_by(slug='herramientas-digitales-e-informatica').first()
        if not curso:
            create_all = True
            curso = Curso(
                titulo='Herramientas Digitales e Informática',
                slug='herramientas-digitales-e-informatica',
                descripcion_corta='Aprende herramientas digitales, informática básica y transformación tecnológica para potenciar tu desarrollo profesional.',
                descripcion_larga='Curso completo que cubre los fundamentos de herramientas digitales, informática y transformación tecnológica. Incluye materiales de estudio, ejercicios prácticos, examen de certificación y acompañamiento de instructor especializado.',
                categoria_id=cat.id, instructor_id=instructor.id,
                nivel='Principiante', duracion_horas=40, precio=0,
                modalidad='En línea', activo=True, tiene_certificado=True,
                temario={'modulos': ['Módulo 1: Introducción a la Informática', 'Módulo 2: Herramientas Digitales Básicas', 'Módulo 3: Internet y Comunicación Digital', 'Módulo 4: Seguridad Digital', 'Módulo 5: Transformación Tecnológica']}
            )
            db.session.add(curso); db.session.flush()
            print('Curso creado: Herramientas Digitales e Informática')

        # === CLASES (solo si curso nuevo) ===
        if create_all:
            for titulo, desc, tipo, duracion in [
                ('Introducción a la Informática', 'Conceptos básicos de informática, hardware y software.', 'grabada', 25),
                ('Sistemas Operativos', 'Conoce los principales sistemas operativos y su funcionamiento.', 'grabada', 30),
                ('Suite de Oficina', 'Uso de procesador de texto, hoja de cálculo y presentaciones.', 'grabada', 35),
                ('Navegación en Internet', 'Uso seguro y eficiente de navegadores web.', 'grabada', 20),
                ('Correo Electrónico', 'Gestión profesional del correo electrónico.', 'grabada', 25),
                ('Herramientas de Colaboración', 'Plataformas de trabajo colaborativo en la nube.', 'vivo', 40),
                ('Seguridad Digital', 'Buenas prácticas de seguridad informática.', 'grabada', 30),
                ('Transformación Digital', 'El impacto de la tecnología en la sociedad y el trabajo.', 'vivo', 35),
            ]:
                db.session.add(Clase(curso_id=curso.id, titulo=titulo, descripcion=desc, tipo=tipo,
                    url_video='https://www.youtube.com/embed/dQw4w9WgXcQ' if tipo == 'grabada' else '',
                    duracion_minutos=duracion, activo=True))
            db.session.flush()
            print('8 clases creadas')

        # === MATERIAL PDF ===
        pdf_path = os.path.join(upload_dir, 'demo_guia_herramientas_digitales.pdf')
        if not os.path.exists(pdf_path):
            _generar_pdf(pdf_path)

        if not MaterialClase.query.filter(MaterialClase.clase_id == Clase.id).join(Clase).filter(Clase.curso_id == curso.id).first():
            primera = Clase.query.filter_by(curso_id=curso.id).first()
            if primera:
                db.session.add(MaterialClase(clase_id=primera.id, titulo='Guía de Herramientas Digitales',
                    tipo='PDF', archivo_url='/uploads/demo_guia_herramientas_digitales.pdf'))
                print('Material PDF registro creado')

        # === TAREA (agregar si no existe) ===
        if not Tarea.query.filter_by(curso_id=curso.id).first():
            db.session.add(Tarea(curso_id=curso.id,
                titulo='Ejercicio práctico: Diagnóstico digital',
                descripcion='Realiza un diagnóstico de tus habilidades digitales actuales y elabora un plan de mejora.',
                fecha_entrega=datetime.utcnow() + timedelta(days=30), activo=True))
            print('Tarea creada')

        # === EXAMEN MIXTO (opción múltiple + verdadero/falso) ===
        examen = Examen.query.filter_by(curso_id=curso.id, titulo='Evaluación - Herramientas Digitales').first()
        if not examen:
            examen = Examen(curso_id=curso.id, titulo='Evaluación - Herramientas Digitales',
                descripcion='Examen de opción múltiple y verdadero/falso para evaluar los conocimientos adquiridos en el curso.',
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
            print(f'Examen creado con {len(preguntas)} preguntas')

        # === EJERCICIO DEDICADO DE FALSO Y VERDADERO ===
        ejercicio_fv = Examen.query.filter_by(curso_id=curso.id, titulo='Ejercicio de Falso y Verdadero').first()
        if not ejercicio_fv:
            ejercicio_fv = Examen(curso_id=curso.id, titulo='Ejercicio de Falso y Verdadero',
                descripcion='10 afirmaciones para evaluar conocimientos básicos de informática y herramientas digitales.',
                tiempo_limite_minutos=10, calificacion_minima=6.0, activo=True)
            db.session.add(ejercicio_fv); db.session.flush()

            fv_preguntas = [
                ('El hardware se refiere a los programas de una computadora.', ['Verdadero', 'Falso'], 1),
                ('Google Chrome es un navegador web.', ['Verdadero', 'Falso'], 0),
                ('URL significa "Universal Reference Language".', ['Verdadero', 'Falso'], 1),
                ('PowerPoint se utiliza para crear hojas de cálculo.', ['Verdadero', 'Falso'], 1),
                ('El correo electrónico es comunicación asíncrona.', ['Verdadero', 'Falso'], 0),
                ('Una contraseña segura puede ser "123456".', ['Verdadero', 'Falso'], 1),
                ('El phishing es un tipo de ataque cibernético mediante engaño.', ['Verdadero', 'Falso'], 0),
                ('Una red LAN conecta dispositivos en un área geográfica extensa.', ['Verdadero', 'Falso'], 1),
                ('La nube permite almacenar y acceder a datos por internet.', ['Verdadero', 'Falso'], 0),
                ('La transformación digital solo significa comprar tecnología nueva.', ['Verdadero', 'Falso'], 1),
            ]
            for texto, opciones, correcta in fv_preguntas:
                db.session.add(Pregunta(examen_id=ejercicio_fv.id, texto=texto, opciones=opciones, respuesta_correcta=correcta))
            print(f'Ejercicio Falso/Verdadero creado con {len(fv_preguntas)} preguntas')

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

                for cl in Clase.query.filter_by(curso_id=curso.id).all():
                    db.session.add(Asistencia(clase_id=cl.id, alumno_id=alumno.id,
                        presente=True,
                        fecha=datetime.utcnow() - timedelta(days=random.randint(1, 14))))

                tarea = Tarea.query.filter_by(curso_id=curso.id).first()
                if tarea:
                    db.session.add(EntregaTarea(tarea_id=tarea.id, alumno_id=alumno.id,
                        comentario='Tarea entregada y completada.',
                        calificacion=random.randint(8, 10),
                        fecha_entrega=datetime.utcnow() - timedelta(days=1)))

                from datetime import datetime as _dt
                folio = f'ENCL-{int(_dt.utcnow().timestamp())}-{alumno.id:04d}'
                db.session.add(Certificado(folio=folio,
                    alumno_id=alumno.id, curso_id=curso.id, instructor_id=instructor.id,
                    codigo_qr=f'https://jor231974.pythonanywhere.com/validar/{folio}', valido=True))

            print(f'5 alumnos creados con inscripciones, asistencias y progreso')
        else:
            print(f'Alumnos demo ya existen ({existing_demos})')

        db.session.commit()
        print("=== CONTENIDO CARGADO EXITOSAMENTE ===")

if __name__ == '__main__':
    seed_demo()
