from flask import Flask
from app.controllers.blueprints.auth_routes.auth import auth_bp
from app.controllers.blueprints.network_routes.interface_summary import int_summary_bp
from app.controllers.blueprints.network_routes.interface_configuration import int_conf_bp
from app.controllers.blueprints.network_routes.interface_dhcp import int_dhcp_bp
from app.controllers.blueprints.network_routes.interface_static_router import int_static_route_bp
from app.controllers.blueprints.network_routes.interface_unit import int_unit_bp


def register_blueprints(app: Flask):
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(int_summary_bp, url_prefix='/network')
    app.register_blueprint(int_conf_bp, url_prefix='/network')
    app.register_blueprint(int_dhcp_bp, url_prefix='/network')
    app.register_blueprint(int_static_route_bp, url_prefix='/network')
    app.register_blueprint(int_unit_bp, url_prefix='/network')
