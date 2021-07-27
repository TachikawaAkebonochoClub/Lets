#!/usr/bin/python
# -*- coding: utf-8 -*-

import csv
import random
import datetime
import json
import re
import sys
from decimal import Decimal, ROUND_HALF_UP, ROUND_HALF_EVEN


def main():
    if len(sys.argv) < 2:
        sys.exit(1)

    sub(sys.argv[2])


def next(filename):
    with open(filename, 'r') as file:

        for line in csv.reader(file):
            yield line


def csv_dic(sb_data):
    return {
        "id": sb_data[0],
        "serialNumber": sb_data[1],
        "batteryType": sb_data[2],
        "brandName": sb_data[3],
        "type": sb_data[4],
        "rechargeEnergySource": sb_data[5],
        "dateLastReported": sb_data[6],
        "location": {
            "type": sb_data[8],
            "coordinates": [sb_data[9], sb_data[10]]
        },
        "owner": sb_data[7]
    }


def createDatas(sb_Dic):

    status_list = ['consumingEnergy', 'givingEnergy', 'standby']
    ini_charge = random.uniform(0.00, 1.00)
    ini_temperature = random.uniform(291.75, 302.55)
    j_sbd = []
    now_charge = 0.0
    now_temperature = 0.0

    for num in range(0, 1440):
        status = random.choice(status_list)

        dic = {
            'serialNumber': sb_Dic["serialNumber"],
            'type': 'StorageBatteryMeasurement',
            'timestamp': str(datetime_create(sys.argv[1], num)),
            'stateOfCharge': battery_status(status, ini_charge, now_charge),
            'location': sb_Dic["location"],
            'temperature': _temperature(num, ini_temperature, now_temperature),
            'batteryStatus': status
        }
        j_sbd.append(dic)
        now_charge = dic['stateOfCharge']
        now_temperature = dic['temperature']

    return j_sbd


def sub(filename):
    for data in next(filename):
        sb_Dic = csv_dic(data)
        out = createDatas(sb_Dic)
        print(json.dumps(out, indent=2))

        # sys.exit(88)


def datetime_create(datestring, num):
    hou = str(num//60)
    min = str(num % 60)
    str_time = ' ' + hou + ':' + min + ':00'
    date_time = datestring + str_time
    to_datetime = datetime.datetime.strptime(date_time, '%Y/%m/%d %H:%M:%S')
    yesterday = to_datetime - datetime.timedelta(days=1)

    return yesterday


def battery_status(status, ini_charge, now_charge):
    if now_charge == 0.0:
        now_charge = ini_charge
    plus_minus = random.uniform(0.01, 0.1)

    if re.fullmatch('standby', status):
        b = Decimal(now_charge).quantize(
            Decimal('0.01'), rounding=ROUND_HALF_UP)
        now_charge = float(b)
    elif re.fullmatch('givingEnergy', status):
        b = now_charge - plus_minus
        if b <= 0.00:
            b = Decimal(0).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
            now_charge = float(b)
        else:
            b = Decimal(b).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
            now_charge = float(b)
    elif re.fullmatch('consumingEnergy', status):
        b = now_charge + plus_minus
        if b >= 1.00:
            b = Decimal(1).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
            now_charge = float(b)
        else:
            b = Decimal(b).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
            now_charge = float(b)
    return now_charge


def _temperature(num, ini_temperature, now_temperature):
    if now_temperature == 0.0:
        now_temperature = ini_temperature
    plus_minus = random.uniform(-0.05, 0.1)
    if num <= 840:
        am = now_temperature + plus_minus
        am = Decimal(am).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        now_temperature = float(am)
        if now_temperature >= 312.65:
            now_temperature = float(312.65)
    elif num >= 841:
        pm = now_temperature - plus_minus
        pm = Decimal(pm).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        now_temperature = float(pm)
        if now_temperature <= 267.65:
            now_temperature = float(267.65)

    return now_temperature


if __name__ == "__main__":
    j_sbd = main()
    sys.exit(j_sbd)
