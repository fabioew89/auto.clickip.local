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
            ('TIP', 'TIP'), ('VAZIO', 'VAZIO'), ('VAZIO', 'VAZIO')
        ]
    )

    state = SelectField(
        label='Estado',
        choices=[
            ('AC', 'AC'), ('AL', 'AL'), ('AM', 'AM'), ('AP', 'AP'),
            ('BA', 'BA'), ('CE', 'CE'), ('DF', 'DF'), ('ES', 'ES'),
            ('GO', 'GO'), ('MA', 'MA'), ('MG', 'MG'), ('MS', 'MS'),
            ('MT', 'MT'), ('PA', 'PA'), ('PB', 'PB'), ('PE', 'PE'),
            ('PI', 'PI'), ('PR', 'PR'), ('RJ', 'RJ'), ('RN', 'RN'),
            ('RO', 'RO'), ('RR', 'RR'), ('RS', 'RS'), ('SC', 'SC'),
            ('SE', 'SE'), ('SP', 'SP'), ('TO', 'TO')])

    city = SelectField(
        label='Cidade',
        choices=[('MNS', 'MNS'), ('PAR', 'PAR'), ('STR', 'STR'), ('MNG', 'MNG')],
        default='MNS',
        validators=[
            DataRequired()
        ],
    )

    number = IntegerField(
        label='Designação',
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
            ('hundred-gigabit-ethernet-1/1/1', 'hundred-gigabit-ethernet-1/1/1'),
            ('hundred-gigabit-ethernet-1/1/2', 'hundred-gigabit-ethernet-1/1/2'),
            ('hundred-gigabit-ethernet-1/1/3', 'hundred-gigabit-ethernet-1/1/3'),
            ('hundred-gigabit-ethernet-1/1/4', 'hundred-gigabit-ethernet-1/1/4'),
            ('hundred-gigabit-ethernet-1/1/5', 'hundred-gigabit-ethernet-1/1/5'),
            ('hundred-gigabit-ethernet-1/1/6', 'hundred-gigabit-ethernet-1/1/6'),
            ('ten-gigabit-ethernet-1/1/1', 'ten-gigabit-ethernet-1/1/1'),
            ('ten-gigabit-ethernet-1/1/2', 'ten-gigabit-ethernet-1/1/2'),
            ('ten-gigabit-ethernet-1/1/3', 'ten-gigabit-ethernet-1/1/3'),
            ('ten-gigabit-ethernet-1/1/4', 'ten-gigabit-ethernet-1/1/4'),
            ('ten-gigabit-ethernet-1/1/5', 'ten-gigabit-ethernet-1/1/5'),
            ('ten-gigabit-ethernet-1/1/6', 'ten-gigabit-ethernet-1/1/6'),
            ('ten-gigabit-ethernet-1/1/7', 'ten-gigabit-ethernet-1/1/7'),
            ('ten-gigabit-ethernet-1/1/8', 'ten-gigabit-ethernet-1/1/8'),
            ('twenty-five-g-ethernet-1/1/1', 'twenty-five-g-ethernet-1/1/1'),
            ('twenty-five-g-ethernet-1/1/2', 'twenty-five-g-ethernet-1/1/2'),
            ('twenty-five-g-ethernet-1/1/3', 'twenty-five-g-ethernet-1/1/3'),
            ('twenty-five-g-ethernet-1/1/4', 'twenty-five-g-ethernet-1/1/4'),
            ('twenty-five-g-ethernet-1/1/5', 'twenty-five-g-ethernet-1/1/5'),
            ('twenty-five-g-ethernet-1/1/6', 'twenty-five-g-ethernet-1/1/6'),
            ('twenty-five-g-ethernet-1/1/7', 'twenty-five-g-ethernet-1/1/7'),
            ('twenty-five-g-ethernet-1/1/8', 'twenty-five-g-ethernet-1/1/8'),
            ('twenty-five-g-ethernet-1/1/9', 'twenty-five-g-ethernet-1/1/9'),
            ('twenty-five-g-ethernet-1/1/10', 'twenty-five-g-ethernet-1/1/10'),
            ('twenty-five-g-ethernet-1/1/11', 'twenty-five-g-ethernet-1/1/11'),
            ('twenty-five-g-ethernet-1/1/12', 'twenty-five-g-ethernet-1/1/12'),
            ('twenty-five-g-ethernet-1/1/13', 'twenty-five-g-ethernet-1/1/13'),
            ('twenty-five-g-ethernet-1/1/14', 'twenty-five-g-ethernet-1/1/14'),
            ('twenty-five-g-ethernet-1/1/15', 'twenty-five-g-ethernet-1/1/15'),
            ('twenty-five-g-ethernet-1/1/16', 'twenty-five-g-ethernet-1/1/16'),
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
