import os
from app import db
from dotenv import load_dotenv
from app.models import Switches
from cryptography.fernet import Fernet
from app.controllers.forms.mpls_l2vpn_vpls_brief_oficial import GetMplsForm
from flask import Blueprint, render_template, flash
from flask_login import current_user, login_required, fresh_login_required
from app.controllers.netmiko.dmos.get_mpls_brief import get_mpls_l2vpn_vpls_brief_oficial

load_dotenv()

# Inicializa o Blueprint
get_mpls_brief_bp = Blueprint('get_mpls_brief_bp', __name__)
fernet_key = Fernet(os.getenv('MY_FERNET_KEY'))


@get_mpls_brief_bp.route('/get_mpls_brief', methods=['GET', 'POST'])
@login_required
@fresh_login_required
def get_mpls_brief():
    form = GetMplsForm()

    current_user_decrypted_password = fernet_key.decrypt(current_user.password).decode('utf-8')
    hosts = db.session.execute(db.select(Switches).order_by(Switches.hostname)).scalars().all()
    form.hostname.choices = [(host.ip_address, host.hostname) for host in hosts]

    output = None

    if form.validate_on_submit():
        output = get_mpls_l2vpn_vpls_brief_oficial(
            hostname=form.hostname.data,
            username=current_user.username,
            password=current_user_decrypted_password,
            tunnel_vlan=form.tunnel_vlan.data,
        )

        flash('Consulta realizada!', category='success')

    else:
        if form.errors:
            for field, errors in form.errors.items():
                for error in errors:
                    flash(f"Error in {field}: {error}", category='danger')

    return render_template(
        'vendors/dmos/get_mpls_brief.html',
        form=form,
        output=output,
    )
