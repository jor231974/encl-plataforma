from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime
import uuid

db = SQLAlchemy()

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='alumno')
    nombre = db.Column(db.String(200), nullable=False)
    apellidos = db.Column(db.String(200), nullable=False)
    foto = db.Column(db.String(500), default='default-user.png')
    video_bienvenida = db.Column(db.String(500))
    telefono = db.Column(db.String(20))
    direccion = db.Column(db.Text)
    fecha_nacimiento = db.Column(db.Date)
    fecha_registro = db.Column(db.DateTime, default=datetime.utcnow)
    activo = db.Column(db.Boolean, default=True)

    # Territorial
    estado_id = db.Column(db.Integer, db.ForeignKey('estado.id'))
    municipio_id = db.Column(db.Integer, db.ForeignKey('municipio.id'))
    distrito_id = db.Column(db.Integer, db.ForeignKey('distrito.id'))
    grupo_id = db.Column(db.Integer, db.ForeignKey('grupo.id'))
    nivel = db.Column(db.String(50), default='Principiante')
    progreso_general = db.Column(db.Float, default=0.0)

    estado = db.relationship('Estado', backref='usuarios')
    municipio = db.relationship('Municipio', backref='usuarios')
    distrito = db.relationship('Distrito', backref='usuarios')
    grupo = db.relationship('Grupo', backref='usuarios')

class Estado(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(200), nullable=False)
    activo = db.Column(db.Boolean, default=True)
    municipios = db.relationship('Municipio', backref='estado', lazy=True)

class Municipio(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(200), nullable=False)
    estado_id = db.Column(db.Integer, db.ForeignKey('estado.id'))
    activo = db.Column(db.Boolean, default=True)
    distritos = db.relationship('Distrito', backref='municipio', lazy=True)

class Distrito(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(200), nullable=False)
    codigo = db.Column(db.String(50))
    municipio_id = db.Column(db.Integer, db.ForeignKey('municipio.id'))
    activo = db.Column(db.Boolean, default=True)
    grupos = db.relationship('Grupo', backref='distrito', lazy=True)

class Grupo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(200), nullable=False)
    codigo = db.Column(db.String(50))
    distrito_id = db.Column(db.Integer, db.ForeignKey('distrito.id'))
    activo = db.Column(db.Boolean, default=True)

class Categoria(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(200), nullable=False)
    descripcion = db.Column(db.Text)
    icono = db.Column(db.String(100), default='fa-book')
    activo = db.Column(db.Boolean, default=True)
    cursos = db.relationship('Curso', backref='categoria', lazy=True)

class Curso(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(300), nullable=False)
    slug = db.Column(db.String(300), unique=True)
    descripcion_corta = db.Column(db.Text)
    descripcion_larga = db.Column(db.Text)
    categoria_id = db.Column(db.Integer, db.ForeignKey('categoria.id'))
    instructor_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    patrocinador_id = db.Column(db.Integer, db.ForeignKey('patrocinador.id'))
    imagen = db.Column(db.String(500), default='default-course.jpg')
    nivel = db.Column(db.String(50), default='Principiante')
    duracion_horas = db.Column(db.Float, default=0)
    precio = db.Column(db.Float, default=0)
    modalidad = db.Column(db.String(50), default='En línea')
    activo = db.Column(db.Boolean, default=True)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    tiene_certificado = db.Column(db.Boolean, default=True)
    video_presentacion = db.Column(db.String(500))
    temario = db.Column(db.JSON)

    instructor = db.relationship('User', backref='cursos_impartidos')
    patrocinador = db.relationship('Patrocinador', backref='cursos')

