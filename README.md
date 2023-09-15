# APC smart UPS snmp monitor
The script is useful to run a program when the following conditions are met on the ups:

- The ups is on battery power
- the battery remaining timw is less than specified in a conf file

Main use is to shutdown a server when in battery power, and the remaining time of battery is lower than a threshold 

# prerequisites
AP9630 card on smart UPS \
snp, libsnmp-dev, python3-dev

# requirements
python requirements are in requirements.txt \
use pip3 package manager to install them

# installation
- copy mib files from mibs to  ~/.snmp/mibs \
- test communications with APC \
```snmpwalk -v1  -c public <address of ups> PowerNet-MIB::upsBasicIdentModel```
- configure parameters in ups.yaml
- put ups.py in crontab

