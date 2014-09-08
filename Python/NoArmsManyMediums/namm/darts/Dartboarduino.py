"""

Classes in the USB Dartboarduino Model


    Copyright (C) 2013-2014  Tim Kracht <timkracht4@gmail.com>

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import pygame
import serial
import sys
from struct import unpack

# from the Arduino sketch:
#define IFACE_ACK           'A'
#define IFACE_HIT           'H'
#define IFACE_CONNECT       'C'
#define IFACE_DISCONNECT    'D'
#define IFACE_PLAY          'P'
#define IFACE_STOP          'X'
#define IFACE_QUERY_STATE   'Q'

# States/commands (dartboard interface command, command text, state text)

STCMD_PLAY = ('P','Playing')
STCMD_STOP = ('X','Stopped')
STCMD_HIT = ('H','Hit')
STCMD_CONNECT = ('C','Connected')
STCMD_DISCONNECT = ('P','Disconnected')
STCMD_QUERY = ('Q','Querying')
STCMD_ACKNOWLEDGE = ('A','Acknowledging')



# USB Dartboarduino

class Dartboarduino(object):

    def __init__(self, Name='Dartboarduino', RetryCount=5, Timeout=10, BaudRate=9600):
        self._name = Name
        self._state = None
        self._usb = None
        self._currentState = None
        self._timeout = Timeout
        self._retryCount = RetryCount
        self._baudRate = BaudRate
        self._port = self._findSerialPort()

        self._statuses = {}
        self._statuses[STCMD_PLAY[0]] = STCMD_PLAY[1]
        self._statuses[STCMD_STOP[0]] = STCMD_STOP[1]
        self._statuses[STCMD_HIT[0]] = STCMD_HIT[1]
        self._statuses[STCMD_CONNECT[0]] = STCMD_CONNECT[1]
        self._statuses[STCMD_DISCONNECT[0]] = STCMD_DISCONNECT[1]
        self._statuses[STCMD_QUERY[0]] = STCMD_QUERY[1]
        self._statuses[STCMD_ACKNOWLEDGE[0]] = STCMD_ACKNOWLEDGE[1]
        
    def __str__(self):
        return self.name

    def __del__(self):
        if self._usb:
            try:
                self._usb.close()
            except:
                pass

    @property
    def state(self):
        result = None
        self._refreshState()
        if self._currentState and self._currentState in self._statuses:
            result = self._statuses[self._currentState]
        return result

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, newName):
        self._name = newName

    @property
    def timeout(self):
        return self._timeout

    @timeout.setter
    def timeout(self, newTimeout):
        self._timeout = newTimeout

    @property
    def retryCount(self):
        return self._retryCount

    @retryCount.setter
    def retryCount(self, newRetryCount):
        self._retryCount = newRetryCount

    @property
    def baudRate(self):
        return self._baudRate

    @baudRate.setter
    def baudRate(self, newBaudRate):
        self._baudRate = newBaudRate

    def flush(self):
        if self._usb != None:
            self._usb.flushInput()

    def getHit(self):
        result = None
        if self._usb and self._currentState == STCMD_PLAY[0]:
            if self._usb.inWaiting() > 0 and ser.read() == 'H':
                w = self._getSerialResponse()
                m = self._getSerialResponse()

                if w and m:
                    try:
                        wedge = unpack('b' * len(w), w)[0]
                        multiplier = unpack('b' * len(m), m)[0]
                        result = (multiplier, wedge)
                    except:
                        pass
        return result

    def connect(self):
        if self.state in (None, STCMD_DISCONNECT[1]):
            if not self._usb:
                try:
                    self._usb = serial.Serial(self._port, self._baudRate)
                except:
                    self._usb = None
                    pass
                else:
                    self._usb.timeout = self._timeout
            return self._getSerialResponse(STCMD_CONNECT[0])

    def reconnect(self):
        try:
            if self._usb:
                self._usb.close()
        except:
            pass
        self._usb = None
        self._port = _findSerialPort()
        return (self._port != None)
        
    def disconnect(self):
        self.stop()
        if self.state == (STCMD_STOP[1]):
            return self._getSerialResponse(STCMD_DISCONNECT[0])

    def stop(self):
        if self.state == (STCMD_PLAY[1]):
            return self._getSerialResponse(STCMD_STOP[0])

    def play(self):
        if self.state == (STCMD_STOP[1]):
            return self._getSerialResponse(STCMD_PLAY[0])

    def _findSerialPort(self):
        result = None
        if self._usb:
            result = self._usb.port
        else:
            ports={'linux2':
                   ('/dev/ttyUSB0','/dev/ttyUSB1','/dev/ttyUSB2','/dev/ttyUSB3','/dev/ttyUSB4','/dev/ttyUSB5',
                    '/dev/ttyUSB6','/dev/ttyUSB7','/dev/ttyUSB8','/dev/ttyUSB9','/dev/ttyUSB10',
                    '/dev/ttyS0','/dev/ttyS1','/dev/ttyS2','/dev/ttyS3','/dev/ttyS4','/dev/ttyS5',
                    '/dev/ttyS6', '/dev/ttyS7','/dev/ttyS8','/dev/ttyS9','/dev/ttyS10',
                    '/dev/ttyACM0','/dev/ttyACM1','/dev/ttyACM2','/dev/ttyACM3','/dev/ttyACM4','/dev/ttyACM5',
                    '/dev/ttyACM6','/dev/ttyACM7','/dev/ttyACM8','/dev/ttyACM9','/dev/ttyACM10'),
                   'win32':
                   ('COM1','COM2','COM3','COM4','COM5','COM6','COM7','COM8','COM9')}
            platform = sys.platform
            if platform in ports:
                for port in ports[platform]:
                    try:
                        self._usb = serial.Serial(port, self._baudRate)
                    except:
                        pass
                    else:
                        self._usb.timeout = self._timeout
                        self._usb.flushInput()
                        if self._getSerialResponse(STCMD_QUERY[0]) in self._statuses:
                            result = port
                    if result:
                        break
        return result

    def _refreshState(self):
        self._currentState = self._getSerialResponse(STCMD_QUERY[0])

    def _getSerialResponse(self, command=None):
        response = None
        if self._usb:
            requests = 0
            response = None
            while (not response and requests <= self._retryCount):
                requests += 1
                if command:
                    self._usb.flushInput()
                    self._usb.write(command)
                response = self._usb.read()
        return response
    

if __name__ == "__main__":
    print("This module contains classes to interface with a USB Dartboarduino.")
    input("\n\nPress enter to exit...")
