from machine import Pin as pin
import pca, utime

_DC_MOTORS = {
    1 : (0, 2, 1),
    2 : (5, 3, 4),
    3 : (9, 11, 10),
    4 : (7, 8, 6)
    }

io = pca.PCA9685()

io.freq(1600)

mappedPin = {
    1 : 14,
    2 : 13,
    3 : 12
}

def getMappedPin(inPin):
    """
        Map the LEDs to the corresponding pins in the PCA
    """
    if (inPin >= 1 and inPin <= 3):
        return mappedPin[inPin]
    else:
        return 1

def enableLED1(lux = 4095):
    """
        Enables the LED on pin 14 of the PCA driver
    """
    io.duty(14, lux)

def enableLED2(lux = 4095):
    """
        Enables the LED on pin 13 of the PCA driver
    """
    io.duty(13, lux)

def enableLED3(lux = 4095):
    """
        Enables the LED on pin 12 of the PCA driver
    """
    io.duty(12, lux)

def toggleLED1():
    """
        Toggles the LED on pin 14 of the PCA driver
    """
    preset = io.duty(14)
    if (preset > 0):
        io.duty(14, 0)
    else:
        io.duty(14, 4095)

def toggleLED2():
    """
        Toggles the LED on pin 13 of the PCA driver
    """
    preset = io.duty(13)
    if (preset > 0):
        io.duty(13, 0)
    else:
        io.duty(13, 4095)

def toggleLED3():
    """
        Toggles the LED on pin 12 of the PCA driver
    """
    preset = io.duty(12)
    if (preset > 0):
        io.duty(12, 0)
    else:
        io.duty(12, 4095)

def enableAll(lux = 4095):
    """
        Enables all the LEDs of the PCA driver
    """
    enableLED1(lux)
    enableLED2(lux)
    enableLED3(lux)

def disableLED1():
    """
        Disable the LED on pin 14 of the PCA driver
    """
    io.duty(14, 0)

def disableLED2():
    """
        Disable the LED on pin 13 of the PCA driver
    """
    io.duty(13, 0)

def disableLED3():
    """
        Disable the LED on pin 12 of the PCA driver
    """
    io.duty(12, 0)

def disableAll():
    """
        Enables all the LEDs of the PCA driver
    """
    disableLED1()
    disableLED2()
    disableLED3()

def blink(LED, lux=4095, dur=0.5, repeatFor=1):
    """
        Blink the "LED" "repeatFor" number of times with max "lux" brightness
        at an interval of "dur" seconds
    """
    LED = getMappedPin(LED)
    io.duty(LED, 0)
    for lim in range (0, repeatFor):
        io.duty(LED, lux)
        utime.sleep(dur)
        io.duty(LED, 0)
        utime.sleep(dur)

def fade(LED, lux=4095, repeatFor=1):
    """
        Fades the "LED" "repeatFor" number of times with max "lux" brightness
    """
    LED = getMappedPin(LED)
    io.duty(LED, 0)
    for lim in range (0, repeatFor):
        for brightness in range(0, lux):
            io.duty(LED, brightness)
        
        for brightness in range(lux, 0, -1):
            io.duty(LED, brightness)
    io.duty(LED, 0)

# the motor controls
def _pin(pin, value=None):
    if value is None:
        return bool(io.pwm(pin)[0])
    if value:
        io.pwm(pin, 4096, 0)
    else:
        io.pwm(pin, 0, 0)

def runMotor(index, value=None):
    if (index in range(1, 5)):
        pwm, in2, in1 = _DC_MOTORS[index]
        if value is None:
            value = io.duty(pwm)
            if _pin(in2) and not _pin(in1):
                value = -value
            return value
        if value > 0:
            # Forward
            _pin(in2, False)
            _pin(in1, True)
        elif value < 0:
            # Backward
            _pin(in1, False)
            _pin(in2, True)
        else:
            # Release
            _pin(in1, False)
            _pin(in2, False)
        io.duty(pwm, abs(value))
    else:
        print("Invalid motor index!")

def brakeMotor(index):
    pwm, in2, in1 = _DC_MOTORS[index]
    _pin(in1, True)
    _pin(in2, True)
    io.duty(pwm, 0)

def brakeAllMotors():
    for i in range(1, 5):
        brakeMotor(i)