import socket

def is_internet_available():
    net = False
    print("Checking Internet")
    try:
        # connect to the host -- tells us if the host is actually
        # reachable
        socket.create_connection(("1.1.1.1", 53))  # Checking for internet conn
        net = True
    except OSError:
        pass
    return net