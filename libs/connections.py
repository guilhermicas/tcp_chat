"""Socket connection handles

This module handles the various client functions to communicate and receive messages with a server
"""
import socket
from ui import *


def connect(host: str, port: int, is_client: bool):
    """
        Faz uma conexão a um IP/Porta remota

        @host <- IP Remoto
        @port <- port Remoto
    """

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    if is_client:
        print(host, port)
        s.connect((host, port))
    else:
        # TODO: Criar servidor separado que remete as mensagens para o destino, este codigo irá desaparecer
        s.bind((host, port))
        s.listen(5)
        print("Á espera de conexão")
        s, ender = s.accept()
        print("Conexão estabelecida: ", ender)
        # TODO: No lado do servidor, fazer verificação se uma conexão morrer e tomar os passos adequados
    return s


def message_listener(connection, msg_history: list, username: str):
    # TODO: deve de haver melhor forma de ver se uma mensagem foi recebida
    while True:
        BUFF_SIZE = 1024
        data = b""
        msg_history

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
            render_screen(msg_history, username)

            #print(data.decode() + "\ngui: ", flush=True)


def send_msg(connection, username: str, msg_history: list):
    #msg = input(username + ": ")
    msg = input()
    msg = username + ": " + msg
    msg_history.append(msg)
    connection.send(str.encode(msg))
    render_screen(msg_history, username)
