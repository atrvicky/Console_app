# This file is executed on every boot (including wake-boot from deepsleep)
#import esp
#esp.osdebug(None)
import uos, machine, utime
#uos.dupterm(None, 1) # disable REPL on UART(0)
import gc
import webrepl
webrepl.start()
gc.collect()
import os

DEBUG = True    # enable or disable debugging
pin = machine.Pin
EV = False      # event loop flag

# Logger to print to the terminal when the debug flag is set True
def log(msg):
        if DEBUG:
                print(msg)

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
        ap.config(essid = ap_essid, password = 'consolePass', channel = 1, authmode = 4)
        ap.active(True)

# The connect_wifi(ssid, authKey, disableAP) routine connects to an
# existing wifi network. It takes the following params:
#       SSID    :       (String) the ssid of the wifi network to connect to
#       authKey :       (String) the password
#       disableAP:      (boolean) should disable built-in access point or not
def connect_wifi(ssid, authKey, disableAP):
        import network
        sta_if = network.WLAN(network.STA_IF)
        if not sta_if.isconnected():
                log('connecting to network...')
                sta_if.active(True)
                sta_if.connect(ssid, authKey)

                # disable the access point
                (network.WLAN(network.AP_IF)).active(not disableAP)

                while not sta_if.isconnected():
                        pass

# The initial setup method
# Search for the config.cfg file. If it does not exist, excute the first_run routine
# If exists, connect to an existing network and configure MQTT
#       override        :       (boolean) force into firstboot
def search_cfg(override):
        inDir = os.listdir()
        if (override) or ('CONFIG.CFG' not in inDir):
                # config not exists - execute first_boot()
                log('first boot')
                first_boot()
        else:
                pass

search_cfg(True)


#scans the i2c pins (1, 2) for devices
#if nothing is returned, it resets the machine
def scan_i2c():
	i2c = machine.I2C(scl=pin(1), sda=pin(2))
	scans = i2c.scan()
	busy_led = pin(0, pin.OUT)
	
	if (len(scans) == 0):
		log("No I2C device found! Reset device..")
		busy_led.on()
		utime.sleep(2)
		busy_led.off()
		utime.sleep_ms(200)
		machine.reset()
	else:
		log("i2c found:")
		for addr in scans:
			log(hex(addr))
                busy_led.off()
                utime.sleep(1)
		
scan_i2c()

def intr(pin):
        global EV
        if not EV:
                EV = True
                global led_stat
                led_stat.on()
                main()
                led_stat.off()
                EV = False

btn_flash = pin(0, pin.IN, pin.PULL_UP)
led_stat = pin(16, pin.OUT)
led_stat.off()
btn_flash.irq(handler=intr, trigger=pin.IRQ_FALLING)