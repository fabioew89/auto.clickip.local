from flask import Blueprint, request, render_template, flash
from flask_login import current_user, login_required, fresh_login_required
from app.controllers.networks import set_interface_unit, \
    get_interface_summary, get_interface_configuration

from app.controllers.forms import NetworkForm
from app.models import Users, Devices
from app import db

from cryptography.fernet import Fernet

# Inicializa o Blueprint
network_bp = Blueprint('network', __name__)

f = Fernet(b'bdilxeLGCHnJo-2HtofB9wGcXaUV7D5NZgxh5Nt5fpg=')


# Rota: get_interface_summary
@network_bp.route('/get_interface_summary', methods=['GET', 'POST'])
@login_required
@fresh_login_required
def interface_summary():
    form = NetworkForm()

    devices = db.session.execute(db.select(Devices)).scalars().all()

    user_record = db.session.execute(
        db.select(Users).filter_by(username=current_user.username)
    ).scalar_one_or_none()

    decrypted_password = f.decrypt(user_record.password).decode('utf-8')

    output = None

    if request.method == 'POST':
        hostname = form.hostname.data
        username = current_user.username
        password = decrypted_password

        output = get_interface_summary(
            hostname,
            username,
            password,
        )

    return render_template(
        'route/get_interface_summary.html',
        form=form,
        output=output,
        devices=devices,
        password=decrypted_password
    )


# Rota: get_interface_configuration
@network_bp.route('/get_interface_configuration', methods=['GET', 'POST'])
@login_required
@fresh_login_required
def interface_configuration():
    users = db.session.execute(db.select(Users)).scalars().all()
    devices = db.session.execute(db.select(Devices)).scalars().all()

    output = None

    if request.method == 'POST':
        hostname = request.form.get('hostname')
        username = request.form.get('username')
        password = request.form.get('password')
        unit = request.form.get('unit')

        output = get_interface_configuration(
            hostname, username, password, unit
        )

    return render_template(
        'route/get_interface_configuration.html',
        users=users,
        output=output,
        devices=devices,
    )


# Rota: set_interface_unit
@network_bp.route('/set_interface_unit', methods=['GET', 'POST'])
@login_required
@fresh_login_required
def interface_unit():
    form = NetworkForm()

    output = None

    users = db.session.execute(db.select(Users).order_by(Users.id)).scalars()
    hosts = db.session.execute(db.select(Devices).order_by(Devices.id)).scalars()  # noqa: E501

    form.username.choices = [(user.username, user.username) for user in users]
    form.hostname.choices = [(host.ip_address, host.hostname) for host in hosts]  # noqa: E501

    if form.validate_on_submit():
        hostname = form.hostname.data
        username = form.username.data
        password = form.password.data
        unit = form.unit_vlan.data
        description = form.description.data
        bandwidth = form.bandwidth.data
        ipv4_gw = form.ipv4_gw.data
        ipv6_gw = form.ipv6_gw.data
        ipv6_cli = form.ipv6_cli.data
        inet6_48 = form.ipv6_48.data

        output = set_interface_unit(
            hostname, username, password, unit, description,
            bandwidth, ipv4_gw, ipv6_gw, ipv6_cli, inet6_48
        )

        flash('Formulário enviado com sucesso!', category='success')

    else:
        if form.errors:
            for field, errors in form.errors.items():
                for error in errors:
                    flash(f"Erro no campo {field}: {error}", category='danger')

    return render_template(
        'route/set_interface_unit.html',
        form=form,
        output=output,
    )
