from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField, IntegerField, StringField
from wtforms.validators import DataRequired, NumberRange, IPAddress


class GetMplsForm(FlaskForm):
    hostname = SelectField('Hostname', choices=[])

    tunnel_vlan = IntegerField(
        'Tunnel VLAN',
        validators=[DataRequired(), NumberRange(min=1, max=4096)],
        default=1024
    )

    service = SelectField(
        'Serviços',
        choices=[('TIP', 'TIP'), ('VAZIO', 'VAZIO')]
    )

    UF_CHOICES = [(uf, uf) for uf in [
        'AC', 'AL', 'AM', 'AP', 'BA', 'CE', 'DF', 'ES', 'GO', 'MA',
        'MG', 'MS', 'MT', 'PA', 'PB', 'PE', 'PI', 'PR', 'RJ', 'RN',
        'RO', 'RR', 'RS', 'SC', 'SE', 'SP', 'TO'
    ]]

    state = SelectField('Estado', choices=UF_CHOICES)

    city = SelectField(
        'Cidade',
        choices=[(c, c) for c in ['MNS', 'PAR', 'STR', 'MNG']],
        default='MNS',
        validators=[DataRequired()]
    )

    number = IntegerField(
        'Designação',
        validators=[NumberRange(min=100000, max=999999), DataRequired()],
        default=100000
    )

    neighbor = StringField(
        'Neighbor target',
        validators=[DataRequired(), IPAddress(ipv4=True)]
    )

    eth_ports = [f"hundred-gigabit-ethernet-1/1/{i}" for i in range(1, 7)]
    ten_gig_ports = [f"ten-gigabit-ethernet-1/1/{i}" for i in range(1, 9)]
    twf_gig_ports = [f"twenty-five-g-ethernet-1/1/{i}" for i in range(1, 17)]
    lags = [f"lag-{i}" for i in range(1, 9)]

    port_choices = eth_ports + ten_gig_ports + twf_gig_ports + lags

    port_dest = SelectField(
        'Porta de Destino',
        choices=[(p, p) for p in port_choices],
        validators=[DataRequired()]
    )

    submit = SubmitField('Commit')
