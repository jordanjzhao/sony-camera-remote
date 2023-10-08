import requests
import json

class CameraAPI:
    def __init__(self, base_url):
        self.base_url = base_url

    def _make_request(self, method, params, version):
        url = f"{self.base_url}/camera"
        payload = {
            "method": method,
            "params": params,
            "id": 1,
            "version": version,
        }
        headers = {
            "Content-Type": "application/json"
        }
        response = requests.post(url, data=json.dumps(payload), headers=headers)
        return response

# Shoot mode
    def setShootMode(self, mode):
        response = self._make_request('setShootMode', [mode], '1.0')
        if response.status_code == 200:
            response_data = response.json()
            return response_data.get('result', None)
        return None
    
    def getShootMode(self):
        response = self._make_request('getShootMode', [], '1.0')
        if response.status_code == 200:
            response_data = response.json()
            return response_data.get('result', None)
        return None
    
    def getSupportedShootMode(self):
        response = self._make_request('getSupportedShootMode', [], '1.0')
        if response.status_code == 200:
            response_data = response.json()
            return response_data.get('result', None)
        return None
    
    def getAvailableShootMode(self):
        response = self._make_request('getAvailableShootMode', [], '1.0')
        if response.status_code == 200:
            response_data = response.json()
            return response_data.get('result', None)
        return None

# # Still capture
    def actTakePicture(self):
        response = self._make_request('actTakePicture', [], '1.0')
        if response.status_code == 200:
            response_data = response.json()
            return response_data.get('result', None)
        return None
    
    def awaitTakePicture(self):
        response = self._make_request('awaitTakePicture', [], '1.0')
        if response.status_code == 200:
            response_data = response.json()
            return response_data.get('result', None)
        return None
    
    def startContShooting(self):
        response = self._make_request('startContShooting', [], '1.0')
        if response.status_code == 200:
            response_data = response.json()
            return response_data.get('result', None)
        return None
    
    def stopContShooting(self):
        response = self._make_request('stopContShooting', [], '1.0')
        if response.status_code == 200:
            response_data = response.json()
            return response_data.get('result', None)
        return None


# # Movie recording
    def startMovieRec(self):
        response = self._make_request('startMovieRec', [], '1.0')
        if response.status_code == 200:
            response_data = response.json()
            return response_data.get('result', None)
        return None

    def stopMovieRec(self):
        response = self._make_request('stopMovieRec', [], '1.0')
        if response.status_code == 200:
            response_data = response.json()
            return response_data.get('result', None)
        return None

# # Liveview
    def startLiveview(self):
        response = self._make_request('startLiveview', [], '1.0')
        if response.status_code == 200:
            response_data = response.json()
            return response_data.get('result', None)
        return None
    
    def stopLiveview(self):
        response = self._make_request('stopLiveview', [], '1.0')
        if response.status_code == 200:
            response_data = response.json()
            return response_data.get('result', None)
        return None

# # Liveview size
    def startLiveviewWithSize(self, size):
        response = self._make_request('startLiveviewWithSize', [size], '1.0')
        if response.status_code == 200:
            response_data = response.json()
            return response_data.get('result', None)
        return None
    
    def getLiveviewSize(self):
        response = self._make_request('getLiveviewSize', [], '1.0')
        if response.status_code == 200:
            response_data = response.json()
            return response_data.get('result', None)
        return None
    
    def getSupportedLiveviewSize(self):
        response = self._make_request('getSupportedLiveviewSize', [], '1.0')
        if response.status_code == 200:
            response_data = response.json()
            return response_data.get('result', None)
        return None

    def getAvailableLiveviewSize(self):
        response = self._make_request('getAvailableLiveviewSize', [], '1.0')
        if response.status_code == 200:
            response_data = response.json()
            return response_data.get('result', None)
        return None

# # Liveview frame
    def setLiveviewFrameInfo(self, frameInfo):
        params = [{"frameInfo": frameInfo}]
        response = self._make_request('setLiveviewFrameInfo', params, '1.0')
        if response.status_code == 200:
            response_data = response.json()
            return response_data.get('result', None)
        return None

    def getLiveviewFrameInfo(self):
        response = self._make_request('getLiveviewFrameInfo', [], '1.0')
        if response.status_code == 200:
            response_data = response.json()
            return response_data.get('result', None)
        return None

