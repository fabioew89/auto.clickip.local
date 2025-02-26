from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField


class Downstream_fec_form(FlaskForm):
    hostname = SelectField(
        'Hostname', choices=[]
    )

    chassis = SelectField(
        'Chassis', choices=[('1', '1')]
    )

    slot = SelectField(
        'Slot', choices=[('1', '1'), ('2', '2')]
    )

    id = SelectField(
        'Id', choices=[
            ('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'),
            ('5', '5'), ('6', '6'), ('7', '7'), ('8', '8'),
            ('9', '9'), ('10', '10'), ('11', '11'), ('12', '12'),
            ('13', '13'), ('14', '14'), ('15', '15'), ('16', '16')
        ]
    )

    command = SelectField(
        'Command', choices=[
            ('no downstream-fec', 'no downstream-fec'),
            ('downstream-fec', 'downstream-fec'),
        ],
        default='no downstream-fec'
    )

    submit = SubmitField('Commit')
