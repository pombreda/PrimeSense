from crayola import CrayolaTestBase
from primesense import openni2
from multiprocessing.dummy import Process
from nose.tools import with_setup
from rpyc.core.stream import Stream
import time
import copy

class TestPermutations(CrayolaTestBase):
                
    def check_frames(self, indexOfDevice, sensorType, videoMode):
        device = self.devices[indexOfDevice]
        stream = device.create_stream(sensorType)
        stream.set_video_mode(videoMode)
        stream.start()
        with stream:
            self.verify_stream_fps(stream, 2)
    
      
    def get_all_permutations(self):
        perList = []
        i = 0
        for device in self.devices:
            for sensorType in [openni2.SENSOR_DEPTH, openni2.SENSOR_COLOR, openni2.SENSOR_IR]:
                sensorInfo = device.get_sensor_info(sensorType)
                if not sensorInfo is None:
                    videoModes = sensorInfo.videoModes
                    for videoMode in videoModes:
                        perList.append([i, copy.deepcopy(sensorType), copy.deepcopy(videoMode)])
            i+=1
        return perList

    def test_permutations(self):
        CrayolaTestBase.setUp(self)
        permutations = self.get_all_permutations()
        CrayolaTestBase.tearDown(self)
        for perm in permutations:
            if  perm[2].resolutionY == 720:
                pass
            else:
                yield self.check_frames, perm[0], perm[1], perm[2]
    
            

            