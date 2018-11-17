import unittest
import socket
from json import JSONDecodeError
from select import select

from .. import connection

class TestConnectionListener(unittest.TestCase):
    def setUp(self):
        self.listener = connection.ConnectionListener()

    def tearDown(self):
        self.listener.close()

    def test_accept(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((socket.gethostname(), 4801))
        self.assertEqual(select([], [sock], [], 0), ([], [sock], []))

        accepted = self.listener.accept()
        self.assertEqual(accepted.sock.getsockname(), sock.getpeername())

        accepted.close()
        sock.shutdown(socket.SHUT_RDWR)
        sock.close()

class TestConnection(unittest.TestCase):
    def setUp(self):
        self.listener = connection.ConnectionListener()
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((socket.gethostname(), 4801))
        self.connection = self.listener.accept()
        self.assertNotEqual(self.connection, None)

    def tearDown(self):
        self.listener.close()
        self.connection.close()
        self.client.shutdown(socket.SHUT_RDWR)
        self.client.close()

    def test_recv_timeout(self):
        self.assertEqual(self.connection.recv(0), None)

    def test_recv_unformatted(self):
        self.client.send(b'test\n')
        self.assertRaises(JSONDecodeError, self.connection.recv, 0.5)

    def test_recv_incomplete(self):
        self.client.send(b'{"test": 1}')
        self.assertEqual(self.connection.recv(0.5), None)

    def test_recv_complete(self):
        self.client.send(b'{"test": 1}\n')
        self.assertEqual(self.connection.recv(0.5), {'test': 1})
    
    def test_recv_complete_plus(self):
        self.client.send(b'{"test": 1}\n{"test": 2}\n{"test": 3}')
        self.assertEqual(self.connection.recv(0.5), {'test': 1})
        self.assertEqual(self.connection.recv(0.5), {'test': 2})
        self.assertEqual(self.connection.recv(0.5), None)
