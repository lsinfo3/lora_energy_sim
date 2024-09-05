from concurrent.futures import ThreadPoolExecutor

from parameters import Parameters
from system import System
import random
import yaml
import simpy
from multiprocessing import Pool

def run_sim(comb):
    for i in range (20):
        print("Start run.")
        env = simpy.Environment()
        params.set_H(comb["header"])
        params.set_CR(comb["coding"])
        params.set_payload(comb["payload"])
        params.set_variable(comb["variable"])
        system = System(env, params)
        env.run()

config = yaml.safe_load(open("configuration.yaml"))
params = Parameters(config)

if __name__ == "__main__":
    ### MONTE CARLO SENSOREN UM GATEWAY
    payloads = params.payloads
    nr_of_payloads = len(payloads)
    coding_rates = params.CRs
    headers = params.Hs

    combinations = [] # An array of dicts with payload -> x, coding_rate -> y, header -> z
    for a in range(len(payloads)):
        combinations.append({"variable": "Payload", "payload": payloads[a], "coding": 4, "header": 0})
    for b in range(len(coding_rates)):
        combinations.append({"variable": "Coding_rate", "payload": 0, "coding": coding_rates[b], "header": 0})
    for c in range(len(headers)):
        combinations.append({"variable": "Header", "payload": 0, "coding": 4, "header": headers[c]})

    with Pool(8) as p:
        results = p.map(run_sim, combinations)