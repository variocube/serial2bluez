from serial import Serial


def read_serial(port: str):
    print(f"Reading from serial port {str}")
    serial = Serial(
        port=port,
        baudrate=115200,
        bytesize=8,
        parity='N',
        stopbits=1,
    )
    with serial:
        while True:
            try:
                read = serial.read(1)
                if read is None:
                    raise EOFError("serial.read() returned None")
                yield read.decode("ascii")
            except Exception as err:
                print(f"Error reading serial port: {err}")
                break
