
# Client Server Chat

import sys
import argparse
import threading
import re

# Custom modules
sys.path.append("./libs/")
from connections import *


def main(username: str, host: str, port: int, is_client: bool):
    msg_history = []         # Used to render the messages to the screen

    socket_connection = connect(host, port, is_client)
    print(username+": ", end="", flush=True)

    # Listening for oncomming messages.
    message_listener_thread = threading.Thread(
        target=message_listener, args=(socket_connection, msg_history, username))
    message_listener_thread.daemon = True
    message_listener_thread.start()

    while True:
        try:
            # TODO: Depois nao vai ser preciso enviar username, isto é so um workaround, o servidor tratará disto dependendo do IP de quem manda a msg, ou depende do chat escolhido
            send_msg(socket_connection, username, msg_history)
        except KeyboardInterrupt:
            print("Exiting chat...")
            sys.exit(0)
        except Exception as error:
            if(args.debug == 1):
                print(msg_history)
                print(error)
            sys.exit(1)


def validate_args(args):
    # Input validation
    error_flag = False

    # Ip address validation
    if not bool(re.match("^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$", args.host)):
        print("Invalid IP address.")
        error_flag = True

    # Port validation
    if not bool(re.match("^([0-9]{1,4}|[1-5][0-9]{4}|6[0-4][0-9]{3}|65[0-4][0-9]{2}|655[0-2][0-9]|6553[0-5])$", args.port)):
        print("Invalid Port Range.")
        error_flag = True

    if args.client not in ["0", "1"]:
        print("--client option must be either 0 or 1.")
        error_flag = True

    if error_flag:
        sys.exit(1)

    args.port = int(args.port)
    is_client = True if args.client == "1" else False

    return args.username, args.host, args.port, is_client


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

    args = validate_args(args)

    main(*args)
