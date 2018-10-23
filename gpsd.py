from gps3 import gps3
import threading

class GPSD():
    def __init__(self):
        self.socket = gps3.GPSDSocket()
        self.data_stream = gps3.DataStream()
        self.socket.connect()
        self.socket.watch()
        self.lock = threading.Lock()

    def loop(self):
        for new_data in self.socket:
            if new_data:
                seld.data_stream.unpack(new_data)
                if self.data_stream.TPV['status'] != 2:
                    self.valid = False
                    continue
                self.valid = True
                self.latitude = data_stream.TPV['lat']
                self.longitude = data_stream.TPV['lon']
                self.altitude = data_stream.TPV['alt']
                self.separation = 0.0
                
