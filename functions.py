import pwm, gpio, sensors

'''
    This file contains all the functions that are to be handled from the boot.py

'''
importPwm()
# importPWM

pwm.toggleLED1()
# toggleLED1
# toggleLED2
# toggleLED3

pwm.enableLED1(lux=4095)
# enableLED1&4095
# enableLED2&4095
# enableLED3&4095

pwm.enableAll(lux=4095)
# enableAllLED&4095

pwm.disableLED1()
# disableLED1
# disableLED2
# disableLED3

pwm.disableAll()
# disableAll

pwm.blink(1, lux=4095, dur=500, repeatFor=1)
# blink&1,4095,500,1

pwm.fade(1, lux=4095, repeatFor=1)
# fade&1,4095,1

pwm.runMotor(1, value=4095)
# runMotor&index=1,val=4095

pwm.brakeMotor(1)
# brakeMotor&index=1

pwm.brakeAllMotors()
# brakeAllMotors

delPWM()
# delPWM

#--------------

importGPIO()
# importGPIO

gpio.runServo(0, duty=10, override=False, freq=50)
# runServo&0,10,0,50

gpio.runServoAngle(0, angle=180, override=False, freq=50)
# runServoAngle&0,180,0,50

gpio.releaseServo(0)
# releaseServo&0

gpio.readPin(0)
# readPin&0$

gpio.readPinPUP(0)
# readPinPUP&0$

gpio.writePin(0,(1))
# writePin&0,1

gpio.togglePin(0)
# togglePin&0

delGPIO()
# delGPIO

#--------------

utime.sleep(1)
# delay=sec

#--------------

importSensors()
# importSensors

sensors.readIR1()
# $readIR1
# $readIR2

sensors.home()
# home

sensors.clear()
# clear

sensors.set_cursor(0, 0)
# setCursor=x,y

sensors.enable_display(True)
# enableDisplay=state

sensors.show_cursor(True)
# showCursor=state

sensors.blink(True)
# blinkCursor=state

sensors.set_backlight(True)
# setBacklight=state

sensors.move_left()
# moveCursorLeft

sensors.move_right()
# moveCursorRight

sensors.set_left_to_right()
# setLCDLTR

sensors.autoscroll(ascrl=True, scrlDelay=0)
# autoscroll=ascrl,delay

pwm.setLCDBrightness(0)
# setLCDBrightness=val

sensors.message('Hello, World!')
# printLCD=msg

sensors.set1604(False)
# LCD1604=state

delSensors()
# delSensors

#--------------

def pin0Listener(pin):

gpio.pinStateListener(0, _listener=pin0Listener)