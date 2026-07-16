import serial


class SerialTransport:
    def __init__(
        self,
        port: str,
        baudrate: int = 115200,
        timeout: float = 1.0,
    ):
        self.serial = serial.Serial(
            port=port,
            baudrate=baudrate,
            timeout=timeout,
        )

    def write(self, frame: bytes, read_reply: bool = True):
        self.serial.write(frame)

        if not read_reply:
            return None

        reply = self.serial.read(10)

        if len(reply) != 10:
            raise TimeoutError(
                f"Expected 10 response bytes, received {len(reply)}"
            )

        return reply

    def close(self):
        self.serial.close()