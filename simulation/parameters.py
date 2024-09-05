class Parameters:
    def __init__(self, configuration: dict):
        # Sim settings
        self.number_of_sensors = configuration["number_of_sensors"]
        self.half_distance = configuration["half_distance"]
        self.sim_termination = configuration["sim_termination"]
        self.coll_calc = configuration["coll_calc"]

        # Header settings
        self.BW = configuration["BW"]
        self.PL = configuration["PL"]
        self.CRC = configuration["CRC"]
        self.DE = configuration["DE"]
        self.npreamble = configuration["npreamble"]

        # Array treatment
        self.payloads = [int(payload) for payload in configuration["payloads"].split(" ")]
        self.payload = 51
        self.CRs = [int(codingrate) for codingrate in configuration["CR"].split(" ")]
        self.CR = 4
        self.Hs = [int(header) for header in configuration["H"].split(" ")]
        self.H = 1

        self.variable = None

    def set_payload(self, payload):
        self.payload = payload

    def set_CR(self, CR):
        self.CR = CR

    def set_H(self, H):
        self.H = H

    def set_variable(self, variable):
        self.variable = variable


