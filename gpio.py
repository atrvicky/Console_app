from machine import Pin as pin

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