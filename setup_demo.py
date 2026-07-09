"""
Setup script: ensures video_bienvenida column exists and assigns demo video
to revisor.instructor. Run once on PythonAnywhere.
"""
import base64, os, sys

DEMO_MP4_B64 = "AAAAIGZ0eXBpc29tAAACAGlzb21pc28yYXZjMW1wNDEAAAAIZnJlZQAAA2dtZGF0AAACrQYF//+p3EXpvebZSLeWLNgg2SPu73gyNjQgLSBjb3JlIDE2NCByMzE5MiBjMjRlMDZjIC0gSC4yNjQvTVBFRy00IEFWQyBjb2RlYyAtIENvcHlsZWZ0IDIwMDMtMjAyNCAtIGh0dHA6Ly93d3cudmlkZW9sYW4ub3JnL3gyNjQuaHRtbCAtIG9wdGlvbnM6IGNhYmFjPTEgcmVmPTMgZGVibG9jaz0xOjA6MCBhbmFseXNlPTB4MzoweDExMyBtZT1oZXggc3VibWU9NyBwc3k9MSBwc3lfcmQ9MS4wMDowLjAwIG1peGVkX3JlZj0xIG1lX3JhbmdlPTE2IGNocm9tYV9tZT0xIHRyZWxsaXM9MSA4eDhkY3Q9MSBjcW09MCBkZWFkem9uZT0yMSwxMSBmYXN0X3Bza2lwPTEgY2hyb21hX3FwX29mZnNldD0tMiB0aHJlYWRzPTkgbG9va2FoZWFkX3RocmVhZHM9MSBzbGljZWRfdGhyZWFkcz0wIG5yPTAgZGVjaW1hdGU9MSBpbnRlcmxhY2VkPTAgYmx1cmF5X2NvbXBhdD0wIGNvbnN0cmFpbmVkX2ludHJhPTAgYmZyYW1lcz0zIGJfcHlyYW1pZD0yIGJfYWRhcHQ9MSBiX2JpYXM9MCBkaXJlY3Q9MSB3ZWlnaHRiPTEgb3Blbl9nb3A9MCB3ZWlnaHRwPTIga2V5aW50PTI1MCBrZXlpbnRfbWluPTEgc2NlbmVjdXQ9NDAgaW50cmFfcmVmcmVzaD0wIHJjX2xvb2thaGVhZD00MCByYz1jcmYgbWJ0cmVlPTEgY3JmPTIzLjAgcWNvbXA9MC42MCBxcG1pbj0wIHFwbWF4PTY5IHFwc3RlcD00IGlwX3JhdGlvPTEuNDAgYXE9MToxLjAwAIAAAACCZYiEABP//vQbPwKbZklUwHBf0GcUuvNd1x++f1px03vPxu8sHrfJZf+yer7ZGAAAAwAAAwAAChdCT341qcMO1z3rGF+Y7QAAAwAACDLK1AABkANoGaFCEVEHEaGcJUQsdIyQAAADAAADAAADAAADAFa0H1pucFPrmUZ8xGpChIAERQAAABFBmiJsQR/+tSqAAAADAAAdUAAAAA8BnkF5BH8AAAMAAAMAE3EAAANObW9vdgAAAGxtdmhkAAAAAAAAAAAAAAAAAAAD6AAAC7gAAQAAAQAAAAAAAAAAAAAAAAEAAAAAAAAAAAAAAAAAAAABAAAAAAAAAAAAAAAAAABAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAgAAAnl0cmFrAAAAXHRraGQAAAADAAAAAAAAAAAAAAABAAAAAAAAC7gAAAAAAAAAAAAAAAAAAAAAAAEAAAAAAAAAAAAAAAAAAAABAAAAAAAAAAAAAAAAAABAAAAAAoAAAAFoAAAAAAAkZWR0cwAAABxlbHN0AAAAAAAAAAEAAAu4AACAAAABAAAAAAHxbWRpYQAAACBtZGhkAAAAAAAAAAAAAAAAAABAAAAAwABVxAAAAAAALWhkbHIAAAAAAAAAAHZpZGUAAAAAAAAAAAAAAABWaWRlb0hhbmRsZXIAAAABnG1pbmYAAAAUdm1oZAAAAAEAAAAAAAAAAAAAACRkaW5mAAAAHGRyZWYAAAAAAAAAAQAAAAx1cmwgAAAAAQAAAVxzdGJsAAAAsHN0c2QAAAAAAAAAAQAAAKBhdmMxAAAAAAAAAAEAAAAAAAAAAAAAAAAAAAAAAoABaABIAAAASAAAAAAAAAABFUxhdmM2MS4xOS4xMDAgbGlieDI2NAAAAAAAAAAAAAAAGP//AAAANmF2Y0MBZAAW/+EAGWdkABas2UCgL/lhAAADAAEAAAMAAg8WLZYBAAZo6+PLIsD9+PgAAAAAFGJ0cnQAAAAAAAAI/QAACP0AAAAYc3R0cwAAAAAAAAABAAAAAwAAQAAAAAAUc3RzcwAAAAAAAAABAAAAAQAAAChjdHRzAAAAAAAAAAMAAAABAACAAAAAAAEAAMAAAAAAAQAAQAAAAAAcc3RzYwAAAAAAAAABAAAAAQAAAAMAAAABAAAAIHN0c3oAAAAAAAAAAAAAAAMAAAM3AAAAFQAAABMAAAAUc3RjbwAAAAAAAAABAAAAMAAAAGF1ZHRhAAAAWW1ldGEAAAAAAAAAIWhkbHIAAAAAAAAAAG1kaXJhcHBsAAAAAAAAAAAAAAAALGlsc3QAAAAkqXRvbwAAABxkYXRhAAAAAQAAAABMYXZmNjEuNy4xMDA="

