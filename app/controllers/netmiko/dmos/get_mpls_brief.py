from netmiko import ConnectHandler


def get_mpls_l2vpn_vpls_brief_oficial(hostname, username, password, tunnel_vlan):
    switch = {
        'device_type': 'cisco_ios',
        'host': hostname,
        'username': username,
        'password': password,
    }

    comando = f'show mpls l2vpn vpls-group brief | include {tunnel_vlan}'
    ssh = None
    output = None

    try:
        ssh = ConnectHandler(**switch)
        output = ssh.send_command(comando, expect_string=r'#')
    except Exception as e:
        print(f'Erro ao executar o comando em {hostname}: {e}')
        output = None
    finally:
        if ssh:
            ssh.disconnect()

    return output