class Clase(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    curso_id = db.Column(db.Integer, db.ForeignKey('curso.id'))
    titulo = db.Column(db.String(300), nullable=False)
    descripcion = db.Column(db.Text)
    tipo = db.Column(db.String(20), default='grabada')
    url_video = db.Column(db.String(500))
    url_reunion = db.Column(db.String(500))
    duracion_minutos = db.Column(db.Integer, default=0)
    fecha_programada = db.Column(db.DateTime)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    activo = db.Column(db.Boolean, default=True)
    material_url = db.Column(db.String(500))

    curso = db.relationship('Curso', backref='clases')

class Inscripcion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    alumno_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    curso_id = db.Column(db.Integer, db.ForeignKey('curso.id'))
    fecha_inscripcion = db.Column(db.DateTime, default=datetime.utcnow)
    progreso = db.Column(db.Float, default=0.0)
    completado = db.Column(db.Boolean, default=False)
    calificacion_final = db.Column(db.Float)
    video_bienvenida_visto = db.Column(db.Boolean, default=False)

    alumno = db.relationship('User', backref='inscripciones')
    curso = db.relationship('Curso', backref='inscripciones')

class Examen(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    curso_id = db.Column(db.Integer, db.ForeignKey('curso.id'))
    titulo = db.Column(db.String(300), nullable=False)
    descripcion = db.Column(db.Text)
    tiempo_limite_minutos = db.Column(db.Integer, default=30)
    calificacion_minima = db.Column(db.Float, default=6.0)
    activo = db.Column(db.Boolean, default=True)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    curso = db.relationship('Curso', backref='examenes')
    preguntas = db.relationship('Pregunta', backref='examen', lazy=True)

class Pregunta(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    examen_id = db.Column(db.Integer, db.ForeignKey('examen.id'))
    texto = db.Column(db.Text, nullable=False)
    opciones = db.Column(db.JSON)
    respuesta_correcta = db.Column(db.Integer, nullable=False)

class IntentoExamen(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    alumno_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    examen_id = db.Column(db.Integer, db.ForeignKey('examen.id'))
    fecha_intento = db.Column(db.DateTime, default=datetime.utcnow)
    calificacion = db.Column(db.Float)
    aprobado = db.Column(db.Boolean)
    respuestas = db.Column(db.JSON)
    alumno = db.relationship('User', backref='intentos_examen')
    examen = db.relationship('Examen', backref='intentos')

class Certificado(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    folio = db.Column(db.String(100), unique=True, default=lambda: str(uuid.uuid4())[:8].upper())
    alumno_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    curso_id = db.Column(db.Integer, db.ForeignKey('curso.id'))
    instructor_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    fecha_emision = db.Column(db.DateTime, default=datetime.utcnow)
    codigo_qr = db.Column(db.String(500))
    valido = db.Column(db.Boolean, default=True)
    alumno = db.relationship('User', foreign_keys=[alumno_id], backref='certificados')
    curso = db.relationship('Curso', backref='certificados')
    instructor = db.relationship('User', foreign_keys=[instructor_id], backref='certificados_emitidos')

class Vacante(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(300), nullable=False)
    empresa = db.Column(db.String(200), nullable=False)
    ciudad = db.Column(db.String(200))
    descripcion = db.Column(db.Text)
    requisitos = db.Column(db.Text)
    salario = db.Column(db.String(100))
    tipo = db.Column(db.String(50))
    activo = db.Column(db.Boolean, default=True)
    fecha_publicacion = db.Column(db.DateTime, default=datetime.utcnow)

class Postulacion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    vacante_id = db.Column(db.Integer, db.ForeignKey('vacante.id'))
    alumno_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    fecha_postulacion = db.Column(db.DateTime, default=datetime.utcnow)
    estado = db.Column(db.String(50), default='Pendiente')
    vacante = db.relationship('Vacante', backref='postulaciones')
    alumno = db.relationship('User', backref='postulaciones')

class Patrocinador(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(200), nullable=False)
    logo = db.Column(db.String(500))
    foto = db.Column(db.String(500))
    cargo = db.Column(db.String(200))
    lema = db.Column(db.Text)
    mensaje = db.Column(db.Text)
    codigo_interno = db.Column(db.String(100), unique=True)
    codigo_qr = db.Column(db.String(500))
    estado_id = db.Column(db.Integer, db.ForeignKey('estado.id'))
    municipio_id = db.Column(db.Integer, db.ForeignKey('municipio.id'))
    activo = db.Column(db.Boolean, default=True)
    estado = db.relationship('Estado', backref='patrocinadores')
    municipio = db.relationship('Municipio', backref='patrocinadores')

class Mensaje(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    remitente_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    destinatario_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    asunto = db.Column(db.String(300))
    contenido = db.Column(db.Text)
    leido = db.Column(db.Boolean, default=False)
    fecha_envio = db.Column(db.DateTime, default=datetime.utcnow)
    remitente = db.relationship('User', foreign_keys=[remitente_id], backref='mensajes_enviados')
    destinatario = db.relationship('User', foreign_keys=[destinatario_id], backref='mensajes_recibidos')

class ContactoMensaje(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(200), nullable=False)
    telefono = db.Column(db.String(20))
    asunto = db.Column(db.String(200))
    mensaje = db.Column(db.Text, nullable=False)
    leido = db.Column(db.Boolean, default=False)
    fecha_envio = db.Column(db.DateTime, default=datetime.utcnow)

class Asistencia(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    clase_id = db.Column(db.Integer, db.ForeignKey('clase.id'))
    alumno_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    presente = db.Column(db.Boolean, default=False)
    fecha = db.Column(db.DateTime, default=datetime.utcnow)
    clase = db.relationship('Clase', backref='asistencias')
    alumno = db.relationship('User', backref='asistencias')

class Tarea(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    curso_id = db.Column(db.Integer, db.ForeignKey('curso.id'))
    titulo = db.Column(db.String(300), nullable=False)
    descripcion = db.Column(db.Text)
    fecha_entrega = db.Column(db.DateTime)
    archivo_url = db.Column(db.String(500))
    activo = db.Column(db.Boolean, default=True)
    curso = db.relationship('Curso', backref='tareas')

class EntregaTarea(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tarea_id = db.Column(db.Integer, db.ForeignKey('tarea.id'))
    alumno_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    archivo_url = db.Column(db.String(500))
    comentario = db.Column(db.Text)
    calificacion = db.Column(db.Float)
    fecha_entrega = db.Column(db.DateTime, default=datetime.utcnow)
    tarea = db.relationship('Tarea', backref='entregas')
    alumno = db.relationship('User', backref='entregas_tareas')

class Pago(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    alumno_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    curso_id = db.Column(db.Integer, db.ForeignKey('curso.id'))
    monto = db.Column(db.Float, nullable=False)
    concepto = db.Column(db.String(300))
    metodo_pago = db.Column(db.String(50), default='Efectivo')
    referencia = db.Column(db.String(200))
    fecha_pago = db.Column(db.DateTime, default=datetime.utcnow)
    verificado = db.Column(db.Boolean, default=False)
    verificado_por = db.Column(db.Integer, db.ForeignKey('user.id'))
    fecha_verificacion = db.Column(db.DateTime)
    notas = db.Column(db.Text)
    alumno = db.relationship('User', foreign_keys=[alumno_id], backref='pagos')
    curso = db.relationship('Curso', backref='pagos')
    verificador = db.relationship('User', foreign_keys=[verificado_por], backref='pagos_verificados')

class ImagenSite(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    seccion = db.Column(db.String(100), nullable=False)
    titulo = db.Column(db.String(300))
    descripcion = db.Column(db.Text)
    url = db.Column(db.String(500), nullable=False)
    orden = db.Column(db.Integer, default=0)
    activo = db.Column(db.Boolean, default=True)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)

class Horario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    curso_id = db.Column(db.Integer, db.ForeignKey('curso.id'))
    grupo_id = db.Column(db.Integer, db.ForeignKey('grupo.id'))
    dia_semana = db.Column(db.Integer, default=0)
    hora_inicio = db.Column(db.String(5))
    hora_fin = db.Column(db.String(5))
    salon = db.Column(db.String(100))
    activo = db.Column(db.Boolean, default=True)
    curso = db.relationship('Curso', backref='horarios')
    grupo = db.relationship('Grupo', backref='horarios')

class MaterialClase(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    clase_id = db.Column(db.Integer, db.ForeignKey('clase.id'))
    titulo = db.Column(db.String(300))
    tipo = db.Column(db.String(50))
    archivo_url = db.Column(db.String(500))
    fecha_subida = db.Column(db.DateTime, default=datetime.utcnow)
    clase = db.relationship('Clase', backref='materiales')

class EnlaceExterno(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    curso_id = db.Column(db.Integer, db.ForeignKey('curso.id'))
    titulo = db.Column(db.String(300))
    url = db.Column(db.String(500))
    plataforma = db.Column(db.String(50))
    activo = db.Column(db.Boolean, default=True)
    curso = db.relationship('Curso', backref='enlaces_externos')

class Banner(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(300))
    subtitulo = db.Column(db.String(500))
    imagen = db.Column(db.String(500), nullable=False)
    tiempo_ms = db.Column(db.Integer, default=5000)
    orden = db.Column(db.Integer, default=0)
    activo = db.Column(db.Boolean, default=True)
    link = db.Column(db.String(500))
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)

class Configuracion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    clave = db.Column(db.String(200), unique=True, nullable=False)
    valor = db.Column(db.Text)
    tipo = db.Column(db.String(50), default='texto')

class Beca(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(300), nullable=False)
    descripcion = db.Column(db.Text)
    tipo = db.Column(db.String(20), nullable=False, default='porcentaje')
    valor = db.Column(db.Float, nullable=False)
    requisitos = db.Column(db.Text)
    cupo_maximo = db.Column(db.Integer, default=0)
    usados = db.Column(db.Integer, default=0)
    fecha_inicio = db.Column(db.Date)
    fecha_fin = db.Column(db.Date)
    activo = db.Column(db.Boolean, default=True)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)

class SolicitudBeca(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    beca_id = db.Column(db.Integer, db.ForeignKey('beca.id'))
    alumno_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    curso_id = db.Column(db.Integer, db.ForeignKey('curso.id'))
    fecha_solicitud = db.Column(db.DateTime, default=datetime.utcnow)
    estado = db.Column(db.String(20), default='pendiente')
    fecha_resolucion = db.Column(db.DateTime)
    resuelto_por = db.Column(db.Integer, db.ForeignKey('user.id'))
    notas = db.Column(db.Text)

    beca = db.relationship('Beca', backref='solicitudes')
    alumno = db.relationship('User', foreign_keys=[alumno_id], backref='solicitudes_becas')
    curso = db.relationship('Curso', backref='solicitudes_becas')
    resolvedor = db.relationship('User', foreign_keys=[resuelto_por], backref='resoluciones_becas')

class TerritorialPage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    slug = db.Column(db.String(200), unique=True, nullable=False)
    activo = db.Column(db.Boolean, default=True)

    # Líder
    nombre = db.Column(db.String(300), nullable=False)
    municipio = db.Column(db.String(200), nullable=False)
    foto = db.Column(db.String(500))
    mensaje = db.Column(db.Text)
    fondo = db.Column(db.String(500))

    # Marca
    logo = db.Column(db.String(500))
    emblema = db.Column(db.String(500))
    frase_institucional = db.Column(db.Text)
    acuerdo_colaboracion = db.Column(db.Text)

    # QR
    codigo_qr = db.Column(db.String(500))
    mensaje_qr = db.Column(db.Text)

    # Colores
    color_primario = db.Column(db.String(20), default='#021a48')
    color_secundario = db.Column(db.String(20), default='#f4a807')
    color_fondo = db.Column(db.String(20), default='#ffffff')
    bg_position = db.Column(db.String(50), default='center')
    bg_size = db.Column(db.String(50), default='contain')
    bg_offset_x = db.Column(db.Integer, default=50)
    bg_offset_y = db.Column(db.Integer, default=50)
    bg_zoom = db.Column(db.Integer, default=100)

    # Banner
    banner_url = db.Column(db.String(500))

    # Contacto
    contacto_telefono = db.Column(db.String(50))
    contacto_email = db.Column(db.String(200))
    contacto_direccion = db.Column(db.Text)

    # SEO
    meta_titulo = db.Column(db.String(300))
    meta_descripcion = db.Column(db.Text)

    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
