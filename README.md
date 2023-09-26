# APC smart UPS snmp monitor
The script is useful to run a program when the following conditions are met on the ups:

- The ups is on battery power
- the battery remaining time is less than specified in a conf file

Main use is to shutdown a server when in battery power, and the remaining time of battery is lower than a threshold \
In this configuration the script call "power_off.sh", that instructs the ups to shutdown the server after a timeout, and the power off itself

# prerequisites
AP9630 card on smart UPS \
snp, libsnmp-dev, python3-dev, snmp-mibs-downloader

# requirements
python requirements are in requirements.txt \
use pip3 package manager to install them \
use a virtualenv if possible to avoid package conflicts

# installation
- copy mib files from mibs to  ~/.snmp/mibs 
- test communications with APC \
```snmpwalk -v1  -c public <ups-address> PowerNet-MIB::upsBasicIdentModel```
- set upsOutletGroupConfigPowerOffDelay to allow the server to shutdown after a timeout, in order to allow server to shutdown\
```snmpset -v1  -c private <ups-address> PowerNet-MIB::upsOutletGroupConfigPowerOffDelay.1 i 180 # 180 sec delay```
- check upsOutletGroupConfigRebootDuration, additional time to boot-off, eventually set \
```snmpwalk -v1  -c private ups-pcfab PowerNet-MIB::upsOutletGroupConfigRebootDuration```
- check upsOutletGroupConfigLoadShedControlTimeOnBattery ( should be disabled ), eventually disable \
```snmpwalk -v1  -c private <ups-address> PowerNet-MIB::upsOutletGroupConfigLoadShedControlTimeOnBattery```
- configure parameters in ups.yaml
- put ups.py in crontab

