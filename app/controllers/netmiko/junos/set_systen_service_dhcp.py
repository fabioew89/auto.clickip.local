import os
import sys
import config
from rich import print
from netmiko import ConnectHandler

# Corrige o caminho para encontrar config.py
config_path = os.path.abspath("app/controllers/netmiko/junos")
sys.path.append(config_path)

def set_access_address_assignment(vlan_id, ipv4_gateway, pool_name, network, address_low, address_high):  # noqa E501
    """Configura o serviço DHCP no roteador Junos via Netmiko."""

    router = {
        'device_type':      config.DEVICE_TYPE,
        'host':             config.HOSTNAME,
        'username':         config.USERNAME,
        'password':         config.PASSWORD,
        'port':             config.PORT,
        'timeout':          config.TIMEOUT,
        'session_timeout':  config.SESSION_TIMEOUT,
    }

    try:
        ssh = ConnectHandler(**router)
        print(f'[green]Conectado ao {config.HOSTNAME} ✅[/green]')
        print(ssh.find_prompt()+'\n')

        commands = [
            f'set interfaces ae0 unit {vlan_id} vlan-id {vlan_id} description "{pool_name}" family inet address {ipv4_gateway}/21',                                     # noqa E501
            f'set system services dhcp-local-server group DHCP-IPHOST-WIRE interface ae0.{vlan_id}',                                                                    # noqa E501
            f'set access address-assignment pool {pool_name} family inet network {network}/21',                                                                         # noqa E501
            f'set access address-assignment pool {pool_name} family inet range address low {address_low}',                                                              # noqa E501
            f'set access address-assignment pool {pool_name} family inet range address high {address_high}',                                                            # noqa E501
            f'set access address-assignment pool {pool_name} family inet dhcp-attributes maximum-lease-time 604800',                                                    # noqa E501
            f'set access address-assignment pool {pool_name} family inet dhcp-attributes server-identifier {ipv4_gateway}',                                             # noqa E501
            f'set access address-assignment pool {pool_name} family inet dhcp-attributes router {ipv4_gateway}',                                                        # noqa E501
            f'set access address-assignment pool {pool_name} family inet dhcp-attributes option 43 string "http://172.25.200.38:7547 dmview dmview datacom datacom"',   # noqa E501
        ]

        ssh.send_config_set(commands, read_timeout=15)
        ssh.commit()

        # Executa os comandos de verificação corretamente
        output = [
            ssh.send_command(f'run show configuration interfaces ae0 unit {vlan_id}\n'),             # noqa E501
            ssh.send_command(f'run show configuration access address-assignment pool {pool_name}'),  # noqa E501
        ]

        # Exibe a saída formatada corretamente
        for line in output:
            print(line)

    except Exception as e:
        import traceback
        print(f'[red]Erro ao executar comandos:❌[/red]\n{e}')
        print(traceback.format_exc())
        output = None

    finally:
        ssh.disconnect()
        print(f'[yellow]Desconectado do {config.HOSTNAME} ⚠️[/yellow]')

    return output


# CALL TO ACTION
set_access_address_assignment(
    vlan_id=input('Digite o ID da VLAN: '),
    network=input('Digite o endereço de rede: '),
    ipv4_gateway=input('Digite o gateway IPv4: '),
    address_low=input('Digite o endereço IP baixo: '),
    address_high=input('Digite o endereço IP alto: '),
    pool_name=input('Digite o nome do pool: '),
)
