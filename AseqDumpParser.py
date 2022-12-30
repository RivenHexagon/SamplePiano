''' 
 * AseqDumpParser.py
 *
 *   Created on:         09.07.2021
 *   Author:             Riven Hexagon      
 * 
 * General description:
 *   Parses output of aseqdump line by line and extracts Note on/off and Pitch
 *   bend MIDI commands. Those are returned in a queue as native python dicts.
 *   Aseqdump is a linux tool that logs incoming MIDI commands to the console.
'''

import subprocess
import sampleTable as st


class AseqDumpParser:

    def __init__(self, _midiClient):
        self.midiCommand  = {}
        aseqDumpArgs      = ["aseqdump", "-p", str(_midiClient)]
        self.popen        = subprocess.Popen( aseqDumpArgs,
                            stdout=subprocess.PIPE,
                            universal_newlines=True )
    

    def getNextMidiCommand(self):
        for stdout_line in iter( self.popen.stdout.readline, b"" ):
            if self.parseLineAndQueueMidiCmd( stdout_line ):
                return self.midiCommand
        # FIXME use prt unsubscribed


    def parseLineAndQueueMidiCmd(self, _line):
        if self.lineContainesWords( ["Waiting", "Source"], _line ):
            return False# line is a headline after startup, not a midi cmd

        lineSegments = self.getLineSegments( _line )
        self.getMidiCmd( lineSegments )
        return True
        #self.midiCommandQ.put( self.midiCommand )


    def lineContainesWords(self, _keyWords, _line):
        for keyWord in _keyWords:
            findCount = _line.find( keyWord )
            if -1 != findCount:
                return True
        return False


    def getLineSegments(self, _line):
        singleBlanksLine = " ".join( _line.split() ) # remove consecutive blanks
        lineSegments     = singleBlanksLine.split( "," )
        return lineSegments


    def getMidiCmd(self, _lineSegs):
        self.midiCommand = {} # clear temp cmd
        self.getMidiCmdTypeAndChannel( _lineSegs[0] )

        if self.isMidiCommandOfTypes( ["Note on", "Note off"] ):
            self.evalNoteCmd( _lineSegs )
        elif self.isMidiCommandOfTypes( ["Pitch bend"] ):
            self.evalPitchBendCmd( _lineSegs )
        else:
            print( "Unsupported MIDI command" )


    def getMidiCmdTypeAndChannel(self, _segment):
        subSegs = _segment.split( " " )
        cmd = " ".join( (subSegs[1],subSegs[2]) )

        self.midiCommand["command"] = cmd
        self.midiCommand["channel"] = subSegs[3]


    def isMidiCommandOfTypes(self, _cmdNames):
        for cmdName in _cmdNames:
            if cmdName == self.midiCommand["command"]:
                return True
        return False


    def evalNoteCmd(self, _lineSegs):
        self.getValue( "note", _lineSegs[1] ) # note index
        self.getValue( "velocity", _lineSegs[2] )


    def evalPitchBendCmd(self, _lineSegs):
        self.getValue( "value", _lineSegs[1] ) # pitch bend value


    def getValue(self, _valueName, _segment):
        subSegs = _segment[1:].split( " " ) # [1:] ommits leading blank
        self.midiCommand[_valueName] = int( subSegs[1] )


if '__main__' == __name__:  # for testing purposes

    myParser = AseqDumpParser( st.midiDeviceNumber )

    while True:
        midiCmd = myParser.getNextMidiCommand()
        print( midiCmd )

''' END '''

