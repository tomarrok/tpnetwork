from . import IPv4Address, binary_to_ipv4, NetworkValueError

import re

IPv4_NETADDR_RE = re.compile(r'^(?:((?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\/(?:((?:([1-9]|[1-2][0-9]|3[0-2]))|(?:((0\.0\.0\.0)|(((1(28|92))|(2((24)|(4(0|8))|(5(2|4)))))\.0\.0\.0)|(255\.((0\.0\.0)|(((1(28|92))|(2((24)|(4(0|8))|(5(2|4)))))\.0\.0)|(255\.((0\.0)|(((1(28|92))|(2((24)|(4(0|8))|(5(2|4)))))\.0)|(255\.(0|(1(28|92))|(2((24)|(4(0|8))|(5(2|4|5))))))))))))))))$')

class IPv4Network:
    def __init__(self, net_address):
        if not self._verify_network(net_address):
            raise NetworkValueError(net_address)
        self._net_address = net_address
        self._address = self._net_address.split('/')[0]
        self._netmask = self._net_address.split('/')[1]
        self._cidr = 0

        if '.' in self._netmask:
            self._set_cidr()
        else:
            self._cidr = int(self._netmask)
            self._set_netmask()
    
    def _verify_network(self, net_address):
        if IPv4_NETADDR_RE.match(net_address):
            return True
        return False
    
    def _set_netmask(self):
        self._netmask = str(binary_to_ipv4('1' * (self._cidr) + '0' * (32 - self._cidr)))
    
    def _set_cidr(self):
        self._cidr = self.__binary__()[1].count('1')
    
    def get_netinfo(self):
        netaddr_bin = self.__binary__()
        net_prefix_index = self._cidr

        network_bin = netaddr_bin[0][:net_prefix_index] + '0' * (32 - net_prefix_index)
        broadcast_bin = netaddr_bin[0][:net_prefix_index] + '1' * (32 - net_prefix_index)
        first_addr_bin = network_bin[:-1] + '1'
        last_addr_bin = broadcast_bin[:-1] + '0'
        
        return {
            'network': binary_to_ipv4(network_bin),
            'first': binary_to_ipv4(first_addr_bin),
            'last': binary_to_ipv4(last_addr_bin),
            'broadcast': binary_to_ipv4(broadcast_bin)
            }
    
    def __str__(self):
        return self._address + '/' + str(self._cidr)

    def __octets__(self):
        return (tuple(map(int, self._address.split('.'))), tuple(map(int, self._netmask.split('.'))))
    
    def __binary__(self):
        return (
            ''.join([ '0'*(8-len(bin(octet)[2:])) + bin(octet)[2:] for octet in self.__octets__()[0] ]),
            ''.join([ '0'*(8-len(bin(octet)[2:])) + bin(octet)[2:] for octet in self.__octets__()[1] ])
            )
