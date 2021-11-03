import socket
import threading
import argparse
import os
from sys import exit, platform

# Client Server Chat

# Global Variables
msg_history = []
username = "guest"


def clear_terminal():
    """
        Limpa o ecrã independentemente do Sistema Operativo
    """
    if platform in ["linux", "linux2", "darwin"]:
        os.system("clear")
    elif platform == "win32":
        os.system("cls")


def connect(host: str, port: int, client: str):
    """
        Faz uma conexão a um IP/Porta remota

        @host <- IP Remoto
        @port <- port Remoto
    """

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    if client == "1":
        s.connect((host, port))
        print(username+": ", end="", flush=True)
    else:
        s.bind((host, port))
        s.listen(5)
        # TODO: Criar servidor separado que remete as mensagens para o destino
        print("Á espera de conexão")
        s, ender = s.accept()
        print("Conexão estabelecida: ", ender)
    return s


def render_screen():
    clear_terminal()
    for msg in msg_history:
        print(msg, flush=True)
    print(username+": ", end="", flush=True)


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
            # Adding to history
            msg_history.append(data.decode())
            # Printing everything
            render_screen()

            #print(data.decode() + "\ngui: ", flush=True)


def send_msg(connection):
    #msg = input(username + ": ")
    msg = input()
    msg = username + ": " + msg
    msg_history.append(msg)
    connection.send(str.encode(msg))
    render_screen()


def main(args):
    conn = connect(args.host, args.port, args.client)

    # Thread sempre para ouvir // Enviar msg para ip
    message_listener_thread = threading.Thread(
        target=message_listener, args=(conn,))
    message_listener_thread.daemon = True
    message_listener_thread.start()

    while True:
        try:
            # Depois nao vai ser preciso enviar username, isto é so um workaround, o servidor tratará disto i think, ou depende do chat escolhido
            send_msg(conn)
        except Exception as e:
            if(args.debug == 1):
                print(msg_history)
                print("Username escolhido foi: " + args.username)
                if e:
                    print(e)
            exit(0)


if __name__ == "__main__":
    parser = argparse.ArgumentParser("Aplicação de chat com socket TCP")
    parser.add_argument(
        "--username", help="IP onde a conexão será estabelecida", default="guest")
    parser.add_argument(
        "--host", help="IP onde a conexão será estabelecida", required=True)
    parser.add_argument(
        "--port", help="Porta onde a conexão será estabelecida", required=True)
    parser.add_argument(
        "--client", help="1 se cliente, 0 se servidor", required=True)
    parser.add_argument(
        "--debug", help="1 to debug")
    args = parser.parse_args()
    args.port = int(args.port)

    # Variavel global
    username = args.username

    main(args)
