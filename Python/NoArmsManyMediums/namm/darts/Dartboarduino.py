"""

Classes in the USB Dartboarduino Model


    Copyright (C) 2013-2015  Tim Kracht <timkracht4@gmail.com>

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

import os
import pygame
import serial
import sys
import time

from struct import unpack
from namm.common import *

# from the Arduino sketch:
# define IFACE_ACK           'A'
# define IFACE_HIT           'H'
# define IFACE_CONNECT       'C'
# define IFACE_DISCONNECT    'D'
# define IFACE_PLAY          'P'
# define IFACE_STOP          'X'
# define IFACE_QUERY_STATE   'Q'

# States/commands (dartboard interface command, command text, state text)

STCMD_PLAY = ('P', 'Playing')
STCMD_STOP = ('X', 'Stopped')
STCMD_HIT = ('H', 'Hit')
STCMD_CONNECT = ('C', 'Connected')
STCMD_DISCONNECT = ('D', 'Disconnected')
STCMD_QUERY = ('Q', 'Querying')
STCMD_ACKNOWLEDGE = ('A', 'Acknowledging')


# USB Dartboarduino

class Dartboarduino(object):

    def __init__(self, log_level='Warn', name='Dartboarduino', retry_count=5, timeout=10, baud_rate=9600):

        if not os.path.exists("log"):
            os.mkdir("log")
        self._logger = utilities.Logger(log_level, os.path.join("log", "Dartboarduino.log"))
        self._logger.start()

        self._logger.log("Debug", "Log Level: " + str(log_level))
        self._logger.log("Debug", "Name: " + str(name))
        self._logger.log("Debug", "Timeout: " + str(timeout))
        self._logger.log("Debug", "Retry Count: " + str(retry_count))
        self._logger.log("Debug", "Baud Rate: " + str(baud_rate))

        self._name = name
        self._timeout = timeout
        self._retryCount = retry_count
        self._baudRate = baud_rate

        self._statuses = {STCMD_PLAY[0]: STCMD_PLAY[1],
                          STCMD_STOP[0]: STCMD_STOP[1],
                          STCMD_HIT[0]: STCMD_HIT[1],
                          STCMD_CONNECT[0]: STCMD_CONNECT[1],
                          STCMD_DISCONNECT[0]: STCMD_DISCONNECT[1],
                          STCMD_QUERY[0]: STCMD_QUERY[1],
                          STCMD_ACKNOWLEDGE[0]: STCMD_ACKNOWLEDGE[1]}

        self._state = None
        self._usb = None
        self._currentState = None

        self._port = self._find_serial_port()
        
    def __str__(self):
        return self.name

    def __del__(self):
        try:
            self._logger.log("Info", "__del__ : Disconnecting the board")
            self.disconnect()
        except Exception, e:
            self._logger.log("Error", str(e))
        finally:
            self._logger.log("Info", "__del__ : Closing the port")
            self._usb = None
        try:
            self._logger.stop()
        except Exception, e:
            print str(e)

    @property
    def state(self):
        result = None
        self._refresh_state()
        if self._currentState is not None and self._currentState in self._statuses:
            result = self._statuses[self._currentState]
        elif self._currentState is not None:
            self._logger.log("Warn", "state : Board is in an unknown state?!")
            self._logger.log("Info", "state : Current board state code: " + str(self._currentState))
        return result

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, new_name):
        self._logger.log("Debug", "Changing Name from '" + str(self._name) + "' to '" + str(new_name) + "'")
        self._name = new_name

    @property
    def timeout(self):
        return self._timeout

    @timeout.setter
    def timeout(self, new_timeout):
        self._logger.log("Debug", "Changing Timeout from '" + str(self._timeout) + "' to '" + str(new_timeout) + "'")
        self._timeout = new_timeout
        if self._usb is not None:
            self._usb.timeout = self._timeout

    @property
    def retry_count(self):
        return self._retryCount

    @retry_count.setter
    def retry_count(self, new_retry_count):
        self._logger.log("Debug", "Changing Retry Count from '" + str(self._retryCount) + "' to '" +
                         str(new_retry_count) + "'")
        self._retryCount = new_retry_count

    @property
    def baud_rate(self):
        return self._baudRate

    @baud_rate.setter
    def baud_rate(self, new_baud_rate):
        self._logger.log("Debug", "Changing Baud Rate from '" + str(self._baudRate) + "' to '" +
                         str(new_baud_rate) + "'")
        self._baudRate = new_baud_rate
        if self._usb is not None:
            self._usb.baudrate = self._baudRate

    @property
    def port(self):
        return self._port

    def flush(self):
        self._logger.log("Debug", "Entering flush() procedure")
        if self._usb is not None:
            self._usb.flushInput()
        else:
            self._logger.log("Debug", "Not connected to serial port, nothing to flush")

    def get_hit(self):
        self._logger.log("Debug", "Entering get_hit() procedure")
        result = None
        if self._usb is not None and self._currentState == STCMD_PLAY[0]:
            if self._usb.inWaiting() > 0 and self._usb.read() == STCMD_HIT[0]:
                w = self._get_serial_response()
                m = self._get_serial_response()

                if w and m:
                    try:
                        wedge = unpack('b' * len(w), w)[0]
                        multiplier = unpack('b' * len(m), m)[0]
                        result = (multiplier, wedge)
                    except Exception:
                        self._logger.log("Error", "get_hit : Could not unpack the response.  Probably missed a hit.")
                        self._logger.log("Info", "get_hit : w: " + str(w))
                        self._logger.log("Info", "get_hit : m: " + str(m))
                else:
                    self._logger.log("Error", "get_hit : Wedge and/or Multiplier not received.  Probably missed a hit.")
                    self._logger.log("Info", "get_hit : w: " + str(w))
                    self._logger.log("Info", "get_hit : m: " + str(m))
            else:
                self._logger.log("Debug", "No '" + STCMD_HIT[0] + "' messages received")
        else:
            self._logger.log("Warn", "get_hit : Board state is not '" + STCMD_PLAY[1] + "', so port was not read.")
            # self._logger.log("Info", "get_hit : Current board state: " + str(self.state))
        self._logger.log("Debug", "get_hit() returning: " + str(result))
        return result

    def connect(self):
        self._logger.log("Debug", "Entering connect() procedure")
        response = None
        if self._currentState in (None, STCMD_DISCONNECT[0]):
            if self._usb is None:
                try:
                    self._usb = serial.Serial(self._port, self._baudRate)
                except Exception, e:
                    self._logger.log("Error", str(e))
                    self._usb = None
                else:
                    self._usb.timeout = self._timeout
            self._logger.log("Debug", "Sending Connect state change to board")
            response = self._get_serial_response(STCMD_CONNECT[0])
            self._refresh_state()
        else:
            self._logger.log("Warn", "connect : Board state is not '" + STCMD_DISCONNECT[1] +
                             "', so Connect request not sent")
            self._logger.log("Info", "connect : Current board state: " + str(self.state))
        self._logger.log("Debug", "connect() returning: " + str(response))
        return response

    def reconnect(self):
        self._logger.log("Debug", "Entering reconnect() procedure")
        try:
            if self._usb is not None:
                self._logger.log("Debug", "Closing serial port")
                self._usb.close()
        except Exception, e:
            self._logger.log("Error", str(e))
        self._usb = None
        self._port = self._find_serial_port()
        response = self._port is not None

        self._logger.log("Debug", "reconnect() returning: " + str(response))
        return response
        
    def disconnect(self):
        self._logger.log("Debug", "Entering disconnect() procedure")
        response = None
        self.stop()
        if self._currentState == (STCMD_STOP[0]):
            self._logger.log("Debug", "Sending Disconnect state change to board")
            response = self._get_serial_response(STCMD_DISCONNECT[0])
            self._refresh_state()
        else:
            self._logger.log("Warn", "disconnect : Board state is not '" + STCMD_STOP[1] +
                             "', so Disconnect request not sent")
            self._logger.log("Info", "disconnect : Current board state: " + str(self.state))
        self._logger.log("Debug", "disconnect() returning: " + str(response))
        return response

    def stop(self):
        self._logger.log("Debug", "Entering stop() procedure")
        response = None
        if self._currentState == (STCMD_PLAY[0]):
            self._logger.log("Debug", "Sending Stop state change to board")
            response = self._get_serial_response(STCMD_STOP[0])
            self._refresh_state()
        else:
            self._logger.log("Warn", "stop : Board state is not '" + STCMD_PLAY[1] + "', so Stop request not sent")
            self._logger.log("Info", "stop : Current board state: " + str(self.state))
        self._logger.log("Debug", "stop() returning: " + str(response))
        return response

    def play(self):
        self._logger.log("Debug", "Entering play() procedure")
        response = None
        if self._currentState == (STCMD_STOP[0]):
            self._logger.log("Debug", "Sending Play state change to board")
            response = self._get_serial_response(STCMD_PLAY[0])
            self._refresh_state()
        else:
            self._logger.log("Warn", "play : Board state is not '" + STCMD_STOP[1] + "', so Play request not sent")
            self._logger.log("Info", "play : Current board state: " + str(self.state))
        self._logger.log("Debug", "play() returning: " + str(response))
        return response

    def _find_serial_port(self):
        self._logger.log("Debug", "Entering _find_serial_port() procedure")
        result = None
        if self._usb is not None:
            self._logger.log("Debug", "Already have a port open, so return that one")
            result = self._usb.port
        else:
            ports = {
                'linux2': (
                    '/dev/ttyUSB0', '/dev/ttyUSB1', '/dev/ttyUSB2', '/dev/ttyUSB3', '/dev/ttyUSB4', '/dev/ttyUSB5',
                    '/dev/ttyUSB6', '/dev/ttyUSB7', '/dev/ttyUSB8', '/dev/ttyUSB9', '/dev/ttyUSB10', '/dev/ttyS0',
                    '/dev/ttyS1', '/dev/ttyS2', '/dev/ttyS3', '/dev/ttyS4', '/dev/ttyS5', '/dev/ttyS6', '/dev/ttyS7',
                    '/dev/ttyS8', '/dev/ttyS9', '/dev/ttyS10', '/dev/ttyACM0', '/dev/ttyACM1', '/dev/ttyACM2',
                    '/dev/ttyACM3', '/dev/ttyACM4', '/dev/ttyACM5', '/dev/ttyACM6', '/dev/ttyACM7', '/dev/ttyACM8',
                    '/dev/ttyACM9', '/dev/ttyACM10'),
                'win32': (
                    'COM1', 'COM2', 'COM3', 'COM4', 'COM5', 'COM6', 'COM7', 'COM8', 'COM9')
            }

            platform = sys.platform
            self._logger.log("Debug", "Platform identified: " + platform)
            if platform in ports:
                for port in ports[platform]:
                    try:
                        self._logger.log("Debug", "Attempting to open port: " + port)
                        self._usb = serial.Serial(port, self._baudRate)
                        self._logger.log("Debug", str(self._usb.getSettingsDict()))
                    except Exception, e:
                        self._logger.log("Info",str(e))
                        self._logger.log("Debug", "Failed to open " + port)
                    else:
                        self._logger.log("Debug", "Opened " + port)
                        self._usb.timeout = self._timeout
                        self._logger.log("Debug", "Asking the port if it is a Dartboarduino")
                        serialRead = self._get_serial_response(STCMD_QUERY[0])
                        if serialRead in self._statuses:
                            self._logger.log("Info", "_find_serial_port : Dartboarduino discovered on " + port)
                            result = port
                        else:
                            self._logger.log("Debug", "Apparently it's not a Dartboarduino, closing the port")
                            self._usb.close()
                            self._usb = None
                    if result is not None:
                        break
        self._logger.log("Debug", "_find_serial_port() returning: " + str(result))
        return result

    def _refresh_state(self):
        self._logger.log("Debug", "Entering _refresh_state() procedure")
        state = "None"
        self._logger.log("Debug", "Querying the board's state")
        self._currentState = self._get_serial_response(STCMD_QUERY[0])
        if self._currentState is not None:
            state = self._statuses[self._currentState]
        self._logger.log("Info", "_refresh_state : Current board state: " + state)

    def _get_serial_response(self, command=None):
        self._logger.log("Debug", "Entering _get_serial_response() procedure")
        response = None
        if self._usb is not None:
            requests = 0
            response = None
            while response is None and requests < self._retryCount:
                requests += 1
                try:
                    self._logger.log("Debug", "Attempt #" + str(requests))
                    if command is not None:
                        try:
                            self._logger.log("Debug", "Flushing port and sending command")
                            self._usb.flushInput()
                            self._usb.write(command)
                        except Exception, e:
                            self._logger.log("Error",str(e))
                            self._logger.log("Debug", "Failed to flush and write to port on attempt #" + str(requests))
                            raise
                    self._logger.log("Debug", "Reading port")
                    response = self._usb.read()
                    if len(response) == 0:
                        self._logger.log("Debug", "Received data with a length of 0 on attempt #" + str(requests))
                        response = None
                except Exception, e:
                    self._logger.log("Error",str(e))
                    self._logger.log("Debug", "Failed to get a response from the port")
        else:
            self._logger.log("Warn", "_get_serial_response : Port not open, so no request was sent")
        self._logger.log("Debug", "_get_serial_response() returning: " + str(response))
        return response


def test(log_level):
    try:
        board = Dartboarduino(log_level)

        if board.state is None:
            print("Did not detect a Dartboarduino, returning to main menu.")
        else:
            print("Detected a Dartboarduino named '" + str(board.name) + "'!")

            command_menu = ["Get Board Status", "Connect to Board", "Disconnect from Board", "Play Game",
                            "Stop Game", "Get Hit"]
            choice = "0"
            i = -1
            while choice != str(i):
                i = 0
                print("\n============[ Commands ]=============")
                while i < len(command_menu):
                    print("[" + str(i) + "] " + command_menu[i])
                    i += 1
                print("[" + str(i) + "] Exit")
                # print(str(board.name) + " state: " + str(board.state))
                print

                choice = raw_input("Enter Menu Option ==>  ")
                if choice == "0":
                    print("Result of Command:\n" + str(board.state))
                elif choice == "1":
                    print("Result of Command:\n" + str(board.connect()))
                elif choice == "2":
                    print("Result of Command:\n" + str(board.disconnect()))
                elif choice == "3":
                    print("Result of Command:\n" + str(board.play()))
                elif choice == "4":
                    print("Result of Command:\n" + str(board.stop()))
                elif choice == "5":
                    print("Result of Command:\n" + str(board.get_hit()))
                elif choice != str(i):
                    print("Why don't you try picking one of the options next time, jackass?")

    except Exception, e:
        print e

if __name__ == "__main__":
    print("This module contains classes to interface with a USB Dartboarduino.")

    main_menu = ["Debug", "Info", "Warn", "Error", "Fatal"]
    choice = "0"
    i = -1
    while choice != str(i):
        i = 0
        print("\n=================[ Main ]=================")
        while i < len(main_menu):
            print("[" + str(i) + "] Test with " + main_menu[i] + " logging")
            i += 1
        print("[" + str(i) + "] Exit")
        print

        choice = raw_input("Enter Menu Option ==>  ")
        if "0" <= choice <= str(len(main_menu)-1):
            print("Detecting Dartboarduinos, might take a minute...")
            test(main_menu[int(choice)])
        elif choice != str(i):
            print("Why don't you try picking one of the options next time, jackass?")
