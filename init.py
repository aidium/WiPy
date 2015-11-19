# init.py
import machine
from network import WLAN
import socket

__ssid='ssid'
__nwpass='nwpass'

# Use a static ip for easier access when developing
__myip = '192.168.1.81'
__gateway = '192.168.1.1'
__netmask = '255.255.255.0'
__dns = '8.8.8.8'
__syslogserver = '192.168.1.166'

# Syslog to the specified syslog server
# Facility USER = 1, Level ERR = 3
# <xx> = Level + Facility * 8 = 3 + 1 * 8 = 11
# Format follows BSD syslog RFC
def syslog(msg):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    ret = s.sendto('<11>' + __myip + ' WiPy ' + msg, (__syslogserver, 514))
    s.close()
    return ret

def wlan_connect():
    wifi = WLAN(mode=WLAN.STA)

    wifi.ifconfig(config=(__myip, __netmask, __gateway, __dns))
    wifi.scan()     # scan for available networks
    wifi.connect(ssid=__ssid, auth=(WLAN.WPA2, __nwpass))
    while not wifi.isconnected():
        pass

    syslog('WiPy is up and running')

    wifi.irq(trigger=WLAN.ANY_EVENT, wake=machine.SLEEP)

    machine.sleep()
