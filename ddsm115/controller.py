from .motor import DDSM115

# Controller for running multiple motors simultaneously
class DDSM115Controller:
    def __init__(self, motors: list[DDSM115]):
        if not motors:
            raise ValueError("At least one motor is required")

        self.motors = {motor.motor_id: motor for motor in motors}

        if len(self.motors) != len(motors):
            raise ValueError("Duplicate motor IDs are not allowed")

        # same transport for all motors
        self.transport = motors[0].transport
        if any(motor.transport is not self.transport for motor in motors[1:]):
            raise ValueError("All motors must use the same transport")

    def motor(self, motor_id: int) -> DDSM115:
        return self.motors[motor_id]

    # Send same command to multiple motors simultaneously
    def _run_all(self, method_name: str, *args, **kwargs):
        results = []
        error = None

        for motor in self.motors.values():
            try:
                results.append(getattr(motor, method_name)(*args, **kwargs))
            except Exception as e:
                if error is None:
                    error = e

        if error is not None:
            raise error

        return results

    def set_mode_velocity_all(self):
        return self._run_all("set_mode_velocity")

    def set_mode_current_all(self):
        return self._run_all("set_mode_current")

    def set_mode_position_all(self):
        return self._run_all("set_mode_position")

    def set_speed_all(self, rpm: int, accel: int = 0):
        return self._run_all("set_speed", rpm, accel=accel)

    def set_current_all(self, amps: float, accel: int = 0):
        return self._run_all("set_current", amps, accel=accel)

    def set_position_all(self, degrees: float, accel: int = 0):
        return self._run_all("set_position", degrees, accel=accel)

    def brake_all(self):
        return self._run_all("brake")

    def close(self):
        self.transport.close()