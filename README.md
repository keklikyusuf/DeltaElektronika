## Delta Elektronika SM15K Power Supply


[![image](https://img.shields.io/badge/Python-v.3.9.1-blue)](https://www.python.org/downloads/)
[![image](https://img.shields.io/badge/GitHUB-SM15K-green)](https://github.com/keklikyusuf/DeltaElektronika)
[![image](https://img.shields.io/badge/Pypi-SM15K-red)](https://pypi.org/project/SM15K/)


This is a created package for functional operation of SM15K.

### Available operations and functions
1. Functions from datasheet [Delta Electronika](https://www.delta-elektronika.nl/upload/MANUAL_ETHERNET_AND_SEQUENCER_PROGRAMMING_SM15K.pdf)
2. Data logging thread for three type of frames (Basic, Ah and Wh)
3. Watchdog thread for safe operation
4. Charging thread for 3 step charging algorithm
5. Discharging thread for discharging algorithm
6. Cycling thread for battery cycling algorithm

### Used build-in modules
1. [Socket Module / import socket](https://docs.python.org/3/library/socket.htmll)
2. [Threading Module / import threading](https://docs.python.org/3/library/threading.html)
3. [Time Module / import time](https://docs.python.org/3/library/time.html)
4. [Csv Module / import csv](https://docs.python.org/3/library/csv.html)
5. [Datetime Module / import datetime](https://docs.python.org/3/library/datetime.html)
6. [Sys Module / import sys](https://docs.python.org/3/library/sys.html)
7. [Logging Module / import logging](https://docs.python.org/3/howto/logging.html)

__Note__: Datalogger logs as txt and comma separated base.
 
#### Installation
```pip install SM15K```


### How to use it?
#### Code and Syntax Examples
```python
from deltaelektronika import SM15K
import time
```

```python
# IP Address of the power supply, can be obtain the device itself.
IPV4 = '0.0.0.0' 

# To activate debugging option. Creates system-log file and logs there
SM15K.activateDebugLogger = True 

# To use colorful printing at console.
ColorPrint = SM15K.ColorPrinter()
ColorPrint.printFeedback(message="Your message to print to console as feedback!")
ColorPrint.printComment(message="Your message to print to console as comment!")
ColorPrint.printError(message="Your message to print to console as error!")
ColorPrint.printNormal(message="Your message to print to console as normal!")
ColorPrint.printColorful(message="Your message to print to console as colorful!", colour="purple")
# Available colors for printColorful method are "purple", "blue", "cyan", "green", "red", "yellow", "normal"

# To use all comments for SM15K
MyDelta = SM15K.SM15K(IPV4=IPV4)

# Source related comments
MyDelta.source."SourceRelatedComments"()
MyDelta.source.ReadPowerSet()
MyDelta.source.SetCurrent(current=20)

# Measure related comments
MyDelta.measure."MeasureRelatedComments"()
MyDelta.measure.MeasurePower()
MyDelta.measure.SetAhMeasurementState(setting="ON")

# Output related comments
MyDelta.output."OutputRelatedComments"()
MyDelta.output.ReadOutputSet()
MyDelta.output.SetOutput(setting="ON")

# System related comments
MyDelta.system."SystemRelatedComments"()
MyDelta.system.ReadWatchdogSet()
MyDelta.system.SetPowerLimit(powerlimit=2000, setting="ON")

# Shutdown related comments
MyDelta.shutdown."ShutdownRelatedComments"()
MyDelta.shutdown.limitShutdownValues()
MyDelta.shutdown.setShutdownOutput()
```
__Note__: All comments group according to datasheet of SM15K.

__Note__: Datasheet for [Delta Electronika](https://www.delta-elektronika.nl/upload/MANUAL_ETHERNET_AND_SEQUENCER_PROGRAMMING_SM15K.pdf)

```python
# There are additional independent features has been added!
# Watchdog operation for safety.
Safety = SM15K.WatchdogOperation(timer=5, sleeptime=4)

```
__Note__: Be sure that sleeptime is lower than timer. This means withing 5 seconds of lack of communication, SM15K will
shut its output down. If sleeptime is lower, watchdog will reset itself for every cycle of sleeptime period.

```python
# Datalogger operation for logging related data.
# Default color is green, available colors are;
# purple, blue, cyan, green, yellow, red and normal                            
BasicDatalogger = SM15K.BasicDataloggerOperation(IPV4, loggingTime=10,
                printColor= 'purple')    
```
__Note__: Basic data frame is; dataFrameBasic = 'Timestamp','Voltage', 'Current', 'Power'
```python
# Datalogger operation for logging related data.
# Default color is green, available colors are;
# purple, blue, cyan, green, yellow, red and normal 
AhDatalogger = SM15K.AhDataloggerOperation(IPV4, loggingTime=10, 
                printColor= 'red')
```
__Note__: Ah data frame is; dataFrameAh = 'Timestamp','Voltage', 'Current', 'Power', 'PositiveAh', 'NegativeAh', 'AhSeconds', 'AhHours'
```python
# Datalogger operation for logging related data.
# Default color is green, available colors are;
# purple, blue, cyan, green, yellow, red and normal            
WhDatalogger = SM15K.WhDataloggerOperation(IPV4, loggingTime=5, 
                printColor='blue')  
```
__Note__: Wh data frame is; dataFrameAh = 'Timestamp','Voltage', 'Current', 'Power', 'PositiveWh', 'NegativeWh', 'WhSeconds', 'WhHours'
```python
# Charging operation for battery charging.
Charging = SM15K.ChargingOperation(IPV4, sleeptime=5, bulkCurrent=100, 
                bulkVoltage= 14.5, floatVoltage=13.8, floatTime=300)

# Discharging operation for battery discharging.
Discharging = SM15K.DischargingOperation(IPV4, sleeptime=5, 
                dischargeCurrent=100, dischargeVoltage=10.5, 
                cutoffCurrent=2)
# Cycling operation for battery cycling.                
Cycling = SM15K.CyclingOperation(IPV4, sleeptime=5, cycletime=10, 
                bulkCurrent=100, bulkVoltage=14.5, floatVoltage=13.8, 
                floatTime=300, dischargeCurrent=100, dischargeVoltage=10.5, 
                cutoffCurrent=2,afterChargingRestTime=30.0, 
                afterDischargingRestTime=30.0, startCharging=True)
```
__Note__: Rest times can be set after each step (after charging and/or after discharging)
__Note__: To be able to start from desired operation (charging or discharging as first step) set ```python startCharging=True or False```
> Each functionality has been created with related parameters at above.  
> To be able to use them ```python threadObject.start()``` must be used to start the thread operation
```python
Safety.start()        # To start watchdog thread class
BasicDatalogger.start() # To start BasicDatalogger thread class
AhDatalogger.start()    # To start AhDatalogger thread class
WhDatalogger.start()    # To start WhDatalogger thread class
Charging.start()        # To start Charging thread class
Discharging.start()     # To start Discharging thread class
Cycling.start()         # To start Cycling thread class
```
> After calling thread start, if main loop ends, thread is going to end as well
> because of being deamon thread true. That is why infinity loop or long term loop needed to run.
> Or it can be used as thread.join() after it has been started to be sure that main does not end before the thread is done.

__Note__: Do not operate charging and discharging threads at the same operation.

__Note__: Do not operate Ah and Wh datalogger threads at the same operation. Delta can log one of them at a time.

__Note__: Watchdog is being set to delta itself, that is why be sure timer is bigger than sleep time to have healthy operation.

```python
while True:
    # Main Code Runs Here in infinity loop.
    time.sleep(30)
    print(f'Main loop runs in here!')
```
> You can run anything you want here as well to have multifunctional operation while system runs with multiple threads.

__Note__: All threads are created as deamon thread which means, if main finishes its operation
threads are going to stop operation. That is why you should keep them in infinite loop. If you like to have the thread 
keeps operation even if your main code has been finished, set the deamonState = False

## License

© 2021 Yusuf Keklik

This repository is licensed under the MIT license. See [LICENSE](https://github.com/keklikyusuf/DeltaElektronika/blob/main/LICENSE) for details.
