#testing mcp23017

#import mcp

#i2c will not work when connect via USB


#def run():
	#io = mcp.MCP23017(gpioScl=1, gpioSda=2)
	#pins = list(range(0,16))
	#nxt = {}
	#for val in pins:
	#	io.setup(val, mcp.OUT)
	#	nxt[val] = True
	#	
	#io.output_pins(nxt)