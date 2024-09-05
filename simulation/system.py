import pandas as pd
import simpy

from gateway import Gateway
from monitor import Monitor
from plotter import Plotter
import numpy as np



class System:
    def __init__(self, env, params):
        self.params = params
        self.env = env
        self.gateway_dict = dict()
        self.sensor_dict = dict()
        self.gateway_sensor_dict = dict()
        self.all_sending_sensors = dict()  # Includes index -> sensor
        self.taken_coordinates = []  # Array of (x,y)-Tupels
        self.monitor = Monitor(self)
        self.current_hour = 0
        self.plotter = Plotter(self)

        self.initialize_system()
        self.time_action = self.env.process(self.time_management())
        self.terminate_action = self.env.process(self.terminate())

    def time_management(self):
        # ToDo: Print out every 1 hour
        while True:
            try:
                yield self.env.timeout(3600000)
                print("Hour " + str(self.current_hour) + " passed.")
                self.current_hour += 1
            except simpy.Interrupt as i:
                break

    def terminate(self):
        # ToDo: Terminate simulation
        yield self.env.timeout(self.params.sim_termination)

        for sensor_idx in self.sensor_dict.keys():
            sensor = self.sensor_dict[sensor_idx]
            sensor.action.interrupt("Terminate simulation")

        self.time_action.interrupt("Terminate simulation")

        print("Simulation terminated.")


    def add_sending_sensor(self, sensor):
        sensor_idx = sensor.get_idx()
        self.all_sending_sensors[sensor_idx] = sensor

    def remove_sending_sensor(self, sensor):
        sensor_idx = sensor.get_idx()
        self.all_sending_sensors.pop(sensor_idx, None)

    def initialize_system(self):
        # Add one gateway and place it in the middle of it
        if not self.params.coll_calc:
            idx = 0
            gateway_x = self.params.half_distance
            gateway_y = self.params.half_distance
            self.gateway_dict[idx] = Gateway(self, idx, gateway_x, gateway_y)
            self.taken_coordinates.append((gateway_x, gateway_y))

            # Add all sensors
            for sensor_idx in range(0, self.params.number_of_sensors):
                idx = sensor_idx + 1

                # Generate new x and y coordinates for each sensor
                while True:
                    sensor_x = np.random.randint(self.params.half_distance*2)
                    sensor_y = np.random.randint(self.params.half_distance*2)
                    distance = np.sqrt((sensor_x - gateway_x) ** 2 + (sensor_y - gateway_y) ** 2)

                    # Sensor-coords are in the circle around gateway
                    if distance <= self.params.half_distance and (sensor_x, sensor_y) not in self.taken_coordinates:
                        break

                # Add sensor to gateway
                gateway = self.gateway_dict[0]
                gateway.add_sensor(idx, sensor_x, sensor_y)

            print(len(self.sensor_dict.keys()))
            print(len(self.gateway_dict.keys()))

            # Update collisions between each sensor
            for sensor_idx in self.sensor_dict.keys():
                sensor = self.sensor_dict[sensor_idx]
                sensor.update_collision_sensors()

            self.plotter.plot_sfs()

        else:
            df = pd.read_csv('collisioncalc.csv')

            # First loop: Create Gateway objects if BestGW is equal to ID
            for index, row in df.iterrows():
                if row['BestGW'] == row['id']:
                    self.gateway_dict[row['id']] = Gateway(self, row['id'], row['lon'], row['lat'])

            # Second loop: Create Sensor objects if BestGW is not equal to ID
            for index, row in df.iterrows():
                if row['BestGW'] != row['id']:
                    gateway_idx = row['BestGW']
                    gateway = self.gateway_dict[gateway_idx]
                    gateway.add_sensor(row['id'], row['lon'], row['lat'], row['SF'], row['sf_collisions'])

            print(len(self.sensor_dict.keys()))
            print(len(self.gateway_dict.keys()))

            self.plotter.plot_sfs()

    def get_env(self):
        return self.env

    def get_sensor_dict(self):
        return self.sensor_dict

    def get_gateway_dict(self):
        return self.gateway_dict

    def get_gateway_sensor_dict(self):
        return self.gateway_sensor_dict

    def get_all_sending_sensors(self):
        return self.all_sending_sensors

    def get_monitor(self):
        return self.monitor

    def get_current_hour(self):
        return self.current_hour
