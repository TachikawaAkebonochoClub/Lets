import csv
import random
import datetime
import json
import re


def _collection_datetime():
    today = datetime.datetime.today()
    date_time = today.replace(hour=0, minute=0, second=0, microsecond=0)
    c_datetime = str(date_time)
    return c_datetime


def _stateOfCharge(batteryStatus):
    n = random.uniform(0.00, 1.00)
    m = random.uniform(0.01, n)
    sleep = n
    if re.fullmatch('standby', batteryStatus):
        temp = format(sleep, '.2f')
        temp = float(temp)
    elif re.fullmatch('givingEnergy', batteryStatus):
        m_temp = n - m
        temp = format(m_temp, '.2f')
        temp = float(temp)
    elif re.fullmatch('consumingEnergy', batteryStatus):
        p_temp = n + m
        temp = format(p_temp, '.2f')
        temp = float(temp)
    return temp


def _location(r1):
    r = []
    for coordinates in r1:
        r.append({
            "location.type": 'Point',
            "location.coordinates": coordinates,
        }
        )
    return r


def _temperature():
    n = random.uniform(272, 313)
    temp = format(n, '.2f')
    temp = float(temp)
    return temp


def main():
    with open('C:\\Users\\b21a0142\\Desktop\\OJT_ishii\\lets\\data.csv', 'r') as file:  # パスは後で変更(変数名も)
        dataline = csv.reader(file)
        s = []
        r1 = []
        for data in dataline:
            s.append(data[0])
            r2 = [data[9], data[10]]
            r1.append(r2)
        arr = []
        s_no = {}
        for i in range(0, len(s)):
            s_no = {i: s[i]}
            arr.append(s_no)
        b_status = ['consumingEnergy', 'givingEnergy', 'standby']
        dic = {}

        for num in arr:
            batteryStatus = random.choice(b_status)
            dic['serialNumber'] = num
            dic['type'] = 'StorageBatteryMeasurement'
            dic['timestamp'] = _collection_datetime()
            dic['stateOfCharge'] = _stateOfCharge(batteryStatus)
            dic['location'] = _location()
            dic['temperature'] = _temperature()
            dic['batteryStatus'] = batteryStatus
            print(dic)
            json_data = json.dumps(dic)
            print(json_data)


main()
