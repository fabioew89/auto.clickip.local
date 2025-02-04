from rich import print
from netmiko import ConnectHandler


def mpls_seg_one(hostname, username, password, vlan, description, ipv4_neighbor): # noqa E501
    switch = {
        'device_type': 'cisco_ios',
        'host': hostname,
        'username': username,
        'password': password,
        'port': 22,
        'verbose': True,
        'global_delay_factor': 2,
        'read_timeout_override': 5,
    }

    try:
        ssh = ConnectHandler(**switch)
        print(f'[green]Conectado ao {hostname}✅[/green]')

        output = ssh.send_command('show mpls l2vpn vpls brief', expect_string=r'#') # noqa E501

        ssh.send_command('config exclusive', expect_string=r'#')

        ssh.send_command(  # descricao do VPLS
            f'mpls l2vpn vpls-group tunnel-{vlan}           \
                vpn {description}                           \
                    description "{description}" ;           \
                administrative-status up', expect_string=r'#'d
            )

        ssh.send_command(
            f'mpls l2vpn vpls-group tunnel-{vlan}           \
            vpn {description} ;                             \
                vfi                                         \
                    pw-type vlan {vlan} ;                   \
                    neighbor {ipv4_neighbor} pw-id {vlan} ; \
                    pw-mtu 1600 ;                           \
                    pw-load-balance                         \
                        flow-label both', expect_string=r'#'
            )

        ssh.send_command(
            f'mpls l2vpn vpls-group tunnel-{vlan}           \
            vpn {description} ;                             \
                bridge-domain                               \
                    dot1q {vlan} ;                          \
                    access-interface ten-gigabit-ethernet-1/1/1', expect_string=r'#' # noqa E501
            )

        ssh.send_command('commit confirmed 3; top', expect_string=r'#')

        output = ssh.send_command(f'show mpls l2vpn vpls-group brief | include {vlan}', expect_string=r'#') # noqa E501

        print(output)

    except Exception as e:
        print(f'Erro ao executar comandos:{e}❌')
        output = None

    finally:
        ssh.disconnect()
        print(f'[yellow]Desconectado do {hostname}⚠️[/yellow]')

    return output


mpls_seg_one(
    hostname='100.127.0.254',
    username='auto.noc',
    password='3#ed$32wSEd5',
    vlan='101',
    description='NETMIKO',
    ipv4_neighbor='100.127.0.3',
)
