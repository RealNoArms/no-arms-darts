"""
No Arms Many Mediums Common Utilities Module

    Copyright (C) 2013, 2014, 2015  Tim Kracht <timkracht4@gmail.com>

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

import datetime


def wrap_increment(n, m):
    return (n + 1) % m


class LoggerException(Exception):
    pass


class InvalidLogLevelException(LoggerException):
    pass


class LoggerStoppedException(LoggerException):
    pass


class Logger():
    def __init__(self, log_level="Warn", file_name=None):
        self.levels = {"Debug": 10, "Info": 20, "Warn": 30, "Error": 40, "Fatal": 50}
        self.logLevel = self.set_log_level(log_level)
        self.fileName = file_name
        self.logFile = None
        self.running = False

    def start(self):
        self.running = True
        if self.fileName is not None:
            try:
                self.logFile = open(self.fileName, 'a')
                msg = datetime.datetime.today().strftime("%c") + " <-------------- File Open -------------->"
                self.write_to_logfile(msg)
                # TODO: file rollover, archive, supthin?
            except Exception, e:
                raise LoggerException("Error opening log file:" + e.message)

    def stop(self):
        if self.running:
            self.running = False
            if self.logFile is not None:
                msg = datetime.datetime.today().strftime("%c") + " <------------- File Closed ------------->"
                self.write_to_logfile(msg)
                self.logFile.flush()
                self.logFile.close()
                self.logFile = None

    def set_log_level(self, log_level):
        if log_level in self.levels:
            return self.levels[log_level]
        else:
            raise InvalidLogLevelException("Invalid log level: " + log_level)

    def log(self, level, message, exception=None):
        if self.running:
            if level in self.levels and self.levels[level] >= self.logLevel:
                msg = datetime.datetime.today().strftime("%c") + " : " + level + " : " + message
                print msg
                self.write_to_logfile(msg)
                if exception is not None:
                    print exception
                    self.logFile.write(exception)
        else:
            raise LoggerStoppedException("Logger must be started first!")

    def write_to_logfile(self, message):
        if message is not None and self.logFile is not None:
            self.logFile.write(message + "\n")