# # Zoom
    def actZoom(self, direction, movement):
        response = self._make_request('actZoom', [direction, movement], '1.0')
        if response.status_code == 200:
            response_data = response.json()
            return response_data.get('result', None)
        return None
    
# # Zoom setting
    def setZoomSetting(self, zoomSetting):
        params = [{"zoom": zoomSetting}]
        response = self._make_request('setZoomSetting', params, '1.0')
        if response.status_code == 200:
            response_data = response.json()
            return response_data.get('result', None)
        return None

    def getZoomSetting(self):
        response = self._make_request('getZoomSetting', [], '1.0')
        if response.status_code == 200:
            response_data = response.json()
            return response_data.get('result', None)
        return None
    
    def getSupportedZoomSetting(self):
        response = self._make_request('getSupportedZoomSetting', [], '1.0')
        if response.status_code == 200:
            response_data = response.json()
            return response_data.get('result', None)
        return None
    
    def getAvailableZoomSetting(self):
        response = self._make_request('getAvailableZoomSetting', [], '1.0')
        if response.status_code == 200:
            response_data = response.json()
            return response_data.get('result', None)
        return None

# # Half-press shutter
    def actHalfPressShutter(self):
        response = self._make_request('actHalfPressShutter', [], '1.0')
        if response.status_code == 200:
            response_data = response.json()
            return response_data.get('result', None)
        return None
    
    def cancelHalfPressShutter(self):
        response = self._make_request('cancelHalfPressShutter', [], '1.0')
        if response.status_code == 200:
            response_data = response.json()
            return response_data.get('result', None)
        return None

# # Touch AF position
    def setTouchAFPosition(self, xPos, yPos):
        params = [xPos, yPos]
        response = self._make_request('setTouchAFPosition', params, '1.0')
        if response.status_code == 200:
            response_data = response.json()
            return response_data.get('result', None)
        return None
    
    def getTouchAFPosition(self):
        response = self._make_request('getTouchAFPosition', [], '1.0')
        if response.status_code == 200:
            response_data = response.json()
            return response_data.get('result', None)
        return None
    
    def cancelTouchAFPosition(self):
        response = self._make_request('cancelTouchAFPosition', [], '1.0')
        if response.status_code == 200:
            response_data = response.json()
            return response_data.get('result', None)
        return None

# # Continuous shooting mode
    def setContShootingMode(self, contShootingMode):
        params = [{"constShootingMode": contShootingMode}]
        response = self._make_request('setContShootingMode', params, '1.0')
        if response.status_code == 200:
            response_data = response.json()
            return response_data.get('result', None)
        return None
    
    def getContShootingMode(self):
        response = self._make_request('getContShootingMode', [], '1.0')
        if response.status_code == 200:
            response_data = response.json()
            return response_data.get('result', None)
        return None
    
    def getSupportedContShootingMode(self):
        response = self._make_request('getSupportedContShootingMode', [], '1.0')
        if response.status_code == 200:
            response_data = response.json()
            return response_data.get('result', None)
        return None

    def getAvailableContShootingMode(self):
        response = self._make_request('getAvailableContShootingMode', [], '1.0')
        if response.status_code == 200:
            response_data = response.json()
            return response_data.get('result', None)
        return None

# # Continuous shooting speed
    def setContShootingSpeed(self, contShootingSpeed):
        params = [{"contShootingSppeed": contShootingSpeed}]
        response = self._make_request('setContShootingSpeed', params, '1.0')
        if response.status_code == 200:
            response_data = response.json()
            return response_data.get('result', None)
        return None
    
    def getContShootingSpeed(self):
        response = self._make_request('getContShootingSpeed', [], '1.0')
        if response.status_code == 200:
            response_data = response.json()
            return response_data.get('result', None)
        return None
    
    def getSupportedContShootingSpeed(self):
        response = self._make_request('getSupportedContShootingSpeed', [], '1.0')
        if response.status_code == 200:
            response_data = response.json()
            return response_data.get('result', None)
        return None

    def getAvailableContShootingSpeed(self):
        response = self._make_request('getAvailableContShootingSpeed', [], '1.0')
        if response.status_code == 200:
            response_data = response.json()
            return response_data.get('result', None)
        return None

