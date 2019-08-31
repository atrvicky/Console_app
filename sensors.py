from machine import Pin as pin
import time
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

# Need to add methods for Ultrasound


# LCD section

# Define MCP pins connected to the LCD.
lcd_rs = 7
lcd_en = 5
lcd_d4 = 4
lcd_d5 = 3
lcd_d6 = 2
lcd_d7 = 1
lcd_k = 0

# Define LCD column and row size for 16x2 LCD.
lcd_columns = 16
lcd_rows = 2

# Commands
LCD_CLEARDISPLAY = 0x01
LCD_RETURNHOME = 0x02
LCD_ENTRYMODESET = 0x04
LCD_DISPLAYCONTROL = 0x08
LCD_CURSORSHIFT = 0x10
LCD_FUNCTIONSET = 0x20
LCD_SETCGRAMADDR = 0x40
LCD_SETDDRAMADDR = 0x80

# Entry flags
LCD_ENTRYRIGHT = 0x00
LCD_ENTRYLEFT = 0x02
LCD_ENTRYSHIFTINCREMENT = 0x01
LCD_ENTRYSHIFTDECREMENT = 0x00

# Control flags
LCD_DISPLAYON = 0x04
LCD_DISPLAYOFF = 0x00
LCD_CURSORON = 0x02
LCD_CURSOROFF = 0x00
LCD_BLINKON = 0x01
LCD_BLINKOFF = 0x00

# Move flags
LCD_DISPLAYMOVE = 0x08
LCD_CURSORMOVE = 0x00
LCD_MOVERIGHT = 0x04
LCD_MOVELEFT = 0x00

# Function set flags
LCD_8BITMODE = 0x10
LCD_4BITMODE = 0x00
LCD_2LINE = 0x08
LCD_1LINE = 0x00
LCD_5x10DOTS = 0x04
LCD_5x8DOTS = 0x00

# Offset for up to 4 rows.
# LCD_ROW_OFFSETS = (0x00, 0x40, 0x14, 0x54)
LCD_ROW_OFFSETS = (0x00, 0x40, 0x10, 0x50)

# Char LCD plate GPIO numbers.
LCD_PLATE_RS = 15
LCD_PLATE_RW = 14
LCD_PLATE_EN = 13
LCD_PLATE_D4 = 12
LCD_PLATE_D5 = 11
LCD_PLATE_D6 = 10
LCD_PLATE_D7 = 9
LCD_PLATE_RED = 6
LCD_PLATE_GREEN = 7
LCD_PLATE_BLUE = 8

# Char LCD plate button names.
SELECT = 0
RIGHT = 1
DOWN = 2
UP = 3
LEFT = 4

# Char LCD backpack GPIO numbers.
LCD_BACKPACK_RS = 1
LCD_BACKPACK_EN = 2
LCD_BACKPACK_D4 = 3
LCD_BACKPACK_D5 = 4
LCD_BACKPACK_D6 = 5
LCD_BACKPACK_D7 = 6
LCD_BACKPACK_LITE = 7

# Initialize display control, function, and mode registers.
displaycontrol = LCD_DISPLAYON | LCD_CURSOROFF | LCD_BLINKOFF
displayfunction = LCD_4BITMODE | LCD_1LINE | LCD_2LINE | LCD_5x8DOTS
displaymode = LCD_ENTRYLEFT | LCD_ENTRYSHIFTDECREMENT

# Setup all pins as outputs.
for pin in (lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7, lcd_k):
    io.setup(pin, mcp.OUT)

def home():
    """Move the cursor back to its home (first line and first column)."""
    write8(LCD_RETURNHOME)  # set cursor position to zero
    _delay_microseconds(3000)  # this command takes a long time!

def clear():
    """Clear the LCD."""
    write8(LCD_CLEARDISPLAY)  # command to clear display
    _delay_microseconds(3000)  # 3000 microsecond sleep, clearing the display takes a long time

def set_cursor(col, row):
    global lcd_rows
    """Move the cursor to an explicit column and row position."""
    # Clamp row to the last row of the display.
    if row > lcd_rows:
        row = lcd_rows - 1
    # Set location.
    write8(LCD_SETDDRAMADDR | (col + LCD_ROW_OFFSETS[row]))

def enable_display(enable):
    global displaycontrol
    """Enable or disable the display.  Set enable to True to enable."""
    if enable:
        displaycontrol |= LCD_DISPLAYON
    else:
        displaycontrol &= ~LCD_DISPLAYON
    write8(LCD_DISPLAYCONTROL | displaycontrol)

