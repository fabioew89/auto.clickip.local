import ipaddress
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, NumberRange, IPAddress
from wtforms import StringField, SubmitField, SelectField, IntegerField


def validate_ip_with_cidr(form, field):
    try:
        ipaddress.ip_network(field.data, strict=False)

    except ValueError as e:
        raise e(f'Ip Address Invalid {e}')


class SetIntAe0UnitVlanForm(FlaskForm):
    hostname = SelectField(
        'Hostname', choices=[]
    )
    unit_vlan = IntegerField(
        'Unit VLAN', validators=[
            DataRequired(),
            NumberRange(min=1, max=4096)
        ]
    )
    description = StringField(
        'Description', validators=[
            DataRequired()
        ]
    )
    bandwidth = IntegerField(
        label='Bandwidth, Ex: 1000',
        validators=[
            DataRequired(),
            NumberRange(min=1, max=9999)
        ]
    )
    ipv4_gw = StringField(
        label='IPv4 with CIDR, Ex: 192.168.0.0/30',
        validators=[
            DataRequired(),
            validate_ip_with_cidr,
        ]
    )
    ipv6_gw = StringField(
        label='IPv6 Gateway, Ex: 2001:db8::1/126',
        validators=[
            DataRequired(),
            validate_ip_with_cidr,
        ]
    )
    ipv6_48 = StringField(
        label='Prefix /48, Ex: 2001:db8::/48',
        validators=[
            DataRequired(),
            validate_ip_with_cidr,
        ]
    )
    submit = SubmitField('Commitar')
