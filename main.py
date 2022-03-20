from module_selectors import *
import time
from example_datacenters import example_datacenters
from flask import Flask
from flask_cors import CORS, cross_origin
import threading
import logging as logger
import random

logger.basicConfig(level=logger.DEBUG)
datacenters = example_datacenters()

app = Flask(__name__)
cors = CORS(app)
app.config["CORS_HEADERS"] = "Content-Type"

# Debug setting set to true
app.debug = True

shifts = []


@app.route("/")
@cross_origin()
def index():
    if len(shifts) == 0:
        return ""

    res = shifts.pop().toJson()
    for shift in shifts:
        res += "|"
        res += shift.toJson()
        shifts.remove(shift)
    return res


class Shift:

    def __init__(self, source, destination, vm_counter, savings) -> None:
        self.source = source
        self.destination = destination
        self.vm_counter = vm_counter
        self.savings = savings

    def toJson(self):
        res = '{'
        res += '"source": {'
        res += '"long": "' + self.source.long + '",'
        res += '"lat": "' + self.source.lat + '"},'
        res += '"destination": {'
        res += '"long": "' + self.destination.long + '",'
        res += '"lat": "' + self.destination.lat + '"},'
        res += '"vm_shifts": ' + str(self.vm_counter) + '}'

        return res


def func():
    relevant_datacenters = datacenters.copy()
    savings = 0
    temp = 0
    while True:
        time.sleep(1)
        dirty_datacenter = find_dirtiest_datacenter(relevant_datacenters)
        if not dirty_datacenter:
            continue

        vm = find_vm_to_move(dirty_datacenter.virtual_machines)
        if not vm:
            continue

        source, destination, vm_count, temp = move_vm(datacenters, dirty_datacenter, vm)
        savings += temp

        for i in range(0, 500):
            vm = find_vm_to_move(dirty_datacenter.virtual_machines)
            dirty_datacenter.virtual_machines.remove(vm)
            destination.virtual_machines.append(vm)
            vm_count = vm_count + 1

        shifts.append(Shift(source, destination, vm_count, savings))
        relevant_datacenters = [dirty_datacenter, destination]


def mock_func():
    example_centers = example_datacenters()
    while True:
        for i in range(random.randrange(1, 5)):
            count = random.randrange(300, 700)
            savings = random.randrange(30000, 700000)
            source = example_centers[random.randrange(0,7)]
            destination = example_centers[random.randrange(0,7)]
            shifts.append(Shift(source, destination, count, savings))
        time.sleep(4)



if __name__ == "__main__":
    #thread = threading.Thread(target=func)
    thread = threading.Thread(target=mock_func)
    thread.start()
    app.run(port=4433)
