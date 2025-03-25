import os
from app import db
from dotenv import load_dotenv
from app.models import Users, Routers
from cryptography.fernet import Fernet
from flask import Blueprint, request, render_template, flash
from app.controllers.network.netmiko import get_interface_ae0_summary
from app.controllers.forms.form_get_interface_ae0_summary import SummaryForm
from flask_login import current_user, login_required, fresh_login_required

load_dotenv()

# Inicializa o Blueprint
int_summary_bp = Blueprint('int_summary_bp', __name__)

fernet_key = Fernet(os.getenv('MY_FERNET_KEY'))


# Rota: get_interface_ae0_summary
@int_summary_bp.route('/get_interface_ae0_summary', methods=['GET', 'POST'])
@login_required
@fresh_login_required
def interface_summary():
    form = SummaryForm()
    hosts = db.session.execute(db.select(Routers).order_by(Routers.id)).scalars().all()
    form.hostname.choices = [(host.ip_address, host.hostname) for host in hosts]
    current_user_decrypted_password = fernet_key.decrypt(current_user.password).decode('utf-8')

    output = None

    if form.validate_on_submit():
        selected_hostname = form.hostname.data
        logged_username = current_user.username
        user_password = current_user_decrypted_password

        output = get_interface_ae0_summary(
            selected_hostname,
            logged_username,
            user_password,
        )

        flash('Command sent successfully!', category='success')

    else:
        if form.errors:
            for field, errors in form.errors.items():
                for error in errors:
                    flash(f"Error in {field}: {error}", category='danger')

    return render_template(
        'vendors/junos/get_interface_ae0_summary.html',
        form=form,
        output=output,
        devices=form.hostname.choices,
    )
