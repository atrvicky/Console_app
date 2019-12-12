from machine import Pin as pin, PWM
import math, time

mappedPin = {
    0 : 3,
    1 : 4,
    2 : 5,
    3 : 9,
    4 : 15,
    5 : 13,
    6 : 12,
    7 : 14,
    8 : 16
}

def dutyCycleMap(x):
    """
        If your number X falls between A and B, and you would like Y to fall between C and D, you can apply the following linear transform:
        Y = (X-A)/(B-A) * (D-C) + C

        @param x {int}: dutyCycle in microSeconds
        Returns the dutycycle between 0 and 1023 for inputs ranging from 1000 and 2000

        The frequency is 50 Hz
        So, the minimum dutyCycle is 0 microseconds
        And the maximum dutyCycle is 20 milliseconds = 20000 microseconds = 20000
        The dutyCycle ranges from 1000 uS (1.0ms) for 0 degree and 2000 uS (2.0ms) for 180 degree (empirical)
    """
    # limit x between 1000 and 2000
    x = min(180, max(0, int(x)))

    #dcm = math.floor((x-1000) / (19000) * (1023))
    dcm = math.floor((x) / 180 * 129 + 1)

    '''
        for 50 Hz, the dcm values would be
        0 deg - 51
        50 deg - 55
        90 deg - 76
        130 deg - 100
        180 deg - 102
    '''

    # print('dc: ' + str(dcm))
    return dcm

def getMappedPin(inPin):
    """
        Map the GPIOs to the corresponding pins in the MCU
    """
    if (inPin >= 0 and inPin <= 8):
        return mappedPin[inPin]
    else:
        return 0

def readPin(pinNo):
    """
        Read and return the pin value.
    """
    pinNo = getMappedPin(pinNo)
    p = pin(pinNo, pin.IN)
    return p.value()

def readPinPUP(pinNo):
    """
        Read and return the pin value.
        Note: The pin is pulled up.
    """
    pinNo = getMappedPin(pinNo)
    p = pin(pinNo, pin.IN, pin.PULL_UP)
    return p.value()

def writePin(pinNo, val):
    """
        Write a value (0 or 1) to the pin.
    """
    pinNo = getMappedPin(pinNo)
    p = pin(pinNo, pin.OUT)
    p.value(val)
    
def togglePin(pinNo):
    """
        Toggle the value (0 or 1) of the pin and return the new value.
    """
    pinNo = getMappedPin(pinNo)
    p = pin(pinNo, pin.OUT)
    p.value(not(p.value()))
    return p.value()

def pinOn(pinNo):
    """
        Set the pin as High and returns the new value
    """
    pinNo = getMappedPin(pinNo)
    p = pin(pinNo, pin.OUT)
    p.on()
    return p.value()

def pinOff(pinNo):
    """
        Set the pin as Low and returns the new value.
    """
    pinNo = getMappedPin(pinNo)
    p = pin(pinNo, pin.OUT)
    p.off()
    return p.value()

def pinStateListener(pinNo, _listener=None, _trigger=pin.IRQ_RISING):
    """
        sets a pin state change listener
    """
    if _listener is not None:
        pinNo = getMappedPin(pinNo)
        p = pin(pinNo, pin.IN, pin.PULL_UP)
        p.irq(handler=_listener, trigger=_trigger)
    else:
        pass

def resetAllPins():
    for pinNo in range(0, 9):
        pinNo = getMappedPin(pinNo)
        p = pin(pinNo, pin.OUT)
        p.off()
        return p.value()

# Servos
# duty = 1 + 0.9277778*angle - 0.00117284*angle^2


def runServo(pinNo, duty=None, override=False, freq=50):
    if not override:
        servoPin = getMappedPin(pinNo)
    else:
        servoPin = pinNo
    servo = PWM(pin(servoPin))
    servo.freq(freq)

    if duty is not None:
        # limit the duty between 1 & 130
        duty = min(130, max(0, int(duty)))
        servo.duty(duty)        
        return servo
    else:
        #return the angle of the servo
        return servo.duty()


def runServoAngle(pinNo, angle=None, override=False, freq=50):
    if not override:
        servoPin = getMappedPin(pinNo)
    else:
        servoPin = pinNo
    servo = PWM(pin(servoPin))
    servo.freq(freq)

    # limit the angle between 1 & 180
    if angle < 0:
        angle = 0
    elif angle > 180:
        angle = 180
    mappedDuty = math.ceil(1 + 0.9277778*angle - 0.00117284*angle*angle)
    servo.duty(mappedDuty)        
    return servo


def releaseServo(pinNo, override=False):
    if not override:
      servoPin = getMappedPin(pinNo)
    else:
      servoPin = pinNo
    servo = PWM(pin(servoPin))
    servo.deinit()



