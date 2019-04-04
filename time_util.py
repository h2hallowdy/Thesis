from datetime import datetime
import logging

def GetTime():
    time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return time
def GetTimeForFile():
    time = datetime.now().strftime('%Y%m%d-%Hh%Mm')
    return time


