from . import AddressValueError

import re

BINARY_RE = re.compile(r'^[0-1]{32}$')
IPv4_ADDR_RE = re.compile(r'^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$')

def binary_to_ipv4(binary):
    if not BINARY_RE.match(binary):
        raise ValueError(binary + ' is not a binary address')

    return IPv4Address('.'.join([ str(int(binary[bit:bit+8], 2)) for bit in range(0, 32, 8) ]))

class IPv4Address:
    def __init__(self, address):
        if not self._verify_address(address):
            raise AddressValueError(address)
        self._address = address
    
    def _verify_address(self, address):
        if IPv4_ADDR_RE.match(address):
            return True
        return False
    
    def __str__(self):
        return self._address

    def __octets__(self):
        return tuple(map(int, self._address.split('.')))

    def __binary__(self):
        return ''.join([ '0'*(8-len(bin(octet)[2:])) + bin(octet)[2:] for octet in self.__octets__() ])
