"""

Logger

    Copyright (C) 2014-2015  Tim Kracht <timkracht4@gmail.com>

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

    Built on code from (Auto-)Didactic Programming:
        http://nebelprog.wordpress.com/

    And the pygame wiki:
        http://www.pygame.org/wiki/textwrapping
"""

import datetime
from error import Error


class Logger(object):
    def __init__(self, log_level="Warn", file_name=None):
        self._levels = {"Debug": 10, "Info": 20, "Warn": 30, "Error": 40, "Fatal": 50}
        self._logLevel = None
        self._logLevelName = None
        self.log_level = log_level
        self._fileName = file_name
        self._logFile = None
        self._running = False

    # Properties
    @property
    def log_level(self):
        return self._logLevelName

    @log_level.setter
    def log_level(self, log_level):
        if log_level in self._levels:
            self._logLevelName = log_level
            self._logLevel = self._levels[log_level]
        else:
            raise InvalidLogLevelError("Invalid log level: " + log_level)

    # Methods
    def start(self):
        self._running = True
        if self._fileName is not None:
            try:
                self._logFile = open(self._fileName, 'a')
                msg = datetime.datetime.today().strftime("%c") + " <-------------- File Open -------------->"
                self._write_to_logfile(msg)
                # TODO: file rollover, archive, supthin?
            except Exception, e:
                raise LoggerError("Error opening log file:" + e.message)

    def stop(self):
        if self._running:
            self._running = False
            if self._logFile is not None:
                msg = datetime.datetime.today().strftime("%c") + " <------------- File Closed ------------->"
                self._write_to_logfile(msg)
                self._logFile.flush()
                self._logFile.close()
                self._logFile = None

    def log(self, level, message, exception=None):
        if self._running:
            if level in self._levels and self._levels[level] >= self._logLevel:
                msg = datetime.datetime.today().strftime("%c") + " : " + level + " : " + str(message)
                print msg
                self._write_to_logfile(msg)
                if exception is not None:
                    print exception
                    self._logFile.write(exception)
        else:
            raise LoggerStoppedError("Logger must be started first!")

    def _write_to_logfile(self, message):
        if message is not None and self._logFile is not None:
            self._logFile.write(message + "\n")


# Errors
class LoggerError(Error):

    def __init__(self, msg=None, obj=None):
        super(LoggerError, self).__init__(msg, obj)
        self._rep = "Logger Error"


class InvalidLogLevelError(LoggerError):

    def __init__(self, msg=None, obj=None):
        super(InvalidLogLevelError, self).__init__(msg, obj)
        self._rep = "Invalid Log Level Error"


class LoggerStoppedError(LoggerError):

    def __init__(self, msg=None, obj=None):
        super(LoggerStoppedError, self).__init__(msg, obj)
        self._rep = "Logger Stopped Error"
