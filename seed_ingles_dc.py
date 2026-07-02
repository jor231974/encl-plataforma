"""Seed the English course with DC PROYECTO content into ENCL's database."""
from app import app, db
from models import Curso, Clase, Examen, Pregunta, Tarea
from datetime import datetime, timedelta
import json

def seed_english_course():
    with app.app_context():
        curso = Curso.query.filter_by(slug='ingles-basico').first()
        if not curso:
            print("ERROR: Curso 'ingles-basico' not found. Run main seed first.")
            return

        curso_id = curso.id

        # Remove existing generic content (including questions via join)
        old_exams = Examen.query.filter_by(curso_id=curso_id).all()
        for old_ex in old_exams:
            Pregunta.query.filter_by(examen_id=old_ex.id).delete()
        Clase.query.filter_by(curso_id=curso_id).delete()
        Examen.query.filter_by(curso_id=curso_id).delete()
        Tarea.query.filter_by(curso_id=curso_id).delete()
        db.session.commit()

        # Update course with rich description
        curso.descripcion_corta = 'Domina las bases del inglés con nuestro curso más popular. 12 clases con videos, ejercicios interactivos y exámenes.'
        curso.descripcion_larga = 'Curso completo de inglés básico A1-A2 para principiantes. Cubre vocabulario esencial, gramática fundamental, conversación básica, pronunciación y comprensión auditiva. Incluye 12 clases con videos de YouTube, 4 tareas prácticas y 2 exámenes (diagnóstico y final) con evaluación automática.'
        curso.duracion_horas = 40
        curso.precio = 0
        curso.tiene_certificado = True
        curso.video_presentacion = 'https://www.youtube.com/embed/1Qq7eQsQ8lM'
        curso.temario = {'modulos': ['Módulo 1: Fundamentos - Alfabeto y Pronunciación', 'Módulo 2: Saludos y Presentaciones', 'Módulo 3: Números y Fechas', 'Módulo 4: Vida Cotidiana', 'Módulo 5: Gramática Básica', 'Módulo 6: Descripciones', 'Módulo 7: Comida y Restaurante', 'Módulo 8: Direcciones', 'Módulo 9: Rutina Diaria', 'Módulo 10: Repaso', 'Módulo 11: Clima', 'Módulo 12: Compras']}

        # === 12 CLASSES ===
        now = datetime.now()
        classes_data = [
            {'titulo': 'Introducción al Inglés - Alfabeto y Pronunciación', 'tipo': 'grabada', 'descripcion': 'Aprende el alfabeto inglés, sonidos básicos y reglas de pronunciación.', 'duracion_minutos': 45, 'url_video': 'https://www.youtube.com/embed/1Qq7eQsQ8lM'},
            {'titulo': 'Saludos y Presentaciones', 'tipo': 'vivo', 'descripcion': 'Clase en vivo: Practica saludos formales e informales, cómo presentarte.', 'duracion_minutos': 60, 'fecha_programada': now + timedelta(days=1)},
            {'titulo': 'Números, Fechas y Horas', 'tipo': 'grabada', 'descripcion': 'Los números cardinales y ordinales, cómo decir la fecha y la hora.', 'duracion_minutos': 40, 'url_video': 'https://www.youtube.com/embed/5Bz8iFyX5hA'},
            {'titulo': 'Vocabulario de la Vida Cotidiana', 'tipo': 'grabada', 'descripcion': 'Palabras y frases útiles para la rutina diaria: casa, comida, familia.', 'duracion_minutos': 50, 'url_video': 'https://www.youtube.com/embed/7g2UyI5Yy6I'},
            {'titulo': 'Gramática Básica - Verb To Be', 'tipo': 'vivo', 'descripcion': 'Clase en vivo: Uso del verbo TO BE en presente afirmativo, negativo e interrogativo.', 'duracion_minutos': 60, 'fecha_programada': now + timedelta(days=3)},
            {'titulo': 'Mi Familia y Amigos - Descripciones', 'tipo': 'grabada', 'descripcion': 'Adjetivos para describir personas, vocabulario de la familia.', 'duracion_minutos': 45, 'url_video': 'https://www.youtube.com/embed/3j5i7e8f9a0'},
            {'titulo': 'En el Restaurante - Pedir Comida', 'tipo': 'grabada', 'descripcion': 'Frases útiles para restaurantes, vocabulario de comidas y bebidas.', 'duracion_minutos': 40, 'url_video': 'https://www.youtube.com/embed/9k1l2m3n4o5'},
            {'titulo': 'Direcciones y Lugares en la Ciudad', 'tipo': 'vivo', 'descripcion': 'Clase en vivo: Cómo preguntar y dar direcciones, lugares de la ciudad.', 'duracion_minutos': 60, 'fecha_programada': now + timedelta(days=7)},
            {'titulo': 'Rutina Diaria - Presente Simple', 'tipo': 'grabada', 'descripcion': 'El presente simple para hablar de rutinas diarias, adverbios de frecuencia.', 'duracion_minutos': 50, 'url_video': 'https://www.youtube.com/embed/6p7q8r9s0t1'},
            {'titulo': 'Repaso General y Práctica', 'tipo': 'vivo', 'descripcion': 'Clase en vivo de repaso: ejercicios interactivos, preguntas y respuestas.', 'duracion_minutos': 90, 'fecha_programada': now + timedelta(days=14)},
            {'titulo': 'El Clima y las Estaciones', 'tipo': 'grabada', 'descripcion': 'Vocabulario del clima, estaciones del año, expresiones del tiempo.', 'duracion_minutos': 40, 'url_video': 'https://www.youtube.com/embed/2u3v4w5x6y7'},
            {'titulo': 'Compras y Ropa', 'tipo': 'grabada', 'descripcion': 'Vocabulario de ropa, colores, tallas, frases para ir de compras.', 'duracion_minutos': 45, 'url_video': 'https://www.youtube.com/embed/8z9a0b1c2d3'},
        ]

        for cd in classes_data:
            clase = Clase(curso_id=curso_id, activo=True, **cd)
            db.session.add(clase)

        # === 4 ASSIGNMENTS ===
        tareas_data = [
            {'titulo': 'Mi Presentación Personal', 'descripcion': 'Graba un video de 1 minuto presentándote en inglés. Di tu nombre, edad, de dónde eres y tus hobbies.', 'fecha_entrega': now + timedelta(days=7)},
            {'titulo': 'Ejercicio de Gramática - Verb To Be', 'descripcion': 'Completa 20 oraciones usando el verbo TO BE en forma afirmativa, negativa e interrogativa.', 'fecha_entrega': now + timedelta(days=14)},
            {'titulo': 'Descripción de mi Familia', 'descripcion': 'Escribe un párrafo describiendo a 3 miembros de tu familia. Incluye edad, personalidad y apariencia física.', 'fecha_entrega': now + timedelta(days=21)},
            {'titulo': 'Mi Rutina Diaria', 'descripcion': 'Escribe 10 oraciones sobre tu rutina diaria usando el presente simple. Incluye horarios.', 'fecha_entrega': now + timedelta(days=28)},
        ]

        for td in tareas_data:
            tarea = Tarea(curso_id=curso_id, activo=True, archivo_url='', **td)
            db.session.add(tarea)

        # === EXAM 1: Diagnóstico ===
        ex1 = Examen(curso_id=curso_id, titulo='Examen Diagnóstico - Inglés Básico A1-A2',
                     descripcion='Evalúa tu nivel de inglés básico. 15 preguntas de opción múltiple.',
                     tiempo_limite_minutos=15, calificacion_minima=6.0)
        db.session.add(ex1)
        db.session.flush()

        preguntas_diag = [
            ('How do you say "Hola" in English?', '["Goodbye","Hello","Thanks","Please"]', 1),
            ('Complete: I ___ a student.', '["am","is","are","be"]', 0),
            ('What is the plural of "child"?', '["childs","children","childes","childrens"]', 1),
            ('Choose: She ___ to music every day.', '["listen","listens","listening","listened"]', 1),
            ('What does "beautiful" mean?', '["Feo","Alto","Hermoso","Bajo"]', 2),
            ('Complete: They ___ playing soccer now.', '["is","am","are","be"]', 2),
            ('What time is it? 3:30', '["Three o\'clock","Half past three","Quarter to four","Three thirty"]', 1),
            ('Choose: I go to work ___ bus.', '["on","in","by","at"]', 2),
            ('What is the opposite of "hot"?', '["Warm","Cold","Cool","Freezing"]', 1),
            ('Complete: She ___ to the store yesterday.', '["go","goes","went","going"]', 2),
            ('How do you say "Gracias" in English?', '["Please","Sorry","Thanks","Hello"]', 2),
            ('Choose: There ___ many books on the table.', '["is","are","am","be"]', 1),
            ('What does "fast" mean?', '["Lento","Rápido","Grande","Pequeño"]', 1),
            ('Complete: We ___ not like coffee.', '["do","does","is","are"]', 0),
            ('Which is a correct greeting?', '["Good night","Good evening","Goodbye morning","Good middle"]', 1),
        ]
        for texto, opciones, correcta in preguntas_diag:
            p = Pregunta(examen_id=ex1.id, texto=texto, opciones=json.loads(opciones), respuesta_correcta=correcta)
            db.session.add(p)

        # === EXAM 2: Final ===
        ex2 = Examen(curso_id=curso_id, titulo='Examen Final - Inglés Básico A1-A2',
                     descripcion='Examen final del curso. 10 preguntas para evaluar tu progreso.',
                     tiempo_limite_minutos=20, calificacion_minima=7.0)
        db.session.add(ex2)
        db.session.flush()

        preguntas_final = [
            ('Complete: My name ___ John.', '["am","is","are","be"]', 1),
            ('Choose the correct sentence:', '["She go to school","She goes to school","She going to school","She to go school"]', 1),
            ('What is "perro" in English?', '["Cat","Dog","Bird","Fish"]', 1),
            ('Complete: I ___ born in 1990.', '["was","were","am","is"]', 0),
            ('Which is a day of the week?', '["January","Monday","Summer","Winter"]', 1),
            ('Choose: There ___ a book on the desk.', '["is","are","am","be"]', 0),
            ('What does "delicious" mean?', '["Delicioso","Horrible","Aburrido","Peligroso"]', 0),
            ('Complete: They ___ watching TV now.', '["is","am","are","be"]', 2),
            ('How do you say "¿Dónde está el baño?"', '["Where is the bathroom?","What is the bathroom?","When is the bathroom?","Who is the bathroom?"]', 0),
            ('Choose: I have ___ apple.', '["a","an","the","some"]', 1),
        ]
        for texto, opciones, correcta in preguntas_final:
            p = Pregunta(examen_id=ex2.id, texto=texto, opciones=json.loads(opciones), respuesta_correcta=correcta)
            db.session.add(p)

        db.session.commit()

        # Verify
        clases_count = Clase.query.filter_by(curso_id=curso_id).count()
        examenes_count = Examen.query.filter_by(curso_id=curso_id).count()
        preguntas_count = Pregunta.query.filter(Pregunta.examen_id.in_([ex1.id, ex2.id])).count()
        tareas_count = Tarea.query.filter_by(curso_id=curso_id).count()

        print(f"OK - Curso '{curso.titulo}' enriquecido:")
        print(f"  Clases: {clases_count}")
        print(f"  Examens: {examenes_count} ({preguntas_count} preguntas)")
        print(f"  Tareas: {tareas_count}")

if __name__ == '__main__':
    seed_english_course()
