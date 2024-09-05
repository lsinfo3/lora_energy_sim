from sensor import Sensor
from states import State


class Gateway:
    def __init__(self, system, idx, x, y):
        self.system = system
        self.env = self.system.get_env()
        self.idx = idx
        self.x = x
        self.y = y
        self.sensors = dict()  # Includes index -> sensor

        # Currently sending sensors
        self.sending_sensors = dict()

        # States and state times
        self.state = State.gw_receive  # For now gw is always receiving
        self.state_change = self.env.now  # Logs when the state changes

    def add_sensor(self, sensor_idx, lon, lat, sf = 7, sf_collisions = None):
        # gateway, idx, lon, lat
        sensor = Sensor(self, sensor_idx, lon, lat, sf, sf_collisions)
        self.sensors[sensor_idx] = sensor
        self.system.sensor_dict[sensor_idx] = sensor

    def add_sending_sensor(self, sensor):
        self.sending_sensors[sensor.get_idx()] = sensor

    # Sensor is done sending, remove it from the list
    def remove_sending_sensor(self, sensor):
        sensor_idx = sensor.get_idx()
        if sensor_idx in self.sending_sensors:
            self.sending_sensors.pop(sensor_idx)

    def get_idx(self):
        return self.idx

    def get_system(self):
        return self.system

    def get_state(self):
        return self.state

    def get_state_change(self):
        return self.state_change
