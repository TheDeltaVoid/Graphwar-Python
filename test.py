from modules.networking import *

t = input()

def callback(text):
    pass

if t == "s":
    server = Server(callback)
    server.start()

    server.start_recv()

    server.send(input())
    server.close()

if t == "c":
    client = Client(callback, "localhost")
    client.start()

    client.start_recv()

    client.send(input())
    client.close()
