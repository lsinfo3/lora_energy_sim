import pandas as pd
import matplotlib


class Plotter:
    def __init__(self, system):
        self.name = "plotter"
        self.system = system

    def plot_sfs(self):
        sensors = self.system.get_sensor_dict()
        sf_array = []

        for sensor in sensors.values():
            sf_array.append(sensor.get_sf())

        sf_series = pd.Series(sf_array)
        value_counts = sf_series.value_counts()

        df = pd.DataFrame({'value': value_counts.index, 'count': value_counts.values})
        print(df)
        df.plot()

        '''plt.figure()
        plt.hist(sf_array, color='orange')
        plt.show()'''
