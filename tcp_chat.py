

import sys
import os
import argparse
import threading

# Custom modules
sys.path.append("./libs/")
from connections import *

# Client Server Chat


def main(args):
    # Global Variables
    msg_history = []
    username = args.username

    conn = connect(args.host, args.port, args.client)
    print(username+": ", end="", flush=True)

    # Thread sempre para ouvir // Enviar msg para ip
    message_listener_thread = threading.Thread(
        target=message_listener, args=(conn, msg_history, username))
    message_listener_thread.daemon = True
    message_listener_thread.start()

    while True:
        try:
            # Depois nao vai ser preciso enviar username, isto é so um workaround, o servidor tratará disto i think, ou depende do chat escolhido
            send_msg(conn, username, msg_history)
        except Exception as e:
            if(args.debug == 1):
                print(msg_history)
                print("Username escolhido foi: " + args.username)
                if e:
                    print(e)
            sys.exit(0)


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

    main(args)
