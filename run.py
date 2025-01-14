from app import create_app
from app.controllers.admin import create_admin

app = create_app()

create_admin()

if __name__ == "__main__":
    app.run()