# # Self-timer
    def setSelfTimer(self, seconds):
        response = self._make_request('setSelfTimer', [seconds], '1.0')
        if response.status_code == 200:
            response_data = response.json()
            return response_data.get('result', None)
        return None
    
    def getSelfTimer(self):
        response = self._make_request('getSelfTimer', [], '1.0')
        if response.status_code == 200:
            response_data = response.json()
            return response_data.get('result', None)
        return None
    
    def getSupportedSelfTimer(self):
        response = self._make_request('getSupportedSelfTimer', [], '1.0')
        if response.status_code == 200:
            response_data = response.json()
            return response_data.get('result', None)
        return None

    def getAvailableSelfTimer(self):
        response = self._make_request('getAvailableSelfTimer', [], '1.0')
        if response.status_code == 200:
            response_data = response.json()
            return response_data.get('result', None)
        return None

# # Exposure mode
    def setExposureMode(self, exposureMode):
        response = self._make_request('setExposureMode', [exposureMode], '1.0')
        if response.status_code == 200:
            response_data = response.json()
            return response_data.get('result', None)
        return None
    
    def getExposureMode(self):
        response = self._make_request('getExposureMode', [], '1.0')
        if response.status_code == 200:
            response_data = response.json()
            return response_data.get('result', None)
        return None
    
    def getSupportedExposureMode(self):
        response = self._make_request('getSupportedExposureMode', [], '1.0')
        if response.status_code == 200:
            response_data = response.json()
            return response_data.get('result', None)
        return None

    def getAvailableExposureMode(self):
        response = self._make_request('getAvailableExposureMode', [], '1.0')
        if response.status_code == 200:
            response_data = response.json()
            return response_data.get('result', None)
        return None

# # Focus mode
    def setFocusMode(self, focusMode):
        response = self._make_request('setFocusMode', [focusMode], '1.0')
        if response.status_code == 200:
            response_data = response.json()
            return response_data.get('result', None)
        return None
    
    def getFocusMode(self):
        response = self._make_request('getFocusMode', [], '1.0')
        if response.status_code == 200:
            response_data = response.json()
            return response_data.get('result', None)
        return None
    
    def getSupportedFocusMode(self):
        response = self._make_request('getSupportedFocusMode', [], '1.0')
        if response.status_code == 200:
            response_data = response.json()
            return response_data.get('result', None)
        return None

    def getAvailableFocusMode(self):
        response = self._make_request('getAvailableFocusMode', [], '1.0')
        if response.status_code == 200:
            response_data = response.json()
            return response_data.get('result', None)
        return None

# # Exposure compensation
    def setExposureCompensation(self, exposureIndex):
        response = self._make_request('setExposureCompensation', [exposureIndex], '1.0')
        if response.status_code == 200:
            response_data = response.json()
            return response_data.get('result', None)
        return None
    
    def getExposureCompensation(self):
        response = self._make_request('getExposureCompensation', [], '1.0')
        if response.status_code == 200:
            response_data = response.json()
            return response_data.get('result', None)
        return None
    
    def getSupportedExposureCompensation(self):
        response = self._make_request('getSupportedExposureCompensation', [], '1.0')
        if response.status_code == 200:
            response_data = response.json()
            return response_data.get('result', None)
        return None

    def getAvailableExposureCompensation(self):
        response = self._make_request('getAvailableExposureCompensation', [], '1.0')
        if response.status_code == 200:
            response_data = response.json()
            return response_data.get('result', None)
        return None

