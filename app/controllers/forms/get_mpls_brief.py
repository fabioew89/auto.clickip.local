from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField, IntegerField, StringField
from wtforms.validators import DataRequired, NumberRange, IPAddress


class GetMplsForm(FlaskForm):
    hostname = SelectField(
        'Hostname', choices=[]
    )

    tunnel_vlan = IntegerField(
        'Tunnel VLAN', validators=[
            DataRequired(),
            NumberRange(min=1, max=4096)
        ], default='1024'
    )
    service = SelectField(
        label='Serviços',
        choices=[
            ('TIP', 'TIP'), ('TIP', 'TIP'), ('TIP', 'TIP')
        ]
    )

    state = SelectField(
        label='Estado',
        choices=[
            ('AM', 'AM'), ('PA', 'PA'), ('MA', 'MA'),
        ]
    )

    city = SelectField(
        label='Cidade',
        choices=[('MAO', 'MAO'), ('STR', 'STR'), ('MON', 'MON')],
        default='MAO',
        validators=[
            DataRequired()
        ],
    )

    number = IntegerField(
        label='Serviços',
        validators=[
            NumberRange(min=100000, max=999999),
            DataRequired()
        ], default=100000
    )

    neighbor = StringField(
        label='Neighbor targed',
        validators=[
            DataRequired(),
            IPAddress(ipv4=True)
        ]
    )

    port_dest = SelectField(
        label='Porta de Destino',
        choices=[
            ('lag-1', 'lag-1'),
            ('lag-2', 'lag-2'),
            ('lag-3', 'lag-3'),
            ('lag-4', 'lag-4'),
            ('lag-5', 'lag-5'),
            ('lag-6', 'lag-6'),
            ('lag-7', 'lag-7'),
            ('lag-8', 'lag-8')
        ],
        default='MAO',
        validators=[
            DataRequired()
        ],
    )

    submit = SubmitField(
        label='Commit'
    )
