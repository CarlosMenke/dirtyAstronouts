import datetime, time
from utils.eco_power import get_power

energy_per_core = 10


class Datacenter:

    def __init__(self, lat, long, country, cores, solar_max, wind_max, storage, bandwidth, virtual_machines):
        self.long = long
        self.lat = lat
        self.country = country
        self.cores = cores
        self.solar_max = solar_max
        self.wind_max = wind_max
        self.storage = storage
        self.bandwidth = bandwidth
        self.virtual_machines = virtual_machines

    def active_cores(self):
        cores = 0
        for VM in self.virtual_machines:
            cores += VM.booked_cores
        return cores

    def dirty_power(self):
        return self.active_cores() * energy_per_core - get_power(self, time.time())


class VM:

    def __init__(self, booked_cores, size, priority, time_created, expected_runtime=60 * 60 * 24 * 365):
        self.booked_cores = booked_cores
        self.size = size
        self.priority = priority
        self.time_created = time_created
        self.expected_runtime = expected_runtime
