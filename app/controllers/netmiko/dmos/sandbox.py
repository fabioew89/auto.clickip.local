vpls = '''vpls-group tunnel-{vlan}
vpn {vlan}
vfi
pw-type vlan
neighbor {ipv4_neighbor}
pw-id {vlan}
pw-mtu {pw-mtu}
pw-load-balance
flow-label both
!
!
!
bridge-domain
dot1q {vlan}
access-interface ten-gigabit-ethernet-1/1/7
!
!
!
!
!
'''
print(vpls)
print(vpls.splitlines())
print(type(vpls))