# Fake vCenter
Tries to act like there are VMs consuming power.

## Run
Windows: 

```bash
py manage.py runserver
```

Linux:

```bash
python3 manage.py runserver
```

## RestAPI of vCenter

1. Create a Session
  
2. Create a VM
  
3. Get details about the VM ("Get VM")
  

### 1. Create Session (NOT IMPORTANT)

Das ist eigentlich hier nicht wichtig, weil immer das gleiche zurückgegeben wird.

```json
http://{hostname}/api/create-session
```

See [Create Session | CIS | vSphere CIS REST APIs](https://developer.vmware.com/apis/vsphere-automation/latest/cis/api/session/post/)

Keine Parameter

Response:

- Nothing
  

### 2. Create a VM

```json
http://{hostname}/api/create-vm
```

See [Create VM | vCenter | vSphere vCenter REST APIs](https://developer.vmware.com/apis/vsphere-automation/latest/vcenter/api/vcenter/vm/post/)

Alternatively for multiple VMs: 
```json
http://{hostname}/api/create-vm/{number-of-vms}
```
e.g., `http://127.0.0.1/api/create-vm/300` would create 300 VMs.
    

Response:

- Success message
  

### 3. Get details about the VM

See [Get VM | vCenter | vSphere vCenter REST APIs](https://developer.vmware.com/apis/vsphere-automation/latest/vcenter/api/vcenter/vm/vm/get/)

```json
http://{hostname}/api/get-all-vms/
```  

Response:

- JSON of all VMs with their parameters