def main():
    sys.path.insert(0, os.path.dirname(__file__) or '.')
    from app import app, db
    from sqlalchemy import text, inspect
    from models import User

    with app.app_context():
        # 1. Ensure column exists
        ins = inspect(db.engine)
        cols = [c['name'] for c in ins.get_columns('user')]
        if 'video_bienvenida' not in cols:
            print("Adding video_bienvenida column...")
            db.session.execute(text('ALTER TABLE user ADD COLUMN video_bienvenida VARCHAR(500)'))
            db.session.commit()
            print("Column added.")
        else:
            print("Column video_bienvenida already exists.")

        # 2. Write demo video
        uploads_dir = os.path.join(os.path.dirname(__file__), 'static', 'uploads')
        os.makedirs(uploads_dir, exist_ok=True)
        demo_path = os.path.join(uploads_dir, 'demo_bienvenida.mp4')
        with open(demo_path, 'wb') as f:
            f.write(base64.b64decode(DEMO_MP4_B64))
        print(f"Demo video written: {demo_path} ({os.path.getsize(demo_path)} bytes)")

        # 3. Ensure revisor.instructor user exists
        from werkzeug.security import generate_password_hash
        user = User.query.filter_by(username='revisor.instructor').first()
        if not user:
            user = User(
                username='revisor.instructor',
                email='revisor.instructor@encl.edu.mx',
                password_hash=generate_password_hash('instructor123'),
                role='instructor',
                nombre='Instructor',
                apellidos='Revisor',
                activo=True
            )
            db.session.add(user)
            db.session.flush()
            print("Created user: revisor.instructor / instructor123")

        # 4. Assign demo video
        user.video_bienvenida = 'demo_bienvenida.mp4'
        db.session.commit()
        print(f"Assigned video to: {user.username} ({user.nombre} {user.apellidos})")

        # 5. Verify
        print(f"\nFinal verification:")
        print(f"  username: {user.username}")
        print(f"  video_bienvenida: {user.video_bienvenida}")
        print(f"  file exists: {os.path.exists(os.path.join(uploads_dir, user.video_bienvenida))}")
        print(f"\nCredentials: revisor.instructor / instructor123")
        print("DONE. Now reload the web app on PythonAnywhere (Web -> Reload).")

if __name__ == '__main__':
    main()
