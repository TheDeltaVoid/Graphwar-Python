import socket as s
import threading

from encryption import *

class Server:
    def __init__(self, recv_callback):
        self.socket = s.socket()
        self.socket.bind(("localhost", 10))

        self.connection_thread = threading.Thread(target=self.listen)
        self.connection_thread.start()

        self.recv_thread = None
        self.send_thread = None

        self.connection, self.addr = None, None
        self.connected = False

        self.run = True
        self.recv_callback_func = recv_callback

    def fire(self, function: str):
        self.send_thread = threading.Thread(target=self.send, args=(function,))
        self.send_thread.start()

    def send(self, text: str):
        if self.connected:
            data = text.encode()
            self.connection.send(data)

    def start_recv(self):
        self.recv_thread = threading.Thread(target=self.recv)
        self.recv_thread.start()

    def recv(self):
        if self.connected:
            while self.run:
                data = self.connection.recv(1024)
                text = data.decode()

                self.recv_callback(text)

    def recv_callback(self, text: str):
        print(text)
        self.recv_callback_func(text)

    def listen(self):
        self.socket.listen(1)
        self.connection, self.addr = self.socket.accept()
        self.connected = True

    def close(self):
        if self.connected:
            self.run = False

            if self.recv_thread != None:
                self.recv_thread.join()

            if self.send_thread != None:
                self.send_thread.join()

            self.connection.close()
            self.connected = False

class Client:
    def __init__(self, recv_callback):
        self.connection = s.socket()

        self.connection_thread = threading.Thread(target=self.connect)
        self.connection_thread.start()

        self.recv_thread = None
        self.send_thread = None

        self.connected = False

        self.run = True
        self.recv_callback_func = recv_callback

    def fire(self, function: str):
        self.send_thread = threading.Thread(target=self.send, args=(function,))
        self.send_thread.start()

    def send(self, text: str):
        if self.connected:
            data = text.encode()
            self.connection.send(data)

    def start_recv(self):
        self.recv_thread = threading.Thread(target=self.recv)
        self.recv_thread.start()

    def recv(self):
        if self.connected:
            while self.run:
                data = self.connection.recv(1024)
                text = data.decode()

                self.recv_callback(text)

    def recv_callback(self, text: str):
        print(text)
        self.recv_callback_func(text)

    def connect(self):
        self.connection.connect(("localhost", 10))
        self.connected = True

    def close(self):
        if self.connected:
            self.run = False

            if self.recv_thread != None:
                self.recv_thread.join()

            if self.send_thread != None:
                self.send_thread.join()

            self.connection.close()
            self.connected = False
