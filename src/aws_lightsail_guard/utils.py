import socket


def check_address(host, port):
    socket.setdefaulttimeout(5)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    location = (host, port)
    result = sock.connect_ex(location)
    sock.close()
    return result == 0
