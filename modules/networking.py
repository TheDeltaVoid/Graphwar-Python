import socket as s
import threading
import time

from modules.encryption import *

DEFAULT_PORT = 59879

class Server:
    def __init__(self, recv_callback):
        self.hostname = s.gethostname()

        self.socket = s.socket()

        self.connection_thread = None
        self.recv_thread = None
        self.send_thread = None

        self.connection, self.addr = None, None
        self.connected = False

        self.run = True
        self.recv_callback_func = recv_callback

    def start(self):
        self.socket.bind(("0.0.0.0", DEFAULT_PORT))

        self.connection_thread = threading.Thread(target=self.listen)
        self.connection_thread.start()

    def fire(self, function: str):
        self.send_thread = threading.Thread(target=self.send, args=(function,))
        self.send_thread.start()

    def send(self, text: str):
        if self.connected:
            data = text.encode()
            print("SERVER SEND: ", text, " | ", self.addr)
            self.connection.send(data)

    def start_recv(self):
        self.recv_thread = threading.Thread(target=self.recv)
        self.recv_thread.start()

    def recv(self):
        while self.run:
            if self.connected:
                try:
                    self.connection.settimeout(1)
                    data = self.connection.recv(1024)
                    text = data.decode()

                    print("SERVER RECV: ", text)
                    self.recv_callback(text)

                except Exception:
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

            except Exception:
                continue

    def close(self):
        if self.connected:
            self.run = False

            if self.recv_thread != None:
                self.recv_thread.join()

            if self.send_thread != None:
                self.send_thread.join()

            self.connection.close()
            self.connected = False

        else:
            self.run = False

            if self.connection_thread != None:
                self.connection_thread.join()

        print("SERVER CLOSED")

class Client:
    def __init__(self, recv_callback, hostname):
        self.hostname = hostname

        self.connection = s.socket()

        self.connection_thread = None
        self.recv_thread = None
        self.send_thread = None

        self.connected = False

        self.run = True
        self.recv_callback_func = recv_callback

    def start(self):
        self.connection_thread = threading.Thread(target=self.connect)
        self.connection_thread.start()

    def fire(self, function: str):
        self.send_thread = threading.Thread(target=self.send, args=(function,))
        self.send_thread.start()

    def send(self, text: str):
        if self.connected:
            data = text.encode()
            print("CLIENT SEND: ", text, " | ", (self.connection.getpeername()))
            self.connection.send(data)

    def start_recv(self):
        self.recv_thread = threading.Thread(target=self.recv)
        self.recv_thread.start()

    def recv(self):
        while self.run:
            if self.connected:
                try:
                    self.connection.settimeout(1)
                    data = self.connection.recv(1024)
                    text = data.decode()

                    print("CLIENT RECV: ", text)
                    self.recv_callback(text)

                except Exception:
                    continue

    def recv_callback(self, text: str):
        print(text)
        self.recv_callback_func(text)

    def connect(self):
        time_n = time.time()
        time_l = time.time()
        while self.run:
            time_n = time.time()
            print(time_n - time_l)
            time_l = time_n
            try:
                print("CLIENT CONNECTING: ", (self.hostname, DEFAULT_PORT))
                self.connection.settimeout(1)
                self.connection.connect((self.hostname, DEFAULT_PORT))

                self.connected = True
                print("CLIENT CONNECTED: ", (self.connection.getpeername()))

            except Exception as e:
                print(e)
                time.sleep(1)
                continue

    def close(self):
        if self.connected:
            self.run = False

            if self.recv_thread != None:
                self.recv_thread.join()

            if self.send_thread != None:
                self.send_thread.join()

            self.connection.close()
            self.connected = False

        else:
            self.run = False

            if self.connection_thread != None:
                self.connection_thread.join()

        print("CLIENT CLOSED")
