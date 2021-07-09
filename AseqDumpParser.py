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

from queue import Queue


class AseqDumpParser:

    def __init__(self):
        self.midiCommandQ = Queue()
        self.midiCommand  = {}


    def getNextMidiCommand(self):
        return self.midiCommandQ.get()


    def parseLineAndQueueMidiCmd(self, _line):
        if self.lineContainesWords( ["Waiting", "Source"], _line ):
            return

        lineSegments = self.getLineSegments( _line )
        self.getMidiCmd( lineSegments )

        self.midiCommandQ.put( self.midiCommand )


    def lineContainesWords(self, _keyWords, _line):
        for keyWord in _keyWords:
            findCount = _line.find( keyWord )
            if -1 != findCount:
                return True # line is a headline after startup, not a midi cmd
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

    import subprocess
    import threading

    def executeCmdAndProcessStdout(_cmd, _parserFunct):
        popen = subprocess.Popen( _cmd, stdout=subprocess.PIPE,
                                  universal_newlines=True )

        for stdout_line in iter( popen.stdout.readline, "" ):
            #print( "stdout line:", stdout_line, end="" )
            _parserFunct( stdout_line )

        popen.stdout.close()
        return_code = popen.wait()

        if return_code:
            raise subprocess.CalledProcessError(return_code, _cmd)


    def startAseqDump(_targetFunct, _parserFunct, _midiClient):
        aseqDumpArgs = ["aseqdump", "-p", str(_midiClient)]
        aseqDump = threading.Thread( target=_targetFunct,
                                     args=(aseqDumpArgs, _parserFunct) )
        aseqDump.daemon = True
        aseqDump.start()
        return aseqDump


    myParser = AseqDumpParser()
    aseqDump = startAseqDump( executeCmdAndProcessStdout, 
                              myParser.parseLineAndQueueMidiCmd,
                              28 ) # identify with 'aconnect -i' on console
    while True:
        midiCmd = myParser.midiCommandQ.get()
        print( midiCmd )

''' END '''

