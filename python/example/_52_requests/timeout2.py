import socket


IP = '0.0.0.0'
PORT = 8080
ADDR = (IP, PORT)


def make_dummy_message(len):
    ret = ""
    for i in range(0, len):
        ret = ret + 'A'
    return ret

head_data = f"""HTTP/1.1 200 OK

Server: Werkzeug/2.2.2 Python/3.8.10
Date: Sat, 14 Oct 2023 01:43:25 GMT
Content-Type: text/html; charset=utf-8
Content-Length: 100000000
Connection: close

<!doctype html>
<html lang=en>
"""

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
    server_socket.bind(ADDR)
    server_socket.listen()
    print(f"listen [{ADDR}]")

    while True:
        client_socket, client_addr = server_socket.accept()
        print(f"accept [{client_addr}]")
        # msg = client_socket.recv(SIZE)
        print(head_data)
        client_socket.sendall(head_data.encode())
        for i in range(1, 100):
            print(f"send {i}")
            client_socket.sendall(make_dummy_message(1000000).encode())

        client_socket.close()