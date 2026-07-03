import os
from flask import (Flask, render_template, redirect, url_for, request,
                   flash, jsonify, session, send_from_directory)
from flask_login import (LoginManager, login_user, logout_user,
                         login_required, current_user)
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
import json
import uuid

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'encl-secret-key-2026-mexico')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///encl.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = os.path.join('static', 'uploads')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

from models import *

db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'public_login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def get_config(key, default=''):
    conf = Configuracion.query.filter_by(clave=key).first()
    return conf.valor if conf else default

def get_theme_config():
    return {
        'site_name': get_config('site_name', 'ESCUELA NACIONAL DE CAPACITACIÓN Y CURSOS EN LÍNEA'),
        'site_subtitle': get_config('site_subtitle', 'Transformando personas, fortaleciendo comunidades y desarrollando talento para el futuro.'),
        'hero_title': get_config('hero_title'),
        'hero_subtitle': get_config('hero_subtitle'),
        'about_text': get_config('about_text'),
        'mision': get_config('mision_text'),
        'vision': get_config('vision_text'),
        'contact_email': get_config('contact_email'),
        'contact_phone': get_config('contact_phone'),
        'contact_address': get_config('contact_address'),
        'primary_color': get_config('primary_color', '#0d6efd'),
        'favicon_url': get_config('favicon_url', ''),
        'get_config': get_config,
    }

def get_territorial_context(user):
    context = {}
    if user.estado:
        context['estado'] = user.estado.nombre
    if user.municipio:
        context['municipio'] = user.municipio.nombre
    if user.distrito:
        context['distrito'] = user.distrito.nombre
    if user.grupo:
        context['grupo'] = user.grupo.nombre
    return context

@app.context_processor
def inject_globals():
    return dict(
        now=datetime.utcnow,
        get_config=get_config,
        theme=get_theme_config(),
        User=User,
        Curso=Curso,
        Inscripcion=Inscripcion,
        Estado=Estado,
        Certificado=Certificado
    )

def admin_required(f):
    context = {}
    if user.estado:
        context['estado'] = user.estado.nombre
    if user.municipio:
        context['municipio'] = user.municipio.nombre
    if user.distrito:
        context['distrito'] = user.distrito.nombre
    if user.grupo:
        context['grupo'] = user.grupo.nombre
    return context

