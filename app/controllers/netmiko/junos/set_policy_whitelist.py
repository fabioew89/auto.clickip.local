from app import create_app
from netmiko import ConnectHandler


# Cria um rota estatica em um dispositivo Juniper
def set_policy_whitelist(hostname, username, password, prefix):
    app = create_app()

    router = {
        'device_type': 'juniper',
        'host': hostname,
        'username': username,
        'password': password,
        'port': app.config.get('NETMIKO_SSH_PORT', 22),
        'timeout': app.config.get('NETMIKO_TIMEOUT', 30),
        'session_timeout': app.config.get('NETMIKO_SESSION_TIMEOUT', 60),
    }

    ssh = ConnectHandler(**router)
    ssh.send_config_set(f'set policy-options prefix-list whitelist-dst {prefix}')
    ssh.commit()

    output = ssh.send_command(f'run show configuration policy-options prefix-list whitelist-dst | display set | match {prefix}')

    ssh.disconnect()
    return output
