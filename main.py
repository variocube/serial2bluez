from select import select
from socket import socket
from _socket import SOL_SOCKET, SO_REUSEADDR, BTPROTO_L2CAP, SOCK_SEQPACKET, AF_BLUETOOTH
from dataclasses import dataclass

from bluez import BluezIface, HID_CTL_PORT, HID_INT_PORT
from keymap import keymap
from sdp import make_sdp_record


def listen(sock: socket, addr: str, port: int):
    sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    sock.settimeout(10)
    print("Binding...")
    sock.bind((addr, port))
    print("Listening...")
    sock.listen(1)


def create_socket():
    return socket(AF_BLUETOOTH, SOCK_SEQPACKET, BTPROTO_L2CAP)


@dataclass
class Client:
    ctl_sock: socket
    int_sock: socket


def accept_client(ctl_sock: socket, int_sock: socket):
    client_ctl_sock = None
    client_int_sock = None

    while True:

        print("Waiting for connections")
        (ready, _, _) = select({ctl_sock, int_sock}, [], [], 10)

        for sock in ready:
            try:
                (client_sock, peer) = sock.accept()
                client_sock.setblocking(True)
                if sock == ctl_sock:
                    print(f"Opened control socket with {peer}")
                    client_ctl_sock = client_sock
                else:
                    print(f"Opened interrupt socket with {peer}")
                    client_int_sock = client_sock
            except Exception as err:
                print(f"Failed to accept: {err}")

        if client_ctl_sock is not None and client_int_sock is not None:
            print(f"Accepted new client")
            yield Client(client_ctl_sock, client_int_sock)
            client_ctl_sock = None
            client_int_sock = None
        else:
            print(f"Incomplete socket pair: ctl={client_ctl_sock}, int={client_int_sock}")


def close_client(client: Client):
    try:
        print(f"Closing client")
        client.ctl_sock.close()
        client.int_sock.close()
    except Exception as err:
        print(f"Failed to close socket {err}")


def send_keys(client: Client, sequence: str):
    for char in sequence:
        lower_char = char.lower()
        if lower_char in keymap:
            code = keymap[lower_char]
            modifier = 0x02 if char.isupper() else 0x00
            client.int_sock.send(bytes([0xA1, 0x01, modifier, 0x00, code, 0x00, 0x00, 0x00, 0x00, 0x00]))
            client.int_sock.send(bytes([0xA1, 0x01, modifier, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]))
        else:
            print(f"Ignoring char {char}")


def main():
    iface = BluezIface(
        iface="hci0",
        alias="serial2bt",
        sdp_record=make_sdp_record("Variocube", "serial2bluez", "Serial to Bluetooth-HID bridge"),
        pairing_required=True,
        auth_required=False,
    )

    with iface:
        iface.configure()
        addr = iface.get_address()

        with create_socket() as ctl_sock, create_socket() as int_sock:
            listen(ctl_sock, addr, HID_CTL_PORT)
            listen(int_sock, addr, HID_INT_PORT)

            for client in accept_client(ctl_sock, int_sock):
                while True:
                    print("Select on client sockets")
                    (ready, _, _) = select({client.ctl_sock, client.int_sock}, [], [], 10)

                    try:
                        for sock in ready:
                            data = sock.recv(1024)

                            if not data:
                                close_client(client)
                                raise IOError("Socket closed.")

                            if sock == client.ctl_sock and data == b"\x71":
                                sock.send(b"\x00")

                        # send a key
                        print("Sending keyboard report")
                        send_keys(client, "peter")

                    except Exception as err:
                        print(f"Exception during connection: {err}")
                        print("Accepting next client")
                        break


if __name__ == '__main__':
    main()


