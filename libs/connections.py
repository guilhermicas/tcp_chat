"""
Socket connection handler

- This module handles the various client functions to communicate and receive messages with a server
"""
import socket
from ui import *

def append_msg_history(msg: str, msg_history: list):
    """
        Adiciona uma mensagem ao histórico de mensagens com um limite default = 150

        @msg <- Mensagem a adicionar no historico
        @msg_history <- Pointer para o historico de mensages
    """
    if(len(msg_history) >= 150):
        msg_history.pop()
    msg_history.append(msg)

def connect(host: str, port: int, is_client: bool):
    """
        Faz uma conexão a um IP/Porta remota

        @host <- IP Remoto
        @port <- port Remoto
    """

    socket_connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    remote_ip = ""
    if is_client:
        print(host, port)
        socket_connection.connect((host, port))
    else:
        # TODO: Criar servidor separado que remete as mensagens para o destino, este codigo irá desaparecer
        socket_connection.bind((host, port))
        socket_connection.listen(5)
        print("Á espera de conexão")
        socket_connection, remote_ip = socket_connection.accept()
        # TODO: No lado do servidor, fazer verificação se uma conexão morrer e tomar os passos adequados

    clear_terminal()
    print("Conexão estabelecida: ", remote_ip)
    return socket_connection


def message_listener(connection, msg_history: list, username: str):
    """
        Listens and receives data from connection

        @connection <- socket_connection with server
        @msg_history <- used for re-rendering the screen
        @username <- used for re-rendering the screen
    """
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
            append_msg_history(data.decode(), msg_history)
            # Printing everything
            render_screen(msg_history, username)
            # TODO: find way to use msg_history and username globally to avoid ambiguous parameters and parameter tunnels


def send_msg(connection, username: str, msg_history: list):
    """
        Crafts and sends message to server

        @connection <- socket_connection with server
        @msg_history <- used for re-rendering the screen
        @username <- used for re-rendering the screen
    """

    msg = username + ": " + input()
    append_msg_history(msg, msg_history)
    connection.send(str.encode(msg))

    render_screen(msg_history, username)
