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
        'gpon', choices=[
            ('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'),
            ('5', '5'), ('6', '6'), ('7', '7'), ('8', '8'),
            ('9', '9'), ('10', '10'), ('11', '11'), ('12', '12'),
            ('13', '13'), ('14', '14'), ('15', '15'), ('16', '16'),
            ('17', '17'), ('18', '18'), ('19', '19'), ('20', '20'),
            ('21', '21'), ('22', '22'), ('23', '23'), ('24', '24'),
            ('25', '25'), ('26', '26'), ('27', '27'), ('28', '28'),
            ('29', '29'), ('30', '30'), ('31', '31'), ('32', '32')
        ]
    )

    dmos_command = SelectField(
        label='Ativar / Desativar',
        choices=[
            ('downstream-fec', 'Habilitar'),
            ('no downstream-fec', 'Desabilitar'),
        ],
        # default='downstream-fec'
    )

    submit = SubmitField('Commit')
