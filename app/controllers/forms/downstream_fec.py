from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField


class Downstream_fec_form(FlaskForm):
    hostname = SelectField(
        'OLT', choices=[]
    )

    chassis = SelectField(
        'chassi', choices=[('1', '1')]
    )

    slot = SelectField(
        'slot', choices=[('1', '1'), ('2', '2')]
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

    submit = SubmitField('Commit')
