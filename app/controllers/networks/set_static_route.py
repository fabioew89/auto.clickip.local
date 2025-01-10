from netmiko import ConnectHandler


# Cria um rota estatica em um dispositivo Juniper
def set_static_route(hostname, username, password, network_dest, next_hop):
    router = {
        'device_type': 'juniper',
        'host': hostname,
        'username': username,
        'password': password,
    }
    ssh = ConnectHandler(**router)
    output = ssh.send_command(f'set routing-options static route {network_dest} next-hop {next_hop}')  # noqa: E501
    ssh.disconnect()
    return output
