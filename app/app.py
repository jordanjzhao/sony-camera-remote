#!/usr/bin/env python3
from flask import Flask
import sys
import socket
import requests
import xml.etree.ElementTree as ET # parsing XML

app = Flask(__name__)

# Make SSDP dsicovery request on a UDP socket connection
def discover_camera(): # M-SEARCH (multicast search) request, MX (max wait time for res), ST (search target)
    discovery_msg = ('M-SEARCH * HTTP/1.1\r\n' +
                    'HOST: 239.255.255.250:1900\r\n' +
                    'MAN: "ssdp:discover"\r\n' +
                    'MX: 3\r\n' +
                    'ST: urn:schemas-sony-com:service:ScalarWebAPI:1\r\n\r\n')
    #essentially a NOTIFY message to multicast address 239.255.255.250 on port 1900

    # ssdp protocol 
    # using sockets to create UDP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP) 
        #AF_INET = Address Family Internet - family used for IPv4 addresses
        #SOCK_DGRAM = Socket User Datagram Protocol (UDP)
    sock.settimeout(5) # optional timeout
        # can add following in try case below
        # except socket.timeout:
        #     print('No more responses.')
    # send SSDP request
    sock.sendto(discovery_msg.encode('utf-8'), ('239.255.255.250', 1900) )
    
    # receive response
    try:
        while True:
            data, addr = sock.recvfrom(1024)
            return data.decode('utf-8')  
    except socket.timeout:
        sock.close()
        return

# Handle SSDP discovery response 
def handle_discovery_response(data):
    location_line = None
    for line in data.split('\r\n'):
        if line.startswith('LOCATION'):
            location_line = line
            break

    if location_line:
        location_url = location_line.split(': ')[1]
        print('Location URL:', location_url)
        return location_url
    else:
        return None

# Retrieve the device description from location URL XML 
def describe_camera(url):
    response = requests.get(url)
    if response.status_code == 200:
        xml_data = response.text
        root = ET.fromstring(xml_data)
        device_name = root.find(".//root:friendlyName", namespaces={'root': 'urn:schemas-upnp-org:device-1-0'}).text
        print("Device:", device_name)
        udn_code = root.find(".//root:UDN", namespaces={'root': 'urn:schemas-upnp-org:device-1-0'}).text
        print("UDN:", udn_code)
        api_version = root.find(".//av:X_ScalarWebAPI_Version", namespaces={'av': 'urn:schemas-sony-com:av'}).text
        print('API Version:', api_version)
        services = []
        for service in root.findall(".//av:X_ScalarWebAPI_Service", namespaces={'av': 'urn:schemas-sony-com:av'}):
            service_type = service.find("av:X_ScalarWebAPI_ServiceType", namespaces={'av': 'urn:schemas-sony-com:av'}).text
            action_list_url = service.find("av:X_ScalarWebAPI_ActionList_URL", namespaces={'av': 'urn:schemas-sony-com:av'}).text

            services.append({
                'ServiceType': service_type,
                'ActionListURL': action_list_url
            })

        # Print the extracted information
        print(f"API Version: {api_version}")
        for service in services:
            print(f"Service Type: {service['ServiceType']}")
            print(f"Action List URL: {service['ActionListURL']}")
        endpoint_url = action_list_url + '/camera'
        return endpoint_url
    else:
        return print('Unable to retrieve device description.')



@app.route('/')
def index():
    response = discover_camera()
    if response:
        location_url = handle_discovery_response(response)
        if location_url:
            endpoint_url = describe_camera(location_url)
            print('Endpoint Url:', endpoint_url)
        else:
            return print('Location URL not found.')
    else:
        return print('Device not found.')

if __name__ == '__main__':
    app.run(debug=True)