def admin_required(f):
    from functools import wraps
    @wraps(f)
    def decorated(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role not in ['admin', 'superadmin']:
            flash('Acceso no autorizado', 'error')
            return redirect(url_for('public_login'))
        return f(*args, **kwargs)
    return decorated

def instructor_required(f):
    from functools import wraps
    @wraps(f)
    def decorated(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role not in ['instructor', 'admin', 'superadmin']:
            flash('Acceso no autorizado', 'error')
            return redirect(url_for('public_login'))
        return f(*args, **kwargs)
    return decorated

def superadmin_required(f):
    from functools import wraps
    @wraps(f)
    def decorated(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != 'superadmin':
            flash('Acceso solo para Super Administrador', 'error')
            return redirect(url_for('admin_dashboard'))
        return f(*args, **kwargs)
    return decorated

# ==================== PUBLIC ROUTES ====================

@app.route('/')
def public_index():
    categorias = Categoria.query.filter_by(activo=True).all()
    cursos = Curso.query.filter_by(activo=True).all()
    instructores = User.query.filter_by(role='instructor', activo=True).all()
    patrocinadores = Patrocinador.query.filter_by(activo=True).all()
    banners = Banner.query.filter_by(activo=True).order_by(Banner.orden).all()
    total_cursos = len(cursos)
    total_alumnos = User.query.filter_by(role='alumno', activo=True).count()
    total_instructores = len(instructores)
    tc = get_theme_config()
    return render_template('public/index.html', **tc,
                         categorias=categorias, cursos=cursos,
                         instructores=instructores, patrocinadores=patrocinadores,
                         banners=banners,
                         total_cursos=total_cursos,
                         total_alumnos=total_alumnos, total_instructores=total_instructores)

@app.route('/cursos')
def public_cursos():
    categoria_id = request.args.get('categoria')
    nivel = request.args.get('nivel')
    busqueda = request.args.get('q')
    query = Curso.query.filter_by(activo=True)
    if categoria_id:
        query = query.filter_by(categoria_id=int(categoria_id))
    if nivel:
        query = query.filter_by(nivel=nivel)
    if busqueda:
        query = query.filter(Curso.titulo.contains(busqueda))
    cursos = query.all()
    categorias = Categoria.query.filter_by(activo=True).all()
    tc = get_theme_config()
    return render_template('public/cursos.html', cursos=cursos, categorias=categorias, **tc)

@app.route('/curso/<slug>')
@login_required
def public_curso_detalle(slug):
    curso = Curso.query.filter_by(slug=slug, activo=True).first_or_404()
    if slug == 'ingles-basico':
        return redirect(url_for('public_curso_ingles'))
    tc = get_theme_config()
    return render_template('public/curso_detalle.html', curso=curso, **tc)

@app.route('/curso-de-ingles')
@login_required
def public_curso_ingles():
    curso = Curso.query.filter_by(slug='ingles-basico', activo=True).first_or_404()
    clases = Clase.query.filter_by(curso_id=curso.id, activo=True).order_by(Clase.id).all()
    examenes = Examen.query.filter_by(curso_id=curso.id).all()
    for ex in examenes:
        ex.preguntas = Pregunta.query.filter_by(examen_id=ex.id).all()
    tareas = Tarea.query.filter_by(curso_id=curso.id, activo=True).all()
    import json as jmod
    examenes_json = []
    for ex in examenes:
        preg = []
        for p in ex.preguntas:
            preg.append({'id': p.id, 'texto': p.texto, 'opciones': p.opciones, 'respuesta_correcta': p.respuesta_correcta})
        examenes_json.append({'id': ex.id, 'titulo': ex.titulo, 'descripcion': ex.descripcion, 'tiempo_limite_minutos': ex.tiempo_limite_minutos, 'calificacion_minima': ex.calificacion_minima, 'preguntas': preg})
    tc = get_theme_config()
    return render_template('public/curso_ingles.html', curso=curso, clases=clases, examenes=examenes, tareas=tareas, examenes_json=jmod.dumps(examenes_json), **tc)

@app.route('/nosotros')
def public_nosotros():
    tc = get_theme_config()
    return render_template('public/nosotros.html', **tc)

@app.route('/contacto', methods=['GET', 'POST'])
def public_contacto():
    if request.method == 'POST':
        flash('Mensaje enviado correctamente. Nos pondremos en contacto pronto.', 'success')
        return redirect(url_for('public_contacto'))
    tc = get_theme_config()
    return render_template('public/contacto.html', **tc)

@app.route('/instructores')
def public_instructores():
    instructores = User.query.filter_by(role='instructor', activo=True).all()
    tc = get_theme_config()
    return render_template('public/instructores.html', instructores=instructores, **tc)

@app.route('/patrocinadores')
def public_patrocinadores():
    patrocinadores = Patrocinador.query.filter_by(activo=True).all()
    tc = get_theme_config()
    return render_template('public/patrocinadores.html', patrocinadores=patrocinadores, **tc)

@app.route('/login', methods=['GET', 'POST'])
def public_login():
    if current_user.is_authenticated:
        return redirect_user_by_role()
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password_hash, password):
            if not user.activo:
                flash('Cuenta desactivada. Contacte al administrador.', 'error')
                return render_template('login.html', **get_theme_config())
            login_user(user)
            flash(f'Bienvenido {user.nombre} {user.apellidos}', 'success')
            return redirect_user_by_role()
        flash('Usuario o contraseña incorrectos', 'error')
    tc = get_theme_config()
    return render_template('login.html', **tc)

@app.route('/registro', methods=['GET', 'POST'])
def public_registro():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        nombre = request.form.get('nombre')
        apellidos = request.form.get('apellidos')

        if User.query.filter_by(username=username).first():
            flash('El usuario ya existe', 'error')
            return render_template('registro.html', **get_theme_config())
        if User.query.filter_by(email=email).first():
            flash('El email ya está registrado', 'error')
            return render_template('registro.html', **get_theme_config())

        user = User(
            username=username,
            email=email,
            password_hash=generate_password_hash(password),
            role='alumno',
            nombre=nombre,
            apellidos=apellidos
        )
        db.session.add(user)
        db.session.commit()
        flash('Registro exitoso. Ya puedes iniciar sesión.', 'success')
        return redirect(url_for('public_login'))
    tc = get_theme_config()
    return render_template('registro.html', **tc)

@app.route('/logout')
@login_required
def public_logout():
    logout_user()
    return redirect(url_for('public_index'))

def redirect_user_by_role():
    if current_user.role == 'admin':
        return redirect(url_for('admin_dashboard'))
    elif current_user.role == 'instructor':
        return redirect(url_for('instructor_dashboard'))
    else:
        return redirect(url_for('alumno_dashboard'))

# ==================== ALUMNO ROUTES ====================

@app.route('/alumno')
@login_required
def alumno_dashboard():
    if current_user.role not in ['alumno', 'admin']:
        return redirect_user_by_role()
    inscripciones = Inscripcion.query.filter_by(alumno_id=current_user.id).all()
    cursos_activos = [i.curso for i in inscripciones if not i.completado]
    cursos_completados = [i for i in inscripciones if i.completado]
    proximas_clases = Clase.query.filter(
        Clase.tipo == 'vivo',
        Clase.fecha_programada >= datetime.utcnow()
    ).join(Curso, Clase.curso_id == Curso.id).join(
        Inscripcion, Inscripcion.curso_id == Curso.id
    ).filter(
        Inscripcion.alumno_id == current_user.id
    ).order_by(Clase.fecha_programada).limit(5).all()
    certificados = Certificado.query.filter_by(alumno_id=current_user.id).all()
    mensajes_no_leidos = Mensaje.query.filter_by(destinatario_id=current_user.id, leido=False).count()
    territorial = get_territorial_context(current_user)
    return render_template('alumno/dashboard.html',
                         inscripciones=inscripciones,
                         cursos_activos=cursos_activos,
                         cursos_completados=cursos_completados,
                         proximas_clases=proximas_clases,
                         certificados=certificados,
                         mensajes_no_leidos=mensajes_no_leidos,
                         territorial=territorial,
                         **get_theme_config())

@app.route('/alumno/mis-cursos')
@login_required
def alumno_cursos():
    inscripciones = Inscripcion.query.filter_by(alumno_id=current_user.id).all()
    return render_template('alumno/mis_cursos.html', inscripciones=inscripciones, **get_theme_config())

@app.route('/alumno/clases-vivo')
@login_required
def alumno_clases_vivo():
    inscripciones = Inscripcion.query.filter_by(alumno_id=current_user.id).all()
    curso_ids = [i.curso_id for i in inscripciones]
    clases = Clase.query.filter(Clase.curso_id.in_(curso_ids), Clase.tipo == 'vivo').order_by(Clase.fecha_programada.desc()).all()
    return render_template('alumno/clases_vivo.html', clases=clases, **get_theme_config())

@app.route('/alumno/clases-grabadas')
@login_required
def alumno_clases_grabadas():
    inscripciones = Inscripcion.query.filter_by(alumno_id=current_user.id).all()
    curso_ids = [i.curso_id for i in inscripciones]
    clases = Clase.query.filter(Clase.curso_id.in_(curso_ids), Clase.tipo == 'grabada').order_by(Clase.fecha_creacion.desc()).all()
    return render_template('alumno/clases_grabadas.html', clases=clases, **get_theme_config())

@app.route('/alumno/examenes')
@login_required
def alumno_examenes():
    inscripciones = Inscripcion.query.filter_by(alumno_id=current_user.id).all()
    curso_ids = [i.curso_id for i in inscripciones]
    examenes = Examen.query.filter(Examen.curso_id.in_(curso_ids)).all()
    intentos = IntentoExamen.query.filter_by(alumno_id=current_user.id).all()
    intentos_dict = {i.examen_id: i for i in intentos}
    return render_template('alumno/examenes.html', examenes=examenes, intentos=intentos_dict, **get_theme_config())

@app.route('/alumno/examen/<int:examen_id>')
@login_required
def alumno_realizar_examen(examen_id):
    examen = Examen.query.get_or_404(examen_id)
    return render_template('alumno/realizar_examen.html', examen=examen, **get_theme_config())

@app.route('/alumno/examen/<int:examen_id>/enviar', methods=['POST'])
@login_required
def alumno_enviar_examen(examen_id):
    examen = Examen.query.get_or_404(examen_id)
    preguntas = Pregunta.query.filter_by(examen_id=examen_id).all()
    correctas = 0
    respuestas = {}
    for p in preguntas:
        respuesta = request.form.get(f'pregunta_{p.id}')
        respuestas[str(p.id)] = respuesta
        if respuesta and int(respuesta) == p.respuesta_correcta:
            correctas += 1
    calificacion = (correctas / len(preguntas)) * 10 if preguntas else 0
    intento = IntentoExamen(
        alumno_id=current_user.id,
        examen_id=examen_id,
        calificacion=calificacion,
        aprobado=calificacion >= examen.calificacion_minima,
        respuestas=respuestas
    )
    db.session.add(intento)

    if calificacion >= examen.calificacion_minima:
        insc = Inscripcion.query.filter_by(alumno_id=current_user.id, curso_id=examen.curso_id).first()
        if insc:
            insc.progreso = min(insc.progreso + 20, 100)
            if insc.progreso >= 100:
                insc.completado = True
                insc.calificacion_final = calificacion
                cert_existente = Certificado.query.filter_by(alumno_id=current_user.id, curso_id=examen.curso_id).first()
                if not cert_existente:
                    certificado = Certificado(
                        folio=f'ENCL-{current_user.id:04d}-{examen.curso_id:04d}',
                        alumno_id=current_user.id,
                        curso_id=examen.curso_id,
                        instructor_id=examen.curso.instructor_id,
                        codigo_qr=f'https://encl.edu.mx/validar/ENCL-{current_user.id:04d}-{examen.curso_id:04d}'
                    )
                    db.session.add(certificado)
    db.session.commit()
    flash(f'Examen completado. Calificación: {calificacion:.1f}/10', 'success')
    return redirect(url_for('alumno_examenes'))

@app.route('/alumno/certificados')
@login_required
def alumno_certificados():
    certificados = Certificado.query.filter_by(alumno_id=current_user.id).all()
    return render_template('alumno/certificados.html', certificados=certificados, **get_theme_config())

@app.route('/alumno/material')
@login_required
def alumno_material():
    inscripciones = Inscripcion.query.filter_by(alumno_id=current_user.id).all()
    curso_ids = [i.curso_id for i in inscripciones]
    tareas = Tarea.query.filter(Tarea.curso_id.in_(curso_ids)).all()
    entregas = EntregaTarea.query.filter_by(alumno_id=current_user.id).all()
    entregas_dict = {e.tarea_id: e for e in entregas}
    return render_template('alumno/material.html', tareas=tareas, entregas=entregas_dict, **get_theme_config())

@app.route('/alumno/calendario')
@login_required
def alumno_calendario():
    inscripciones = Inscripcion.query.filter_by(alumno_id=current_user.id).all()
    curso_ids = [i.curso_id for i in inscripciones]
    clases = Clase.query.filter(Clase.curso_id.in_(curso_ids), Clase.fecha_programada.isnot(None)).order_by(Clase.fecha_programada).all()
    return render_template('alumno/calendario.html', clases=clases, **get_theme_config())

@app.route('/alumno/mensajes')
@login_required
def alumno_mensajes():
    mensajes = Mensaje.query.filter(
        (Mensaje.destinatario_id == current_user.id) |
        (Mensaje.remitente_id == current_user.id)
    ).order_by(Mensaje.fecha_envio.desc()).all()
    return render_template('alumno/mensajes.html', mensajes=mensajes, **get_theme_config())

@app.route('/alumno/enviar-mensaje', methods=['POST'])
@login_required
def alumno_enviar_mensaje():
    destinatario_id = request.form.get('destinatario_id')
    asunto = request.form.get('asunto')
    contenido = request.form.get('contenido')
    mensaje = Mensaje(
        remitente_id=current_user.id,
        destinatario_id=destinatario_id or current_user.id,
        asunto=asunto,
        contenido=contenido
    )
    db.session.add(mensaje)
    db.session.commit()
    flash('Mensaje enviado', 'success')
    return redirect(url_for('alumno_mensajes'))

@app.route('/alumno/leer-mensaje/<int:mensaje_id>')
@login_required
def alumno_leer_mensaje(mensaje_id):
    mensaje = Mensaje.query.get_or_404(mensaje_id)
    mensaje.leido = True
    db.session.commit()
    return jsonify({'status': 'ok'})

@app.route('/alumno/inscribir/<int:curso_id>')
@login_required
def alumno_inscribir(curso_id):
    existente = Inscripcion.query.filter_by(alumno_id=current_user.id, curso_id=curso_id).first()
    if not existente:
        insc = Inscripcion(alumno_id=current_user.id, curso_id=curso_id)
        db.session.add(insc)
        db.session.commit()
        flash('Inscripción exitosa', 'success')
    else:
        flash('Ya estás inscrito en este curso', 'info')
    return redirect(url_for('alumno_cursos'))

@app.route('/alumno/perfil')
@login_required
def alumno_perfil():
    territorial = get_territorial_context(current_user)
    return render_template('alumno/perfil.html', territorial=territorial, **get_theme_config())

# ==================== INSTRUCTOR ROUTES ====================

@app.route('/instructor')
@login_required
@instructor_required
def instructor_dashboard():
    cursos = Curso.query.filter_by(instructor_id=current_user.id).all()
    curso_ids = [c.id for c in cursos]
    total_alumnos = Inscripcion.query.filter(Inscripcion.curso_id.in_(curso_ids)).count() if curso_ids else 0
    clases_proximas = Clase.query.filter(
        Clase.curso_id.in_(curso_ids),
        Clase.tipo == 'vivo',
        Clase.fecha_programada >= datetime.utcnow()
    ).order_by(Clase.fecha_programada).limit(5).all() if curso_ids else []
    return render_template('instructor/dashboard.html', cursos=cursos,
                         total_alumnos=total_alumnos, clases_proximas=clases_proximas,
                         **get_theme_config())

@app.route('/instructor/cursos')
@login_required
@instructor_required
def instructor_cursos():
    cursos = Curso.query.filter_by(instructor_id=current_user.id).all()
    return render_template('instructor/cursos.html', cursos=cursos, **get_theme_config())

@app.route('/instructor/curso/<int:curso_id>')
@login_required
@instructor_required
def instructor_curso_detalle(curso_id):
    curso = Curso.query.get_or_404(curso_id)
    if curso.instructor_id != current_user.id and current_user.role != 'admin':
        flash('Acceso no autorizado', 'error')
        return redirect(url_for('instructor_dashboard'))
    inscripciones = Inscripcion.query.filter_by(curso_id=curso_id).all()
    clases = Clase.query.filter_by(curso_id=curso_id).order_by(Clase.fecha_creacion).all()
    examenes = Examen.query.filter_by(curso_id=curso_id).all()
    horarios = Horario.query.filter_by(curso_id=curso_id, activo=True).all()
    enlaces = EnlaceExterno.query.filter_by(curso_id=curso_id, activo=True).all()
    grupos = Grupo.query.all()
    asistencias = {a.clase_id: {a.alumno_id: a.presente for a in Asistencia.query.filter(Asistencia.clase_id.in_([c.id for c in clases])).all()} for c in clases}
    return render_template('instructor/curso_detalle.html', curso=curso,
                         inscripciones=inscripciones, clases=clases, examenes=examenes,
                         horarios=horarios, enlaces=enlaces, grupos=grupos,
                         asistencias=asistencias,
                         **get_theme_config())

@app.route('/instructor/clase/nueva', methods=['POST'])
@login_required
@instructor_required
def instructor_nueva_clase():
    import os as fmod
    curso_id = request.form.get('curso_id')
    titulo = request.form.get('titulo')
    tipo = request.form.get('tipo', 'grabada')
    url_reunion = request.form.get('url_reunion')
    descripcion = request.form.get('descripcion')
    fecha_str = request.form.get('fecha_programada')
    url_video = ''
    archivo = request.files.get('archivo')
    if archivo and archivo.filename:
        fname = f'mat_{int(datetime.utcnow().timestamp())}_{archivo.filename}'
        upload_dir = app.config['UPLOAD_FOLDER']
        fmod.makedirs(upload_dir, exist_ok=True)
        archivo.save(fmod.path.join(upload_dir, fname))
        url_video = f'/uploads/{fname}'

    clase = Clase(
        curso_id=curso_id,
        titulo=titulo,
        tipo=tipo,
        descripcion=descripcion,
        url_reunion=url_reunion,
        url_video=url_video,
        fecha_programada=datetime.strptime(fecha_str, '%Y-%m-%dT%H:%M') if fecha_str else None
    )
    db.session.add(clase)
    db.session.commit()

    if url_video:
        mat = MaterialClase(clase_id=clase.id, titulo='Material de clase', tipo='video', archivo_url=url_video)
        db.session.add(mat)
        db.session.commit()

    flash('Clase creada exitosamente', 'success')
    return redirect(url_for('instructor_curso_detalle', curso_id=curso_id))

@app.route('/instructor/examen/crear', methods=['POST'])
@login_required
@instructor_required
def instructor_crear_examen():
    curso_id = request.form.get('curso_id')
    curso = Curso.query.get_or_404(curso_id)
    if curso.instructor_id != current_user.id and current_user.role != 'admin':
        flash('Acceso no autorizado', 'error')
        return redirect(url_for('instructor_dashboard'))
    examen = Examen(
        curso_id=curso_id,
        titulo=request.form.get('titulo'),
        descripcion=request.form.get('descripcion'),
        tiempo_limite_minutos=int(request.form.get('tiempo_limite', 30)),
        calificacion_minima=float(request.form.get('calificacion_minima', 6))
    )
    db.session.add(examen)
    db.session.commit()
    for i in range(1, 11):
        texto = request.form.get(f'pregunta_{i}')
        if texto:
            opciones = [
                request.form.get(f'opcion_{i}_0'),
                request.form.get(f'opcion_{i}_1'),
                request.form.get(f'opcion_{i}_2'),
                request.form.get(f'opcion_{i}_3')
            ]
            correcta = int(request.form.get(f'correcta_{i}', 0))
            pregunta = Pregunta(
                examen_id=examen.id, texto=texto,
                opciones=[o for o in opciones if o],
                respuesta_correcta=correcta
            )
            db.session.add(pregunta)
    db.session.commit()
    flash('Examen creado', 'success')
    return redirect(url_for('instructor_curso_detalle', curso_id=curso_id))

@app.route('/instructor/asistencia', methods=['POST'])
@login_required
@instructor_required
def instructor_asistencia():
    clase_id = request.form.get('clase_id')
    curso_id = request.form.get('curso_id')
    presentes = request.form.getlist('presentes')
    clase = Clase.query.get_or_404(clase_id)
    for insc in Inscripcion.query.filter_by(curso_id=curso_id).all():
        existe = Asistencia.query.filter_by(clase_id=clase_id, alumno_id=insc.alumno_id).first()
        if not existe:
            asis = Asistencia(clase_id=clase_id, alumno_id=insc.alumno_id,
                             presente=str(insc.alumno_id) in presentes,
                             fecha=datetime.utcnow())
            db.session.add(asis)
        else:
            existe.presente = str(insc.alumno_id) in presentes
    db.session.commit()
    flash('Asistencia registrada', 'success')
    return redirect(url_for('instructor_curso_detalle', curso_id=curso_id))

@app.route('/instructor/horario/crear', methods=['POST'])
@login_required
@instructor_required
def instructor_crear_horario():
    horario = Horario(
        curso_id=request.form.get('curso_id'),
        grupo_id=request.form.get('grupo_id') or None,
        dia_semana=int(request.form.get('dia_semana', 0)),
        hora_inicio=request.form.get('hora_inicio'),
        hora_fin=request.form.get('hora_fin'),
        salon=request.form.get('salon')
    )
    db.session.add(horario)
    db.session.commit()
    flash('Horario agregado', 'success')
    return redirect(url_for('instructor_curso_detalle', curso_id=horario.curso_id))

@app.route('/instructor/enlace/crear', methods=['POST'])
@login_required
@instructor_required
def instructor_crear_enlace():
    enlace = EnlaceExterno(
        curso_id=request.form.get('curso_id'),
        titulo=request.form.get('titulo'),
        url=request.form.get('url'),
        plataforma=request.form.get('plataforma', 'Zoom')
    )
    db.session.add(enlace)
    db.session.commit()
    flash('Enlace agregado', 'success')
    return redirect(url_for('instructor_curso_detalle', curso_id=enlace.curso_id))

# ==================== ADMIN ROUTES ====================

@app.route('/admin')
@login_required
@admin_required
def admin_dashboard():
    total_alumnos = User.query.filter_by(role='alumno').count()
    total_instructores = User.query.filter_by(role='instructor').count()
    total_cursos = Curso.query.count()
    total_certificados = Certificado.query.count()
    inscripciones_recientes = Inscripcion.query.order_by(Inscripcion.fecha_inscripcion.desc()).limit(10).all()
    ultimos_usuarios = User.query.order_by(User.fecha_registro.desc()).limit(10).all()

    cursos_por_categoria = db.session.query(
        Categoria.nombre, db.func.count(Curso.id)
    ).join(Curso).group_by(Categoria.nombre).all()

    inscripciones_por_mes = db.session.query(
        db.func.strftime('%m', Inscripcion.fecha_inscripcion).label('mes'),
        db.func.count(Inscripcion.id)
    ).group_by('mes').order_by('mes').all()

    return render_template('admin/dashboard.html',
                         total_alumnos=total_alumnos,
                         total_instructores=total_instructores,
                         total_cursos=total_cursos,
                         total_certificados=total_certificados,
                         inscripciones_recientes=inscripciones_recientes,
                         ultimos_usuarios=ultimos_usuarios,
                         cursos_por_categoria=cursos_por_categoria,
                         inscripciones_por_mes=inscripciones_por_mes,
                         **get_theme_config())

@app.route('/admin/usuarios')
@login_required
@admin_required
def admin_usuarios():
    usuarios = User.query.order_by(User.fecha_registro.desc()).all()
    estados = Estado.query.all()
    grupos = Grupo.query.all()
    return render_template('admin/usuarios.html', usuarios=usuarios, estados=estados, grupos=grupos, **get_theme_config())

@app.route('/admin/usuarios/crear', methods=['POST'])
@login_required
@admin_required
def admin_crear_usuario():
    username = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')
    nombre = request.form.get('nombre')
    apellidos = request.form.get('apellidos')
    role = request.form.get('role', 'alumno')
    estado_id = request.form.get('estado_id')
    grupo_id = request.form.get('grupo_id')

    if User.query.filter_by(username=username).first():
        flash('El usuario ya existe', 'error')
        return redirect(url_for('admin_usuarios'))

    user = User(
        username=username,
        email=email,
        password_hash=generate_password_hash(password),
        role=role,
        nombre=nombre,
        apellidos=apellidos,
        estado_id=int(estado_id) if estado_id else None,
        grupo_id=int(grupo_id) if grupo_id else None
    )
    db.session.add(user)
    db.session.commit()
    flash('Usuario creado exitosamente', 'success')
    return redirect(url_for('admin_usuarios'))

@app.route('/admin/usuarios/editar/<int:user_id>', methods=['POST'])
@login_required
@admin_required
def admin_editar_usuario(user_id):
    user = User.query.get_or_404(user_id)
    user.nombre = request.form.get('nombre', user.nombre)
    user.apellidos = request.form.get('apellidos', user.apellidos)
    user.email = request.form.get('email', user.email)
    user.role = request.form.get('role', user.role)
    user.activo = request.form.get('activo', '1') == '1'
    user.estado_id = request.form.get('estado_id', user.estado_id)
    user.grupo_id = request.form.get('grupo_id', user.grupo_id)
    if request.form.get('password'):
        user.password_hash = generate_password_hash(request.form.get('password'))
    db.session.commit()
    flash('Usuario actualizado', 'success')
    return redirect(url_for('admin_usuarios'))

@app.route('/admin/usuarios/eliminar/<int:user_id>')
@login_required
@admin_required
def admin_eliminar_usuario(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    flash('Usuario eliminado', 'success')
    return redirect(url_for('admin_usuarios'))

@app.route('/admin/cursos')
@login_required
@admin_required
def admin_cursos():
    cursos = Curso.query.order_by(Curso.fecha_creacion.desc()).all()
    categorias = Categoria.query.all()
    instructores = User.query.filter_by(role='instructor', activo=True).all()
    patrocinadores = Patrocinador.query.filter_by(activo=True).all()
    return render_template('admin/cursos.html', cursos=cursos, categorias=categorias, instructores=instructores, patrocinadores=patrocinadores, **get_theme_config())

@app.route('/admin/cursos/crear', methods=['POST'])
@login_required
@admin_required
def admin_crear_curso():
    titulo = request.form.get('titulo')
    slug = titulo.lower().replace(' ', '-').replace('á','a').replace('é','e').replace('í','i').replace('ó','o').replace('ú','u').replace('ñ','n')
    curso = Curso(
        titulo=titulo,
        slug=slug,
        descripcion_corta=request.form.get('descripcion_corta'),
        descripcion_larga=request.form.get('descripcion_larga'),
        categoria_id=request.form.get('categoria_id'),
        instructor_id=request.form.get('instructor_id'),
        patrocinador_id=request.form.get('patrocinador_id') or None,
        nivel=request.form.get('nivel', 'Principiante'),
        duracion_horas=float(request.form.get('duracion_horas', 0)),
        precio=float(request.form.get('precio', 0))
    )
    db.session.add(curso)
    db.session.commit()
    flash('Curso creado exitosamente', 'success')
    return redirect(url_for('admin_cursos'))

@app.route('/admin/cursos/editar/<int:curso_id>', methods=['POST'])
@login_required
@admin_required
def admin_editar_curso(curso_id):
    curso = Curso.query.get_or_404(curso_id)
    curso.titulo = request.form.get('titulo', curso.titulo)
    curso.descripcion_corta = request.form.get('descripcion_corta', curso.descripcion_corta)
    curso.descripcion_larga = request.form.get('descripcion_larga', curso.descripcion_larga)
    curso.categoria_id = request.form.get('categoria_id', curso.categoria_id)
    curso.instructor_id = request.form.get('instructor_id', curso.instructor_id)
    curso.patrocinador_id = request.form.get('patrocinador_id') or None
    curso.nivel = request.form.get('nivel', curso.nivel)
    curso.precio = float(request.form.get('precio', curso.precio))
    curso.activo = request.form.get('activo', '1') == '1'
    db.session.commit()
    flash('Curso actualizado', 'success')
    return redirect(url_for('admin_cursos'))

@app.route('/admin/cursos/eliminar/<int:curso_id>')
@login_required
@admin_required
def admin_eliminar_curso(curso_id):
    curso = Curso.query.get_or_404(curso_id)
    db.session.delete(curso)
    db.session.commit()
    flash('Curso eliminado', 'success')
    return redirect(url_for('admin_cursos'))

@app.route('/admin/categorias')
@login_required
@admin_required
def admin_categorias():
    categorias = Categoria.query.all()
    return render_template('admin/categorias.html', categorias=categorias, **get_theme_config())

@app.route('/admin/categorias/crear', methods=['POST'])
@login_required
@admin_required
def admin_crear_categoria():
    cat = Categoria(
        nombre=request.form.get('nombre'),
        descripcion=request.form.get('descripcion'),
        icono=request.form.get('icono', 'fa-book')
    )
    db.session.add(cat)
    db.session.commit()
    flash('Categoría creada', 'success')
    return redirect(url_for('admin_categorias'))

@app.route('/admin/categorias/eliminar/<int:cat_id>')
@login_required
@admin_required
def admin_eliminar_categoria(cat_id):
    cat = Categoria.query.get_or_404(cat_id)
    db.session.delete(cat)
    db.session.commit()
    flash('Categoría eliminada', 'success')
    return redirect(url_for('admin_categorias'))

@app.route('/admin/territorial')
@login_required
@admin_required
def admin_territorial():
    estados = Estado.query.all()
    return render_template('admin/territorial.html', estados=estados, **get_theme_config())

@app.route('/admin/territorial/crear-estado', methods=['POST'])
@login_required
@admin_required
def admin_crear_estado():
    estado = Estado(nombre=request.form.get('nombre'))
    db.session.add(estado)
    db.session.commit()
    flash('Estado creado', 'success')
    return redirect(url_for('admin_territorial'))

@app.route('/admin/territorial/crear-municipio', methods=['POST'])
@login_required
@admin_required
def admin_crear_municipio():
    muni = Municipio(nombre=request.form.get('nombre'), estado_id=request.form.get('estado_id'))
    db.session.add(muni)
    db.session.commit()
    flash('Municipio creado', 'success')
    return redirect(url_for('admin_territorial'))

@app.route('/admin/territorial/crear-distrito', methods=['POST'])
@login_required
@admin_required
def admin_crear_distrito():
    dist = Distrito(nombre=request.form.get('nombre'), codigo=request.form.get('codigo'), municipio_id=request.form.get('municipio_id'))
    db.session.add(dist)
    db.session.commit()
    flash('Distrito creado', 'success')
    return redirect(url_for('admin_territorial'))

@app.route('/admin/territorial/crear-grupo', methods=['POST'])
@login_required
@admin_required
def admin_crear_grupo():
    grupo = Grupo(nombre=request.form.get('nombre'), codigo=request.form.get('codigo'), distrito_id=request.form.get('distrito_id'))
    db.session.add(grupo)
    db.session.commit()
    flash('Grupo creado', 'success')
    return redirect(url_for('admin_territorial'))

@app.route('/admin/api/municipios/<int:estado_id>')
@login_required
@admin_required
def admin_api_municipios(estado_id):
    municipios = Municipio.query.filter_by(estado_id=estado_id).all()
    return jsonify([{'id': m.id, 'nombre': m.nombre} for m in municipios])

@app.route('/admin/api/distritos/<int:municipio_id>')
@login_required
@admin_required
def admin_api_distritos(municipio_id):
    distritos = Distrito.query.filter_by(municipio_id=municipio_id).all()
    return jsonify([{'id': d.id, 'nombre': d.nombre} for d in distritos])

@app.route('/admin/api/grupos/<int:distrito_id>')
@login_required
@admin_required
def admin_api_grupos(distrito_id):
    grupos = Grupo.query.filter_by(distrito_id=distrito_id).all()
    return jsonify([{'id': g.id, 'nombre': g.nombre} for g in grupos])

@app.route('/admin/patrocinadores')
@login_required
@admin_required
def admin_patrocinadores():
    patrocinadores = Patrocinador.query.all()
    return render_template('admin/patrocinadores.html', patrocinadores=patrocinadores, **get_theme_config())

@app.route('/admin/patrocinadores/crear', methods=['POST'])
@login_required
@admin_required
def admin_crear_patrocinador():
    import os as fmod
    logo_url = ''
    archivo = request.files.get('logo')
    if archivo and archivo.filename:
        fname = f'pat_{int(datetime.utcnow().timestamp())}_{archivo.filename}'
        upload_dir = app.config['UPLOAD_FOLDER']
        fmod.makedirs(upload_dir, exist_ok=True)
        archivo.save(fmod.path.join(upload_dir, fname))
        logo_url = f'/uploads/{fname}'
    pat = Patrocinador(
        nombre=request.form.get('nombre'),
        logo=logo_url,
        cargo=request.form.get('cargo'),
        lema=request.form.get('lema')
    )
    db.session.add(pat)
    db.session.commit()
    flash('Patrocinador creado', 'success')
    return redirect(url_for('admin_patrocinadores'))

@app.route('/admin/patrocinadores/editar/<int:pat_id>', methods=['POST'])
@login_required
@admin_required
def admin_editar_patrocinador(pat_id):
    import os as fmod
    pat = Patrocinador.query.get_or_404(pat_id)
    pat.nombre = request.form.get('nombre', pat.nombre)
    pat.cargo = request.form.get('cargo', pat.cargo)
    pat.lema = request.form.get('lema', pat.lema)
    pat.activo = request.form.get('activo', '1') == '1'
    archivo = request.files.get('logo')
    if archivo and archivo.filename:
        fname = f'pat_{int(datetime.utcnow().timestamp())}_{archivo.filename}'
        upload_dir = app.config['UPLOAD_FOLDER']
        fmod.makedirs(upload_dir, exist_ok=True)
        archivo.save(fmod.path.join(upload_dir, fname))
        pat.logo = f'/uploads/{fname}'
    db.session.commit()
    flash('Patrocinador actualizado', 'success')
    return redirect(url_for('admin_patrocinadores'))

@app.route('/admin/patrocinadores/eliminar/<int:pat_id>')
@login_required
@admin_required
def admin_eliminar_patrocinador(pat_id):
    pat = Patrocinador.query.get_or_404(pat_id)
    db.session.delete(pat)
    db.session.commit()
    flash('Patrocinador eliminado', 'success')
    return redirect(url_for('admin_patrocinadores'))

@app.route('/admin/certificados')
@login_required
@admin_required
def admin_certificados():
    certificados = Certificado.query.order_by(Certificado.fecha_emision.desc()).all()
    return render_template('admin/certificados.html', certificados=certificados, **get_theme_config())

@app.route('/admin/validar-certificado/<folio>')
def admin_validar_certificado(folio):
    certificado = Certificado.query.filter_by(folio=folio).first()
    if certificado and certificado.valido:
        return jsonify({'valido': True, 'alumno': f'{certificado.alumno.nombre} {certificado.alumno.apellidos}',
                       'curso': certificado.curso.titulo, 'fecha': certificado.fecha_emision.strftime('%d/%m/%Y')})
    return jsonify({'valido': False})

@app.route('/admin/examenes')
@login_required
@admin_required
def admin_examenes():
    examenes = Examen.query.order_by(Examen.fecha_creacion.desc()).all()
    cursos = Curso.query.all()
    return render_template('admin/examenes.html', examenes=examenes, cursos=cursos, **get_theme_config())

@app.route('/admin/examenes/crear', methods=['POST'])
@login_required
@admin_required
def admin_crear_examen():
    examen = Examen(
        curso_id=request.form.get('curso_id'),
        titulo=request.form.get('titulo'),
        descripcion=request.form.get('descripcion'),
        tiempo_limite_minutos=int(request.form.get('tiempo_limite', 30)),
        calificacion_minima=float(request.form.get('calificacion_minima', 6))
    )
    db.session.add(examen)
    db.session.commit()

    for i in range(1, 11):
        texto = request.form.get(f'pregunta_{i}')
        if texto:
            opciones = [
                request.form.get(f'opcion_{i}_0'),
                request.form.get(f'opcion_{i}_1'),
                request.form.get(f'opcion_{i}_2'),
                request.form.get(f'opcion_{i}_3')
            ]
            correcta = int(request.form.get(f'correcta_{i}', 0))
            pregunta = Pregunta(
                examen_id=examen.id,
                texto=texto,
                opciones=[o for o in opciones if o],
                respuesta_correcta=correcta
            )
            db.session.add(pregunta)
    db.session.commit()
    flash('Examen creado', 'success')
    return redirect(url_for('admin_examenes'))

@app.route('/admin/reportes')
@login_required
@admin_required
def admin_reportes():
    return render_template('admin/reportes.html', **get_theme_config())

@app.route('/admin/cms')
@login_required
@admin_required
def admin_cms():
    configs = Configuracion.query.all()
    return render_template('admin/cms.html', configs=configs, **get_theme_config())

@app.route('/admin/cms/guardar', methods=['POST'])
@login_required
@admin_required
def admin_cms_guardar():
    for clave, valor in request.form.items():
        conf = Configuracion.query.filter_by(clave=clave).first()
        if conf:
            conf.valor = valor
        else:
            conf = Configuracion(clave=clave, valor=valor, tipo='texto')
            db.session.add(conf)
    db.session.commit()
    flash('Configuración guardada exitosamente', 'success')
    return redirect(url_for('admin_cms'))

@app.route('/admin/inscripciones')
@login_required
@admin_required
def admin_inscripciones():
    inscripciones = Inscripcion.query.order_by(Inscripcion.fecha_inscripcion.desc()).all()
    return render_template('admin/inscripciones.html', inscripciones=inscripciones, **get_theme_config())

@app.route('/admin/pagos')
@login_required
@admin_required
def admin_pagos():
    pagos = Pago.query.order_by(Pago.fecha_pago.desc()).all()
    alumnos = User.query.filter_by(role='alumno').all()
    cursos = Curso.query.all()
    total_ingresos = sum(p.monto for p in pagos if p.verificado)
    pendientes = sum(1 for p in pagos if not p.verificado)
    completados = sum(1 for p in pagos if p.verificado)
    ingresos_mes = sum(p.monto for p in pagos if p.verificado and p.fecha_pago and p.fecha_pago.month == datetime.utcnow().month)
    return render_template('admin/pagos.html', pagos=pagos, alumnos=alumnos, cursos=cursos,
                         total_ingresos=total_ingresos, pendientes=pendientes,
                         completados=completados, ingresos_mes=ingresos_mes, **get_theme_config())

@app.route('/admin/pagos/crear', methods=['POST'])
@login_required
@admin_required
def admin_crear_pago():
    pago = Pago(
        alumno_id=request.form.get('alumno_id'),
        curso_id=request.form.get('curso_id'),
        monto=float(request.form.get('monto', 0)),
        concepto=request.form.get('concepto'),
        metodo_pago=request.form.get('metodo_pago', 'Efectivo'),
        referencia=request.form.get('referencia'),
        notas=request.form.get('notas')
    )
    db.session.add(pago)
    db.session.commit()
    flash('Pago registrado exitosamente', 'success')
    return redirect(url_for('admin_pagos'))

@app.route('/admin/pagos/verificar/<int:pago_id>')
@login_required
@admin_required
def admin_verificar_pago(pago_id):
    pago = Pago.query.get_or_404(pago_id)
    pago.verificado = True
    pago.verificado_por = current_user.id
    pago.fecha_verificacion = datetime.utcnow()
    alumno = User.query.get(pago.alumno_id)
    if alumno:
        alumno.activo = True
    db.session.commit()
    flash('Pago verificado y alumno activado', 'success')
    return redirect(url_for('admin_pagos'))

@app.route('/admin/pagos/eliminar/<int:pago_id>')
@login_required
@admin_required
def admin_eliminar_pago(pago_id):
    pago = Pago.query.get_or_404(pago_id)
    db.session.delete(pago)
    db.session.commit()
    flash('Pago eliminado', 'success')
    return redirect(url_for('admin_pagos'))

@app.route('/admin/usuario/toggle/<int:user_id>')
@login_required
@admin_required
def admin_toggle_usuario(user_id):
    user = User.query.get_or_404(user_id)
    user.activo = not user.activo
    db.session.commit()
    estado = 'activado' if user.activo else 'desactivado'
    flash(f'Usuario {user.nombre} {user.apellidos} ha sido {estado}', 'success')
    return redirect(url_for('admin_usuarios'))

@app.route('/admin/imagenes')
@login_required
@admin_required
def admin_imagenes():
    imagenes = ImagenSite.query.order_by(ImagenSite.seccion, ImagenSite.orden).all()
    secciones = db.session.query(ImagenSite.seccion).distinct().all()
    secciones = [s[0] for s in secciones]
    return render_template('admin/imagenes.html', imagenes=imagenes, secciones=secciones, **get_theme_config())

@app.route('/admin/imagenes/crear', methods=['POST'])
@login_required
@admin_required
def admin_crear_imagen():
    import os as fmod
    seccion = request.form.get('seccion')
    titulo = request.form.get('titulo')
    descripcion = request.form.get('descripcion')
    archivo = request.files.get('archivo')
    url = ''
    if archivo and archivo.filename:
        fname = f'img_{int(datetime.utcnow().timestamp())}_{archivo.filename}'
        upload_dir = app.config['UPLOAD_FOLDER']
        fmod.makedirs(upload_dir, exist_ok=True)
        archivo.save(fmod.path.join(upload_dir, fname))
        url = f'/uploads/{fname}'
    img = ImagenSite(seccion=seccion, titulo=titulo, descripcion=descripcion, url=url, orden=int(request.form.get('orden', 0)))
    db.session.add(img)
    db.session.commit()
    flash('Imagen agregada', 'success')
    return redirect(url_for('admin_imagenes'))

@app.route('/admin/imagenes/eliminar/<int:img_id>')
@login_required
@admin_required
def admin_eliminar_imagen(img_id):
    img = ImagenSite.query.get_or_404(img_id)
    db.session.delete(img)
    db.session.commit()
    flash('Imagen eliminada', 'success')
    return redirect(url_for('admin_imagenes'))

@app.route('/admin/favicon', methods=['POST'])
@login_required
@superadmin_required
def admin_subir_favicon():
    archivo = request.files.get('favicon')
    tipo = request.form.get('tipo', 'favicon_url')
    if archivo and archivo.filename:
        import os as fmod
        ext = archivo.filename.rsplit('.', 1)[-1].lower()
        prefix = tipo.replace('_url', '').replace('_image', '')
        fname = f'{prefix}_{int(datetime.utcnow().timestamp())}.{ext}'
        upload_dir = app.config['UPLOAD_FOLDER']
        fmod.makedirs(upload_dir, exist_ok=True)
        archivo.save(fmod.path.join(upload_dir, fname))
        url = f'/uploads/{fname}'
        clave = tipo if tipo.startswith('site_') or tipo.startswith('hero_') else 'favicon_url'
        conf = Configuracion.query.filter_by(clave=clave).first()
        if conf:
            conf.valor = url
        else:
            conf = Configuracion(clave=clave, valor=url, tipo='texto')
            db.session.add(conf)
        db.session.commit()
        flash('Imagen actualizada', 'success')
    return redirect(url_for('admin_cms'))

@app.route('/admin/imagenes/toggle/<int:img_id>')
@login_required
@admin_required
def admin_toggle_imagen(img_id):
    img = ImagenSite.query.get_or_404(img_id)
    img.activo = not img.activo
    db.session.commit()
    return redirect(url_for('admin_imagenes'))

@app.route('/admin/banners')
@login_required
@superadmin_required
def admin_banners():
    banners = Banner.query.order_by(Banner.orden).all()
    return render_template('admin/banners.html', banners=banners, **get_theme_config())

@app.route('/admin/banners/crear', methods=['POST'])
@login_required
@superadmin_required
def admin_crear_banner():
    import os as fmod
    titulo = request.form.get('titulo')
    subtitulo = request.form.get('subtitulo')
    link = request.form.get('link')
    tiempo_ms = int(request.form.get('tiempo_ms', 5000))
    archivo = request.files.get('imagen')
    url = request.form.get('imagen_url', '')
    if not url and archivo and archivo.filename:
        fname = f'banner_{int(datetime.utcnow().timestamp())}_{archivo.filename}'
        upload_dir = app.config['UPLOAD_FOLDER']
        fmod.makedirs(upload_dir, exist_ok=True)
        archivo.save(fmod.path.join(upload_dir, fname))
        url = f'/uploads/{fname}'
    max_orden = db.session.query(db.func.max(Banner.orden)).scalar() or 0
    banner = Banner(titulo=titulo, subtitulo=subtitulo, imagen=url, link=link, tiempo_ms=tiempo_ms, orden=max_orden + 1)
    db.session.add(banner)
    db.session.commit()
    flash('Banner creado exitosamente', 'success')
    return redirect(url_for('admin_banners'))

@app.route('/admin/banners/editar/<int:banner_id>', methods=['POST'])
@login_required
@superadmin_required
def admin_editar_banner(banner_id):
    import os as fmod
    banner = Banner.query.get_or_404(banner_id)
    banner.titulo = request.form.get('titulo', banner.titulo)
    banner.subtitulo = request.form.get('subtitulo', banner.subtitulo)
    banner.link = request.form.get('link', banner.link)
    banner.tiempo_ms = int(request.form.get('tiempo_ms', banner.tiempo_ms))
    banner.activo = request.form.get('activo', '1') == '1'
    archivo = request.files.get('imagen')
    if archivo and archivo.filename:
        fname = f'banner_{int(datetime.utcnow().timestamp())}_{archivo.filename}'
        upload_dir = app.config['UPLOAD_FOLDER']
        fmod.makedirs(upload_dir, exist_ok=True)
        archivo.save(fmod.path.join(upload_dir, fname))
        banner.imagen = f'/uploads/{fname}'
    db.session.commit()
    flash('Banner actualizado', 'success')
    return redirect(url_for('admin_banners'))

@app.route('/admin/banners/eliminar/<int:banner_id>')
@login_required
@superadmin_required
def admin_eliminar_banner(banner_id):
    banner = Banner.query.get_or_404(banner_id)
    db.session.delete(banner)
    db.session.commit()
    flash('Banner eliminado', 'success')
    return redirect(url_for('admin_banners'))

@app.route('/admin/banners/toggle/<int:banner_id>')
@login_required
@superadmin_required
def admin_toggle_banner(banner_id):
    banner = Banner.query.get_or_404(banner_id)
    banner.activo = not banner.activo
    db.session.commit()
    return redirect(url_for('admin_banners'))

@app.route('/admin/banners/reordenar', methods=['POST'])
@login_required
@superadmin_required
def admin_reordenar_banners():
    ordenes = request.json.get('ordenes', [])
    for item in ordenes:
        banner = Banner.query.get(item['id'])
        if banner:
            banner.orden = item['orden']
    db.session.commit()
    return jsonify({'status': 'ok'})

# ==================== STATIC FILES ====================

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

# ==================== ERROR HANDLERS ====================

@app.errorhandler(404)
def not_found(e):
    return render_template('404.html', **get_theme_config()), 404

@app.errorhandler(500)
def server_error(e):
    return render_template('500.html', **get_theme_config()), 500

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    import webbrowser
    webbrowser.open('http://127.0.0.1:5000')
    debug_mode = os.environ.get('FLASK_DEBUG', '1') == '1'
    app.run(debug=debug_mode, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