# # F number
    def setFNumber(self, fNumber):
        response = self._make_request('setFNumber', [fNumber], '1.0')
        if response.status_code == 200:
            response_data = response.json()
            return response_data.get('result', None)
        return None
    
    def getFNumber(self):
        response = self._make_request('getFNumber', [], '1.0')
        if response.status_code == 200:
            response_data = response.json()
            return response_data.get('result', None)
        return None
    
    def getSupportedFNumber(self):
        response = self._make_request('getSupportedFNumber', [], '1.0')
        if response.status_code == 200:
            response_data = response.json()
            return response_data.get('result', None)
        return None

    def getAvailableFNumber(self):
        response = self._make_request('getAvailableFNumber', [], '1.0')
        if response.status_code == 200:
            response_data = response.json()
            return response_data.get('result', None)
        return None

# # Shutter speed
    def setShutterSpeed(self, shutterSpeed):
        response = self._make_request('setShutterSpeed', [shutterSpeed], '1.0')
        if response.status_code == 200:
            response_data = response.json()
            return response_data.get('result', None)
        return None
    
    def getShutterSpeed(self):
        response = self._make_request('getShutterSpeed', [], '1.0')
        if response.status_code == 200:
            response_data = response.json()
            return response_data.get('result', None)
        return None
    
    def getSupportedShutterSpeed(self):
        response = self._make_request('getSupportedShutterSpeed', [], '1.0')
        if response.status_code == 200:
            response_data = response.json()
            return response_data.get('result', None)
        return None

    def getAvailableShutterSpeed(self):
        response = self._make_request('getAvailableShutterSpeed', [], '1.0')
        if response.status_code == 200:
            response_data = response.json()
            return response_data.get('result', None)
        return None
    
# # ISO speed rate
    def setIsoSpeedRate(self, isoSpeed):
        response = self._make_request('setIsoSpeedRate', [isoSpeed], '1.0')
        if response.status_code == 200:
            response_data = response.json()
            return response_data.get('result', None)
        return None
    
    def getIsoSpeedRate(self):
        response = self._make_request('getIsoSpeedRate', [], '1.0')
        if response.status_code == 200:
            response_data = response.json()
            return response_data.get('result', None)
        return None
    
    def getSupportedIsoSpeedRate(self):
        response = self._make_request('getSupportedIsoSpeedRate', [], '1.0')
        if response.status_code == 200:
            response_data = response.json()
            return response_data.get('result', None)
        return None

    def getAvailableIsoSpeedRate(self):
        response = self._make_request('getAvailableIsoSpeedRate', [], '1.0')
        if response.status_code == 200:
            response_data = response.json()
            return response_data.get('result', None)
        return None

# # White balance
    def setWhiteBalance(self, mode, colorTempEnabledFlag, colorTemp):
        response = self._make_request('setWhiteBalance', [mode, colorTempEnabledFlag, colorTemp], '1.0')
        if response.status_code == 200:
            response_data = response.json()
            return response_data.get('result', None)
        return None
    
    def getWhiteBalance(self):
        response = self._make_request('getWhiteBalance', [], '1.0')
        if response.status_code == 200:
            response_data = response.json()
            return response_data.get('result', None)
        return None
    
    def getSupportedWhiteBalance(self):
        response = self._make_request('getSupportedWhiteBalance', [], '1.0')
        if response.status_code == 200:
            response_data = response.json()
            return response_data.get('result', None)
        return None

    def getAvailableWhiteBalance(self):
        response = self._make_request('getAvailableWhiteBalance', [], '1.0')
        if response.status_code == 200:
            response_data = response.json()
            return response_data.get('result', None)
        return None

    def actWhiteBalanceOnePushCustom(self):
        response = self._make_request('actWhiteBalanceOnePushCustom', [], '1.0')
        if response.status_code == 200:
            response_data = response.json()
            return response_data.get('result', None)
        return None

# # Program shift
    def setProgramShift(self, shiftAmount):
        response = self._make_request('setProgramShift', [shiftAmount], '1.0')
        if response.status_code == 200:
            response_data = response.json()
            return response_data.get('result', None)
        return None

    def getSupportedProgramShift(self):
        response = self._make_request('getSupportedProgramShift', [], '1.0')
        if response.status_code == 200:
            response_data = response.json()
            return response_data.get('result', None)
        return None

