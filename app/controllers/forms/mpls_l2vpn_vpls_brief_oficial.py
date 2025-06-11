from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField, IntegerField
from wtforms.validators import DataRequired, NumberRange


class GetMplsForm(FlaskForm):
    hostname = SelectField(
        'Switch', choices=[]
    )

    tunnel_vlan = IntegerField(
        'Número tunnel', validators=[
            DataRequired(),
            NumberRange(min=1, max=4096)
        ], default='1258'
    )

    submit = SubmitField(
        label='Consultar'
    )
