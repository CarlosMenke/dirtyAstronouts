import math
from datacenter import Datacenter, VM
import datetime, time
import logging as logger
from utils.eco_power import *

latency_factor = 1/10
energy_per_core = 4


def cal_latency(datacenter1: Datacenter, datacenter2: Datacenter):
    lat1 = float(datacenter1.lat)
    lat1 = (lat1 / 180) * math.pi
    lon1 = float(datacenter1.long)
    lon1 = (lon1 / 180) * math.pi
    lat2 = float(datacenter2.lat)
    lat2 = (lat2 / 180) * math.pi
    lon2 = float(datacenter2.long)
    lon2 = (lon2 / 180) * math.pi

    distancefloat = 6378.388 * math.acos(math.sin(lat1) * math.sin(lat2) + math.cos(lat1) * math.cos(lat2) * math.cos(lon2 - lon1))
    distance = int(distancefloat)*1000
    latency = distance / 100000000
    return latency


def find_bandwidth(datacenter1: Datacenter, datacenter2: Datacenter):
    return min(datacenter1.bandwidth, datacenter2.bandwidth)


def free_eco_power(datacenter: Datacenter, time):
    """returns the free ecopower and is negative if there is dirty power used"""
    return get_power(datacenter, time) - datacenter.active_cores()*energy_per_core


def energy_cost(datacenter: Datacenter, vm: VM):
    """returns the energy cost of running the given vm on the given datacenter until finished"""
    cost = 0
    current_time = time.time()
    time_left = vm.expected_runtime - (current_time - vm.time_created)

    while time_left > 0:
        cost = free_eco_power(datacenter,current_time + time_left)
        time_left -= 60 * 60

    return cost


def time_span_energy_cost(datacenter: Datacenter, vm: VM, time_span):
    """returns the energy cost of running the given vm on the given datacenter for a given time span"""
    cost = 0
    current_time = time.time()
    time_left = time_span - (current_time - vm.time_created)

    while time_left > 0:
        cost = free_eco_power(datacenter,current_time + time_left)
        time_left -= 60 * 60

    if cost < 0:
        # when there is no non-eco energy used the cost does not matter
        return 0

    return cost


def transfer_energy_cost(source: Datacenter, destination: Datacenter, vm: VM):
    """returns the energy cost of transfering a vm between two given datacenters also taking into account latency"""
    bandwidth = find_bandwidth(source, destination)
    transfer_time = vm.size/bandwidth

    cost = energy_cost(source, vm) + time_span_energy_cost(destination, vm, transfer_time)
    cost *= cal_latency(source, destination) * latency_factor

    return cost


def energy_savings(source: Datacenter, destination: Datacenter, vm: VM):
    """calculates the energy savings when transfering the vm from datacenters"""
    if source == destination:
        return 0

    savings = energy_cost(datacenter=source, vm=vm) - energy_cost(datacenter=destination, vm=vm) - transfer_energy_cost(source=source, destination=destination, vm=vm)
    return savings