def show_cursor(show):
    global displaycontrol
    """Show or hide the cursor.  Cursor is shown if show is True."""
    if show:
        displaycontrol |= LCD_CURSORON
    else:
        displaycontrol &= ~LCD_CURSORON
    write8(LCD_DISPLAYCONTROL | displaycontrol)

def blink(blink):
    global displaycontrol
    """Turn on or off cursor blinking.  Set blink to True to enable blinking."""
    if blink:
        displaycontrol |= LCD_BLINKON
    else:
        displaycontrol &= ~LCD_BLINKON
    write8(LCD_DISPLAYCONTROL | displaycontrol)

def move_left():
    """Move display left one position."""
    write8(LCD_CURSORSHIFT | LCD_DISPLAYMOVE | LCD_MOVELEFT)

def move_right():
    """Move display right one position."""
    write8(LCD_CURSORSHIFT | LCD_DISPLAYMOVE | LCD_MOVERIGHT)

def set_left_to_right():
    global displaymode
    """Set text direction left to right."""
    displaymode |= LCD_ENTRYLEFT
    write8(LCD_ENTRYMODESET | displaymode)

def set_right_to_left():
    global displaymode
    displaymode &= ~LCD_ENTRYLEFT
    write8(LCD_ENTRYMODESET | displaymode)

def autoscroll(ascrl=False, scrlDelay=0):
    global displaymode
    delay=0
    if ascrl:
        displaymode |= LCD_ENTRYSHIFTINCREMENT
        delay = scrlDelay
    else:
        delay=0
        displaymode &= ~LCD_ENTRYSHIFTINCREMENT
    write8(LCD_ENTRYMODESET | displaymode, delay)

def message(text):
    line = 0
    # Iterate through each character.
    for char in text:
        # Advance to next line if character is a new line.
        if char == '\n':
            line += 1
            # Move to left or right side depending on text direction.
            col = 0 if displaymode & LCD_ENTRYLEFT > 0 else lcd_columns-1
            set_cursor(col, line)
        # Write the character to the display.
        else:
            write8(ord(char), True)

def set_backlight(backlight):
    """Enable or disable the backlight.  If PWM is not enabled (default), a
    non-zero backlight value will turn on the backlight and a zero value will
    turn it off.  If PWM is enabled, backlight can be any value from 0.0 to
    1.0, with 1.0 being full intensity backlight.
    """
    io.output(lcd_k, (not backlight))
    

def write8(value, char_mode=False, scrollDelay=0):
    # One millisecond delay to prevent writing too quickly.
    _delay_microseconds(scrollDelay)
    # Set character / data bit.
    io.output(lcd_rs, char_mode)
    # Write upper 4 bits.
    io.output_pins({ lcd_d4: ((value >> 4) & 1) > 0,
                                lcd_d5: ((value >> 5) & 1) > 0,
                                lcd_d6: ((value >> 6) & 1) > 0,
                                lcd_d7: ((value >> 7) & 1) > 0 })
    _pulse_enable()
    # Write lower 4 bits.
    io.output_pins({ lcd_d4: (value        & 1) > 0,
                                lcd_d5: ((value >> 1) & 1) > 0,
                                lcd_d6: ((value >> 2) & 1) > 0,
                                lcd_d7: ((value >> 3) & 1) > 0 })
    _pulse_enable()

def create_char(location, pattern):
    # only position 0..7 are allowed
    location &= 0x7
    write8(LCD_SETCGRAMADDR | (location << 3))
    for i in range(8):
        write8(pattern[i], char_mode=True)

def _delay_microseconds(microseconds):
    # Busy wait in loop because delays are generally very short (few microseconds).
    end = time.time() + (microseconds/1000000.0)
    while time.time() < end:
        pass

def set1604(mode=True):
    global lcd_rows
    """
        Enable support for 16x4 mode
    """
    if (mode):
        lcd_rows = 4
    else:
        lcd_rows = 2


def _pulse_enable():
    # Pulse the clock enable line off, on, off to send command.
    io.output(lcd_en, False)
    _delay_microseconds(1)       # 1 microsecond pause - enable pulse must be > 450ns
    io.output(lcd_en, True)
    _delay_microseconds(1)       # 1 microsecond pause - enable pulse must be > 450ns
    io.output(lcd_en, False)
    _delay_microseconds(1)       # commands need > 37us to settle

# Initialize the display.
write8(0x33)
write8(0x32)

# Write registers.
write8(LCD_DISPLAYCONTROL | displaycontrol)
write8(LCD_FUNCTIONSET | displayfunction)
write8(LCD_ENTRYMODESET | displaymode)  # set the entry mode
clear()