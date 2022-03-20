from geopy.geocoders import Nominatim
from datacenter import Datacenter, VM
import json
import requests
import time

# 6250 vms per Datacenter
#
# Assumption: 
#       1 Center    --> 100 Cluster
#       1 Cluster   --> 14 ESXis
#       1 ESXi      --> 10 vms
#
vms_per_center = 14000
datacenter_locations = {

    "London, United Kingdom",
    "Glasgow, United Kingdom",
    "Cork, Ireland",
    "Manchester, United Kingdom",
    "Galway, United Kingdom",
    "Swansea, United Kingdom",
    "Aberdeen, United Kingdom",
    "Dublin, United Kingdom",

}

def example_datacenters():

    app = Nominatim(user_agent="Data Center Distribution")
    data_centers = []

    for location in datacenter_locations:
        geoinfo = app.geocode(location).raw

        long = geoinfo['lon']
        lat = geoinfo['lat']
        country = geoinfo['display_name']
        storage = 100000
        
        # kWh
        solar_max = 180000
        wind_max = 7000000
        
        vms = []
        vm_json = get_vms()
        for vm_key in vm_json:
            number_cores = vm_json[vm_key]['number_of_cores']
            priority = vm_json[vm_key]['priority']
            expected_runtime = vm_json[vm_key]['expected_runtime']
            vms.append(VM(booked_cores=number_cores,
                          size=0,
                          priority=priority,
                          time_created=time.time(),
                          expected_runtime=expected_runtime
                      ))

        total_cores = calculate_number_of_cores(vms)

        center = Datacenter(
                long=long, 
                lat=lat, 
                cores=total_cores, 
                solar_max=solar_max, 
                wind_max=wind_max,
                country=country,
                storage=storage,
                bandwidth=10000,
                virtual_machines=vms
            )
        
        data_centers.append(center)
    
    return data_centers


def get_vms():
    delete_vms()
    create_vms(vms_per_center)
    return get_all_vms()


def delete_vms():
    requests.get("http://127.0.0.1:8000/api/delete-all")


def create_vms(number=1):
    request_url = "http://127.0.0.1:8000/api/create-vm/" + str(number)
    r = requests.get(request_url)


def get_all_vms():
    request_url = "http://127.0.0.1:8000/api/get-all-vms"
    r = requests.get(request_url)
    return json.loads(r.text)


def calculate_number_of_cores(vms):
    total_count = 0
    for vm in vms:
        total_count = total_count + vm.booked_cores
    return total_count
