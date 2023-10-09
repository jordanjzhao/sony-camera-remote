#!/usr/bin/env python3
from flask import Flask, render_template, Response, request, jsonify
import sys
import socket
import requests
import xml.etree.ElementTree as ET # parsing XML
import json
from sony_api import CameraAPI
import cv2
import numpy as np
import asyncio


app = Flask(__name__, static_url_path='/static')

camera_api = None


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
    try:
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            bytes = b''
            for chunk in response.iter_content(chunk_size=1024):
                bytes += chunk
                startFrame = bytes.find(b'\xff\xd8')
                endFrame = bytes.find(b'\xff\xd9')
                if startFrame != -1 and endFrame != -1: #both start and end found - complete jpeg received
                    jpg = bytes[startFrame:endFrame+2]
                    bytes = bytes[endFrame+2:]
                    # decodes the JPEG frame (jpg) into an image using OpenCV 
                    # convert the JPEG bytes into a NumPy array of unsigned 8-bit integer
                    # reads this array as an image, specify image loaded in color mode
                    im = cv2.imdecode(np.frombuffer(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)
                    if im is not None: # decode successful
                        # encode back to jpeg format, res (boolean) jpeg (image)
                        res, jpeg = cv2.imencode('.jpg', im)
                        if res: #encoding succesful
                            frame = jpeg.tobytes() # convert
                            # yields the bytes of the JPEG frame as part of a multipart response. This is suitable for streaming video over HTTP
                            yield (b'--frame\r\n'
                                    b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
                else:
                    bytes = bytes[endFrame+2:] # skip jpeg image frames 
            # cv2.imdecode is used to decode the JPEG bytes into an image. This is necessary because the raw JPEG bytes need to be interpreted and converted into a format that can be displayed or further processed by OpenCV.
            # The reason for re-encoding the image back to JPEG format with cv2.imencode is to ensure that the image is in a consistent format before it is sent as a response. This is important if the original format of the incoming stream is not guaranteed to be JPEG. Encoding it back to JPEG ensures that it is sent as a standard image format.
            # Essentially, this step ensures that the image is in a standardized format (JPEG) before being streamed or further processed.
        else:
            print(f"Failed to retrieve live view data. Status code: {response.status_code}")
    except Exception as e:
        print(f"An error occurred: {e}")

def initCamera():
    global camera_api
    global available_f_numbers
    response = discover_camera()
    if response:
        location_url = handle_discovery_response(response)
        if location_url:
            endpoint_url = describe_camera(location_url)
            camera_api = CameraAPI(endpoint_url)
            camera_api.startRecMode()
            available_apis = camera_api.getAvailableApiList()
            print('CAMERA APIS:', available_apis)
        else:
            return print('Location URL not found.')
    else:
        return print('Device not found.')
   

@app.route('/')
def index():
    # initCamera()
    # available_f_numbers = camera_api.getAvailableFNumber()  
    # Create a dictionary to hold all the variables
    # template_data = {
    #     'available_f_numbers': available_f_numbers,
    #     'other_variable': 'some_value',
    #     # Add more variables as needed
    # }
    global camera_api
    global available_f_numbers
    response = discover_camera()
    if response:
        location_url = handle_discovery_response(response)
        if location_url:
            endpoint_url = describe_camera(location_url)
            camera_api = CameraAPI(endpoint_url)
            available_iso_numbers = camera_api.getAvailableIsoSpeedRate()
            available_f_numbers = camera_api.getAvailableFNumber()
            available_ss_numbers = camera_api.getAvailableShutterSpeed()
            data = {
                'available_iso_numbers': available_iso_numbers,
                'available_f_numbers': available_f_numbers,
                'available_ss_numbers': available_ss_numbers,
                # Add more variables as needed
            }
        else:
            print('Location URL not found.')
    else:
        print('Device not found.')

    return render_template('index.html', **data)
    # return render_template('index.html', available_f_numbers=available_f_numbers)

    # return render_template('index.html')

    # # initCamera()
    # available_f_numbers = camera_api.getAvailableFNumber()  
    # print('Curr F number:', available_f_numbers[0])
    # print('F number range:', available_f_numbers[1])
    # return render_template('index.html', available_f_numbers=available_f_numbers)

@app.route('/video_feed')
def video_feed():
    # response = discover_camera()
    # if response:
    #     location_url = handle_discovery_response(response)
    #     if location_url:
    #         endpoint_url = describe_camera(location_url)
    #         camera_api = CameraAPI(endpoint_url)
    result_rec_mode = camera_api.startRecMode()
    if result_rec_mode is not None and result_rec_mode[0] == 0:
        print("Started recording mode successfully.")
        # print(camera_api.getAvailableIsoSpeedRate())
        # print(camera_api.getAvailableFNumber())
        # print(camera_api.getAvailableShutterSpeed())
        result = camera_api.startLiveview()
        print('Result from startliveview():', result)
        if result is not None:
            liveview_url = result[0]
            return Response(fetch_liveview_data(liveview_url), mimetype='multipart/x-mixed-replace; boundary=frame')
        else:
            return "Failed to start live view."
    #     else:
    #         return print('Location URL not found.')
    # else:
    #     return print('Device not found.')

@app.route('/update_f_number', methods=['POST'])
def update_f_number():
    f_number = request.json.get('f_number')

    # Call the API function to set the F Number
    response = camera_api.setFNumber(f_number)
    camera_api.actHalfPressShutter()

    if response is not None and response[0] == 0:
        return jsonify({'message': 'F Number updated successfully'}), 200
    else:
        return jsonify({'error': 'Failed to update F Number'}), 500
    
@app.route('/update_iso_number', methods=['POST'])
def update_iso_number():
    iso_number = request.json.get('iso_number')

    # Call the API function to set the F Number
    response = camera_api.setIsoSpeedRate(iso_number)
    camera_api.actHalfPressShutter()

    if response is not None and response[0] == 0:
        return jsonify({'message': 'ISO Speed Rate updated successfully'}), 200
    else:
        return jsonify({'error': 'Failed to update ISO Speed Rate'}), 500
    
@app.route('/update_ss_number', methods=['POST'])
def update_ss_number():
    ss_number = request.json.get('ss_number')

    # Call the API function to set the F Number
    response = camera_api.setShutterSpeed(ss_number)
    camera_api.actHalfPressShutter()

    if response is not None and response[0] == 0:
        return jsonify({'message': 'Shutter Speed updated successfully'}), 200
    else:
        return jsonify({'error': 'Failed to update Shutter Speed'}), 500


if __name__ == '__main__':
    app.run(debug=True)