# # Flash Mode
    def setFlashMode(self, flashMode):
        response = self._make_request('setFlashMode', [flashMode], '1.0')
        if response.status_code == 200:
            response_data = response.json()
            return response_data.get('result', None)
        return None

    def getFlashMode(self):
        response = self._make_request('getFlashMode', [], '1.0')
        if response.status_code == 200:
            response_data = response.json()
            return response_data.get('result', None)
        return None
    
    def getSupportedFlashMode(self):
        response = self._make_request('getSupportedFlashMode', [], '1.0')
        if response.status_code == 200:
            response_data = response.json()
            return response_data.get('result', None)
        return None

    def getAvailableFlashMode(self):
        response = self._make_request('getAvailableFlashMode', [], '1.0')
        if response.status_code == 200:
            response_data = response.json()
            return response_data.get('result', None)
        return None

# # Postview image size
    def setPostviewImageSize(self, postviewImageSize):
        response = self._make_request('setPostviewImageSize', [postviewImageSize], '1.0')
        if response.status_code == 200:
            response_data = response.json()
            return response_data.get('result', None)
        return None

    def getPostviewImageSize(self):
        response = self._make_request('getPostviewImageSize', [], '1.0')
        if response.status_code == 200:
            response_data = response.json()
            return response_data.get('result', None)
        return None
    
    def getSupportedPostviewImageSize(self):
        response = self._make_request('getSupportedPostviewImageSize', [], '1.0')
        if response.status_code == 200:
            response_data = response.json()
            return response_data.get('result', None)
        return None

    def getAvailablePostviewImageSize(self):
        response = self._make_request('getAvailablePostviewImageSize', [], '1.0')
        if response.status_code == 200:
            response_data = response.json()
            return response_data.get('result', None)
        return None

# # Camera setup
    def startRecMode(self):
        response = self._make_request('startRecMode', [], '1.0')
        if response.status_code == 200:
            response_data = response.json()
            return response_data.get('result', None)
        return None

    def stopRecMode(self):
        response = self._make_request('stopRecMode', [], '1.0')
        if response.status_code == 200:
            response_data = response.json()
            return response_data.get('result', None)
        return None

# # Camera function
    def setCameraFunction(self, cameraFunction):
        response = self._make_request('setCameraFunction', [cameraFunction], '1.0')
        if response.status_code == 200:
            response_data = response.json()
            return response_data.get('result', None)
        return None

    def getCameraFunction(self):
        response = self._make_request('getCameraFunction', [], '1.0')
        if response.status_code == 200:
            response_data = response.json()
            return response_data.get('result', None)
        return None
    
    def getSupportedCameraFunction(self):
        response = self._make_request('getSupportedCameraFunction', [], '1.0')
        if response.status_code == 200:
            response_data = response.json()
            return response_data.get('result', None)
        return None

    def getAvailableCameraFunction(self):
        response = self._make_request('getAvailableCameraFunction', [], '1.0')
        if response.status_code == 200:
            response_data = response.json()
            return response_data.get('result', None)
        return None

# # Transferring images
    def getSchemeList(self):
        response = self._make_request('getSchemeList', [], '1.0')
        if response.status_code == 200:
            response_data = response.json()
            return response_data.get('result', None)
        return None

    def getSourceList(self, schemeName):
        params = [{"scheme": schemeName}]
        response = self._make_request('getSourceList', params, '1.0')
        if response.status_code == 200:
            response_data = response.json()
            return response_data.get('result', None)
        return None
    
    def getContentCount(self, uri, typeOp, target, view): # (v1.2)
        if typeOp:
            params = [{"uri": uri, "type": typeOp, "target": target, "view": view}]
        else:
            params = [{"uri": uri, "target": target, "view": view}]
        response = self._make_request('getContentCount', params, '1.2')
        if response.status_code == 200:
            response_data = response.json()
            return response_data.get('result', None)
        return None

    def getContentList(self, uri, startIndex, count, typeOp, view, sort): # (v1.3)
        if typeOp:
            params = [{"uri": uri, "stIdx": startIndex, "cnt": count, "type": typeOp, "view": view, "sort": sort}]
        else:
            params = [{"uri": uri, "stIdx": startIndex, "cnt": count, "view": view, "sort": sort}]
        response = self._make_request('getContentList', params, '1.3')
        if response.status_code == 200:
            response_data = response.json()
            return response_data.get('result', None)
        return None

