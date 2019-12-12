import gpio as g, time

sleep_int = 10
sleep_mini = 100

rightLowerDown = 130    #180 degree
rightLowerUp = 75       #90 degree
rightUpperDown = 1      #0 degree
rightUpperUp = 55       #60 degree

leftLowerDown = 1       #0 degree
leftLowerUp = 75        #90 degree
leftUpperDown = 130     #180 degree
leftUpperUp = 95        #130 degree

# the supported pins are 0(D3), 2(D4), 4(D2), 5(D1), 12(D6), 13(D7), 14(D5) & 15(D8)

mappedPin = {
    'frontRightLower' : 4,
    'frontRightUpper' : 5,
    'rearRightLower' : 0,
    'rearRightUpper' : 2,
    'frontLeftLower' : 12,
    'frontLeftUpper' : 13,
    'rearLeftLower' : 14,
    'rearLeftUpper' : 15,
}

def lowerLimbTest(count=10):
    for i in range(0, count):
        g.runServo(mappedPin['frontRightLower'], rightLowerDown, True)
        g.runServo(mappedPin['rearRightLower'], rightLowerDown, True)
        g.runServo(mappedPin['frontLeftLower'], leftLowerDown, True)
        g.runServo(mappedPin['rearLeftLower'], leftLowerDown, True)

        time.sleep_ms(1000)
        
        g.runServo(mappedPin['frontRightLower'], rightLowerUp, True)
        g.runServo(mappedPin['rearRightLower'], rightLowerUp, True)
        g.runServo(mappedPin['frontLeftLower'], leftLowerUp, True)
        g.runServo(mappedPin['rearLeftLower'], leftLowerUp, True)

        time.sleep_ms(1000)

    g.runServo(mappedPin['frontRightLower'], rightLowerDown, True)
    g.runServo(mappedPin['rearRightLower'], rightLowerDown, True)
    g.runServo(mappedPin['frontLeftLower'], leftLowerDown, True)
    g.runServo(mappedPin['rearLeftLower'], leftLowerDown, True)

def upperLimbTest(count=10):    
    for i in range(0, count):
        g.runServo(mappedPin['frontRightUpper'], rightUpperDown, True)
        g.runServo(mappedPin['rearRightUpper'], rightUpperDown, True)
        g.runServo(mappedPin['frontLeftUpper'], leftUpperDown, True)
        g.runServo(mappedPin['rearLeftUpper'], leftUpperDown, True)
        time.sleep_ms(1000)

        g.runServo(mappedPin['frontRightUpper'], rightUpperUp, True)
        g.runServo(mappedPin['rearRightUpper'], rightUpperUp, True)
        g.runServo(mappedPin['frontLeftUpper'], leftUpperUp, True)
        g.runServo(mappedPin['rearLeftUpper'], leftUpperUp, True)
        time.sleep_ms(1000)
    
    g.runServo(mappedPin['frontRightUpper'], rightUpperDown, True)
    g.runServo(mappedPin['rearRightUpper'], rightUpperDown, True)
    g.runServo(mappedPin['frontLeftUpper'], leftUpperDown, True)
    g.runServo(mappedPin['rearLeftUpper'], leftUpperDown, True)

def limbTest(count=10):    
    for i in range(0, count):
        g.runServo(mappedPin['frontRightUpper'], rightUpperDown, True)
        g.runServo(mappedPin['rearRightUpper'], rightUpperDown, True)
        g.runServo(mappedPin['frontLeftUpper'], leftUpperDown, True)
        g.runServo(mappedPin['rearLeftUpper'], leftUpperDown, True)
        g.runServo(mappedPin['frontRightLower'], rightLowerDown, True)
        g.runServo(mappedPin['rearRightLower'], rightLowerDown, True)
        g.runServo(mappedPin['frontLeftLower'], leftLowerDown, True)
        g.runServo(mappedPin['rearLeftLower'], leftLowerDown, True)
        time.sleep_ms(1000)

        g.runServo(mappedPin['frontRightUpper'], rightUpperUp, True)
        g.runServo(mappedPin['rearRightUpper'], rightUpperUp, True)
        g.runServo(mappedPin['frontLeftUpper'], leftUpperUp, True)
        g.runServo(mappedPin['rearLeftUpper'], leftUpperUp, True)
        g.runServo(mappedPin['frontRightLower'], rightLowerUp, True)
        g.runServo(mappedPin['rearRightLower'], rightLowerUp, True)
        g.runServo(mappedPin['frontLeftLower'], leftLowerUp, True)
        g.runServo(mappedPin['rearLeftLower'], leftLowerUp, True)
        time.sleep_ms(1000)
    
    g.runServo(mappedPin['frontRightUpper'], rightUpperDown, True)
    g.runServo(mappedPin['rearRightUpper'], rightUpperDown, True)
    g.runServo(mappedPin['frontLeftUpper'], leftUpperDown, True)
    g.runServo(mappedPin['rearLeftUpper'], leftUpperDown, True)
    g.runServo(mappedPin['frontRightLower'], rightLowerDown, True)
    g.runServo(mappedPin['rearRightLower'], rightLowerDown, True)
    g.runServo(mappedPin['frontLeftLower'], leftLowerDown, True)
    g.runServo(mappedPin['rearLeftLower'], leftLowerDown, True)
	
def dogStance(count=10):
    g.runServo(mappedPin['frontRightUpper'], rightUpperDown, True)
    g.runServo(mappedPin['rearRightUpper'], rightUpperDown, True)
    g.runServo(mappedPin['frontLeftUpper'], leftUpperDown, True)
    g.runServo(mappedPin['rearLeftUpper'], leftUpperDown, True)
        
    for i in range(0, count):
        g.runServo(mappedPin['frontRightLower'], rightLowerDown, True)
        g.runServo(mappedPin['rearRightLower'], rightLowerDown, True)
        g.runServo(mappedPin['frontLeftLower'], leftLowerDown, True)
        g.runServo(mappedPin['rearLeftLower'], leftLowerDown, True)
        time.sleep_ms(1000)
        g.runServo(mappedPin['frontRightLower'], rightLowerUp, True)
        g.runServo(mappedPin['rearRightLower'], rightLowerUp, True)
        g.runServo(mappedPin['frontLeftLower'], leftLowerUp, True)
        g.runServo(mappedPin['rearLeftLower'], leftLowerUp, True)
        time.sleep_ms(1000)
