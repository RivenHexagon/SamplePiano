
''' 
 * AconnectParser.py
 *
 *   Created on:         09.07.2021
 *   Author:             Riven Hexagon      
 * 
 * General description:
 *   Parses output of aconnect. It identifies the line representing the desired
 *   MIDI input device and extrtacts its device number. The number is returned
 *   as an int. Aconnect is a linux tool that lists connected MIDI devices.
 *   https://stackoverflow.com/questions/4760215/running-shell-command-and-capturing-the-output?rq=1
'''

class AconnectParser:

    def __init__(self):
        pass


    def fetchDeviceNumber(self,  _midiDevName, _aConnectOutput ):
        outStr = self.decodeAconOutput( _aConnectOutput )
        lines  = self.getSeparateLines( outStr )
        line   = self.findLineOfMidiDevice( _midiDevName, lines )
        if line:
            deviceNumber = self.getDeviceNumberFromLine( line )
            return deviceNumber
        else:
            return None


    def decodeAconOutput(self, _output):
        outputAsString = _output.stdout.decode('utf-8')
        return outputAsString


    def getSeparateLines(self, _outStr):
        lines = _outStr.split("\n")
        #print("lines ", lines)
        return lines


    def findLineOfMidiDevice(self, _device, _lines):
        for line in _lines:
            #print("line: ", line)
            if self.lineContainesWords([_device], line):
                return line

        print( "Device", _device, "not found" )
        return None


    def lineContainesWords(self, _keyWords, _line):
        for keyWord in _keyWords:
            findCount = _line.find( keyWord )
            if -1 != findCount:
                return True
        return False


    def getDeviceNumberFromLine(self, _line):
        segments = _line.split(" ")
        # [:-1] ommits ":" after device number
        deviceNumber = int( segments[1][:-1] )
        return deviceNumber


if '__main__' == __name__:

    import subprocess
    import sampleTable as st

    myAcp = AconnectParser()

    output = subprocess.run( ['aconnect', '-i'],
                          stdout=subprocess.PIPE )

    midiDevNumber = myAcp.fetchDeviceNumber( st.midiDeviceName,
                                             output )
    if midiDevNumber:
        print("device number:", midiDevNumber)



''' END '''

