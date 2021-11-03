import socket
import threading
import argparse
import os
from sys import exit

# Client Server Chat


def connect(host: str, port: int, client: str):
    """
    Faz uma conexão a um IP/Porta remota

    @host <- IP Remoto
    @port <- port Remoto
    """

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    if client == "1":
        s.connect((host, port))
    else:
        s.bind((host, port))
        s.listen(5)
        # TODO: Melhorar esta parte
        print("Á espera de conexão")
        s, ender = s.accept()
        print("Conexão estabelecida: ", ender)
    return s


def message_listener(connection):
    # TODO: deve de haver melhor forma de ver se uma mensagem foi recebida
    while True:
        BUFF_SIZE = 1024
        data = b""

        while True:
            part = connection.recv(BUFF_SIZE)
            data += part
            if len(part) < BUFF_SIZE:
                # either 0 or end of data
                break

        if data != b"":
            os.system("clear")
            print(data.decode() + "\ngui: ", flush=True)


def send_msg(connection, username):
    msg = input(username + ": ")
    connection.send(str.encode(username + ": " + msg))


def main(args):
    conn = connect(args.host, args.port, args.client)

    # Thread sempre para ouvir // Enviar msg para ip
    message_listener_thread = threading.Thread(
        target=message_listener, args=(conn,))
    message_listener_thread.daemon = True
    message_listener_thread.start()

    while True:
        send_msg(conn, args.username)
#        exit(0)


if __name__ == "__main__":
    parser = argparse.ArgumentParser("Aplicação de chat com socket TCP")
    parser.add_argument(
        "--username", help="IP onde a conexão será estabelecida", required=True)
    parser.add_argument(
        "--host", help="IP onde a conexão será estabelecida", required=True)
    parser.add_argument(
        "--port", help="Porta onde a conexão será estabelecida", required=True)
    parser.add_argument(
        "--client", help="1 se cliente, 0 se servidor", required=True)
    args = parser.parse_args()
    args.port = int(args.port)
    main(args)
