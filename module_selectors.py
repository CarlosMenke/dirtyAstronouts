from costs import *
from datacenter import Datacenter, VM
import logging as logger


def find_dirtiest_datacenter(datacenters: list):
    """returns the datacenter using the most dirty power, return """
    logger.debug("Looking for dirty datacenters .. ")

    if len(datacenters) == 0:
        logger.debug("No datacenter in list .. ")
        return False

    dirty_datacenter = datacenters[0]
    exists_clean_datacenter = False
    for datacenter in datacenters:
        dirty_power = round(datacenter.dirty_power())
        logger.debug(f"Looking for dirty datacenters .. {dirty_power}")
        if dirty_power < 0:
            exists_clean_datacenter = True

        if dirty_power > dirty_datacenter.dirty_power():
            dirty_datacenter = datacenter

    if dirty_datacenter.dirty_power() < 0:
        logger.debug("No dirty datacenter found .. ")
        return False

    if not exists_clean_datacenter:
        logger.debug("No clean datacenter found .. ")
        return False

    logger.debug(f"Found a dirty datacenter in {dirty_datacenter.country}")
    return dirty_datacenter


def find_vm_to_move(vms: list):
    vm_to_move = vms[0]

    for vm in vms:
        if vm.priority == 1 and vm.expected_runtime > vm_to_move.expected_runtime:
            vm_to_move = vm
    if vm_to_move.priority == 1:
        return vm_to_move

    for vm in vms:
        if vm.priority == 2 and vm.expected_runtime > vm_to_move.expected_runtime:
            vm_to_move = vm
    if vm_to_move.priority == 2:
        return vm_to_move

    logger.debug("No VM with priority 1 or 2 found .. ")
    return False


def move_vm(datacenters: list, dirty_datacenter: Datacenter, vm: VM):
    logger.debug("Looking for datacenter to move VM to .. ")

    destination = datacenters[0]
    savings = 0

    for datacenter in datacenters:
        if datacenter.dirty_power() > 0:
            continue
        current_savings = energy_savings(source=dirty_datacenter, destination=datacenter, vm=vm)
        if current_savings > savings:
            destination = datacenter
            savings = current_savings

    logger.debug("Found Datacenter to move VM to .. trying to move ..  ")
    dirty_datacenter.virtual_machines.remove(vm)
    destination.virtual_machines.append(vm)
    logger.debug("Removed VM from dirty datacenter and move it to clean one ..")
    return dirty_datacenter, destination, 1, savings
