import gpio as g, time

sleep_int = 10
sleep_mini = 100

# rightLowerDown = 130    #180 degree
# rightLowerUp = 75       #90 degree
# rightUpperDown = 1      #0 degree
# rightUpperUp = 55       #60 degree

# leftLowerDown = 1       #0 degree
# leftLowerUp = 75        #90 degree
# leftUpperDown = 130     #180 degree
# leftUpperUp = 95        #130 degree

rightLowerDown = 180
rightLowerUp = 90
rightUpperDown = 0
rightUpperUp = 60

leftLowerDown = 0
leftLowerUp = 90
leftUpperDown = 180
leftUpperUp = 130

# the supported pins are 0(D3), 2(D4), 4(D2), 5(D1), 12(D6), 13(D7), 14(D5) & 15(D8)

mappedUpperAngle = {
    'frontRightLower' : rightLowerUp,
    'frontRightUpper' : rightUpperUp,
    'rearRightLower' : rightLowerUp,
    'rearRightUpper' : rightUpperUp,
    'frontLeftLower' : leftLowerUp,
    'frontLeftUpper' : leftUpperUp,
    'rearLeftLower' : leftLowerUp,
    'rearLeftUpper' : leftUpperUp,
    'frl' : rightLowerUp,
    'fru' : rightUpperUp,
    'rrl' : rightLowerUp,
    'rru' : rightUpperUp,
    'fll' : leftLowerUp,
    'flu' : leftUpperUp,
    'rll' : leftLowerUp,
    'rlu' : leftUpperUp
}

mappedLowerAngle = {
    'frontRightLower' : rightLowerDown,
    'frontRightUpper' : rightUpperDown,
    'rearRightLower' : rightLowerDown,
    'rearRightUpper' : rightUpperDown,
    'frontLeftLower' : leftLowerDown,
    'frontLeftUpper' : leftUpperDown,
    'rearLeftLower' : leftLowerDown,
    'rearLeftUpper' : leftUpperDown,
    'frl' : rightLowerDown,
    'fru' : rightUpperDown,
    'rrl' : rightLowerDown,
    'rru' : rightUpperDown,
    'fll' : leftLowerDown,
    'flu' : leftUpperDown,
    'rll' : leftLowerDown,
    'rlu' : leftUpperDown
}

mappedPin = {
    'frontRightLower' : 4,
    'frontRightUpper' : 5,
    'rearRightLower' : 0,
    'rearRightUpper' : 2,
    'frontLeftLower' : 12,
    'frontLeftUpper' : 13,
    'rearLeftLower' : 14,
    'rearLeftUpper' : 15,
    'frl' : 4,
    'fru' : 5,
    'rrl' : 0,
    'rru' : 2,
    'fll' : 12,
    'flu' : 13,
    'rll' : 14,
    'rlu' : 15
}

def lowerLimbTest(count=10):
    for i in range(0, count):
        g.runServoAngle(mappedPin['frontRightLower'], mappedLowerAngle['frontRightLower'], True)
        g.runServoAngle(mappedPin['rearRightLower'], mappedLowerAngle['rearRightLower'], True)
        g.runServoAngle(mappedPin['frontLeftLower'], mappedLowerAngle['frontLeftLower'], True)
        g.runServoAngle(mappedPin['rearLeftLower'], mappedLowerAngle['rearLeftLower'], True)

        time.sleep_ms(1000)
        
        g.runServoAngle(mappedPin['frontRightLower'], mappedUpperAngle['frontRightLower'], True)
        g.runServoAngle(mappedPin['rearRightLower'], mappedUpperAngle['rearRightLower'], True)
        g.runServoAngle(mappedPin['frontLeftLower'], mappedUpperAngle['frontLeftLower'], True)
        g.runServoAngle(mappedPin['rearLeftLower'], mappedUpperAngle['rearLeftLower'], True)

        time.sleep_ms(1000)

    g.runServoAngle(mappedPin['frontRightLower'], mappedLowerAngle['frontRightLower'], True)
    g.runServoAngle(mappedPin['rearRightLower'], mappedLowerAngle['rearRightLower'], True)
    g.runServoAngle(mappedPin['frontLeftLower'], mappedLowerAngle['frontLeftLower'], True)
    g.runServoAngle(mappedPin['rearLeftLower'], mappedLowerAngle['rearLeftLower'], True)

