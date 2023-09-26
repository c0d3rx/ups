#!/bin/bash

# first, tell ups to graceful shutdown
snmpset -v1  -c private ups-pcfab PowerNet-MIB::upsBasicControlConserveBattery.0 i 2

# second, shutdown computer
##sudo poweroff

