import os
from app import db, admin
from dotenv import load_dotenv

from flask import url_for, redirect
from flask_login import current_user
from flask_admin.menu import MenuLink
from flask_admin.contrib.sqla import ModelView
from flask_admin.contrib.fileadmin import FileAdmin

from wtforms import PasswordField
from wtforms.validators import Length, IPAddress, InputRequired
from app.models import Users, Routers, Switches, Olts, NeighborBgpIpv4, NeighborBgpIpv6
from cryptography.fernet import Fernet

load_dotenv()
path = os.path.join(os.path.dirname(__file__), 'static')


class UserView(ModelView):
    # Permissões de visualização e edição
    def is_accessible(self):
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('auth_bp.login'))

    def get_query(self):
        # Admin vê todos, usuário comum só vê a si mesmo
        if current_user.is_admin:
            return super().get_query()
        return super().get_query().filter(self.model.id == current_user.id)

    def get_count_query(self):
        if current_user.is_admin:
            return super().get_count_query()
        return super().get_count_query().filter(self.model.id == current_user.id)

    def scaffold_form(self):
        form_class = super().scaffold_form()
        # Só admin pode ver/editar o campo is_admin
        if not getattr(current_user, 'is_authenticated', False) or not getattr(current_user, 'is_admin', False):
            if hasattr(form_class, 'is_admin'):
                delattr(form_class, 'is_admin')
        return form_class

    def on_model_change(self, form, model, is_created):
        # Criptografa a senha se foi alterada
        if form.password.data:
            fernet_key = Fernet(os.getenv('MY_FERNET_KEY'))
            model.password = fernet_key.encrypt(form.password.data.encode('utf-8'))
        # Usuário comum só pode editar a si mesmo
        if not current_user.is_admin and model.id != current_user.id:
            raise Exception("Você só pode editar seus próprios dados.")
        # Usuário comum não pode se tornar admin
        if not current_user.is_admin:
            model.is_admin = False

    # Permissões de criação e deleção
    def can_create(self):
        return getattr(current_user, 'is_authenticated', False) and getattr(current_user, 'is_admin', False)

    def can_delete(self, obj=None):
        return current_user.is_admin or (obj and obj.id == current_user.id)

    def can_edit(self, obj=None):
        return current_user.is_admin or (obj and obj.id == current_user.id)

    # Configurações de exibição
    edit_modal = details_modal = True
    can_view_details = can_set_page_size = True
    can_export = True

    column_default_sort = 'username'
    column_exclude_list = ['password']

    column_searchable_list = ['username']
    column_filters = ['username', 'is_admin']
    column_editable_list = ['username']  # Apenas admin pode editar is_admin

    form_overrides = {
        'password': PasswordField
    }

    form_args = {
        'password': {
            'validators': [
                InputRequired(),
                Length(min=6, max=30)
            ],
        },
    }


class DeviceView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('auth_bp.login'))

    edit_modal = details_modal = True
    can_view_details = can_set_page_size = True
    can_edit = can_create = can_export = can_delete = True

    column_default_sort = 'hostname'
    column_searchable_list = column_filters = column_editable_list = ['hostname', 'ip_address']

    form_args = {
        'ip_address': {
            'label': 'Endereço IP',
            'validators': [InputRequired(), IPAddress(ipv4=True)],
            'description': 'Digite um IPv4 válido (ex: 192.168.1.1)'
        }
    }

    form_widget_args = {
        'ip_address': {
            'placeholder': '192.168.1.1',
        }
    }


class OltView(DeviceView):
    column_labels = dict(hostname='Hostname - OLTs')


class RouterView(DeviceView):
    column_labels = dict(hostname='Hostname - Router')


class SwitchView(DeviceView):
    column_labels = dict(hostname='Hostname - Switch')


class BgpNeighborView(DeviceView):
    column_default_sort = 'description'
    column_searchable_list = column_filters = column_editable_list = ['description', 'neighbor']


class BgpNeighborIpv4View(BgpNeighborView):
    column_labels = dict(neighbor='Neighbor IPv4')

    form_args = {
        'neighbor': {
            'label': 'Endereço IP',
            'validators': [InputRequired(), IPAddress(ipv4=True)],
            'description': 'Digite um IPv4 válido (ex: 192.168.1.1)'
        }
    }


class BgpNeighborIpv6View(BgpNeighborView):
    column_labels = dict(neighbor='Neighbor IPv6')

    form_args = {
        'neighbor': {
            'label': 'Endereço IP',
            'validators': [InputRequired(), IPAddress(ipv6=True, ipv4=False)],
            'description': 'Digite um IPv6 válido (ex: 2001:db8::1)'
        }
    }


class LogoutLink(MenuLink):
    def get_url(self):
        return url_for('auth_bp.logout')


class AppLink(MenuLink):
    def get_url(self):
        return url_for('int_summary_bp.interface_summary')


class UploadsFileAdmin(FileAdmin):
    def is_accessible(self):
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('auth_bp.login'))

    # permissions
    can_upload = can_download = can_delete = True
    can_mkdir = can_rename = True
    can_delete_dirs = False

    # config files
    allowed_extensions = editable_extensions = ('txt', 'csv')
    max_file_size = 10 * 1024 * 1024  # 10MB


def flask_admin():
    admin.name = 'auto.clickip.local'
    admin.base_path = os.path.join(os.path.dirname(__file__), 'static')
    admin.base_url = '/static/'

    admin.add_view(UserView(Users, db.session))

    admin.add_view(OltView(Olts, db.session, name='OLTs', category='Ativos'))
    admin.add_view(RouterView(Routers, db.session, category='Ativos'))
    admin.add_view(SwitchView(Switches, db.session, category='Ativos'))

    admin.add_view(BgpNeighborIpv4View(NeighborBgpIpv4, db.session, category='Neighbor'))
    admin.add_view(BgpNeighborIpv6View(NeighborBgpIpv6, db.session, category='Neighbor'))

    admin.add_view(UploadsFileAdmin(base_path=admin.base_path, name='Uploads'))

    admin.add_link(AppLink(name='App', category=''))
    admin.add_link(LogoutLink(name='Logout', category=''))
