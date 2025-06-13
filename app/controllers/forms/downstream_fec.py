from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField
from wtforms.validators import DataRequired


class Downstream_fec_form(FlaskForm):
    hostname = SelectField(
        '',
        choices=[],
        validators=[DataRequired(message='Por favor, selecione uma OLT')]
    )

    chassis = SelectField(
        'chassi', choices=[('1', '1')]
    )

    slot = SelectField(
        'slot', choices=[(str(i), str(i)) for i in range(1, 3)]
    )

    port_id = SelectField(
        'gpon',
        choices=[(str(i), str(i)) for i in range(1, 33)]
    )

    dmos_command = SelectField(
        label='Ativar / Desativar',
        choices=[
            ('downstream-fec', 'Habilitar'),
            ('no downstream-fec', 'Desabilitar'),
        ],
    )

    submit = SubmitField('Executar commit')
