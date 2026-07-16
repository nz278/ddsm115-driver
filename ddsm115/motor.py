from .protocol import build_mode_command, build_drive_command, build_frame


class DDSM115:
    def __init__(self, motor_id: int, transport, direction: int = 1):
        if not isinstance(motor_id, int) or isinstance(motor_id, bool):
            raise TypeError("Motor ID must be an integer")
        if not 0 <= motor_id <= 0xFF:
            raise ValueError("Motor ID must be in range 0 to 255")
        if direction not in (-1, 1):
            raise ValueError("Direction must be 1 or -1")

        self.motor_id = motor_id
        self.transport = transport
        self.direction = direction

    def set_id(self, motor_id: int):
        if not isinstance(motor_id, int) or isinstance(motor_id, bool):
            raise TypeError("Motor ID must be an integer")
        if not 0 <= motor_id <= 0xFF:
            raise ValueError("Motor ID must be in range 0 to 255")

        frame = bytes([0xAA, 0x55, 0x53, motor_id, 0, 0, 0, 0, 0, 0])

        for _ in range(5):
            self.transport.write(frame, read_reply=False)


    def id_query(self):
        frame = bytes([0xC8, 0x64, 0, 0, 0, 0, 0, 0, 0, 0xDE])
        return self.transport.write(frame, read_reply=True)

    def feedback_query(self):
        payload = bytes([self.motor_id, 0x74, 0, 0, 0, 0, 0, 0, 0])
        frame = build_frame(payload)
        return self.transport.write(frame, read_reply=True)

    def set_mode_position(self):
        frame = build_mode_command(self.motor_id, 0x03)
        return self.transport.write(frame, read_reply=False)

    def set_mode_velocity(self):
        frame = build_mode_command(self.motor_id, 0x02)
        return self.transport.write(frame, read_reply=False)

    def set_mode_current(self):
        frame = build_mode_command(self.motor_id, 0x01)
        return self.transport.write(frame, read_reply=False)

    def set_speed(self, rpm: int, accel: int = 0):
        if not isinstance(rpm, int) or isinstance(rpm, bool):
            raise TypeError("Speed must be an integer")
        if not -330 <= rpm <= 330:
            raise ValueError("Speed must be between -330 and 330 rpm")

        frame = build_drive_command(
            motor_id=self.motor_id,
            value=self.direction * rpm,
            accel=accel,
            brake=False,
        )
        return self.transport.write(frame, read_reply=True)

    def set_current(self, amps: float, accel: int = 0):
        if not -8.0 <= amps <= 8.0:
            raise ValueError("Current must be between -8.0A and 8.0A")

        raw = int((amps / 8.0) * 32767)

        frame = build_drive_command(
            motor_id=self.motor_id,
            value=self.direction * raw,
            accel=accel,
        )
        return self.transport.write(frame, read_reply=True)

    def set_position(self, degrees: float, accel: int = 0):
        if not 0 <= degrees <= 360:
            raise ValueError("Position must be between 0 and 360 degrees")

        if self.direction == -1:
            degrees = 360 - degrees
            if degrees == 360:
                degrees = 0

        raw = int((degrees / 360) * 32767)

        frame = build_drive_command(
            motor_id=self.motor_id,
            value=raw,
            accel=accel,
        )
        return self.transport.write(frame, read_reply=True)

    def brake(self):
        frame = build_drive_command(
            motor_id=self.motor_id,
            value=0,
            accel=0,
            brake=True,
        )
        return self.transport.write(frame, read_reply=True)