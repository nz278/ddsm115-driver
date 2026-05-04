import time
from src.ddsm115.controller import DDSM115Controller
from src.ddsm115.motor import DDSM115
from src.ddsm115.transport import SerialTransport

transport = SerialTransport("/dev/tty.usbserial-BG02Q0ZT")

def main():
    fl = DDSM115(1, transport, direction=-1)
    rl = DDSM115(2, transport, direction=-1)
    fr = DDSM115(3, transport, direction=1)
    rr = DDSM115(4, transport, direction=1)

    controller = DDSM115Controller([fl, rl, fr, rr])

    try:
        # Run each motor individually first
        print("Running individual motors")
        fl.set_mode_velocity()
        time.sleep(0.5)
        fl.set_speed(30)
        time.sleep(2)
        fl.set_speed(0)
        time.sleep(0.5)

        fr.set_mode_velocity()
        time.sleep(0.5)
        fr.set_speed(30)
        time.sleep(2)
        fr.set_speed(0)
        time.sleep(0.5)

        rl.set_mode_velocity()
        time.sleep(0.5)
        rl.set_speed(30)
        time.sleep(2)
        rl.set_speed(0)
        time.sleep(0.5)

        rr.set_mode_velocity()
        time.sleep(0.5)
        rr.set_speed(30)
        time.sleep(2)
        rr.set_speed(0)
        time.sleep(0.5)

        # Simultaneous commands
        print("\nSetting velocity mode")
        controller.set_mode_velocity_all()

        print("Setting speed to 30 RPM")
        controller.set_speed_all(30)
        time.sleep(2.5)

        print("Braking")
        controller.brake_all()
        time.sleep(2.5)

        print("Setting speed to -30 RPM")
        controller.set_speed_all(-30)
        time.sleep(2.5)

        print("Stopping")
        controller.set_speed_all(0)
        time.sleep(2.5)

        print("\nSetting current mode")
        controller.set_mode_current_all()

        # Less than 0.1A appears to not be effective
        print("Setting current to 0.1 A")
        controller.set_current_all(0.1)
        time.sleep(2.5)

        controller.set_current_all(0)
        time.sleep(2.5)

        print("Setting current to -0.1")
        controller.set_current_all(-0.1)
        time.sleep(2.5)

        controller.set_current_all(0)
        time.sleep(2.5)

        print("\nSetting position mode")
        controller.set_mode_position_all()
        time.sleep(2.5)

        print("Setting position to 90 degrees")
        controller.set_position_all(90)
        time.sleep(5)

        print("Setting position to 180 degrees")
        controller.set_position_all(180)
        time.sleep(5)

        print("Setting position to 0 degrees")
        controller.set_position_all(0)
        time.sleep(5)

        print("\nDone")

    finally:
        controller.close()
        print("Connection closed")


if __name__ == "__main__":
    main()
