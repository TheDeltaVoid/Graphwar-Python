import socket as s
import threading
import time

from modules.encryption import *

DEFAULT_PORT = 59879

class Server:
    def __init__(self, recv_callback):
        self.hostname = s.gethostname()

        self.socket = s.socket(s.AF_INET, s.SOCK_STREAM)

        self.connection_thread = None
        self.recv_thread = None
        self.send_thread = None

        self.connection, self.addr = None, None
        self.connected = False

        self.run = True
        self.recv_callback_func = recv_callback

        self.shuld_close = False
        self.closed = False

    def update(self, delta_time: float):
        if self.shuld_close and not self.connected:
            self.close()

    def start(self):
        self.socket.bind(("0.0.0.0", DEFAULT_PORT))

        self.connection_thread = threading.Thread(target=self.listen)
        self.connection_thread.start()

    def send(self, text: str):
        self.send_thread = threading.Thread(target=self._send, args=(text,))
        self.send_thread.start()

    def _send(self, text: str):
        if self.connected and not self.shuld_close:
            data = text.encode()
            print("SERVER SEND: ", text, " | ", self.addr)
            self.connection.send(data)

    def start_recv(self):
        if self.recv_thread == None:
            self.recv_thread = threading.Thread(target=self.recv)
            self.recv_thread.start()

    def recv(self):
        while self.run and not self.shuld_close:
            if self.connected:
                try:
                    self.connection.settimeout(1)
                    data = self.connection.recv(1024)
                    text = data.decode()

                    print("SERVER RECV: ", text)
                    if text != "CLOSE":
                        self.recv_callback(text)

                    else:
                        self.shuld_close = True

                except s.timeout:
                    continue

    def recv_callback(self, text: str):
        self.recv_callback_func(text)

    def listen(self):
        while self.run:
            try:
                self.socket.settimeout(1)
                self.socket.listen(1)
                print("SERVER LISTEN: ", (self.hostname, DEFAULT_PORT))
                self.connection, self.addr = self.socket.accept()

                self.connected = True
                print("SERVER CONNECTED: ", self.addr)
                break

            except s.timeout:
                continue

    def close(self):
        if self.closed:
            return
        
        if self.connected:
            self.run = False

            self._send("CLOSE")

            if self.recv_thread != None:
                self.recv_thread.join()

            if self.send_thread != None:
                self.send_thread.join()

            self.connection.close()
            self.connected = False
            
            self.closed = True
            print("SERVER CLOSED")

        else:
            self.run = False

            if self.connection_thread != None:
                self.connection_thread.join()

            self.closed = True
            print("SERVER CLOSED")

class Client:
    def __init__(self, recv_callback, hostname):
        self.hostname = hostname

        self.connection = s.socket(s.AF_INET, s.SOCK_STREAM)

        self.connection_thread = None
        self.recv_thread = None
        self.send_thread = None

        self.connected = False

        self.run = True
        self.recv_callback_func = recv_callback

        self.shuld_close = False
        self.closed = False

    def update(self, delta_time: float):
        if self.shuld_close:
            self.close()

    def start(self):
        self.connection_thread = threading.Thread(target=self.connect)
        self.connection_thread.start()

    def send(self, text: str):
        self.send_thread = threading.Thread(target=self._send, args=(text,))
        self.send_thread.start()

    def _send(self, text: str):
        if self.connected and not self.shuld_close:
            data = text.encode()
            print("CLIENT SEND: ", text, " | ", (self.connection.getpeername()))
            self.connection.send(data)

    def start_recv(self):
        if self.recv_thread == None:
            self.recv_thread = threading.Thread(target=self.recv)
            self.recv_thread.start()

    def recv(self):
        while self.run and not self.shuld_close:
            if self.connected:
                try:
                    self.connection.settimeout(1)
                    data = self.connection.recv(1024)
                    text = data.decode()

                    print("CLIENT RECV: ", text)
                    if text != "CLOSE":
                        self.recv_callback(text)

                    else:
                        self.shuld_close = True

                except s.timeout:
                    continue

    def recv_callback(self, text: str):
        self.recv_callback_func(text)

    def connect(self):
        while self.run:
            try:
                print("CLIENT CONNECTING: ", (self.hostname, DEFAULT_PORT))
                self.connection.settimeout(1)
                self.connection.connect((self.hostname, DEFAULT_PORT))

                self.connected = True
                print("CLIENT CONNECTED: ", (self.connection.getpeername()))
                break

            except s.timeout as e:
                self.connection = s.socket(s.AF_INET, s.SOCK_STREAM)
                self.connection.settimeout(1)
                continue

    def close(self):
        if self.closed:
            return
        
        if self.connected:
            self.run = False

            self._send("CLOSE")

            if self.recv_thread != None:
                self.recv_thread.join()

            if self.send_thread != None:
                self.send_thread.join()

            self.connection.close()
            self.connected = False

            self.closed = True
            print("CLIENT CLOSED")

        else:
            self.run = False

            if self.connection_thread != None:
                self.connection_thread.join()

            self.closed = True
            print("CLIENT CLOSED")
