from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, IPAddress
from wtforms import SelectField, StringField, SubmitField


class SetPolicyWhitelistForm(FlaskForm):
    hostname = SelectField(
        label='Hostname',
        choices=[],
        default=None
    )

    prefix_address = StringField(
        label='Ex: 192.168.0.1',
        validators=[
            DataRequired(),
            IPAddress(ipv4=True, ipv6=False)
        ],
    )

    submit = SubmitField(
        label='Commit'
    )


class GetPolicyWhitelistForm(FlaskForm):
    hostname = SelectField(
        label='Hostname',
        choices=[],
        default=None
    )

    submit = SubmitField(
        label='Enviar'
    )
