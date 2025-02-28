from netmiko import ConnectHandler


def no_downstream_fec(hostname, username, password, chassis, slot, port_id):
    device = {
        'device_type': 'cisco_ios',
        'host': hostname,
        'username': username,
        'password': password,
        'port': 22,  # Porta SSH padrão
        'timeout': 30,  # Timeout de 30 segundos para a conexão
        'session_timeout': 30,  # Tempo máximo para a sessão SSH
    }

    commands = [
        'config',
        'interface gpon 1/1/8 ; no downstream-fec',
        'commit and-quit | suppress-validate-warning-prompt',
        'show interface gpon 1/1/8',
    ]

    try:
        ssh = ConnectHandler(**device)
        print(f'[green]Conectado ao Switch {ssh.find_prompt()} - {hostname} ✅[/green]')

        for command in commands:
            output = ssh.send_command(command, expect_string=r'#', read_timeout=15)
            print(output)

    except Exception as e:
        print(f'Erro ao executar comandos:{e}❌')
        output = None

    finally:
        ssh.disconnect()
        print(f'[yellow]Desconectado: {hostname} ⚠️[/yellow]')

    return output
