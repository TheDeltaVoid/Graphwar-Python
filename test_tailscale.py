import socket as s

hostname = s.gethostname()

print(hostname)

test = input()

if test != "s":
    print("SERVER")
    sock = s.socket()
    sock.bind(("0.0.0.0", 25762))
    sock.listen(1)

    conn, addr = sock.accept()

    print("connected: ", addr)

    while True:
        print(conn.recv(1024).decode())
        text = input()

        if text == "exit":
            break

        conn.send(text.encode())

else:
    hostname = input()
    print("CLIENT")
    sock = s.socket()
    sock.settimeout(1)
    
    count = 1
    while True:
        try:
            sock.connect((hostname, 25762))
            break

        except s.timeout as e:
            sock.close()
            sock = s.socket()
            sock.settimeout(1)
            print("timed out")

    print("connected: ", sock.getpeername())

    sock.settimeout(None)

    while True:
        text = input()

        if text == "exit":
            break

        sock.send(text.encode())

        print(sock.recv(1024).decode())
