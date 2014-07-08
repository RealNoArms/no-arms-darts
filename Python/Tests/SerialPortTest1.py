'''

Python-Arduino Serial test 1

Free To The People

'''
import time
import serial
from struct import unpack


connected = False
playing = False

wedge = 0
multiplier = 0

requestCount = 0
maxRequests = 5
yorn = ''

ser = serial.Serial("COM3", 9600)
# *nix: ser = serial.Serial('/dev/ttyblah1', 9600)  or whetever
# TODO: look at scan example to try to automagically find the right port?

ser.timeout = 5

print "Hit double bull to exit."

while not connected:
    if requestCount >= maxRequests:
        yorn = raw_input("Failed to connect after {0:d} attempts, try again [y/n]? ".format(requestCount))
        while not yorn in ['y','n']:
            yorn = raw_input("y or n: ")

        if yorn == 'n':
            quit()
        else:
            requestCount = 0
            
    ser.write('C')
    requestCount += 1
    print 'Sent connection request...'  
    connected = (ser.read() == 'C')

print 'Connected to dartboard!'
requestCount = 0

while not playing:
    if requestCount >= maxRequests:
        yorn = raw_input("Failed to get a response to a play request after {0:d} attempts, try again [y/n]? ".format(requestCount))
        while not yorn in ['y','n']:
            yorn = raw_input("y or n: ")

        if yorn == 'n':
            quit()
        else:
            requestCount = 0
    ser.write('P')
    requestCount += 1
    print 'Requesting that the board start a game...'  
    playing = (ser.read() == 'P')

print 'Entered the playing state!' 

while playing:
    while ser.inWaiting() > 0:
        if ser.read() == 'H':
            s1 = ser.read()
            s2 = ser.read()

            wedge = unpack('b' * len(s1), s1)[0]
            multiplier = unpack('b' * len(s2), s2)[0]
            
            hitMessage = []
            hitMessage.append("Hit a ");
            
            if multiplier == 1:
                hitMessage.append("single ")
            elif multiplier == 2:
                hitMessage.append("double ")
            elif multiplier == 3:
                hitMessage.append("triple ")
            else:
                hitMessage.append("unknown ")

            if wedge == 25:
                hitMessage.append("bullseye")
            else:
                hitMessage.append("{0:d}".format(wedge))

            print ''.join(hitMessage)

            if wedge == 25 and multiplier == 2:
                playing = False
                
                print "Stopping game..."
                ser.write('X')
                ser.read()
                
                ser.write('Q')
                while (ser.read() != 'X'):
                    ser.write('Q')

                print "Game stopped!"

                print "Disconnecting dartboard..."
                ser.write('D')
                ser.read()
                
                ser.write('Q')
                while (ser.read() != 'D'):
                    ser.write('Q')

                print "Dartboard disconnected!"
                



