import network

'''
wifi class to connect to local router
'''
class MyWifiClass:
    def __init__(self, 
                wifi_ssid = None, 
                wifi_PW = None):

        if (wifi_ssid == None) or (wifi_PW == None):
            raise ValueError('WiFi ssid and PW must be specified')
        
        self.wifi_ssid = wifi_ssid
        self.wifi_PW = wifi_PW
        self.sta_if = network.WLAN(network.STA_IF)

    def do_connect(self):
        try:
            self.sta_if.active(False)
            
            if self.sta_if.isconnected() == True:
                self.sta_if.disconnect()
                
            if not self.sta_if.isconnected():
                print('Connecting to network...')
                self.sta_if.active(True)
                self.sta_if.connect(self.wifi_ssid, self.wifi_PW)
                while not self.sta_if.isconnected():
                    pass

            print('Connected!')
            print(f'Network configuration: {self.sta_if.ifconfig()}')
            print(f'Network strength: {self.sta_if.status('rssi')}')
                  
        except:
            raise

    def do_disconnect(self):
        print('Disconnecting from network...')
        if self.sta_if.isconnected() == True:
            self.sta_if.disconnect()

    def wifi_strength(self):
        return self.sta_if.status('rssi')
'''
End MyWifiClass class
'''