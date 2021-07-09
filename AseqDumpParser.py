''' 
 * AseqDumpParser.py
 *
 *   Created on:         09.07.2021
 *   Author:             Riven Hexagon      
 * 
 * General description:
 *   Reads MIDI data on Linux via aseqdump from a piano and plays corresponding
 *   audio files using pygame mixer module.
 *   Find your MIDI device client number with 'aconnect -i' on the console. Use
 *   client number as aseqdump argument for the MIDI port number for e.g. -p 28:
 *   aseqDumpArgs = ["aseqdump", "-p", "<client_number>"]
'''

import subprocess
import threading
from queue import Queue

import sampleTable as st

class AseqDumpParser:

    def __init__(self):
        self.midiCommandQ = Queue()
        self.noteCmdParam = {}


    def parseLineAndQueueCmdParams(self, _line):
        if self.isHeader( _line ):
            return

        lineSegments = self.getLineSegments( _line )
        self.getCmdParameters( lineSegments )

        self.midiCommandQ.put( self.noteCmdParam )
        print( self.noteCmdParam )


    def isHeader(self, _line):
        findCount = _line.find( 'Source' )
        if -1 != findCount:
            return True
        else:
            return False


    def getLineSegments(self, _line):
        singleBlanksLine = " ".join( _line.split() ) # remove consecutive blanks
        lineSegments     = singleBlanksLine.split( "," )
        return lineSegments


    def getCmdParameters(self, _lineSegs):
        self.noteCmdParam = {}
    
        self.getCmdAndChannel( _lineSegs[0] )
        if self.isNoteCmd():
            self.evalNoteCmd( _lineSegs )


    def getCmdAndChannel(self, _segment):
        subSegs = _segment.split( " " )
        cmd = " ".join( (subSegs[1],subSegs[2]) )
        print( "cmd:", cmd)
        self.cmdParam["command"] = cmd
        self.cmdParam["channel"] = subSegs[3]


    def isNoteCmd():
        if "Note on" == self.cmdParam["command"]:
            return True
        elif "Note off" == self.cmdParam["command"]:
            return True
        else:
            return False


    def evalNoteCmd(self, _lineSegs):
        self.getNoteIndex( _lineSegs[1] )
        self.getVelocity ( _lineSegs[2] )


    def getNoteIndex(self, _segment):
        subSegs = _segment[1:].split( " " ) # [1:] ommits leading blank
        self.noteCmdParam["note"] = subSegs[1] 


    def getVelocity(self, _segment):
        subSegs = _segment[1:].split( " " ) # [1:] ommits leading blank
        self.noteCmdParam["velocity"] = subSegs[1]

''' ---- ---- ---- '''

def executeCmdAndProcessStdout(_cmd, _parserFunct):
    popen = subprocess.Popen( _cmd, stdout=subprocess.PIPE,
                              universal_newlines=True )

    for stdout_line in iter( popen.stdout.readline, "" ):
        print( stdout_line )
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


if '__main__' == __name__:

    myParser = AseqDumpParser()
    aseqDump = startAseqDump( executeCmdAndProcessStdout, 
                              myParser.parseLineAndQueueCmdParams,
                              st.midiClient )

''' END '''

