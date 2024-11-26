from app import db
from flask_wtf import FlaskForm
from app.models.model import Table_Register
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import (
    DataRequired, Length, EqualTo, ValidationError, IPAddress
)


class Form_Register(FlaskForm):
    def validate_username(self, field):
        username = db.session.execute(
            db.select(Table_Register).filter_by(username=field.data)
        ).scalar_one_or_none()
        if username:
            raise ValidationError('Usuário já cadastrado')

    username = StringField(
        'Username',
        validators=[
            DataRequired(),
            Length(min=3, max=25),
        ]
    )
    password = PasswordField(
        'Password',
        validators=[
            DataRequired(),
            Length(min=6),
        ]
    )
    password_confirm = PasswordField(
        'Confirm Password',
        validators=[
            DataRequired(),
            EqualTo('password', message='As senhas devem coincidir'),
        ]
    )
    submit = SubmitField('Cadastrar')


class Form_Login(FlaskForm):
    username = StringField(
        validators=[
            DataRequired(),
        ]
    )
    password = PasswordField(
        validators=[
            DataRequired(),
        ]
    )
    submit = SubmitField('Entrar')


class Form_Devices(FlaskForm):
    hostname = StringField(
        validators=[
            DataRequired(),
            Length(min=3, max=10),
        ]
    )
    ip_address = StringField(
        validators=[
            DataRequired(),
            IPAddress(),
        ]
    )
    submit = SubmitField('Cadastrar')
