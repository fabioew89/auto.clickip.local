import logging
from app import create_app
from netmiko import ConnectHandler


def get_mpls_brief(hostname, username, password, vlan):
    app = create_app()
    logger = logging.getLogger(__name__)

    switch = {
        'device_type': 'cisco_ios',
        'host': hostname,
        'username': username,
        'password': password,
        'port': app.config.get('NETMIKO_PORT', 22),
        'timeout': app.config.get('NETMIKO_TIMEOUT', 30),
        'session_timeout': app.config.get('NETMIKO_SESSION_TIMEOUT', 60),
        'fast_cli': False
    }

    try:
        with ConnectHandler(**switch) as ssh:
            logger.info(f"Conexão estabelecida com {hostname}")

            output = ssh.send_command(
                f'show mpls l2vpn vpls-group brief | include {vlan}',
                expect_string=r'#',
                read_timeout=app.config.get('NETMIKO_TIMEOUT', 30)
            )

            return True, output.strip(), None

    except Exception as e:
        error_msg = f"Erro não esperado em {hostname}: {str(e)}"
        logger.error(error_msg, exc_info=True)
        return False, None, error_msg
    finally:
        ssh.disconnect()

    return output
