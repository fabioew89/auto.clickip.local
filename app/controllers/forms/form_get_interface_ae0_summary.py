from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField


class SummaryForm(FlaskForm):
    hostname = SelectField(
        'Hostname', choices=[],
    )
    submit = SubmitField(
        'Enviar'
    )
