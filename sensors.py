from machine import Pin as pin
import mcp

io = mcp.MCP23017()

def enableIR1():
    """
        Enables the IR1 on pin B0 of the MCP as input
    """
    io.setup(8, mcp.IN)

def enableIR2():
    """
        Enables the IR2 on pin B1 of the MCP as input
    """
    io.setup(9, mcp.IN)

def readIR1():
    """
        Returns the state of IR1 at B0 of the MCP
    """
    return io.input(8)

def readIR2():
    """
        Returns the state of IR2 at B1 of the MCP
    """
    return io.input(9)

# The IR would be enabled by default. It could also be bypassed for some extra pin real-estate
enableIR1()
enableIR2()

def bypassIR1():
    """
        Enables the IR1 on pin B0 of the MCP as output
    """
    io.setup(8, mcp.OUT)

def bypassIR2():
    """
        Enables the IR2 on pin B1 of the MCP as output
    """
    io.setup(9, mcp.OUT)

#Need to add methods for Ultrasound