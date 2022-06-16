# Copyright 2020 Evan Flynn
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
"""
Functions to configure the GRBL device.

The grbl device configure functions
"""
import time


class configure(object):
    """Configure class to hold all configure functions for the grbl device."""

    def setSpeed(self, speed):
        """Set the default machine speed."""
        self.defaultSpeed = speed

    def setOrigin(self, x=0, y=0, z=0):
        """Set the machine origin."""
        # set current position to be (0,0,0), or a custom (x,y,z)
        gcode = 'G92 x{} y{} z{}\n'.format(x, y, z)
        self.send(self, gcode)
        # update our internal location
        self.pos = [x, y, z]

    def clearAlarm(self):
        """Clear the alarm on the GRBL machine."""
        print('Clearing alarm...')
        response = self.send(str('$X'))
        response += ', ' + self.send(str('?'))
        return response

    def flushStop(self):
        """Stop active command, flush and clear alarm."""
        # Don't know if 100% correct, but it seems to work.
        # Inspired by bcnc bCNC/bCNC/controllers/_GenericController.py:line 176
        # (def purgeController(self):)
        # self.s.write(b'!')
        # self.s.flush()
        # time.sleep(1)
        # self.s.write(b'\030')
        # response = self.send(str('$X'))
        # # response += ', ' + self.send(str('$G'))
        # response += ', ' + self.send(str('?'))
        # What bcnc does?
        self.s.write(b'!')
        self.s.flush()
        time.sleep(1)
        self.s.write(b'\030')
        response = self.send(str('#'))
        self.s.write(b'$G\n')
        response += ', ' + self.send(str('$G'))
        response += ', ' + self.send(str('$X'))
        response += ', ' + self.send(str('G0 G54 G17 G21 G90 G94'))
        response += ', ' + self.send(str('G43.1Z0.000'))
        response += ', ' + self.send(str('$G'))
        response += ', ' + self.send(str('?'))
        return response

    def Cancel(self):
        """Stop active command, flush and clear alarm."""
        # Don't know if 100% correct, but it seems to work.
        # Inspired by bcnc bCNC/bCNC/controllers/_GenericController.py:line 176
        # (def purgeController(self):)
        # self.s.write(b'!')
        # self.s.flush()
        # time.sleep(1)
        # self.s.write(b'\030')
        # response = self.send(str('$X'))
        # # response += ', ' + self.send(str('$G'))
        # response += ', ' + self.send(str('?'))
        # What bcnc does?
        self.s.write(b'!')
        self.s.flush()
        time.sleep(1)
        self.s.write(b'\030')
        response = self.send(str('#'))
        self.s.write(b'$G\n')
        response += ', ' + self.send(str('$G'))
        response += ', ' + self.send(str('$X'))
        response += ', ' + self.send(str('G0 G54 G17 G21 G90 G94'))
        # response += ', ' + self.send(str('G43.1Z0.000')) # Restore state?
        response += ', ' + self.send(str('$G'))
        response += ', ' + self.send(str('?'))
        return response

    def enableSteppers(self):
        """Enable the motors on the GRBL machine."""
        response = self.send(str('M17'))
        response += ', ' + self.send(str('?'))
        return response

    def feedHold(self):
        """Feed hold the GRBL machine."""
        response = self.send(str(r'!'))
        response += ', ' + self.send(str('?'))
        return response

    def disableSteppers(self):
        """Disable the motors on the GRBL machine."""
        response = self.send(str('M17'))
        response += ', ' + self.send(str('?'))
        return response

    def ensureMovementMode(self, absoluteMode=True):
        """Set movement to desired form."""
        # GRBL has two movement modes
        # if necessary this function tells GRBL to switch modes
        if self.abs_move == absoluteMode:
            return
        self.abs_move = absoluteMode
        if absoluteMode:
            self.s.write(b'G90\r\n')  # absolute movement mode
        else:
            self.s.write(b'G91\r\n')  # relative movement mode
            self.s.readline()
