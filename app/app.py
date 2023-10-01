#!/usr/bin/env python3
from flask import Flask, render_template
import sys
import socket
import requests
import xml.etree.ElementTree as ET # parsing XML
import json
from sony_api import CameraAPI
# pip install opencv-python-headless - cv2 - to capture frams from live view and use JavaScript to update the 'src'attribute of img with live view URL
import cv2
import urllib.request
import numpy as np

# class CameraAPI:
#     def __init__(self, base_url):
#         self.base_url = base_url

#     def _make_request(self, method, params):
#         url = f"{self.base_url}/camera"
#         payload = {
#             "method": method,
#             "params": params,
#             "id": 1,
#             "version": "1.0"
#         }
#         headers = {
#             "Content-Type": "application/json"
#         }
#         response = requests.post(url, data=json.dumps(payload), headers=headers)
#         return response

#     def execute_command(self, command, params):
#         response = self._make_request(command, params)
#         if response.status_code == 200:
#             response_data = response.json()
#             return response_data.get('result', None)
#         return None

#     def start_liveview(self):
#         response = self._make_request("startLiveview", [])
#         if response.status_code == 200:
#             response_data = response.json()
#             return response_data.get('result', None)
#         return None

#     def stop_liveview(self):
#         response = self._make_request("stopLiveview", [])
#         if response.status_code == 200:
#             response_data = response.json()
#             return response_data.get('result', None)
#         return None

app = Flask(__name__)

# Add a global variable to store the live view URL
# liveview_url = None
# camera_api = None

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
        return action_list_url 
    else:
        return print('Unable to retrieve device description.')

def fetch_liveview_data(url):
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        return response.iter_content(chunk_size=1024)
    return None        

def process_packet(packet):
    # decode JPEG data
    try:
        if packet is not None and len(packet) > 0:
            np_arr = np.frombuffer(packet, np.uint8)
            image = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
            if image is not None:
                if image.shape[0] > 0 and image.shape[1] > 0:
                    cv2.imshow('Live View', image)
                    cv2.waitKey(1)
    except Exception as e:
        print(f"An error occurred: {e}")
    


@app.route('/')
def index():
    response = discover_camera()
    if response:
        location_url = handle_discovery_response(response)
        if location_url:
            endpoint_url = describe_camera(location_url)
            camera_api = CameraAPI(endpoint_url)

            result_rec_mode = camera_api.start_rec_mode()
            if result_rec_mode is not None and result_rec_mode[0] == 0:
                print("Started recording mode successfully.")
                result = camera_api.start_liveview()
                if result is not None:
                    liveview_url = result[0]
                    print("LIVE VIEW URL:", liveview_url)
                    # OpenCV processing loop
                    data_stream = fetch_liveview_data(liveview_url)
                    if data_stream is not None:
                        for packet in data_stream:
                            process_packet(packet)

                    cv2.destroyAllWindows()
                    return "Live view closed."
                    # return render_template('index.html', liveview_url=liveview_url)
                    # cap = cv2.VideoCapture(liveview_url)
                    # ret, frame = cap.read()
                    # cap.realease()
                    # if ret:
                    #     cv2.imwrite('captured_image.jpg', frame)
                else:
                    return "Failed to start live view."

            # if camera_api.start_rec_mode() and camera_api.start_liveview():
            #     return render_template('index.html', liveview_url=liveview_url)
            # else:
            #     return "Failed to start recording mode or liveview."
        else:
            return print('Location URL not found.')
    else:
        return print('Device not found.')
    
# @app.route('/start_liveview', methods=['POST'])
# def start_liveview_route():
#     if camera_api.start_liveview():
#         return f"Liveview started. URL: {liveview_url}"
#     else:
#         return "Failed to start liveview"

# @app.route('/stop_liveview', methods=['POST'])
# def stop_liveview_route():
#     if camera_api.stop_liveview():
#         return "Liveview stopped successfully"
#     else:
#         return "Failed to stop liveview"

# @app.route('/capture_picture', methods=['POST'])
# def capture_picture():
#     global liveview_url

#     if liveview_url is not None:
#         cap = cv2.VideoCapture(liveview_url)
#         ret, frame = cap.read()
#         cap.release()

#         if ret:
#             cv2.imwrite('captured_image.jpg', frame)
#             return "Image captured successfully."
#         else:
#             return "Failed to capture image."
#     else:
#         return "Live view not available."

# @app.route('/')
# def index():
#     response = discover_camera()
#     if response:
#         location_url = handle_discovery_response(response)
#         if location_url:
#             endpoint_url = describe_camera(location_url)
#             #intantiate
#             camera_api = CameraAPI(endpoint_url)
#             # Start liveview
#             result = camera_api.start_liveview()
#             if result is not None:
#                 liveview_url = result[0]
#                 print("LIVE VIEW URL:", liveview_url)
#                 print("Liveview started successfully.")
#                 return render_template('index.html', liveview_url=liveview_url)
#             else:
#                 return "Failed to start liveview."
#         else:
#             return print('Location URL not found.')
#     else:
#         return print('Device not found.')
    
# @app.route('/start_liveview', methods=['POST'])
# def start_liveview():
#     global liveview_url, camera_api
#     result = camera_api.start_liveview()

#     if result is not None:
#         liveview_url = result[0]
#         return f"Liveview started. URL: {liveview_url}"
#     else:
#         return "Failed to start liveview"

# @app.route('/stop_liveview', methods=['POST'])
# def stop_liveview():
#     global liveview_url, camera_api
#     result = camera_api.stop_liveview()

#     if result is not None and result[0] == 0:
#         liveview_url = None
#         return "Liveview stopped successfully"
#     else:
#         return "Failed to stop liveview"

# @app.route('/display_liveview')
# def display_liveview():
#     global liveview_url

#     if liveview_url is not None:
#         cap = cv2.VideoCapture(liveview_url)
#         while True:
#             ret, frame = cap.read()
#             if not ret:
#                 break
#             cv2.imshow('Live View', frame)
#             if cv2.waitKey(1) & 0xFF == ord('q'):
#                 break
#         cap.release()
#         cv2.destroyAllWindows()
#         return "Live view closed."
#     else:
#         return "Live view not available."

if __name__ == '__main__':
    app.run(debug=True)
