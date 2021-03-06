# This file is executed on every boot (including wake-boot from deepsleep)
#import esp
#esp.osdebug(None)
import os, uos, utime, gc, webrepl
from machine import Pin as pin
from machine import I2C as _i2c
#uos.dupterm(None, 1) # disable REPL on UART(0)

webrepl.start()
gc.enable()

# global varibles
DEBUG = True    # enable or disable debugging
EV = False      # event loop flag
IP = ''         # the server ip address

# Logger to print to the terminal when the debug flag is set True
def log(msg):
        if DEBUG:
                print(msg)

# wifi state flags
WIFI_ERROR = -1
WIFI_DISABLED = 0
WIFI_ENABLED = 1
WIFI_CONNECTED = 2
WIFI_AP = 3

#I2C flags
I2C_FOUND = 1
I2C_NIL = 0

# wifi flag setter
def updateWifiState(state = WIFI_ENABLED):
        global wifi_state
        wifi_state = state
        log('wifi state set to %d'%(state))

# i2c flag setter
def updateI2CState(state = I2C_NIL):
        global i2c_state
        i2c_state = state
        log('i2c state set to %d'%(state))

# ip flag setter
def updateIP(ip):
        global IP
        IP = ip
        log('ip set to %s'%str(ip))

# wifi flag getter
def getWifiState():
        global wifi_state
        return wifi_state

# i2c flag getter
def getI2CState():
        global i2c_state
        return i2c_state

# ip flag getter
def getIP():
        global IP
        return IP

# runtime flags
updateWifiState(WIFI_DISABLED)
updateI2CState(I2C_NIL)

# The first_boot routine first sets up the access point
# Then helps to configure the default wifi network
# ESSID: console AP
# Password: consolePass
def first_boot():
        import network
        import ubinascii
        # first configure as a access point

        #  get the MAC address
        ap = network.WLAN(network.AP_IF)
        ap_mac = ubinascii.hexlify(ap.config('mac'),':').decode()
        
        # strip the last 6 characters to add them to the essid
        ap_mac = ap_mac[9::]
        ap_mac = ap_mac.split(':')
        ap_essid = ('Console-%s%s%s' %(ap_mac[0], ap_mac[1], ap_mac[2]))
        
        # configure the access point and enable it
        ap.active(True)
        ap.config(essid = ap_essid, password = 'consolePass', channel = 1, authmode = 4)       
        if ap.active():
                log('%s active:' % str(ap_essid))
                updateWifiState(WIFI_AP)
                utime.sleep_ms(500)
        else:
                log('could not initiate AP!! Try resetting device')
                updateWifiState(WIFI_ERROR)

# The connect_wifi(ssid, authKey, disableAP) routine connects to an
# existing wifi network. It takes the following params:
#       SSID    :       (String) the ssid of the wifi network to connect to
#       authKey :       (String) the password
#       disableAP:      (boolean) should disable built-in access point or not
def connect_wifi(ssid, authKey, disableAP):
        import network
        sta_if = network.WLAN(network.STA_IF)
        updateWifiState(WIFI_ENABLED)
        if not sta_if.isconnected():
                sta_if.active(True)
                log('connecting to %s Please wait' %str(ssid))
                sta_if.connect(ssid, authKey)

                utime.sleep_ms(3000)
                if not sta_if.isconnected():
                        log('Could not connect to %s! Enabling Access Point' %str(ssid))                       
                        updateWifiState(WIFI_ERROR)
                        sta_if.active(False)
                        utime.sleep_ms(500)
                        first_boot()
                else:
                        log('Connected to network')
                        updateWifiState(WIFI_CONNECTED)
                        # disable the access point
                        (network.WLAN(network.AP_IF)).active(not disableAP)

# The initial setup method
# Search for the config.cfg file. If it does not exist, excute the first_run routine
# If exists, connect to an existing network and configure MQTT
#       override        :       (boolean) force into firstboot
def search_cfg(override):
        inDir = os.listdir()
        if (override) or ('config.py' not in inDir):
                # config not exists - execute first_boot()
                log('first boot')
                first_boot()
        else:
                import config
                connect_wifi(config.wifi_ssid, config.wifi_key, config.wifi_autoConnect)
                pass

search_cfg(False)


#scans the i2c pins (1, 2) for devices
#if nothing is returned, it resets the machine
def scan_i2c():
        log('scanning i2c port')
        i2c = _i2c(scl=pin(1), sda=pin(2))
        scans = i2c.scan()
        busy_led = pin(0, pin.OUT)

        if (len(scans) == 0):
                log("No I2C device found! Reset device..")
                busy_led.on()
                utime.sleep(2)
                busy_led.off()
                utime.sleep_ms(200)
                updateI2CState(I2C_NIL)
        else:
                log("i2c found:")
                for addr in scans:
                        log(hex(addr))
                busy_led.off()
                utime.sleep(1)
                updateI2CState(I2C_FOUND)
    
scan_i2c()

# Handle the query from the GET request
# Takes the query string as arg
def handleGET(query):
        gc.collect()
        import pwm, sensors, gpio, utime
        query = query.replace('&','\r\n')
        query = query.replace('%20',' ')
        exec(query, {'pwm': pwm, 'gpio': gpio, 'sensors': sensors, 'utime': utime})

# create a webserver to read all the inputs from the remote
# supports only live mode
def createServer():
        if (wifi_state != WIFI_ERROR or wifi_state != WIFI_DISABLED or wifi_state != WIFI_ENABLED):
                log('initiating server')
                # create a socket obj
                import socket, network
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

                # get the ip address if connected to a foreign network
                serverIp = '192.168.4.1'
                if (wifi_state == WIFI_CONNECTED):
                        conn = network.WLAN(network.STA_IF)
                        serverIp = conn.ifconfig()[0]
                
                sock.bind((serverIp, 80))
                sock.listen(1)
                log('server running at %s port 80'%str(serverIp))

                while True:
                        cxn, addr = sock.accept()
                        log('incoming from %s'%str(addr))
                        req = cxn.recv(500)
                        req = str(req)
                        log('request: %s'%req)
                        sendBack = 'true'

                        # process the request here and only if it is not a favicon req
                        try:
                                if (req.find('/?') != -1):
                                        # it is a search query
                                        query = req.split("/?")
                                        log('firstPass: %s'%str(query))
                                        # filter out the favicon query
                                        if (req.find('/favicon.ico') == -1):
                                                query = query[1].split('?/')[0]
                                                log('secondPass: %s'%str(query))
                                                # look for queries demanding a return
                                                sendBack = handleGET(query)
                                cxn.send('HTTP/1.1 200 OK\n')
                        except Exception as e:
                                log('something went wrong: %s'%str(e))
                                cxn.send('HTTP/1.1 405 Method Not Allowed\n')
                        

                        cxn.send('Content-Type: text/html\n')
                        cxn.send('Connection: close\n\n')
                        cxn.sendall('Connection Successful!%s'%(sendBack))
                        cxn.close()

createServer()

def intr(pin):
        global EV
        if not EV:
                EV = True
                global led_stat
                led_stat.on()
                main()
                led_stat.off()
                EV = False

led_stat = pin(16, pin.OUT)

def liveMode(enable=True):
        global led_stat
        if (enable):
                btn_flash = pin(0, pin.OUT)
                led_stat.on()
                log('liveMode')
        else:
                btn_flash = pin(0, pin.IN, pin.PULL_UP)
                led_stat.off()
                btn_flash.irq(handler=intr, trigger=pin.IRQ_FALLING)
                log('eventMode')

#liveMode(False)