def upperLimbTest(count=10):    
    for i in range(0, count):
        g.runServoAngle(mappedPin['frontRightUpper'], mappedUpperAngle['frontRightUpper'], True)
        g.runServoAngle(mappedPin['rearRightUpper'], mappedUpperAngle['rearRightUpper'], True)
        g.runServoAngle(mappedPin['frontLeftUpper'], mappedUpperAngle['frontLeftUpper'], True)
        g.runServoAngle(mappedPin['rearLeftUpper'], mappedUpperAngle['rearLeftUpper'], True)

        time.sleep_ms(1000)

        g.runServoAngle(mappedPin['frontRightUpper'], mappedLowerAngle['frontRightUpper'], True)
        g.runServoAngle(mappedPin['rearRightUpper'], mappedLowerAngle['rearRightUpper'], True)
        g.runServoAngle(mappedPin['frontLeftUpper'], mappedLowerAngle['frontLeftUpper'], True)
        g.runServoAngle(mappedPin['rearLeftUpper'], mappedLowerAngle['rearLeftUpper'], True)
       
        time.sleep_ms(1000)
    
    g.runServoAngle(mappedPin['frontRightUpper'], mappedUpperAngle['frontRightUpper'], True)
    g.runServoAngle(mappedPin['rearRightUpper'], mappedUpperAngle['rearRightUpper'], True)
    g.runServoAngle(mappedPin['frontLeftUpper'], mappedUpperAngle['frontLeftUpper'], True)
    g.runServoAngle(mappedPin['rearLeftUpper'], mappedUpperAngle['rearLeftUpper'], True)

def limbTest(legs, count):
    for leg in legs:
        for i in range(0, count):
            g.runServoAngle(mappedPin[leg], mappedLowerAngle[leg], True)
            time.sleep(1)
            g.runServoAngle(mappedPin[leg], mappedUpperAngle[leg], True)
            time.sleep(1)
	
def dogStance(count=10):
    g.runServoAngle(mappedPin['frontRightUpper'], mappedUpperAngle['frontRightUpper'], True)
    g.runServoAngle(mappedPin['rearRightUpper'], mappedUpperAngle['rearRightUpper'], True)
    g.runServoAngle(mappedPin['frontLeftUpper'], mappedUpperAngle['frontLeftUpper'], True)
    g.runServoAngle(mappedPin['rearLeftUpper'], mappedUpperAngle['rearLeftUpper'], True)
        
    for i in range(0, count):
        g.runServoAngle(mappedPin['frontRightLower'], mappedLowerAngle['frontRightLower'], True)
        g.runServoAngle(mappedPin['rearRightLower'], mappedLowerAngle['rearRightLower'], True)
        g.runServoAngle(mappedPin['frontLeftLower'], mappedLowerAngle['frontLeftLower'], True)
        g.runServoAngle(mappedPin['rearLeftLower'], mappedLowerAngle['rearLeftLower'], True)

        time.sleep_ms(1000)
        
        g.runServoAngle(mappedPin['frontRightLower'], mappedUpperAngle['frontRightLower'], True)
        g.runServoAngle(mappedPin['rearRightLower'], mappedUpperAngle['rearRightLower'], True)
        g.runServoAngle(mappedPin['frontLeftLower'], mappedUpperAngle['frontLeftLower'], True)
        g.runServoAngle(mappedPin['rearLeftLower'], mappedUpperAngle['rearLeftLower'], True)

        time.sleep_ms(1000)

def resetServos():
    g.runServoAngle(mappedPin['frontRightLower'], mappedLowerAngle['frontRightLower'], True)
    g.runServoAngle(mappedPin['rearRightLower'], mappedLowerAngle['rearRightLower'], True)
    g.runServoAngle(mappedPin['frontLeftLower'], mappedLowerAngle['frontLeftLower'], True)
    g.runServoAngle(mappedPin['rearLeftLower'], mappedLowerAngle['rearLeftLower'], True)
    g.runServoAngle(mappedPin['frontRightUpper'], mappedLowerAngle['frontRightUpper'], True)
    g.runServoAngle(mappedPin['rearRightUpper'], mappedLowerAngle['rearRightUpper'], True)
    g.runServoAngle(mappedPin['frontLeftUpper'], mappedLowerAngle['frontLeftUpper'], True)
    g.runServoAngle(mappedPin['rearLeftUpper'], mappedLowerAngle['rearLeftUpper'], True)

def dogStand():
    g.runServoAngle(mappedPin['fru'], 35, True)
    g.runServoAngle(mappedPin['rru'], 35, True)
    g.runServoAngle(mappedPin['flu'], 165, True)
    g.runServoAngle(mappedPin['rlu'], 165, True)

    g.runServoAngle(mappedPin['frl'], 130, True)
    g.runServoAngle(mappedPin['rrl'], 110, True)
    g.runServoAngle(mappedPin['fll'], 65, True)
    g.runServoAngle(mappedPin['rll'], 65, True)
