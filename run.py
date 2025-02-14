from app import create_app
from app.controllers.admin import flask_admin
from create_admin import ensure_admin

app = create_app()

flask_admin()
ensure_admin()

if __name__ == "__main__":
    app.run()
