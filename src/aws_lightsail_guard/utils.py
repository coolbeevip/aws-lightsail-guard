import socket


def check_address(host, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    location = (host, port)
    result = sock.connect_ex(location)
    sock.close()
    return result == 0
