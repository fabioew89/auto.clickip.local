import os
from netmiko import ConnectHandler


# Retrieves the interface summary from a Juniper device
def get_interface_ae0_summary(hostname, username, password):
    router = {
        'device_type': 'juniper',
        'host': hostname,
        'username': username,
        'password': password,
        'port': os.getenv('NETMIKO_PORT'),
        'timeout': os.getenv('NETMIKO_TIMEOUT'),
        'session_timeout': os.getenv('NETMIKO_SESSION_TIMEOUT'),
    }

    ssh = ConnectHandler(**router)
    output = ssh.send_command('show interfaces terse lo0 | match lo')
    ssh.disconnect()
    return output
