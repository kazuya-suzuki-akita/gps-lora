from gps3 import gps3

class GPSD():
    def __init__(self):
        self.socket = gps3.GPSDSocket()
        self.data_stream = gps3.DataStream()
        self.socket.connect()
        self.socket.watch()

def loop(self):
        for new_data in gps_socket:
            if new_data:
                data_stream.unpack(new_data)
                if data_stream.TPV['status'] != 2:
                    self.valid = False
                    continue
                self.valid = True
                self.latitude = data_stream.TPV['lat']
                self.longitude = data_stream.TPV['lon']
                self.altitude = data_stream.TPV['alt']
                self.separation = 0.0
                
