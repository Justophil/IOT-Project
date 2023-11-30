import json
import sys
from bluepy.btle import Scanner, DefaultDelegate
from pygments import highlight, lexers, formatters
 
rssi_threshold = -50
def scan(rssi_threshold):
    try:
    
        scanner = Scanner() 
        devices = scanner.scan(10.0)
    
        devices_m = []
        devices_threshold = []
    
        for dev in devices:
            name = ""
            power = ""
            for (adtype, desc, value) in dev.getScanData():
                if (desc == "Complete Local Name"):
                    name = str(value)
                elif (desc == "Tx Power"):
                    power = str(value)
    
            # add device addr, addType and rssi to devices_m
            devices_m.append({'addr': dev.addr, 'addType': dev.addrType, 'rssi': dev.rssi, 'name': name, 'power': power})
            if dev.rssi > rssi_threshold:
                devices_threshold.append({'addr': dev.addr, 'addType': dev.addrType, 'rssi': dev.rssi, 'name': name, 'power': power})
                
        # standard print
        # json_devices = json.dumps(devices_m)
        # print(json_devices)
    
        # colored print
        formatted_json = json.dumps(devices_m, indent=4)
        colorful_json = highlight(formatted_json, lexers.JsonLexer(), formatters.TerminalFormatter())
        # print(colorful_json)
        print(devices_threshold)
        return len(devices_threshold)
    
    except Exception as ex:
        # print ( "Unexpected error in BLE Scanner BLUEPY: %s" % ex )
        return -1

if __name__ == '__main__':
    print(scan(rssi_threshold))
