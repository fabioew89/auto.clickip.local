from app import create_app
from app.controllers.admin import flask_admin

app = create_app()

flask_admin()

if __name__ == "__main__":
    app.run()
