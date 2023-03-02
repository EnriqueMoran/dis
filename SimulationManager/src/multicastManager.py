"""TBD"""

import socket

from io import BytesIO
from opendis.DataOutputStream import DataOutputStream

class MulticastManager:
    """TBD"""
    def __init__(self, multicast_group="0.0.0.0", multicast_port=3000, multicast_iface='0.0.0.0',
                 ttl=2):
        self.multicast_group = multicast_group
        self.multicast_port = multicast_port
        self.multicast_iface = multicast_iface
        self.ttl = ttl
        self.sock = None

    def create_connection(self):
        """TBD"""
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, self.ttl)
        # self.sock.setsockopt(socket.SOL_SOCKET, socket.IP_MULTICAST_TTL, self.ttl)
        self.sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_IF,
                              socket.inet_aton(self.multicast_iface))

    def send_pdu(self, pdu):
        """TBD"""
        memory_stream = BytesIO()
        output_stream = DataOutputStream(memory_stream)
        pdu.serialize(output_stream)
        data = memory_stream.getvalue()
        self.sock.sendto(data, (self.multicast_group, self.multicast_port))
