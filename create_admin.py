import os
from app.models import Users
from dotenv import load_dotenv
from app import create_app, db
from cryptography.fernet import Fernet

load_dotenv()  # load all env variables?

fernet_key = Fernet(os.getenv('MY_FERNET_KEY'))

app = create_app()

with app.app_context():
    admin_username = os.getenv('ADMIN_USERNAME')
    admin_password = os.getenv('ADMIN_PASSWORD')

    if not admin_username or not admin_password:
        raise ValueError("ADMIN_USERNAME ou ADMIN_PASSWORD não encontrados no arquivo .env")  # noqa E501

    auto_noc = Users.query.filter_by(username=admin_username).first()

    if not auto_noc:
        auto_noc = Users(
            username=admin_username,
            password=fernet_key.encrypt(admin_password.encode('utf-8')),
        )
        db.session.add(auto_noc)
        db.session.commit()
        print("🚀 Usuário admin criado com sucesso!")
    else:
        print("✅ Usuário admin já existe.")
