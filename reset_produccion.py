"""
Script de limpieza para paso a producción.
Conserva: admins, superadmins, instructores, cursos, clases, exámenes,
categorías, patrocinadores, configuración, páginas territoriales,
catálogo de estados/municipios/distritos/grupos, becas.
Elimina: alumnos demo, inscripciones, asistencias, entregas,
certificados de prueba, solicitudes de beca, pagos, mensajes de contacto.

Ejecutar: python3 reset_produccion.py
"""
from app import app, db
from models import *
from sqlalchemy import text


def reset():
    with app.app_context():
        print("=== LIMPIEZA PARA PRODUCCIÓN ===")

        # 1. Eliminar mensajes de contacto
        count = ContactoMensaje.query.count()
        ContactoMensaje.query.delete()
        print(f"  ContactoMensaje: {count} eliminados")

        # 2. Eliminar solicitudes de beca
        count = SolicitudBeca.query.count()
        SolicitudBeca.query.delete()
        print(f"  SolicitudBeca: {count} eliminadas")

        # 3. Eliminar pagos (si existen)
        try:
            count = Pago.query.count()
            Pago.query.delete()
            print(f"  Pago: {count} eliminados")
        except Exception:
            pass

        # 4. Eliminar certificados de prueba
        count = Certificado.query.count()
        Certificado.query.delete()
        print(f"  Certificado: {count} eliminados")

        # 5. Eliminar entregas de tareas
        count = EntregaTarea.query.count()
        EntregaTarea.query.delete()
        print(f"  EntregaTarea: {count} eliminadas")

        # 6. Eliminar asistencias
        count = Asistencia.query.count()
        Asistencia.query.delete()
        print(f"  Asistencia: {count} eliminadas")

        # 7. Eliminar inscripciones
        count = Inscripcion.query.count()
        Inscripcion.query.delete()
        print(f"  Inscripcion: {count} eliminadas")

        # 8. Eliminar alumnos demo
        roles_no_permitidos = ['admin', 'superadmin', 'instructor']
        alumnos = User.query.filter(~User.role.in_(roles_no_permitidos)).all()
        print(f"  Alumnos demo: {len(alumnos)} eliminados")
        for a in alumnos:
            db.session.delete(a)

        db.session.commit()

        # 9. Mostrar resumen
        admins = User.query.filter_by(role='admin').all()
        supers = User.query.filter_by(role='superadmin').all()
        instrs = User.query.filter_by(role='instructor').all()
        cursos = Curso.query.count()
        clases = Clase.query.count()
        examenes = Examen.query.count()

        print(f"\n=== CONSERVADO ===")
        print(f"  Super Admins: {len(supers)}")
        for u in supers:
            print(f"    - {u.username}")
        print(f"  Admins: {len(admins)}")
        for u in admins:
            print(f"    - {u.username}")
        print(f"  Instructores: {len(instrs)}")
        print(f"  Cursos: {cursos}")
        print(f"  Clases: {clases}")
        print(f"  Exámenes: {examenes}")
        print(f"\n=== LISTO PARA PRODUCCIÓN ===")

    # Recomendación post-ejecución
    print()
    print("=" * 50)
    print("RECOMENDACIONES FINALES:")
    print("1. Ejecuta: python3 setup_demo.py (para tener usuario revisor.instructor)")
    print("2. Ve a Web → Reload en PythonAnywhere")
    print("3. Cambia la contraseña del admin y superadmin en producción")
    print("4. Revisa que los cursos tengan instructores asignados correctamente")
    print("=" * 50)


if __name__ == '__main__':
    reset()
