import socket
import json
from select import select
from time import time

class ConnectionListener:
    """
    Socket that listens for new connections from clients.
    """
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setblocking(0)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((socket.gethostname(), 4801))
        self.sock.listen(5)

    def accept(self):
        acceptable, _, _ = select([self.sock], [], [], 0)
        if acceptable == [self.sock]:
            client_sock, _ = self.sock.accept()
            return Connection(client_sock)
        else:
            return None

    def close(self):
        self.sock.close()

class Connection:
    """
    Wraps a socket connection to send and receive dictionaries.
    """
    def __init__(self, sock):
        self.sock = sock
        self.sock.setblocking(0)
        self.buffer = []

    def recv(self, time_limit):
        end_time = time() + time_limit
        chunks = []
        chunk = b''
        # Read in any previously buffered messages
        if len(self.buffer) > 1:
            # Buffered complete message
            message = self.buffer.pop(0).decode('utf-8')
            return json.loads(message)
        elif len(self.buffer) == 1:
            # Buffered incomplete message
            chunks.append(self.buffer.pop())

        # Buffer will be empty at this point
        readable, _, _ = select([self.sock], [], [], max(end_time - time(), 0))
        # At this point there are 5 possible outcomes:
        # 1. Socket is not readable within the time limit
        # 2. Client does not send a complete message within the time limit
        # 3. Client connection closes
        # 4. Client sends one complete message
        # 5. Client sends one complete message and more
        while readable == [self.sock] and time() < end_time:
            chunk = self.sock.recv(2048)
            if chunk == b'':
                # Connection closed
                raise RuntimeError('Socket connection broken')
            if b'\n' in chunk:
                # At least one complete message received
                delimited = chunk.split(b'\n')
                chunks.append(delimited[0])
                self.buffer.extend(delimited[1:])
                message = b''.join(chunks).decode('utf-8')
                return json.loads(message)
            chunks.append(chunk)
            readable, _, _ = select([self.sock], [], [], max(end_time - time(), 0))

        # No/incomplete message received within time limit
        self.buffer = []
        return None

    def send(self, data, time_limit):
        end_time = time() + time_limit
        # TODO: Ensure data is of correct type and structure
        message = str.encode(json.dumps(data))
        total_sent = 0
        _, writable, _ = select([], [self.sock], [], max(end_time - time(), 0))
        while total_sent < len(message) and writable == [self.sock] and time() < end_time:
            sent = self.sock.send(message[total_sent:])
            if sent == 0:
                raise RuntimeError('Socket connection broken')
            total_sent += sent
            _, writable, _ = select([], [self.sock], [], max(end_time - time(), 0))
        if writable == [self.sock]:
            sent = self.sock.send(b'\n')
            if sent == 0:
                raise RuntimeError('Socket connection broken')
            total_sent += sent
        if total_sent != len(message) + 1:
            raise RuntimeError('Message not completed')

    def close(self):
        self.sock.close()

class ClientConnection(Connection):
    """
    Connection to the server.
    """
    def __init__(self, server_addr):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(server_addr)
        super().__init__(sock)
