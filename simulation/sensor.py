import random
from states import State

import numpy as np
import simpy
import math
import ast


class Sensor:
    def __init__(self, gateway, idx, x, y, sf = 7, sf_collisions = None):
        # Initialize sensor
        self.gateway = gateway
        self.env = gateway.env
        self.system = gateway.system
        self.coding_rate = self.system.params.CR
        self.header = self.system.params.H
        self.idx = idx
        self.x = x
        self.y = y
        self.sf_collisions = []
        self.max_dist = -1

        if not self.system.params.coll_calc:
            self.sf = self.add_spreading_factor()
        else:
            self.sf = sf
            self.update_collision_sensors(sf_collisions)

        self.successful_transmissions = 0
        self.error_transmissions = 0

        self.last_interrupted_time = self.env.now
        self.is_sending = False
        self.last_idle_time = self.env.now

        # Sending details
        self.waiting_duration = np.random.randint(0, 3600000)
        self.sending_duration = -1  # in ms

        self.payload = self.system.params.payload  # in bytes
        self.random_payload = False
        if self.payload == 0:
            self.random_payload = True

        self.total_symbols = 0
        self.payload_symbols = 0
        self.was_successful = True

        # Logging monitor
        self.monitor = self.system.monitor

        # States and state times
        self.state = State.sensor_standby
        self.state_change = self.env.now  # Logs when the state changes

        # Run processes
        self.is_running = True  # Flag to control send loop
        self.action = self.env.process(self.send())
        # self.interrupt_action = self.env.process(self.interrupt_sending())

    def hata(self, sf, gw_height, sens_height):  # returns distance in m
        # represents Spreading Factor Tolerances for Path Loss in dB
        plrange = [131, 134, 137, 140, 141, 144]
        distance = 10 ** (-(69.55 + 76.872985 - 13.82 * math.log10(gw_height) - 3.2 * (math.log10(
            11.75 * sens_height) ** 2) + 4.97 - plrange[sf - 7]) / (44.9 - 6.55 * math.log10(gw_height)))
        return distance * 1000

    def add_spreading_factor(self):
        # dist is distance from sensor to gateway
        gateway_x = self.gateway.x
        gateway_y = self.gateway.y
        dist = math.sqrt((gateway_x - self.x) ** 2 + (gateway_y - self.y) ** 2)

        currsf = 12
        for new_sf in range(12, 6, -1):
            hata_dist = self.hata(new_sf, 15, 1)
            if dist < hata_dist:
                currsf = new_sf
                self.max_dist = hata_dist
        return currsf

    def update_collision_sensors(self, sf_collisions = None):
        if not self.system.params.coll_calc:
            # Add collisions
            for other_idx in self.gateway.sensors.keys():
                if other_idx != self.idx:
                    other_sensor = self.gateway.sensors[other_idx]
                    other_x = other_sensor.x
                    other_y = other_sensor.y

                    distance_sensor1 = self.max_dist
                    distance_sensor2 = other_sensor.max_dist

                    distance = math.sqrt((other_x - self.x)**2 + (other_y - self.y)**2)
                    if distance <= max(self.max_dist, other_sensor.max_dist):
                        self.sf_collisions.append(other_idx)
            # print(f"Sensor {self.idx}: {self.sf_collisions}")
        else:
            all_six_lists = ast.literal_eval(sf_collisions) # 6 listen
            for list in all_six_lists:
                if list: # ausgefüllte liste
                    self.sf_collisions = list
            # print(self.sf_collisions)

    def send(self):
        while self.is_running:
            try:
                # Wait for random time interval before sending
                yield self.env.timeout(self.waiting_duration)

                # Try sending packet for a random time
                if self.random_payload:
                    self.payload = random.choice(self.system.params.payloads)
                self.is_successful = True  # Only for successful transmission
                self.sending_duration = round(self.payload_size_to_time(self.payload, self.sf), 3)

                # Calculate next waiting interval until sending again
                diff = np.floor((self.env.now + self.sending_duration) / 3600000)
                if diff != self.system.get_current_hour():
                    overlapping_time = (self.env.now + self.sending_duration) % 3600000
                    self.waiting_duration = np.random.randint(0, 3600000 - overlapping_time)
                else:
                    next_hour = (self.system.get_current_hour() + 1) * 3600000
                    lower = next_hour - (self.env.now + self.sending_duration)
                    upper = lower + 3600000

                    self.waiting_duration = np.random.randint(lower, upper)

                # Check if sensor disturbs someone else
                all_sending_sensors = self.system.get_all_sending_sensors()
                sending_coll_sensors = []
                for coll_sensor_idx in self.sf_collisions:
                    # If yes, increment errors and interrupt other sensor
                    if coll_sensor_idx in all_sending_sensors.keys() and not coll_sensor_idx == self.idx:
                        self.set_is_not_successful()
                        coll_sensor = self.system.get_sensor_dict()[coll_sensor_idx]
                        coll_sensor.set_is_not_successful()
                        sending_coll_sensors.append(coll_sensor_idx)

                # sending_coll_sensors not empty -> sensor would interrupt others
                # if sending_coll_sensors:
                #    print(f"Sensor {self.idx}: end at {self.env.now}s and would interrupt {sending_coll_sensors}")
                #    continue

                # Send and append sensor to list of all sending sensors in system and gateway
                #self.monitor.update_events_log(self, f"Sensor {self.idx}: Send {self.payload} bytes at {self.env.now}ms")
                #if sending_coll_sensors:
                    #(self.monitor.update_events_log(self, f"Sensor {self.idx}: Collides with sensors {sending_coll_sensors}"))
                self.gateway.add_sending_sensor(self)
                self.system.add_sending_sensor(self)
                self.is_sending = True

                # Update state change to transmit
                #self.monitor.update_state_log(self)
                self.state = State.sensor_transmit
                self.state_change = self.env.now

                yield self.env.timeout(self.sending_duration)

                # After being done with sending, remove the sensor from the sending dicts
                self.gateway.remove_sending_sensor(self)
                self.system.remove_sending_sensor(self)
                self.is_sending = False

                # Update state change back to sleep
                # self.monitor.update_state_log(self)
                self.state = State.sensor_sleep
                self.state_change = self.env.now

                # Was transmission successful?
                if self.is_successful:
                    self.increment_successful_transmissions()
                else:
                    self.increment_error_transmissions()

                # Update transmission
                self.monitor.update_transmission_log(self)

            except simpy.Interrupt as i:
                # Sending packet was interrupted by someone else wanting to send
                if i.args[0] == "Sending packet failed":
                    if self.last_interrupted_time != self.env.now:
                        # Do not remove collision sensor but mark as error transmission
                        self.increment_error_transmissions()
                        print(f"Sensor {self.idx}: Sending packet was interrupted at {self.env.now} seconds")

                        # Update monitoring variables
                        self.last_interrupted_time = self.env.now
                        self.is_successful = False
                    else:
                        pass
                elif i.args[0] == "Terminate simulation":
                    break
                else:
                    pass

    # Calculate ToA in ms, time drift and GW channel use
    def payload_size_to_time(self, payload, sf):
        BW = self.system.params.BW
        PL = payload + self.system.params.PL
        CR = self.system.params.CR
        CRC = self.system.params.CRC
        H = self.system.params.H
        DE = self.system.params.DE
        SF = sf
        npreamble = self.system.params.npreamble
        if sf >= 11:
            DE = 0

        Rs = BW / (math.pow(2, SF))
        Ts = 1 / Rs
        symbol = 8 + max(math.ceil((8.0 * PL - 4.0 * SF + 28 + 16 * CRC - 20.0 * H) /
                                   (4.0 * (SF - 2.0 * DE))) * (CR + 4), 0)
        # ohne crc und ohne header
        self.payload_symbols = 8 + max(math.ceil((8.0 * PL - 4.0 * SF + 28) /
                                   (4.0 * SF)) * (CR + 4), 0)
        self.total_symbols = symbol + (npreamble + 4.25)
        Tpreamble = (npreamble + 4.25) * Ts
        Tpayload = symbol * Ts
        ToA = Tpreamble + Tpayload
        return ToA

    def get_gateway(self):
        return self.gateway

    def get_sf(self):
        return self.sf

    def get_sf_collisions(self):
        return self.sf_collisions

    def increment_successful_transmissions(self):
        self.successful_transmissions = self.successful_transmissions + 1

    def increment_error_transmissions(self):
        self.error_transmissions = self.error_transmissions + 1

    def set_is_not_successful(self):
        self.is_successful = False

    def get_successful_transmissions(self):
        return self.successful_transmissions

    def get_error_transmissions(self):
        return self.error_transmissions

    def get_last_idle_time(self):
        return self.last_idle_time

    def get_idx(self):
        return self.idx

    def get_sending_duration(self):
        return self.sending_duration

    def get_payload(self):
        return self.payload

    def get_is_successful(self):
        return self.is_successful

    def get_state(self):
        return self.state

    def get_state_change(self):
        return self.state_change

    def get_total_symbols(self):
        return self.total_symbols

    def get_payload_symbols(self):
        return self.payload_symbols

    def get_coding_rate(self):
        return self.coding_rate

    def get_header(self):
        return self.header