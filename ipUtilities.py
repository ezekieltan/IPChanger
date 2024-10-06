import ipaddress

def isIPValid(ip):
    try:
        ip_obj = ipaddress.ip_address(ip)
        return True
    except ValueError:
        return False

def cidrToSubnetMask(cidr):
    binaryMask = '1' * cidr + '0' * (32 - cidr)
    octets = [int(binaryMask[i:i + 8], 2) for i in range(0, 32, 8)]
    subnetMask = '.'.join(map(str, octets))
    return subnetMask

def inputChecks(enteredIP, cidr, enteredGateway, setGateway):

    # Basic syntax checks
    if not isIPValid(enteredIP):
        return 'IP Invalid'
    if setGateway and not isIPValid(enteredGateway):
        return 'Gateway Invalid'
    if not (0 <= cidr <= 32):
        return 'CIDR must be between 0 and 32.'

    # Further sanity checks
    subnetMask = cidrToSubnetMask(cidr)
    intendedIP = ipaddress.ip_address(enteredIP)
    network = ipaddress.ip_network(f"{enteredIP}/{subnetMask}", strict=False)
    if setGateway:
        gatewayIP = ipaddress.ip_address(enteredGateway)

    if enteredIP.startswith("127."):
        return 'IP cannot be in 127.0.0.0/8'
    if enteredGateway.startswith("127."):
        return 'Gateway cannot be in 127.0.0.0/8'
    if setGateway and gatewayIP not in network:
        return "Gateway not in subnet mask"
    if intendedIP == network.network_address:
        return "IP cannot be the network address."
    if intendedIP == network.broadcast_address:
        return "IP cannot be the broadcast address."
    if setGateway and gatewayIP == network.network_address:
        return "Gateway cannot be the network address."
    if setGateway and gatewayIP == network.broadcast_address:
        return "Gateway cannot be the broadcast address."

    return "OK"
