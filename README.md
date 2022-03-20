# HackHPI

## Dependencies
```
python3
pip3 install -r requirement.txt
```

## Run

### 1. Run the Fake vCenter
See [here](fakevcenter/README.md).

### 2. Run the Scheduler
```bash
python3 main.py
```

### 3. Run the Visualizer
Use whatever webserver is desired to host a HTML file. Additionally, 
it can also be double-clicked to open directly in the browser without 
a webserver, since the Visualizer does not hold relative references.