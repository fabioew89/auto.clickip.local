from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, Length, EqualTo
from wtforms import StringField, PasswordField, SubmitField, BooleanField


class LoginForm(FlaskForm):
    username = StringField(
        label='',
        validators=[
            DataRequired(),
            Length(max=30),
        ]
    )

    password = PasswordField(
        label='',
        validators=[
            DataRequired(),
            Length(max=30),
        ]
    )

    checkbox = BooleanField(
        label='Remember me!',
        default=True
    )

    submit = SubmitField(label='Entrar')


class RegisterForm(FlaskForm):
    username = StringField(
        label='Username',
        validators=[
            DataRequired(),
            Length(max=30),
        ]
    )

    password = PasswordField(
        label='Password',
        validators=[
            DataRequired(),
            Length(min=6, max=30),
        ]
    )

    confirm_password = PasswordField(
        label='Confirm Password',
        validators=[
            DataRequired(),
            Length(max=30),
            EqualTo('password', message='Your password and confir password must be equal!!!')
        ]
    )

    checkbox = BooleanField(
        label='Accept Terms',
        validators=[
            DataRequired()
        ],
        default=False
    )

    submit = SubmitField(
        label='Cadastrar'
    )
