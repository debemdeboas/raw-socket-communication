import socket
import struct
from typing import Any, List, Tuple
import netifaces
from typing import NewType


IFACE = 'eth0'
ETH_P_ALL = 3
ETH_FRAME_SIZE = 1518
ETH_CUSTOM_PROTOCOL = 0x8044
MAC_BROADCAST = 'FF:FF:FF:FF:FF:FF'
Header = NewType('Header', bytes)

def create_and_bind_socket(iface: str) -> socket.SocketType:
    s = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.htons(ETH_P_ALL))
    s.bind((iface, 0))
    return s

def get_mac_data(iface: str) -> Tuple[List[int], str]:
    src_mac_data = netifaces.ifaddresses(iface)[netifaces.AF_LINK][0]
    src_mac_addr = [int(d, 16) for d in src_mac_data['addr'].split(':')]
    return (src_mac_addr, src_mac_data['addr'].upper())

def pack_eth_header(src: List[int], dst: List[int], packet_type: int = ETH_CUSTOM_PROTOCOL) -> Header:
    return Header(struct.pack('!6B6BH', *dst, *src, packet_type))

def unpack_eth_header(buf: Header) -> Tuple[str, str, Any]:
    if len(buf) > 14:
        buf = Header(buf[:14])
    data = struct.unpack('!6B6BH', buf)
    dst = ':'.join(f'{hex(b)[2:].upper():>02}' for b in data[:6])
    src = ':'.join(f'{hex(b)[2:].upper():>02}' for b in data[6:12])
    packet_type = data[12:14][0]
    return src, dst, packet_type

def mac_to_bytes(mac: List[str]) -> bytearray:
    data = [int(d, 16) for d in mac]
    return bytearray(data)
