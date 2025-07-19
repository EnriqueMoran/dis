"""TBD"""

import socket

from io import BytesIO

from opendis.PduFactory import createPdu
from opendis.DataOutputStream import DataOutputStream


class MulticastManager:
    """TBD"""
    def __init__(
        self,
        multicast_group: str = "0.0.0.0",
        multicast_port: int = 3000,
        multicast_iface: str = "0.0.0.0",
        ttl: int = 2,
    ) -> None:
        self.multicast_group = multicast_group
        self.multicast_port = multicast_port
        self.multicast_iface = multicast_iface
        self.ttl = ttl
        self.sock = None
        self.listeners = []

    def create_connection(self) -> None:
        """TBD"""
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, self.ttl)
        self.sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_LOOP, 0)
        # self.sock.setsockopt(socket.SOL_SOCKET, socket.IP_MULTICAST_TTL, self.ttl)
        self.sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_IF,
                              socket.inet_aton(self.multicast_iface))
        self.sock.bind((self.multicast_group, self.multicast_port))

    def send_pdu(self, pdu) -> None:
        """TBD"""
        memory_stream = BytesIO()
        output_stream = DataOutputStream(memory_stream)
        pdu.serialize(output_stream)
        data = memory_stream.getvalue()
        self.sock.sendto(data, (self.multicast_group, self.multicast_port))
    
    def add_listener(self, listener) -> None:
        self.listeners.append(listener)
    
    def receive_pdu(self) -> None:
        """TBD"""
        while True:
            data = self.sock.recv(1024)
            pdu = createPdu(data)
            for listener in self.listeners:
                listener.on_pdu_received(pdu)