# #  Remote playback
    def setStreamingContent(self, uri, remotePlayType):
        params = [{"uri":uri, "remotePlayType": remotePlayType}]
        response = self._make_request('setStreamingContent', params, '1.0')
        if response.status_code == 200:
            response_data = response.json()
            return response_data.get('result', None)
        return None
    
    def startStreaming(self): 
        response = self._make_request('startStreaming', [], '1.0')
        if response.status_code == 200:
            response_data = response.json()
            return response_data.get('result', None)
        return None

    def pauseStreaming(self): 
        response = self._make_request('pauseStreaming', [], '1.0')
        if response.status_code == 200:
            response_data = response.json()
            return response_data.get('result', None)
        return None
    
    def seekStreamingPosition(self, seekPosition):
        params = [{"positionMsec": seekPosition}]
        response = self._make_request('seekStreamingPosition', params, '1.0')
        if response.status_code == 200:
            response_data = response.json()
            return response_data.get('result', None)
        return None
    
    def stopStreaming(self): 
        response = self._make_request('stopStreaming', [], '1.0')
        if response.status_code == 200:
            response_data = response.json()
            return response_data.get('result', None)
        return None

    def requestToNotifyStreamingStatus(self, pollingFlag): 
        params = [{"polling": pollingFlag}]
        response = self._make_request('requestToNotifyStreamingStatus', params, '1.0')
        if response.status_code == 200:
            response_data = response.json()
            return response_data.get('result', None)
        return None

# # Delete contents
    def deleteContent(self, uriList): # (v1.1)
        params = [{"uri": uriList}]
        response = self._make_request('deleteContent', params, '1.1')
        if response.status_code == 200:
            response_data = response.json()
            return response_data.get('result', None)
        return None

# # Storage information
    def getStorageInformation(self): 
        response = self._make_request('getStorageInformation', [], '1.0')
        if response.status_code == 200:
            response_data = response.json()
            return response_data.get('result', None)
        return None

# # Event notification
    def getEvent(self, longPollingFlag): # (v1.0)
        response = self._make_request('getEvent', [longPollingFlag], '1.0')
        if response.status_code == 200:
            response_data = response.json()
            return response_data.get('result', None)
        return None
    
    def getEvent(self, longPollingFlag): # (v1.1)
        response = self._make_request('getEvent', [longPollingFlag], '1.1')
        if response.status_code == 200:
            response_data = response.json()
            return response_data.get('result', None)
        return None
    
    def getEvent(self, longPollingFlag): # (v1.2)
        response = self._make_request('getEvent', [longPollingFlag], '1.2')
        if response.status_code == 200:
            response_data = response.json()
            return response_data.get('result', None)
        return None
    
    def getEvent(self, longPollingFlag):  #  (v1.3)
        response = self._make_request('getEvent', [longPollingFlag], '1.3')
        if response.status_code == 200:
            response_data = response.json()
            return response_data.get('result', None)
        return None

