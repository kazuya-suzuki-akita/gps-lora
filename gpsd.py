from gps3 import gps3
import threading

class GPSD():
    def __init__(self):
        self.socket = gps3.GPSDSocket()
        self.data_stream = gps3.DataStream()
        self.socket.connect()
        self.socket.watch()
        self.lock = threading.Lock()
        self.valid = False

    def loop(self):
        for new_data in self.socket:
            if new_data:
                self.data_stream.unpack(new_data)
                mode = self.data_stream.TPV['mode']
                if not isinstance(mode, int) or mode < 2 :
                    self.valid = False
                    continue
                self.valid = True
                self.latitude = self.data_stream.TPV['lat']
                self.longitude = self.data_stream.TPV['lon']
                self.altitude = self.data_stream.TPV['alt']
                self.separation = 0.0
                
