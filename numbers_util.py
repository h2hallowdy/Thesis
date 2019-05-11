#-------------------------------------------------------------------------------
# Name:             Numbers_util
# Purpose:          Change numbers to string to UART
# Author:           NXH
# Created:          Wednesday April 24
# Note:             1-negative; 0-positive
#-------------------------------------------------------------------------------
def UARTMessage(aveX, aveY, aveAng, mode):
    if mode == 'c':
        message = 'c-'
    elif mode == 'r':
        message = 'r-'
    elif mode == 'g':
        message = 'g-'

    #region: X point
    if aveX > 0.0:
        intX, pointX = SplitNumber(aveX, 2)
        message += '0' + '{:02d}'.format(intX) + '{:02d}'.format(pointX) + '-'
    else:
        aveX = -aveX
        intX, pointX = SplitNumber(aveX, 2)
        message += '1' + '{:02d}'.format(intX) + '{:02d}'.format(pointX) + '-'
    #endregion

    #region: Y point
    if aveY > 0.0:
        intY, pointY = SplitNumber(aveY, 2)
        message += '0' + '{:02d}'.format(intY) + '{:02d}'.format(pointY) + '-'
    else:
        aveY = -aveY
        intY, pointY = SplitNumber(aveY, 2)
        message += '1' + '{:02d}'.format(intY) + '{:02d}'.format(pointY) + '-'
    #endregion

    #region: Angle
    if aveAng > 0.0:
        intA, pointA = SplitNumber(aveAng, 1)
        message += '0' + '{:03d}'.format(intA) + '{:01d}'.format(pointA) + '-0'
    else:
        aveAng = -aveAng
        intA, pointA = SplitNumber(aveAng, 1)
        message += '1' + '{:03d}'.format(intA) + '{:01d}'.format(pointA) + '-0'
    #endregion

    return message

def SplitNumber(num, num2round):
    num = round(num, num2round)
    if num2round == 1:
        intPart = int(num)
        pointPart = int(round((num - intPart) * 10, 0))
    elif num2round == 2:
        intPart = int(num)
        pointPart = int(round((num - intPart) * 100, 0))
    return intPart, pointPart




