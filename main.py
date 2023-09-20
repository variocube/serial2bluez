#!/usr/bin/env python3

from argparse import ArgumentParser
from time import sleep

from keyboard import Keyboard
from read_serial import read_serial
from serial.tools.list_ports_linux import comports


def main():
    parser = ArgumentParser(
        prog="serial2bluez",
        description="Reads data from a serial port and sends it to a target device by emulating a bluetooth keyboard.",
    )
    parser.add_argument(
        "input",
        nargs="?",
        help="Specifies where data is read from. Default is to auto-detect a serial port. Set a specific serial port"
             " device file like `/dev/ttyUSB0` or use `stdin` or `-` to read from stdin."
    )
    args = parser.parse_args()

    keyboard = Keyboard()
    keyboard.start()

    if args.input == "stdin" or args.input == "-":
        while True:
            sequence = input("Enter keys to send: ")
            keyboard.send_keys(sequence)

    elif args.input is not None and len(args.input) > 0:
        for char in read_serial(args.input):
            keyboard.send_keys(char)

    else:
        while True:
            for port in comports():
                print(f"Found serial port {port.device}. Checking for Elatec device...")
                # Elatecs vendor id is 0x09d8. We'll assume compatibility with all their devices.
                if port.vid == 0x09d8:
                    for char in read_serial(port.device):
                        keyboard.send_keys(char)
            print("Waiting 5 seconds before checking serial ports again.")
            sleep(5)


if __name__ == '__main__':
    main()


