from dataclasses import dataclass
from typing import Optional


# Communication protocol
@dataclass
class MotorStatus:
    motor_id: int
    mode: int
    current: int
    speed_rpm: int
    error: int
    position: Optional[int] = None
    winding_temp_c: Optional[int] = None
    position_u8: Optional[int] = None


# Adds CRC for 10-byte frame
def build_frame(payload: bytes):
    if len(payload) != 9:
        raise ValueError("Payload must be exactly 9 bytes")

    crc = crc8_maxim(payload)  # Checksum
    return payload + bytes([crc])  # Append crc


# Convert int to two bytes
def int16_to_bytes(value: int):
    if not -32768 <= value <= 32767:
        raise ValueError("Value out of int16 range")

    value &= 0xFFFF

    msb = (value >> 8) & 0xFF
    lsb = value & 0xFF

    return msb, lsb


# Convert two bytes back to signed 16-bit int
def bytes_to_int16(msb: int, lsb: int):
    value = (msb << 8) | lsb  # combine bytes
    if value & 0x8000:
        value -= 0x10000

    return value


def build_mode_command(motor_id: int, mode: int):
    if not isinstance(motor_id, int) or isinstance(motor_id, bool):
        raise TypeError("Motor ID must be an integer")
    if not 0 <= motor_id <= 0xFF:
        raise ValueError("Motor ID must be in range 0 to 255")
    if mode not in (0x01, 0x02, 0x03):
        raise ValueError("Mode must be 0x01, 0x02, or 0x03")

    return bytes([
        motor_id,
        0xA0,
        0, 0, 0, 0, 0, 0, 0,
        mode  # mode instead of CRC
    ])


# Apply control value
def build_drive_command(motor_id: int, value: int, accel: int = 0, brake: bool = False):
    if not isinstance(motor_id, int) or isinstance(motor_id, bool):
        raise TypeError("Motor ID must be an integer")
    if not 0 <= motor_id <= 0xFF:
        raise ValueError("Motor ID must be in range 0 to 255")
    if not isinstance(accel, int) or isinstance(accel, bool):
        raise TypeError("Acceleration must be an integer")
    if not 0 <= accel <= 0xFF:
        raise ValueError("Acceleration must be in range 0 to 255")

    msb, lsb = int16_to_bytes(value)
    payload = bytes([
        motor_id,
        0x64,  # In documentation
        msb,  # Current/rpm/target angle depending on mode
        lsb,
        0,
        0,
        accel,
        0xFF if brake else 0x00,
        0
    ])

    return build_frame(payload)


def crc8_maxim(data: bytes):
    crc = 0

    for byte in data:
        crc ^= byte

        for _ in range(8):
            if crc & 0x01:
                crc = (crc >> 1) ^ 0x8C
            else:
                crc >>= 1

    return crc & 0xFF