# # Server information
    def getAvailableApiList(self): 
        response = self._make_request('getAvailableApiList', [], '1.0')
        if response.status_code == 200:
            response_data = response.json()
            return response_data.get('result', None)
        return None
    
    def getApplicationInfo(self):
        response = self._make_request('getApplicationInfo', [], '1.0')
        if response.status_code == 200:
            response_data = response.json()
            return response_data.get('result', None)
        return None
    
    def getVersions(self): 
        response = self._make_request('getVersions', [], '1.0')
        if response.status_code == 200:
            response_data = response.json()
            return response_data.get('result', None)
        return None

    def getMethodTypes(self, version): 
        response = self._make_request('getMethodTypes', [version], '1.0')
        if response.status_code == 200:
            response_data = response.json()
            return response_data.get('result', None)
        return None


    # Supported API methods
    # {
    #     Shoot mode
    #         -setShootMode
    #         -getShootMode
    #         -getSupportedShootMode
    #         -getAvailableShootMode

    #     Still capture
    #         -actTakePicture
    #         -awaitTakePicture
    #         -startContShooting
    #         -stopContShooting

    #     Movie recording
    #         -startMovieRec
    #         -stopMovieRec

    #     Liveview
    #         -startLiveview
    #         -stopLiveview

    #     Liveview size
    #         -startLiveviewWithSize
    #         -getLiveviewSize
    #         -getSupportedLiveviewSize
    #         -getAvailableLiveviewSize

    #     Liveview frame
    #         -setLiveviewFrameInfo
    #         -getLiveviewFrameInfo

    #     Zoom
    #         -actZoom

    #     Zoom setting
    #         -setZoomSetting
    #         -getZoomSetting
    #         -getSupportedZoomSetting
    #         -getAvailableZoomSetting

    #     Half-press shutter
    #         -actHalfPressShutter
    #         -cancelHalfPressShutter

    #     Touch AF position
    #         -setTouchAFPosition
    #         -getTouchAFPosition
    #         -cancelTouchAFPosition

    #     Continuous shooting mode
    #         -setContShootingMode
    #         getContShootingMode
    #         getSupportedContShootingMode
    #         getAvailableContShootingMode

    #     Continuous shooting speed
    #         setContShootingSpeed
    #         getContShootingSpeed
    #         getSupportedContShootingSpeed
    #         getAvailableContShootingSpeed

    #     Self-timer
    #         -setSelfTimer
    #         getSelfTimer
    #         getSupportedSelfTimer
    #         getAvailableSelfTimer

    #     Exposure mode
    #         -setExposureMode
    #         getExposureMode
    #         getSupportedExposureMode
    #         getAvailableExposureMode

    #     Focus mode
    #         -setFocusMode
    #         getFocusMode
    #         getSupportedFocusMode
    #         getAvailableFocusMode

    #     Exposure compensation
    #         -setExposureCompensation
    #         getExposureCompensation
    #         getSupportedExposureCompensation
    #         getAvailableExposureCompensation

    #     F number
    #         -setFNumber
    #         getFNumber
    #         getSupportedFNumber
    #         getAvailableFNumber

    #     Shutter speed
    #         -setShutterSpeed
    #         getShutterSpeed
    #         getSupportedShutterSpeed
    #         getAvailableShutterSpeed

    #     ISO speed rate
    #         -setIsoSpeedRate
    #         getIsoSpeedRate
    #         getSupportedIsoSpeedRate
    #         getAvailableIsoSpeedRate

    #     White balance
    #         -setWhiteBalance
    #         getWhiteBalance
    #         getSupportedWhiteBalance
    #         getAvailableWhiteBalance
    #         actWhiteBalanceOnePushCustom

    #     Program shift
    #         -setProgramShift
    #         -getSupportedProgramShift

    #     Flash Mode
    #         -setFlashMode
    #         getFlashMode
    #         getSupportedFlashMode
    #         getAvailableFlashMode

    #     Postview image size
    #         -setPostviewImageSize
    #         getPostviewImageSize
    #         getSupportedPostviewImageSize
    #         getAvailablePostviewImageSize

    #     Camera setup
    #         -startRecMode
    #         stopRecMode

    #     Camera function
    #         -setCameraFunction
    #         getCameraFunction
    #         getSupportedCameraFunction
    #         getAvailableCameraFunction

    #     Transferring images
    #         -getSchemeList
    #         getSourceList
    #         getContentCount (v1.2)
    #         getContentList (v1.3)

    #     Remote playback
    #         -setStreamingContent
    #         startStreaming
    #         pauseStreaming
    #         seekStreamingPosition
    #         stopStreaming
    #         requestToNotifyStreamingStatus

    #     Delete contents
    #         -deleteContent (v1.1)

    #     Storage information
    #         -getStorageInformation

    #     Event notification
    #         -getEvent (v1.0)
    #         getEvent (v1.1)
    #         getEvent (v1.2)
    #         getEvent (v1.3)

    #     Server information
    #         -getAvailableApiList
    #         getApplicationInfo
    #         getVersions
    #         getMethodTypes

    # }