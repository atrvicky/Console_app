import utime
from machine import Pin as pin

def resetBtnFlash():
    btn_flash = pin(0, pin.OUT)
    btn_flash.off()

def main():
    resetBtnFlash()
    # do something in the main loop
    while True:
        print("banana")
        utime.sleep(1)