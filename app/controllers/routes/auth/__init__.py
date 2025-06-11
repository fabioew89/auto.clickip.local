import os
from app import db, create_app
from app.models import Users
from app.controllers.forms.auth_form import LoginForm, RegisterForm

from flask_login import login_required, login_user, logout_user
from flask import Blueprint, render_template, redirect, url_for, flash


from dotenv import load_dotenv
from cryptography.fernet import Fernet

load_dotenv()

auth_bp = Blueprint('auth_bp', __name__)
fernet_key = Fernet(os.getenv('MY_FERNET_KEY'))


def check_password(stored_password, provided_password):
    try:
        decrypted_password = fernet_key.decrypt(stored_password).decode('utf-8')
        return decrypted_password == provided_password
    except Exception as e:
        print(f'[Erro] Fail, verify your password: {e}')
        return False


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():

        username_recorder = db.session.execute(
            db.select(Users).filter_by(username=form.username.data)
        ).scalar_one_or_none()

        if username_recorder and check_password(username_recorder.password, form.password.data):
            login_user(username_recorder, remember=form.checkbox.data)
            flash(f'Bem vindo, {form.username.data}', category='success')
            return redirect(url_for('int_summary_bp.interface_summary'))

        else:
            flash('check your password or username', category='danger')

    if form.errors:
        for field_name, error_messages in form.errors.items():
            for error_message in error_messages:
                flash(f'Error in {field_name}: {error_message}', category='danger')

    return render_template(
        'accounts/login.html',
        form=form)


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        new_user = form.username.data
        new_pass = form.password.data

        app = create_app()

        with app.app_context():

            if not db.session.execute(db.select(Users).filter_by(username=new_user)).first():
                encrypted_password = fernet_key.encrypt(new_pass.encode('utf-8'))
                new_user_add = Users(username=new_user, password=encrypted_password, is_admin=False)

                db.session.add(new_user_add)
                db.session.commit()

                return redirect(url_for('auth_bp.login'))

            else:
                flash(message='Username already exist', category='danger')

    if form.errors:
        for field_name, error_messages in form.errors.items():
            for error_message in error_messages:
                flash(f'Error in {field_name}: {error_message}', category='danger')

    return render_template(
        'accounts/register.html',
        form=form
    )


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Saindo...', category='info')
    return redirect(url_for('auth_bp.login'))
