import os
from app import db
from dotenv import load_dotenv

import ipaddress as ip

from flask import Blueprint, render_template, flash
from flask_login import current_user, login_required, fresh_login_required

from app.models import Routers
from app.controllers.forms.set_interface_ae0_unit_vlan import SetIntAe0UnitVlanForm
from app.controllers.netmiko.junos.set_interface_ae0_unit_vlan import set_interface_unit

from cryptography.fernet import Fernet

load_dotenv()

# Inicializa o Blueprint
set_interface_ae0_unit_vlan_bp = Blueprint('set_interface_ae0_unit_vlan_bp', __name__)
fernet_key = Fernet(os.getenv('MY_FERNET_KEY'))


# Rota: set_interface_ae0_unit_vlan
@set_interface_ae0_unit_vlan_bp.route('/set_interface_ae0_unit_vlan', methods=['GET', 'POST'])
@login_required
@fresh_login_required
def interface_unit():
    form = SetIntAe0UnitVlanForm()
    user_decrypted_password = fernet_key.decrypt(current_user.password).decode('utf-8')
    hosts = db.session.execute(db.select(Routers).order_by(Routers.hostname)).scalars()
    form.hostname.choices = [(host.ip_address, host.hostname) for host in hosts]
    output = None

    if form.validate_on_submit():
        inet_48 = ip.IPv6Network(address=form.ipv6_48.data, strict=False)
        first_ip = ip.IPv4Network(address=form.ipv4_gw.data, strict=False).network_address + 1
        prefix_v4 = ip.IPv4Network(address=form.ipv4_gw.data, strict=False).prefixlen

        first_ip6 = ip.IPv6Network(address=form.ipv6_gw.data, strict=False).network_address + 1
        prefix_v6 = ip.IPv6Network(address=form.ipv6_gw.data, strict=False).prefixlen

        output = set_interface_unit(
            hostname=form.hostname.data,
            username=current_user.username,
            password=user_decrypted_password,

            unit=form.unit_vlan.data,
            description=form.description.data,
            bandwidth=form.bandwidth.data,

            ipv4_gw=f'{first_ip}/{prefix_v4}',
            ipv6_gw=f'{first_ip6}/{prefix_v6}',
            ipv6_cli=first_ip6 + 1,
            ipv6_48=inet_48,
        )

        flash('Command sent successfully!', category='success')

    else:
        if form.errors:
            for field, errors in form.errors.items():
                for error in errors:
                    flash(f"Error in {field}: {error}", category='danger')

    return render_template(
        'vendors/junos/set_interface_ae0_unit_vlan.html',
        form=form,
        output=output,
    )
