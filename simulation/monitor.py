import datetime
import os
import random
import string


class Monitor:

    def __init__(self, system):
        added_headers = False
        # Generate random string of 5 letters, date, and time
        random_string = ''.join(random.choices(string.ascii_letters, k=5))
        current_datetime = datetime.datetime.now().strftime("%d.%m.%Y_%H.%M.%S")

        H = system.params.H
        CR = system.params.CR
        payload = system.params.payload
        current_variable = system.params.variable

        current_file_path = os.path.abspath(__file__)
        log_directory = os.path.dirname(os.path.dirname(current_file_path))
        log_directory = os.path.join(log_directory, "logs")
        if current_variable == "Payload":
            log_directory = os.path.join(log_directory, "Payload_" + str(payload))
        elif current_variable == "Coding_rate":
            log_directory = os.path.join(log_directory, "Codingrate_" + str(CR))
        else:
            log_directory = os.path.join(log_directory, "Header_" + str(H))
        log_directory = os.path.join(log_directory, random_string + "_" + current_datetime)
        # Create folder if it does not exist
        os.makedirs(log_directory, exist_ok=True)
        print(log_directory)

        self.transmission_log = os.path.join(log_directory, "transmission_log.csv")
        self.state_log = os.path.join(log_directory, "state_log.csv")
        self.interrupt_log = os.path.join(log_directory, "interrupt_log.csv")
        self.events_log = os.path.join(log_directory, "events_log.csv")

        # Class variable for adding header only if necessary
        if not added_headers:
            self.add_headers()
            added_headers = True

    def add_headers(self):
        # add all headers to each file
        transmission_header = "timestamp;gateway;sensor;sf;codingrate;payload_bytes;payload_symbols;header;total_symbols;duration;success"
        state_header = "timestamp;gateway;sensor;state;start;end;bytes"

        with open(self.transmission_log, "a") as f:
            f.write(f"{transmission_header}")
            f.write("\n")

        with open(self.state_log, "a") as f:
            f.write(f"{state_header}")
            f.write("\n")

    def update_transmission_log(self, sensor):
        # "timestamp;gateway;sensor;sf;codingrate;payload_bytes;payload_symbols;header;total_symbols;duration;success"
        timestamp = sensor.get_gateway().get_system().get_env().now
        gateway_idx = sensor.get_gateway().get_idx()
        sensor_idx = sensor.get_idx()
        sf = sensor.get_sf()

        coding_rate = sensor.get_coding_rate()
        payload_bytes = sensor.get_payload()
        payload_symbols = sensor.get_payload_symbols()
        total_symbols = sensor.get_total_symbols()
        header = sensor.get_header()

        duration = sensor.get_sending_duration()
        success = sensor.get_is_successful()
        with open(self.transmission_log, "a") as f:
            f.write(f"{timestamp};{gateway_idx};{sensor_idx};{sf};{coding_rate};{payload_bytes};{payload_symbols};{header};{total_symbols};{duration};{success}")
            f.write("\n")

    def update_state_log(self, sensor):
        sensor_idx = sensor.get_idx()
        gateway = sensor.get_gateway()
        gateway_idx = gateway.get_idx()
        timestamp = gateway.get_system().get_env().now
        start = sensor.get_state_change()
        end = gateway.get_system().get_env().now
        state = sensor.get_state().get_value()
        if state == "sensor_transmit":
            bytes = sensor.get_payload()
        else:
            bytes = 0

        with open(self.state_log, "a") as f:
            f.write(f"{timestamp};{gateway_idx};{sensor_idx};{state};{start};{end};{bytes}")
            f.write("\n")

    def update_events_log(self, sensor, event):
        sensor_idx = sensor.get_idx()
        gateway_idx = sensor.get_gateway().get_idx()
        time = sensor.system.env.now

        with open(self.events_log, "a") as f:
            f.write(f"{time} | S{sensor_idx} | GW{gateway_idx} | {event}")
            f.write("\n")
