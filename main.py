import esp
import gc

from lib.wifi_connect import MyWifiClass
from lib.networkTime import NtpTimeClass
from secrets.wifi_config import SSID, PASSWORD

wifi = None
ntp = None


def setupNetwork():
    global wifi
    
    #SSID = 'GC_Star24'
    #PW = 'Misty911!'
    
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
    
if __name__ == "__main__":
    try:
        setupNetwork()
        #get_ntp_time()
        get_mem_info()
        
        import ota_test
        
        print('Importing test_file >>>>')
        import test_file
        
    except KeyboardInterrupt:
        print("Keyboard interrupt ctrl-c")


print('Exit to REPL')