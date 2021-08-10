
''' 
 * AconnectParser.py
 *
 *   Created on:         09.07.2021
 *   Author:             Riven Hexagon      
 * 
 * General description:
 *   Parses output of aconnect. It identifies the line representing the desired
 *   MIDI input device and extrtacts its client number. The number is returned
 *   as an int. Aconnect is a linux tool that lists connected MIDI devices.
 *   https://stackoverflow.com/questions/4760215/running-shell-command-and-capturing-the-output?rq=1
'''

class AconnectParser:

    def __init__(self):
        pass


    def decodeAconOutput(self, _output):
        outputAsString = _output.stdout.decode('utf-8')
        return outputAsString


    def lineContainesWords(self, _keyWords, _line):
        for keyWord in _keyWords:
            findCount = _line.find( keyWord )
            if -1 != findCount:
                return True
        return False


    def getSeparateLines(self, _outStr):
        lines = outStr.split("\n")
        return lines


    def getClientNumberFromLine(self, _line):
        segments = _line.split(" ")
        # [:-1] ommits ":" after client number
        clientNumber = int( segments[1][:-1] )
        return clientNumber


    def findLineOfMidiDevice(self, _device, _lines):
        for line in _lines:
            if self.lineContainesWords([_device], line):
                return line

        print( "Device", _device, "not found" )
        return None


if '__main__' == __name__:

    import subprocess
    import sampleTable as st

    myAcp = AconnectParser()

    output = subprocess.run( ['aconnect', '-i'],
                          stdout=subprocess.PIPE )

    outStr = myAcp.decodeAconOutput( output )
    lines  = myAcp.getSeparateLines( outStr )
    line   = myAcp.findLineOfMidiDevice( st.midiDeviceName, lines )
    if line:
        print(line)
        clientNumber = myAcp.getClientNumberFromLine( line )
        print("client number:", clientNumber)




''' END '''

