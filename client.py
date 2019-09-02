import socket

host = "localhost"
port = 5000

sock = socket.socket()
sock.connect((host, port))

while True:
    message = "hoge"
    sock.send(message.encode("UTF-8"))
    sock.close()
    break
print("complete")
