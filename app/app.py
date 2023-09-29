#!/usr/bin/env python3
# from flask import Flask, request
# import requests # pypi.org/project/requests - making HTTP requests
# import sys
import socket # socket to make connection between nodes of a network

# app = Flask(__name__)

# SSDP_RECEIVE_TIMEOUT = 10000 # msec
# PACKET_BUFFER_SIZE = 1024

SSDP_PORT = 1900
SSDP_MX = 1
SSDP_ADDR = '239.255.255.250'
SSDP_ST = "urn:schemas-sony-com:service:ScalarWebAPI:1"

def discover_camera(): # M-SEARCH (multicast search) request, MX (max wait time for res), ST (search target)
    discovery_msg = ('M-SEARCH * HTTP/1.1\r\n' +
                    'HOST: 239.255.255.250:1900\r\n' +
                    'MAN: "ssdp:discover"\r\n' +
                    'MX: 3\r\n' +
                    'ST: urn:schemas-sony-com:service:ScalarWebAPI:1\r\n\r\n')
    # ssdp protocol 
    #ssdp_response = requests.request('M-SEARCH', 'ssdp:discover', data=ssdp_payload) - did not work
    # instead - let's use sockets to create UDP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP) 
        #AF_INET = Address Family Internet - family used for IPv4 addresses
        #SOCK_DGRAM = Socket User Datagram Protocol (UDP)
    sock.settimeout(5) # optional timeout
        # can add following in try case below
        # except socket.timeout:
        #     print('No more responses.')
    # send SSDP request
    sock.sendto(discovery_msg.encode('utf-8'), ('239.255.255.250', 1900) )
    
    
    try:
        while True:
            data, addr = sock.recvfrom(1024)
            print('ADDRESS: ', addr)
            print('DATA', data)
            response = data.decode('utf-8')
            print('DECODED DATA:\n', response)
            if 'LOCATION' in response:
                location_url = response.strip().split(' ')[1]
                print(location_url)
    except socket.timeout:
        pass

discover_camera()

# @app.route('/')
# def index():
#     response = discover_camera()
#     if response:
#         print('Camera URL found: ', response)
#     else:
#         print('Camera not found.')
#     return

# def create_app():
#    return app

# if __name__ == '__main__':
#     app.run(debug=True)
