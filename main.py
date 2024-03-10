# Adding a change to force ota update 5x 

import esp
import gc
import machine
from time import sleep

from lib.wifi_connect import MyWifiClass
from lib.networkTime import NtpTimeClass
from secrets.wifi_config import SSID, PASSWORD

wifi = None
ntp = None


def setupNetwork():
    global wifi
    
    wifi = MyWifiClass(SSID, PASSWORD)
    wifi.do_connect()
    
    print('wifi strength: ', wifi.wifi_strength())

def get_ntp_time():
    global ntp
    
    ntp = NtpTimeClass(-8)
    
    print('\nDate: ', ntp.getDate())
    print('Time: ', ntp.getTime())
    print('Date Time: ', ntp.getDateTime())
    
def get_mem_info():
    flashSize = 0
    memFree = 0
    
    flashSize = esp.flash_size()
    memFree = gc.mem_free()
    
    print('Flash size: ', flashSize)
    print('Free memory: ', memFree) 

def checkForUpdates():
    from ota import OTAUpdater
    
    needReset = False
    
    print('\nUPDATING main.py')
    firmware_url = "https://raw.githubusercontent.com/wilki48/ESP32-S3_TestCode/main/"
    ota_updater = OTAUpdater(SSID, PASSWORD, firmware_url, "main.py")
    if (ota_updater.download_and_install_update_if_available() == True):
        needReset = True
    
    print('\nUPDATING ota.py')
    firmware_url = "https://raw.githubusercontent.com/wilki48/ESP32-S3_TestCode/main/"
    ota_updater = OTAUpdater(SSID, PASSWORD, firmware_url, "ota.py")
    if (ota_updater.download_and_install_update_if_available() == True):
        needReset = True
    
    if (needReset == True):
        # Restart the device to run the new code.
        print("Restarting device...")
        sleep(0.25)
        machine.reset()  # Reset the device to run the new code.
    
if __name__ == "__main__":
    try:
        setupNetwork()
        #get_ntp_time()
        get_mem_info()
        checkForUpdates()
        
    except KeyboardInterrupt:
        print("Keyboard interrupt ctrl-c")


print('Exit to REPLsfgh nertnuyetyumtyjm')