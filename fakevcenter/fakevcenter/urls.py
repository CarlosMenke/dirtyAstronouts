import string
import json
import random
from django.urls import path
from django.http import HttpResponse

def create_session(request):
    return successResponse()

def create_vm(request):
    addVM()
    return successResponse()

def get_vm(request):
    responseText = "{"
    counter = 0
    for vm in VMManager.vms:
        responseText = responseText + "\"" + str(counter) + "\": " + vm.toJson() + ","
        counter = counter + 1
    
    if (responseText[-1] == ','):
        responseText = responseText[:-1]

    responseText = responseText + "}"
    return HttpResponse(responseText)

def create_number_of_vms(request, number):
    # For a variance.
    multiplicator = random.randrange(1, 10)
    for i in range(0, number):
        addVM(multiplicator)
    return successResponse()

def delete_all(request):
    VMManager.vms = []
    return successResponse()

urlpatterns = [
    path('api/create-session', create_session),
    path('api/create-vm', create_vm),
    path('api/create-vm/<int:number>', create_number_of_vms),
    path('api/get-all-vms', get_vm),
    path('api/delete-all', delete_all)
]

def addVM(multiplicator):
    VMManager.vms.append(VM(multiplicator))

class VMManager:
    # Static variable
    vms = []

class VM:

    def __init__(self, multiplicator) -> None:
        self.cores = random.randrange(1, 2 * multiplicator, 1)
        self.priority = random.randrange(1, 3, 1)
        self.expected_runtime = random.randrange(1, 24, 1) # in hours
 
    def toJson(self) -> string:
        serializable = {
            "number_of_cores": self.cores,
            "priority": self.priority,
            "expected_runtime": self.expected_runtime
        }

        return json.dumps(serializable, indent=4)

def successResponse():
    return HttpResponse("<http><head></head><body><img src='https://i.pinimg.com/originals/7b/4d/a9/7b4da9ca53fd8f43d340d5f19b8d6944.jpg' /></body></html>")