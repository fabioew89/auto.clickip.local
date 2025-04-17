import os
from app import db
from dotenv import load_dotenv
from app.models import Routers
from cryptography.fernet import Fernet
from flask import Blueprint, render_template, flash
from app.controllers.netmiko.junos.set_policy_whitelist import set_policy_whitelist as whitelist
from flask_login import login_required, fresh_login_required, current_user
from app.controllers.forms.general_network_forms import GeneralNetworkForm

load_dotenv()

# Inicializa o Blueprint
set_policy_whitelist_bp = Blueprint('set_policy_whitelist_bp', __name__)
fernet_key = Fernet(os.getenv('MY_FERNET_KEY'))


@set_policy_whitelist_bp.route('/set_policy_whitelist', methods=['GET', 'POST'])
@login_required
@fresh_login_required
def set_policy_whitelist():
    form = GeneralNetworkForm()
    hosts = db.session.execute(db.select(Routers).order_by(Routers.ip_address)).scalars().all()
    form.hostname.choices = [(host.ip_address, host.hostname) for host in hosts]
    current_user_decrypted_password = fernet_key.decrypt(current_user.password).decode('utf-8')

    output = None

    if form.validate_on_submit():
        output = whitelist(
            hostname=form.hostname.data,
            username=current_user.username,
            password=current_user_decrypted_password,
            prefix=form.prefix_address.data
        )

        flash('Command sent successfully!', category='success')

    else:
        if form.errors:
            for field, errors in form.errors.items():
                for error in errors:
                    flash(f"Error in {field}: {error}", category='danger')

    return render_template(
        'vendors/junos/set_policy_whitelist.html',
        form=form,
        output=output,
    )
