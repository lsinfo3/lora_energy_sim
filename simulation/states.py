from enum import Enum


class State(Enum):
    sensor_sleep = 'sensor_sleep'
    sensor_standby = 'sensor_standby'
    sensor_fstx = 'sensor_fstx'
    sensor_receive = 'sensor_receive'
    sensor_transmit = 'sensor_transmit'

    gw_sleep = 'gw_sleep'
    gw_standby = 'gw_standby'
    gw_idle = 'gw_idle'
    gw_receive = 'gw_receive'
    gw_transmit = 'gw_transmit'

    def get_value(self):
        return self.value


if __name__ == '__main__':
    state = State.gw_receive
    print(state.get_value())
