''' 
 * AseqDumpParser.py
 *
 *   Created on:         09.07.2021
 *   Author:             Riven Hexagon      
 * 
 * General description:
 *   Parses output of aseqdump line by line and extracts Note on/off and Pitch
 *   bend midi commands. Those are returned in a queue as native python dicts.
'''

from queue import Queue


class AseqDumpParser:

    def __init__(self):
        self.midiCommandQ = Queue()
        self.cmdParam = {}


    def getNextMidiCommand(self):
        return self.midiCommandQ.get()


    def parseLineAndQueueCmdParams(self, _line):
        if self.isHeader( _line ):
            return

        lineSegments = self.getLineSegments( _line )
        self.getCmdParameters( lineSegments )

        self.midiCommandQ.put( self.cmdParam )


    def isHeader(self, _line):
        findCount1 = _line.find( 'Waiting' )
        findCount2 = _line.find( 'Source' )
        if (-1 != findCount1) or (-1 != findCount2):
            return True
        else:
            return False


    def getLineSegments(self, _line):
        singleBlanksLine = " ".join( _line.split() ) # remove consecutive blanks
        lineSegments     = singleBlanksLine.split( "," )
        return lineSegments


    def getCmdParameters(self, _lineSegs):
        self.cmdParam = {}
        self.getCmdAndChannel( _lineSegs[0] )

        if self.isNoteCmd():
            self.evalNoteCmd( _lineSegs )
        elif self.isPitchBendCmd():
            self.evalPitchBendCmd( _lineSegs )


    def getCmdAndChannel(self, _segment):
        subSegs = _segment.split( " " )
        cmd = " ".join( (subSegs[1],subSegs[2]) )
        self.cmdParam["command"] = cmd
        self.cmdParam["channel"] = subSegs[3]


    def isNoteCmd(self):
        if "Note on" == self.cmdParam["command"]:
            return True
        elif "Note off" == self.cmdParam["command"]:
            return True
        else:
            return False


    def isPitchBendCmd(self):
        if "Pitch bend" == self.cmdParam["command"]:
            return True
        else:
            return False


    def evalNoteCmd(self, _lineSegs):
        self.getValue( "note", _lineSegs[1] ) # note index
        self.getValue( "velocity", _lineSegs[2] )


    def evalPitchBendCmd(self, _lineSegs):
        self.getValue( "value", _lineSegs[1] ) # pitch bend value


    def getValue(self, _valueName, _segment):
        subSegs = _segment[1:].split( " " ) # [1:] ommits leading blank
        self.cmdParam[_valueName] = int( subSegs[1] )


if '__main__' == __name__:

    import subprocess
    import threading

    import sampleTable as st

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
                                  myParser.parseLineAndQueueCmdParams,
                                  st.midiClient )
    while True:
        midiCmd = myParser.midiCommandQ.get()
        print( midiCmd )


''' END '''

