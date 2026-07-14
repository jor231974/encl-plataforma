# -*- coding: utf-8 -*-
"""
Seed: English for Opportunity - Nivel A1 (12 semanas, 36 sesiones)
Ejecutar: python3 seed_english.py
"""
import sys, os, json
sys.path.insert(0, os.path.dirname(__file__) or '.')
from app import app, db
from models import *
from werkzeug.security import generate_password_hash

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

ACTIVITIES = {
    1: [  # Bienvenida e introducción
        {'tipo': 'flashcard', 'titulo': 'Greetings Vocabulary', 'instrucciones': 'Learn these greetings.',
         'config': {'frontal': 'Hello', 'reverso': 'Hola'}},
        {'tipo': 'flashcard', 'titulo': 'More Greetings', 'instrucciones': 'Study these basic phrases.',
         'config': {'frontal': 'Good morning', 'reverso': 'Buenos días'}},
        {'tipo': 'multiple', 'titulo': 'The Alphabet', 'instrucciones': 'Choose the correct letter.',
         'config': {'pregunta': 'What letter comes after "D"?', 'opciones': ['E', 'F', 'C', 'G'], 'respuesta': '0'}},
        {'tipo': 'ordenar', 'titulo': 'Greeting Dialogue', 'instrucciones': 'Order the conversation.',
         'config': {'items': ['Hi, how are you?', 'I am fine, thanks.', 'Goodbye!', 'See you later!'],
                    'orden': ['Hi, how are you?', 'I am fine, thanks.', 'Goodbye!', 'See you later!']}},
    ],
    2: [  # Información personal
        {'tipo': 'flashcard', 'titulo': 'Countries Vocabulary', 'instrucciones': 'Learn country names.',
         'config': {'frontal': 'Mexico', 'reverso': 'México'}},
        {'tipo': 'multiple', 'titulo': 'Nationalities', 'instrucciones': 'Choose the correct nationality.',
         'config': {'pregunta': 'She is from Mexico. She is...', 'opciones': ['Mexican', 'Mexicanese', 'Mexic', 'Mexico'],
                    'respuesta': '0'}},
        {'tipo': 'completar', 'titulo': 'Introduce Yourself', 'instrucciones': 'Complete the sentences.',
         'config': {'plantilla': {'campo_0': {'label': 'Name'}, 'campo_1': {'label': 'Country'}, 'campo_2': {'label': 'Age'}},
                    'respuestas': {'campo_0': 'My name is', 'campo_1': 'I am from', 'campo_2': 'I am'}}},
        {'tipo': 'verdadero_falso', 'titulo': 'Personal Info', 'instrucciones': 'True or false?',
         'config': {'pregunta': '"I am 20 years old" means "Tengo 20 años".', 'respuesta': 'true'}},
    ],
    3: [  # Consolidación
        {'tipo': 'relacionar', 'titulo': 'Match Questions & Answers', 'instrucciones': 'Match each question with the correct answer.',
         'config': {'pares': {'item_0': 'My name is Ana.', 'item_1': 'I am from Spain.', 'item_2': 'I am 25.', 'item_3': 'I am a teacher.'},
                    'opciones_derecha': ['My name is Ana.', 'I am from Spain.', 'I am 25.', 'I am a teacher.']}},
        {'tipo': 'ordenar', 'titulo': 'Spelling Bee', 'instrucciones': 'Order the letters to form the word.',
         'config': {'items': ['C-A-T', 'D-O-G', 'B-O-O-K', 'H-O-U-S-E'],
                    'orden': ['C-A-T', 'D-O-G', 'B-O-O-K', 'H-O-U-S-E']}},
        {'tipo': 'multiple', 'titulo': 'Basic Conversation', 'instrucciones': 'Choose the best reply.',
         'config': {'pregunta': 'What do you say when someone says "Thank you"?',
                    'opciones': ['You are welcome', 'Yes', 'Hello', 'Goodbye'], 'respuesta': '0'}},
    ],
    4: [  # Verbo To Be
        {'tipo': 'multiple', 'titulo': 'Verb To Be - Affirmative', 'instrucciones': 'Choose the correct form.',
         'config': {'pregunta': 'She ___ a doctor.', 'opciones': ['is', 'am', 'are', 'be'], 'respuesta': '0'}},
        {'tipo': 'completar', 'titulo': 'To Be - Negative', 'instrucciones': 'Write the negative form.',
         'config': {'plantilla': {'campo_0': {'label': 'I (not) tired'}, 'campo_1': {'label': 'He (not) here'}},
                    'respuestas': {'campo_0': 'am not', 'campo_1': 'is not'}}},
        {'tipo': 'verdadero_falso', 'titulo': 'To Be - Questions', 'instrucciones': 'True or false?',
         'config': {'pregunta': '"Are you happy?" is a correct question.', 'respuesta': 'true'}},
        {'tipo': 'flashcard', 'titulo': 'Pronouns', 'instrucciones': 'Learn subject pronouns.',
         'config': {'frontal': 'Yo (I)', 'reverso': 'I'}},
    ],
    5: [  # Descripciones
        {'tipo': 'flashcard', 'titulo': 'Adjectives', 'instrucciones': 'Study these adjectives.',
         'config': {'frontal': 'Tall', 'reverso': 'Alto/a'}},
        {'tipo': 'flashcard', 'titulo': 'Colors', 'instrucciones': 'Learn the colors.',
         'config': {'frontal': 'Blue', 'reverso': 'Azul'}},
        {'tipo': 'completar', 'titulo': 'Describe a Person', 'instrucciones': 'Complete the description.',
         'config': {'plantilla': {'campo_0': {'label': 'He is tall and'}, 'campo_1': {'label': 'She has hair'}},
                    'respuestas': {'campo_0': 'thin', 'campo_1': 'long'}}},
        {'tipo': 'multiple', 'titulo': 'Appearance', 'instrucciones': 'Choose the correct adjective.',
         'config': {'pregunta': 'A person with green eyes has...', 'opciones': ['green eyes', 'green hair', 'green skin', 'green clothes'],
                    'respuesta': '0'}},
    ],
    6: [  # Integración
        {'tipo': 'relacionar', 'titulo': 'Match Description to Person', 'instrucciones': 'Match each description.',
         'config': {'pares': {'item_0': 'Tall and thin', 'item_1': 'Short hair', 'item_2': 'Blue eyes', 'item_3': 'Friendly'},
                    'opciones_derecha': ['Tall and thin', 'Short hair', 'Blue eyes', 'Friendly']}},
        {'tipo': 'ordenar', 'titulo': 'Interview Order', 'instrucciones': 'Order the interview questions.',
         'config': {'items': ['What is your name?', 'Where are you from?', 'What do you do?', 'How old are you?'],
                    'orden': ['What is your name?', 'Where are you from?', 'How old are you?', 'What do you do?']}},
        {'tipo': 'multiple', 'titulo': 'Describing People', 'instrucciones': 'Choose the best description.',
         'config': {'pregunta': 'She has long, curly hair. She is...',
                    'opciones': ['tall with brown hair', 'short with straight hair', 'tall with blonde hair', 'short with curly hair'],
                    'respuesta': '0'}},
    ],
    7: [  # Familia
        {'tipo': 'flashcard', 'titulo': 'Family Members', 'instrucciones': 'Learn family vocabulary.',
         'config': {'frontal': 'Mother', 'reverso': 'Madre'}},
        {'tipo': 'flashcard', 'titulo': 'More Family', 'instrucciones': 'Study these family words.',
         'config': {'frontal': 'Brother', 'reverso': 'Hermano'}},
        {'tipo': 'multiple', 'titulo': 'This / These', 'instrucciones': 'Choose the correct word.',
         'config': {'pregunta': '___ are my parents.', 'opciones': ['These', 'This', 'That', 'It'], 'respuesta': '0'}},
        {'tipo': 'completar', 'titulo': 'My Family', 'instrucciones': 'Complete the sentences.',
         'config': {'plantilla': {'campo_0': {'label': 'My mother is'}, 'campo_1': {'label': 'My father is'}, 'campo_2': {'label': 'I have a'}},
                    'respuestas': {'campo_0': 'Maria', 'campo_1': 'Juan', 'campo_2': 'sister'}}},
    ],
    8: [  # Posesivos
        {'tipo': 'multiple', 'titulo': 'Possessive Adjectives', 'instrucciones': 'Choose the correct possessive.',
         'config': {'pregunta': 'This is ___ book.', 'opciones': ['my', 'I', 'me', 'mine'], 'respuesta': '0'}},
        {'tipo': 'completar', 'titulo': 'Possessive S', 'instrucciones': 'Complete with possessive form.',
         'config': {'plantilla': {'campo_0': {'label': 'The car of John'}, 'campo_1': {'label': 'The house of Maria'}},
                    'respuestas': {'campo_0': "John's car", 'campo_1': "Maria's house"}}},
        {'tipo': 'verdadero_falso', 'titulo': 'His or Her', 'instrucciones': 'True or false?',
         'config': {'pregunta': '"Her name is Ana" means Ana is a man.', 'respuesta': 'false'}},
        {'tipo': 'relacionar', 'titulo': 'Match Possessives', 'instrucciones': 'Match pronoun to possessive.',
         'config': {'pares': {'item_0': 'my', 'item_1': 'your', 'item_2': 'his', 'item_3': 'her'},
                    'opciones_derecha': ['I', 'you', 'he', 'she']}},
    ],
    9: [  # Conversación sobre familia
        {'tipo': 'ordenar', 'titulo': 'Family Tree', 'instrucciones': 'Order from oldest to youngest.',
         'config': {'items': ['Grandfather', 'Father', 'Son', 'Grandson'],
                    'orden': ['Grandfather', 'Father', 'Son', 'Grandson']}},
        {'tipo': 'multiple', 'titulo': 'Describe Family', 'instrucciones': 'Choose the correct sentence.',
         'config': {'pregunta': 'How do you say "Mi hermana es alta"?',
                    'opciones': ['My sister is tall', 'My brother is tall', 'My sister is short', 'My mother is tall'],
                    'respuesta': '0'}},
        {'tipo': 'completar', 'titulo': 'Talk About Family', 'instrucciones': 'Complete the conversation.',
         'config': {'plantilla': {'campo_0': {'label': 'How many brothers'}, 'campo_1': {'label': 'He is my'}},
                    'respuestas': {'campo_0': 'do you have?', 'campo_1': 'father'}}},
    ],
    10: [  # Simple Present
        {'tipo': 'multiple', 'titulo': 'Simple Present - He/She/It', 'instrucciones': 'Choose the correct form.',
         'config': {'pregunta': 'She ___ coffee every morning.', 'opciones': ['drinks', 'drink', 'drinking', 'drank'],
                    'respuesta': '0'}},
        {'tipo': 'completar', 'titulo': 'Daily Routines', 'instrucciones': 'Complete with the correct verb.',
         'config': {'plantilla': {'campo_0': {'label': 'I ___ up at 7am'}, 'campo_1': {'label': 'He ___ breakfast at 8am'}, 'campo_2': {'label': 'We ___ to work'}},
                    'respuestas': {'campo_0': 'wake', 'campo_1': 'has', 'campo_2': 'go'}}},
        {'tipo': 'verdadero_falso', 'titulo': 'Daily Habits', 'instrucciones': 'True or false?',
         'config': {'pregunta': '"I goes to school" is correct grammar.', 'respuesta': 'false'}},
        {'tipo': 'flashcard', 'titulo': 'Daily Actions', 'instrucciones': 'Study these verbs.',
         'config': {'frontal': 'Wake up', 'reverso': 'Despertarse'}},
    ],
    11: [  # Tiempo
        {'tipo': 'multiple', 'titulo': 'Telling the Time', 'instrucciones': 'What time is it? 7:30',
         'config': {'pregunta': '7:30 = ___', 'opciones': ['Half past seven', 'Half to seven', 'Seven thirty', 'A and C'],
                    'respuesta': '3'}},
        {'tipo': 'ordenar', 'titulo': 'Days of the Week', 'instrucciones': 'Order the days.',
         'config': {'items': ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'],
                    'orden': ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']}},
        {'tipo': 'flashcard', 'titulo': 'Months', 'instrucciones': 'Learn the months.',
         'config': {'frontal': 'January', 'reverso': 'Enero'}},
        {'tipo': 'completar', 'titulo': 'Dates', 'instrucciones': 'Write the date in English.',
         'config': {'plantilla': {'campo_0': {'label': '1/1 = January'}, 'campo_1': {'label': '25/12 = December'}},
                    'respuestas': {'campo_0': 'first', 'campo_1': 'twenty-fifth'}}},
    ],
    12: [  # Conversación rutina diaria
        {'tipo': 'ordenar', 'titulo': 'My Daily Routine', 'instrucciones': 'Order the daily routine.',
         'config': {'items': ['Wake up', 'Have breakfast', 'Go to work', 'Have lunch', 'Go home', 'Sleep'],
                    'orden': ['Wake up', 'Have breakfast', 'Go to work', 'Have lunch', 'Go home', 'Sleep']}},
        {'tipo': 'relacionar', 'titulo': 'Match Time to Activity', 'instrucciones': 'Match the time to the activity.',
         'config': {'pares': {'item_0': '7:00', 'item_1': '8:00', 'item_2': '12:00', 'item_3': '22:00'},
                    'opciones_derecha': ['Wake up', 'Go to work', 'Have lunch', 'Sleep']}},
        {'tipo': 'multiple', 'titulo': 'Role Play - Routine', 'instrucciones': 'What do you say?',
         'config': {'pregunta': 'What time do you usually have lunch?',
                    'opciones': ['At 12:00', 'In the morning', 'Yes, I do', 'I like lunch'], 'respuesta': '0'}},
    ],
    13: [  # Likes
        {'tipo': 'multiple', 'titulo': 'Like / Love / Hate', 'instrucciones': 'Choose the correct word.',
         'config': {'pregunta': 'I ___ pizza. It is my favorite food!', 'opciones': ['love', 'hate', 'dislike', 'don\'t like'],
                    'respuesta': '0'}},
        {'tipo': 'completar', 'titulo': 'Express Likes', 'instrucciones': 'Complete the sentences.',
         'config': {'plantilla': {'campo_0': {'label': 'I like'}, 'campo_1': {'label': 'She loves'}, 'campo_2': {'label': 'They hate'}},
                    'respuestas': {'campo_0': 'music', 'campo_1': 'dogs', 'campo_2': 'spiders'}}},
        {'tipo': 'verdadero_falso', 'titulo': 'Like Grammar', 'instrucciones': 'True or false?',
         'config': {'pregunta': '"He like soccer" is grammatically correct.', 'respuesta': 'false'}},
    ],
    14: [  # Hobbies
        {'tipo': 'flashcard', 'titulo': 'Hobbies', 'instrucciones': 'Learn hobby vocabulary.',
         'config': {'frontal': 'Swimming', 'reverso': 'Natación'}},
        {'tipo': 'flashcard', 'titulo': 'Sports', 'instrucciones': 'Study sport words.',
         'config': {'frontal': 'Soccer', 'reverso': 'Fútbol'}},
        {'tipo': 'multiple', 'titulo': 'Hobby Questions', 'instrucciones': 'Choose the correct question.',
         'config': {'pregunta': 'How do you ask about hobbies?',
                    'opciones': ['What do you do in your free time?', 'Where do you work?', 'How old are you?', 'What is your name?'],
                    'respuesta': '0'}},
        {'tipo': 'relacionar', 'titulo': 'Match Hobby to Place', 'instrucciones': 'Match activity to location.',
         'config': {'pares': {'item_0': 'Swimming', 'item_1': 'Reading', 'item_2': 'Watching movies', 'item_3': 'Playing soccer'},
                    'opciones_derecha': ['Pool', 'Library', 'Cinema', 'Field']}},
    ],
    15: [  # Integración gustos
        {'tipo': 'ordenar', 'titulo': 'Survey Questions', 'instrucciones': 'Order the survey questions.',
         'config': ['What is your name?', 'What is your favorite hobby?', 'Why do you like it?', 'How often do you do it?']},
        {'tipo': 'multiple', 'titulo': 'Survey Responses', 'instrucciones': 'Choose the best response.',
         'config': {'pregunta': 'Do you like playing video games?',
                    'opciones': ['Yes, I do. I love them.', 'I am a video game.', 'Yes, it is.', 'No, I am not.'],
                    'respuesta': '0'}},
        {'tipo': 'completar', 'titulo': 'Talk About Hobbies', 'instrucciones': 'Complete the conversation.',
         'config': {'plantilla': {'campo_0': {'label': 'Do you like'}, 'campo_1': {'label': 'I prefer'}},
                    'respuestas': {'campo_0': 'reading?', 'campo_1': 'sports'}}},
    ],
    16: [  # Places
        {'tipo': 'flashcard', 'titulo': 'City Places', 'instrucciones': 'Learn places in the city.',
         'config': {'frontal': 'Hospital', 'reverso': 'Hospital'}},
        {'tipo': 'flashcard', 'titulo': 'More Places', 'instrucciones': 'Study more locations.',
         'config': {'frontal': 'Supermarket', 'reverso': 'Supermercado'}},
        {'tipo': 'multiple', 'titulo': 'Places Vocabulary', 'instrucciones': 'Where do you go for medicine?',
         'config': {'pregunta': 'You need medicine. You go to the ___', 'opciones': ['pharmacy', 'school', 'park', 'restaurant'],
                    'respuesta': '0'}},
        {'tipo': 'relacionar', 'titulo': 'Match Place to Purpose', 'instrucciones': 'Match place to its purpose.',
         'config': {'pares': {'item_0': 'Hospital', 'item_1': 'School', 'item_2': 'Restaurant', 'item_3': 'Park'},
                    'opciones_derecha': ['To get medical help', 'To study', 'To eat', 'To relax']}},
    ],
    17: [  # There is/are
        {'tipo': 'multiple', 'titulo': 'There is / There are', 'instrucciones': 'Choose the correct form.',
         'config': {'pregunta': '___ a park near my house.', 'opciones': ['There is', 'There are', 'Is there', 'Are there'],
                    'respuesta': '0'}},
        {'tipo': 'completar', 'titulo': 'Some / Any', 'instrucciones': 'Complete with some or any.',
         'config': {'plantilla': {'campo_0': {'label': 'There are ___ books'}, 'campo_1': {'label': 'There are not ___ students'}},
                    'respuestas': {'campo_0': 'some', 'campo_1': 'any'}}},
        {'tipo': 'verdadero_falso', 'titulo': 'There is/are Grammar', 'instrucciones': 'True or false?',
         'config': {'pregunta': '"There are a bank near here" is correct.', 'respuesta': 'false'}},
    ],
    18: [  # Directions
        {'tipo': 'flashcard', 'titulo': 'Directions', 'instrucciones': 'Learn direction words.',
         'config': {'frontal': 'Turn left', 'reverso': 'Gira a la izquierda'}},
        {'tipo': 'ordenar', 'titulo': 'Give Directions', 'instrucciones': 'Order the directions.',
         'config': {'items': ['Go straight', 'Turn left', 'Walk two blocks', 'It is on your right'],
                    'orden': ['Go straight', 'Turn left', 'Walk two blocks', 'It is on your right']}},
        {'tipo': 'multiple', 'titulo': 'Asking for Directions', 'instrucciones': 'Choose the correct way to ask.',
         'config': {'pregunta': 'How do you ask for directions to the bank?',
                    'opciones': ['Excuse me, where is the bank?', 'What is the bank?', 'I like the bank.', 'The bank is blue.'],
                    'respuesta': '0'}},
        {'tipo': 'completar', 'titulo': 'Prepositions', 'instrucciones': 'Complete with next to, between, or behind.',
         'config': {'plantilla': {'campo_0': {'label': 'The bank is ___ the park'}, 'campo_1': {'label': 'The school is ___ the hospital and the library'}},
                    'respuestas': {'campo_0': 'next to', 'campo_1': 'between'}}},
    ],
    19: [  # Food
        {'tipo': 'flashcard', 'titulo': 'Food Vocabulary', 'instrucciones': 'Learn food names.',
         'config': {'frontal': 'Rice', 'reverso': 'Arroz'}},
        {'tipo': 'flashcard', 'titulo': 'Fruits', 'instrucciones': 'Study fruit names.',
         'config': {'frontal': 'Apple', 'reverso': 'Manzana'}},
        {'tipo': 'multiple', 'titulo': 'Food Categories', 'instrucciones': 'Which is a vegetable?',
         'config': {'pregunta': 'Which one is a vegetable?',
                    'opciones': ['carrot', 'banana', 'chicken', 'cheese'], 'respuesta': '0'}},
        {'tipo': 'completar', 'titulo': 'Food Sentences', 'instrucciones': 'Complete with a food word.',
         'config': {'plantilla': {'campo_0': {'label': 'I eat ___ for breakfast'}, 'campo_1': {'label': 'She drinks ___ for lunch'}},
                    'respuestas': {'campo_0': 'cereal', 'campo_1': 'water'}}},
    ],
    20: [  # Restaurant
        {'tipo': 'ordenar', 'titulo': 'At the Restaurant', 'instrucciones': 'Order the restaurant conversation.',
         'config': {'items': ['A table for two, please.', 'Here is the menu.', 'I would like pasta.', 'The bill, please.'],
                    'orden': ['A table for two, please.', 'Here is the menu.', 'I would like pasta.', 'The bill, please.']}},
        {'tipo': 'multiple', 'titulo': 'Ordering Food', 'instrucciones': 'How do you order?',
         'config': {'pregunta': 'You want to order pasta. You say:',
                    'opciones': ['I would like pasta.', 'I am pasta.', 'I like pasta yes.', 'Pasta me.'],
                    'respuesta': '0'}},
        {'tipo': 'relacionar', 'titulo': 'Match Food to Menu Section', 'instrucciones': 'Match food to menu section.',
         'config': {'pares': {'item_0': 'Salad', 'item_1': 'Chicken', 'item_2': 'Ice cream', 'item_3': 'Water'},
                    'opciones_derecha': ['Appetizer', 'Main course', 'Dessert', 'Drink']}},
    ],
    21: [  # Role play compras
        {'tipo': 'ordenar', 'titulo': 'At the Supermarket', 'instrucciones': 'Order the shopping dialogue.',
         'config': {'items': ['How much is this?', 'It is $5.', 'I will take it.', 'Here is your change.'],
                    'orden': ['How much is this?', 'It is $5.', 'I will take it.', 'Here is your change.']}},
        {'tipo': 'multiple', 'titulo': 'Shopping Questions', 'instrucciones': 'How do you ask the price?',
         'config': {'pregunta': 'How do you ask "¿Cuánto cuesta?"',
                    'opciones': ['How much is it?', 'How many is it?', 'What price?', 'Cost much?'],
                    'respuesta': '0'}},
        {'tipo': 'completar', 'titulo': 'Shopping Dialogue', 'instrucciones': 'Complete the dialogue.',
         'config': {'plantilla': {'campo_0': {'label': 'Can I help'}, 'campo_1': {'label': 'I am just'}},
                    'respuestas': {'campo_0': 'you?', 'campo_1': 'looking.'}}},
    ],
    22: [  # Present Continuous
        {'tipo': 'multiple', 'titulo': 'Present Continuous', 'instrucciones': 'Choose the correct form.',
         'config': {'pregunta': 'She ___ (read) a book right now.',
                    'opciones': ['is reading', 'reads', 'read', 'reading'], 'respuesta': '0'}},
        {'tipo': 'completar', 'titulo': 'Verb + ing', 'instrucciones': 'Write the -ing form.',
         'config': {'plantilla': {'campo_0': {'label': 'run'}, 'campo_1': {'label': 'swim'}, 'campo_2': {'label': 'write'}},
                    'respuestas': {'campo_0': 'running', 'campo_1': 'swimming', 'campo_2': 'writing'}}},
        {'tipo': 'verdadero_falso', 'titulo': 'Present Continuous Grammar', 'instrucciones': 'True or false?',
         'config': {'pregunta': '"He is work right now" is correct.', 'respuesta': 'false'}},
    ],
    23: [  # Actividades
        {'tipo': 'flashcard', 'titulo': 'Action Verbs', 'instrucciones': 'Study action verbs.',
         'config': {'frontal': 'Working', 'reverso': 'Trabajando'}},
        {'tipo': 'multiple', 'titulo': 'Actions in Progress', 'instrucciones': 'What is happening?',
         'config': {'pregunta': 'He is sitting and writing. He is...',
                    'opciones': ['working', 'sleeping', 'eating', 'driving'], 'respuesta': '0'}},
        {'tipo': 'relacionar', 'titulo': 'Match Verb to Picture', 'instrucciones': 'Match verb to description.',
         'config': {'pares': {'item_0': 'Driving', 'item_1': 'Studying', 'item_2': 'Cooking', 'item_3': 'Reading'},
                    'opciones_derecha': ['A person in a car', 'A person with books', 'A person in the kitchen', 'A person with a book']}},
    ],
    24: [  # Conversación acciones
        {'tipo': 'ordenar', 'titulo': 'What Are You Doing?', 'instrucciones': 'Order the conversation.',
         'config': ['Hi, what are you doing?', 'I am reading a book.', 'Is it good?', 'Yes, it is very interesting!']},
        {'tipo': 'multiple', 'titulo': 'Describe the Image', 'instrucciones': 'Choose the correct description.',
         'config': {'pregunta': 'A man is running in the park.',
                    'opciones': ['He is running.', 'He is sleeping.', 'He is eating.', 'He is reading.'],
                    'respuesta': '0'}},
        {'tipo': 'completar', 'titulo': 'What Is Happening?', 'instrucciones': 'Complete the description.',
         'config': {'plantilla': {'campo_0': {'label': 'The children are'}, 'campo_1': {'label': 'The dog is'}},
                    'respuestas': {'campo_0': 'playing', 'campo_1': 'sleeping'}}},
    ],
    25: [  # Simple Past
        {'tipo': 'multiple', 'titulo': 'Was / Were', 'instrucciones': 'Choose the correct past form.',
         'config': {'pregunta': 'I ___ at home yesterday.', 'opciones': ['was', 'were', 'am', 'is'], 'respuesta': '0'}},
        {'tipo': 'completar', 'titulo': 'Past Tense Verbs', 'instrucciones': 'Write the past form.',
         'config': {'plantilla': {'campo_0': {'label': 'walk'}, 'campo_1': {'label': 'study'}, 'campo_2': {'label': 'play'}},
                    'respuestas': {'campo_0': 'walked', 'campo_1': 'studied', 'campo_2': 'played'}}},
        {'tipo': 'flashcard', 'titulo': 'Irregular Verbs', 'instrucciones': 'Learn irregular past forms.',
         'config': {'frontal': 'Go - Went', 'reverso': 'Ir - Fui'}},
        {'tipo': 'verdadero_falso', 'titulo': 'Simple Past', 'instrucciones': 'True or false?',
         'config': {'pregunta': '"I go to the store yesterday" is correct.', 'respuesta': 'false'}},
    ],
    26: [  # Expresiones de tiempo
        {'tipo': 'multiple', 'titulo': 'Time Expressions', 'instrucciones': 'Choose the correct expression.',
         'config': {'pregunta': 'Which means "la semana pasada"?',
                    'opciones': ['last week', 'next week', 'this week', 'every week'], 'respuesta': '0'}},
        {'tipo': 'ordenar', 'titulo': 'Time Line', 'instrucciones': 'Order from past to future.',
         'config': {'items': ['Yesterday', 'Today', 'Tomorrow', 'Next week'],
                    'orden': ['Yesterday', 'Today', 'Tomorrow', 'Next week']}},
        {'tipo': 'completar', 'titulo': 'Past Time Sentences', 'instrucciones': 'Complete with yesterday, last, or ago.',
         'config': {'plantilla': {'campo_0': {'label': 'I saw her ___ week'}, 'campo_1': {'label': 'He called two days'}},
                    'respuestas': {'campo_0': 'last', 'campo_1': 'ago'}}},
    ],
    27: [  # Conversación pasado
        {'tipo': 'ordenar', 'titulo': 'Weekend Conversation', 'instrucciones': 'Order the dialogue.',
         'config': ['How was your weekend?', 'It was great!', 'What did you do?', 'I went to the beach.']},
        {'tipo': 'multiple', 'titulo': 'Talking about Vacation', 'instrucciones': 'Choose the best reply.',
         'config': {'pregunta': 'Did you enjoy your vacation?',
                    'opciones': ['Yes, I did. It was wonderful.', 'Yes, I do.', 'No, I am not.', 'Yes, it is.'],
                    'respuesta': '0'}},
        {'tipo': 'completar', 'titulo': 'My Weekend', 'instrucciones': 'Complete the story.',
         'config': {'plantilla': {'campo_0': {'label': 'Last weekend I'}, 'campo_1': {'label': 'I visited my'}},
                    'respuestas': {'campo_0': 'visited my family', 'campo_1': 'grandparents'}}},
    ],
    28: [  # Going to
        {'tipo': 'multiple', 'titulo': 'Future with Going To', 'instrucciones': 'Choose the correct form.',
         'config': {'pregunta': 'She ___ (travel) to Cancún next month.',
                    'opciones': ['is going to travel', 'going to travel', 'travels', 'traveled'], 'respuesta': '0'}},
        {'tipo': 'completar', 'titulo': 'Plans for Tomorrow', 'instrucciones': 'Complete the plans.',
         'config': {'plantilla': {'campo_0': {'label': 'Tomorrow I am going to'}, 'campo_1': {'label': 'We are going to'}},
                    'respuestas': {'campo_0': 'study English', 'campo_1': 'visit the museum'}}},
        {'tipo': 'verdadero_falso', 'titulo': 'Going To Grammar', 'instrucciones': 'True or false?',
         'config': {'pregunta': '"I going to travel" is grammatically correct.', 'respuesta': 'false'}},
    ],
    29: [  # Vocabulario futuro
        {'tipo': 'flashcard', 'titulo': 'Future Time Words', 'instrucciones': 'Study future time expressions.',
         'config': {'frontal': 'Tomorrow', 'reverso': 'Mañana'}},
        {'tipo': 'flashcard', 'titulo': 'Next...', 'instrucciones': 'Learn future time phrases.',
         'config': {'frontal': 'Next year', 'reverso': 'El próximo año'}},
        {'tipo': 'relacionar', 'titulo': 'Match Time Expression', 'instrucciones': 'Match Spanish to English.',
         'config': {'pares': {'item_0': 'Tomorrow', 'item_1': 'Next week', 'item_2': 'Next month', 'item_3': 'Next year'},
                    'opciones_derecha': ['Mañana', 'La próxima semana', 'El próximo mes', 'El próximo año']}},
        {'tipo': 'multiple', 'titulo': 'Future Plans', 'instrucciones': 'Choose the correct sentence.',
         'config': {'pregunta': 'How do you say "Voy a viajar el próximo año"?',
                    'opciones': ['I am going to travel next year.', 'I traveled last year.', 'I travel every year.', 'I was traveling.'],
                    'respuesta': '0'}},
    ],
    30: [  # Conversación futuro
        {'tipo': 'ordenar', 'titulo': 'Future Plans Dialogue', 'instrucciones': 'Order the conversation.',
         'config': ['What are you going to do this weekend?', 'I am going to visit my family.', 'That sounds nice!', 'Yes, I am excited.']},
        {'tipo': 'multiple', 'titulo': 'Goals and Plans', 'instrucciones': 'Choose the best response.',
         'config': {'pregunta': 'What are your goals for this year?',
                    'opciones': ['I am going to learn English.', 'I learned English.', 'I learn English.', 'I was learning English.'],
                    'respuesta': '0'}},
        {'tipo': 'completar', 'titulo': 'My Future Plans', 'instrucciones': 'Complete your plans.',
         'config': {'plantilla': {'campo_0': {'label': 'Next year I am going to'}, 'campo_1': {'label': 'I plan to'}},
                    'respuestas': {'campo_0': 'get a new job', 'campo_1': 'save money'}}},
    ],
    31: [  # Oficina
        {'tipo': 'flashcard', 'titulo': 'Office Vocabulary', 'instrucciones': 'Study office words.',
         'config': {'frontal': 'Computer', 'reverso': 'Computadora'}},
        {'tipo': 'flashcard', 'titulo': 'More Office', 'instrucciones': 'Learn more office vocabulary.',
         'config': {'frontal': 'Meeting', 'reverso': 'Reunión'}},
        {'tipo': 'multiple', 'titulo': 'Office Items', 'instrucciones': 'Which is an office item?',
         'config': {'pregunta': 'Which one do you find in an office?',
                    'opciones': ['desk', 'bed', 'stove', 'shower'], 'respuesta': '0'}},
        {'tipo': 'completar', 'titulo': 'Phone Call', 'instrucciones': 'Complete the phone call.',
         'config': {'plantilla': {'campo_0': {'label': 'Hello, may I speak'}, 'campo_1': {'label': 'Please hold the'}},
                    'respuestas': {'campo_0': 'to Mr. Smith?', 'campo_1': 'line.'}}},
    ],
    32: [  # Conversaciones profesionales
        {'tipo': 'ordenar', 'titulo': 'Business Presentation', 'instrucciones': 'Order the presentation.',
         'config': ['Good morning everyone.', 'Let me introduce myself.', 'Today we are going to talk about...', 'Any questions?']},
        {'tipo': 'multiple', 'titulo': 'Small Talk', 'instrucciones': 'Choose appropriate small talk.',
         'config': {'pregunta': 'What is appropriate small talk at work?',
                    'opciones': ['Nice weather today.', 'Give me your report now.', 'You are wrong.', 'I do not like you.'],
                    'respuesta': '0'}},
        {'tipo': 'relacionar', 'titulo': 'Match Professional Phrases', 'instrucciones': 'Match the phrases.',
         'config': {'pares': {'item_0': 'Nice to meet you', 'item_1': 'Let me introduce', 'item_2': 'I work as', 'item_3': 'I am in charge of'},
                    'opciones_derecha': ['Meeting someone new', 'Introducing a colleague', 'Telling your position', 'Telling your responsibility']}},
    ],
    33: [  # Role plays profesionales
        {'tipo': 'ordenar', 'titulo': 'Customer Service', 'instrucciones': 'Order the service dialogue.',
         'config': ['How can I help you?', 'I have a problem with my order.', 'Let me check for you.', 'Here is the solution.']},
        {'tipo': 'multiple', 'titulo': 'Meeting Phrases', 'instrucciones': 'What do you say in a meeting?',
         'config': {'pregunta': 'To express agreement you say:',
                    'opciones': ['I agree.', 'I disagree.', 'I do not know.', 'Maybe.'],
                    'respuesta': '0'}},
        {'tipo': 'completar', 'titulo': 'Professional Role Play', 'instrucciones': 'Complete the dialogue.',
         'config': {'plantilla': {'campo_0': {'label': 'Could you please'}, 'campo_1': {'label': 'I will send you the'}},
                    'respuestas': {'campo_0': 'send me the report?', 'campo_1': 'documents.'}}},
    ],
    34: [  # Repaso
        {'tipo': 'multiple', 'titulo': 'Grammar Review', 'instrucciones': 'Choose the correct option.',
         'config': {'pregunta': 'Which sentence is correct?',
                    'opciones': ['She is a teacher.', 'She a teacher.', 'She be teacher.', 'She am teacher.'],
                    'respuesta': '0'}},
        {'tipo': 'relacionar', 'titulo': 'Match Tense to Use', 'instrucciones': 'Match each tense to its use.',
         'config': {'pares': {'item_0': 'Simple Present', 'item_1': 'Present Continuous', 'item_2': 'Simple Past', 'item_3': 'Going to'},
                    'opciones_derecha': ['Routines and facts', 'Actions now', 'Past events', 'Future plans']}},
        {'tipo': 'completar', 'titulo': 'Complete the Review', 'instrucciones': 'Fill in the correct tense.',
         'config': {'plantilla': {'campo_0': {'label': 'I ___ (study) every day'}, 'campo_1': {'label': 'She ___ (work) now'}, 'campo_2': {'label': 'They ___ (travel) last year'}},
                    'respuestas': {'campo_0': 'study', 'campo_1': 'is working', 'campo_2': 'traveled'}}},
        {'tipo': 'flashcard', 'titulo': 'Key Vocabulary Review', 'instrucciones': 'Review key words.',
         'config': {'frontal': 'Vocabulary Review Complete!', 'reverso': 'Great job!'}},
    ],
    35: [  # Proyecto final
        {'tipo': 'ordenar', 'titulo': 'Final Presentation Steps', 'instrucciones': 'Order the presentation steps.',
         'config': ['Introduce yourself', 'Talk about your family', 'Describe your daily routine', 'Talk about your future plans']},
        {'tipo': 'multiple', 'titulo': 'Final Project - Choose', 'instrucciones': 'What is the first step?',
         'config': {'pregunta': 'To start your presentation you should...',
                    'opciones': ['greet the audience', 'say goodbye', 'show pictures', 'sit down'], 'respuesta': '0'}},
        {'tipo': 'completar', 'titulo': 'My Final Presentation', 'instrucciones': 'Complete your presentation.',
         'config': {'plantilla': {'campo_0': {'label': 'Hello everyone, my name is'}, 'campo_1': {'label': 'I am from'}, 'campo_2': {'label': 'In the future, I want to'}},
                    'respuestas': {'campo_0': '[your name]', 'campo_1': '[your country]', 'campo_2': '[your goal]'}}},
    ],
    36: [  # Evaluación
        {'tipo': 'multiple', 'titulo': 'Final Evaluation - Grammar', 'instrucciones': 'Choose the correct answer.',
         'config': {'pregunta': 'Which sentence uses the past tense correctly?',
                    'opciones': ['I walked to school yesterday.', 'I walk to school yesterday.', 'I walking to school yesterday.', 'I walks to school yesterday.'],
                    'respuesta': '0'}},
        {'tipo': 'multiple', 'titulo': 'Vocabulary Check', 'instrucciones': 'What does "hospital" mean?',
         'config': {'pregunta': 'Hospital means...',
                    'opciones': ['hospital', 'escuela', 'casa', 'parque'], 'respuesta': '0'}},
        {'tipo': 'verdadero_falso', 'titulo': 'Course Review', 'instrucciones': 'True or false?',
         'config': {'pregunta': '"I am going to study more English" is a future plan.', 'respuesta': 'true'}},
        {'tipo': 'completar', 'titulo': 'Self Assessment', 'instrucciones': 'Complete the sentences about you.',
         'config': {'plantilla': {'campo_0': {'label': 'I learned to'}, 'campo_1': {'label': 'I need to practice'}},
                    'respuestas': {'campo_0': 'speak basic English', 'campo_1': 'pronunciation'}}},
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
                titulo='English for Opportunity - Nivel A1',
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
                    db.session.flush()

                    acts = ACTIVITIES.get(s_num, [])
                    for i, act_data in enumerate(acts):
                        config = act_data.get('config', {})
                        if isinstance(config, list):
                            config = {'items': config, 'orden': config[:]}
                        act = Actividad(
                            sesion_id=ses.id,
                            tipo=act_data['tipo'],
                            titulo=act_data['titulo'],
                            instrucciones=act_data.get('instrucciones', ''),
                            config=json.dumps(config),
                            calificacion_minima=70,
                            max_intentos=3,
                            orden=i + 1
                        )
                        db.session.add(act)

            print('12 semanas y 36 sesiones creadas')
        else:
            print(f'Curso ya existe (ID {curso.id})')
            needs_activities = False
            for sem in CursoSemana.query.filter_by(curso_id=curso.id).all():
                for ses in SemanaSesion.query.filter_by(semana_id=sem.id).all():
                    if Actividad.query.filter_by(sesion_id=ses.id).count() == 0:
                        needs_activities = True
                        break
                if needs_activities:
                    break
            if needs_activities:
                print('Agregando actividades faltantes...')
                for sem in CursoSemana.query.filter_by(curso_id=curso.id).order_by(CursoSemana.orden).all():
                    for ses in SemanaSesion.query.filter_by(semana_id=sem.id).order_by(SemanaSesion.orden).all():
                        existing = Actividad.query.filter_by(sesion_id=ses.id).count()
                        if existing == 0:
                            acts = ACTIVITIES.get(ses.numero, [])
                            for i, act_data in enumerate(acts):
                                config = act_data.get('config', {})
                                if isinstance(config, list):
                                    config = {'items': config, 'orden': config[:]}
                                act = Actividad(
                                    sesion_id=ses.id,
                                    tipo=act_data['tipo'],
                                    titulo=act_data['titulo'],
                                    instrucciones=act_data.get('instrucciones', ''),
                                    config=json.dumps(config),
                                    calificacion_minima=70,
                                    max_intentos=3,
                                    orden=i + 1
                                )
                                db.session.add(act)
                print('Actividades agregadas')
            else:
                print('Todas las sesiones ya tienen actividades')

        db.session.commit()

        # Crear alumno de prueba carlos
        alumno = User.query.filter_by(username='carlos').first()
        if not alumno:
            alumno = User(
                username='carlos', email='carlos@correo.com',
                password_hash=generate_password_hash('alumno123'),
                role='alumno', nombre='Carlos', apellidos='García López',
                activo=True, telefono='5512345678'
            )
            db.session.add(alumno)
            db.session.flush()
            print('Alumno carlos creado')
        if curso and alumno:
            insc = Inscripcion.query.filter_by(alumno_id=alumno.id, curso_id=curso.id).first()
            if not insc:
                insc = Inscripcion(alumno_id=alumno.id, curso_id=curso.id, progreso=0)
                db.session.add(insc)
                print(f'{alumno.nombre} inscrito al curso')
        db.session.commit()

        total_acts = Actividad.query.join(SemanaSesion).join(CursoSemana).filter(CursoSemana.curso_id == curso.id).count()
        print()
        print('=== ENGLISH FOR OPPORTUNITY - NIVEL A1 ===')
        print(f'Instructor: marifer / instructor123')
        print(f'Semanas: {CursoSemana.query.filter_by(curso_id=curso.id).count()}')
        print(f'Sesiones: {SemanaSesion.query.join(CursoSemana).filter(CursoSemana.curso_id == curso.id).count()}')
        print(f'Actividades: {total_acts}')
        print('DONE.')

if __name__ == '__main__':
    seed()
