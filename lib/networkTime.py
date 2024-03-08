import machine
import ntptime
import utime

# A network connection must be established befor instantiating this class!
class NtpTimeClass:
    def __init__(self, utcShift):
        ntptime.settime()           # Synchronise the system time using NTP
        rtc = machine.RTC()
        utc_shift = utcShift
        tm = utime.localtime(utime.mktime(utime.localtime()) + utc_shift*3600)
        print('tm: ', tm)
        tm = tm[0:3] + (0,) + tm[3:6] + (0,)
        print('tm: ', tm)
        rtc.datetime(tm) 

    def getDate(self):
        (year, month, mday, hour, minute, second, weekday, yearday) = utime.localtime()
        return "%s/%s/%s" % (year, month, mday)
    
    def getTime(self):
        (year, month, mday, hour, minute, second, weekday, yearday) = utime.localtime()
        return "%s:%s:%s" % (hour, minute, second)
    
    def getDateTime(self):
        (year, month, mday, hour, minute, second, weekday, yearday) = utime.localtime()
        return (year, month, mday, hour, minute, second, weekday, yearday)
        return "%s/%s/%s %s:%s:%s" % (year, month, mday, hour, minute, second)