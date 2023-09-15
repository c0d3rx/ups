#!/usr/bin/env python3

import argparse
import logging.config
import tyaml
from easysnmp import Session
from datetime import timedelta
import os

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='solarinfo',
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument("--conf-file", help="conf file", default="ups.yaml", required=False)
    parser.add_argument("--dry-run", action="store_true", help="simulate outage", required=False, default=False)

    args = parser.parse_args()

    conf = tyaml.load_and_replace(args.conf_file)
    # init & get main logger
    logging.config.dictConfig(conf.get("logging"))

    log = logging.getLogger("ups")
    log.info("started")
    if args.dry_run:
        log.info("dry run mode: no actions will be done")

    ups_conf: dict = conf.get("ups")

    cmd = ups_conf.get("cmd")
    log.debug(f"{cmd=}")

    min_battery_runtime = timedelta(**ups_conf.get("min_battery_runtime"))
    log.debug(f"{min_battery_runtime.__str__()=}")

    snmp_conf: dict = conf.get("snmp")
    session_conf = snmp_conf.get("session")

    session = Session(**session_conf)
    log.debug(f"{session}")

    upsAdvConfigShutoffDelay = float(session.get("PowerNet-MIB::upsAdvConfigShutoffDelay.0").value)/100
#
    log.debug(f"{upsAdvConfigShutoffDelay=}")

    upsBasicOutputStatus = int(session.get("PowerNet-MIB::upsBasicOutputStatus.0").value)  # 2 = online, 3 = onbattery
    log.debug(f"{upsBasicOutputStatus=}")

    upsAdvBatteryRunTimeRemaining = timedelta(
        microseconds=int(session.get("PowerNet-MIB::upsAdvBatteryRunTimeRemaining.0").value)*10000)

    log.debug(f"{upsAdvBatteryRunTimeRemaining.__str__()=}")

    if args.dry_run or ((upsBasicOutputStatus == 3) and (upsAdvBatteryRunTimeRemaining < min_battery_runtime)):
        log.info(f"Calling {cmd}")
        if not args.dry_run:
            os.system(cmd)



