import requests
import json

class CameraAPI:
    def __init__(self, base_url):
        self.base_url = base_url

    def _make_request(self, method, params):
        url = f"{self.base_url}/camera"
        payload = {
            "method": method,
            "params": params,
            "id": 1,
            "version": "1.0"
        }
        headers = {
            "Content-Type": "application/json"
        }
        response = requests.post(url, data=json.dumps(payload), headers=headers)
        return response

    def execute_command(self, command, params):
        response = self._make_request(command, params)
        if response.status_code == 200:
            response_data = response.json()
            return response_data.get('result', None)
        return None
    
    def start_rec_mode(self):
        response = self._make_request("startRecMode", [])
        if response.status_code == 200:
            response_data = response.json()
            return response_data.get('result', None)
        return None

    def start_liveview(self):
        response = self._make_request("startLiveview", [])
        if response.status_code == 200:
            response_data = response.json()
            return response_data.get('result', None)
        return None

    def stop_liveview(self):
        response = self._make_request("stopLiveview", [])
        print(response.content)
        if response.status_code == 200:
            response_data = response.json()
            return response_data.get('result', None)
        return None

    # Add more API methods here as needed...
