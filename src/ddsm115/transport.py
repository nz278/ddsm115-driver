import serial
import threading
import time


# Serial transport to handle raw bytes
class SerialTransport:

    def __init__(self, port: str, baudrate: int = 115200, timeout: float = 0.5):
        self.serial = serial.Serial(
            port=port,
            baudrate=baudrate,
            bytesize=serial.EIGHTBITS,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            timeout=timeout,
        )

        self._lock = threading.Lock()

    # Send raw bytes to motor, question/response format
    def write(self, data: bytes, read_reply: bool = True, reply_size: int = 10):
        with self._lock:
            self.serial.reset_input_buffer()
            self.serial.write(data)
            self.serial.flush()

            print("TX:", data.hex(" "))
            time.sleep(0.001)

            if not read_reply:
                return None

            reply = self.serial.read(reply_size)
            print("RX:", reply.hex(" "))
            return reply

    def close(self):
        with self._lock:
            if self.serial.is_open:
                self.serial.close()
