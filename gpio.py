from machine import Pin as pin

def readPin(pinNo):
    """
        Read and return the pin value.
    """
    p = pin(pinNo, pin.IN)
    return p.value()

def readPinPUP(pinNo):
    """
        Read and return the pin value.
        Note: The pin is pulled up.
    """
    p = pin(pinNo, pin.IN, pin.PULL_UP)
    return p.value()

def writePin(pinNo, val):
    """
        Write a value (0 or 1) to the pin.
    """
    p = pin(pinNo, pin.OUT)
    p.value(val)
    
def togglePin(pinNo):
    """
        Toggle the value (0 or 1) of the pin and return the new value.
    """
    p = pin(pinNo, pin.OUT)
    p.value(not(p.value()))
    return p.value()

def pinOn(pinNo):
    """
        Set the pin as High and returns the new value
    """
    p = pin(pinNo, pin.OUT)
    p.on()
    return p.value()

def pinOff(pinNo):
    """
        Set the pin as Low and returns the new value.
    """
    p = pin(pinNo, pin.OUT)
    p.off()
    return p.value()

def pinStateListener(pinNo, _listener=None, _trigger=pin.IRQ_RISING):
    """
        sets a pin state change listener
    """
    if _listener is not None:
        p = pin(pinNo, pin.IN, pin.PULL_UP)
        p.irq(handler=_listener, trigger=_trigger)
    else:
        pass