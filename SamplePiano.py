''' 
 * SamplePiano.py
 *
 *   Created on:         29.06.2021
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
import sys
from pygame import mixer
from queue import Queue

import sampleTable as st

class AseqDump:

    def __init__(self): # TODO add aseqdump args
        self.midiCommandQ = Queue()
        self.noteCmdParam = {}
        self.aseqDump = None


    def startAseqDump(self, _midiClient):
        aseqDumpArgs = ["aseqdump", "-p", _midiClient]
        self.aseqDump = threading.Thread( target=self.executeCmdAndParseStdout, 
                                      args=(aseqDumpArgs, lineQ) )
        self.aseqDump.daemon = True
        self.aseqDump.start()


    def executeCmdAndParseStdout(_cmd, _lineQ):
        popen = subprocess.Popen( self.aseqCmd, stdout=subprocess.PIPE,
                                  universal_newlines=True )

        for stdout_line in iter( popen.stdout.readline, "" ):
            print( stdout_line )
            if self.isHeader( stdout_line ):
                continue
            self.parseLineAndQueueCmdParams( stdout_line )

        popen.stdout.close()
        return_code = popen.wait()

        if return_code:
            raise subprocess.CalledProcessError(return_code, _cmd)


    def isHeader(self, _line):
        findCount = _line.find( 'Source' )
        if -1 != findCount:
            return True
        else:
            return False


    def parseLineAndQueueCmdParams(self, _line):
        lineSegments = self.getLineSegments( _line )
        self.getCmdParameters( lineSegments )

        self.midiCommandQ.put( self.noteCmdParam )


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
        elif: "Note off" == self.cmdParam["command"]:
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


class SamplePiano:

    def __init__(self):
        pass


def evalNoteAndPlaySound(_note):
    global soundTable

    try:
        sample = soundTable[_note]
        sample.play()
        print("playing sample for", _note)
    except:
        print("No sample for", _note)


def checkExitOnNote(_note):
    if "note 36" == _note:
        print( "sys.exit() on note 36" )
        mixer.stop()
        mixer.quit()
        sys.exit()


def createSoundTable():
    print("\nCreating sound table...")
    global soundTable

    for key in st.sampleTable:
        filename = st.sampleTable[key]
        print(" ", key, "plays", filename)
        try:
            soundTable[key] = mixer.Sound(filename)
        except:
            print("invalid file")

    print("  ...done\n")

if __name__ == "__main__":

    soundTable = {}
    lineQ = Queue()

    aseqDumpArgs = ["aseqdump", "-p", str(st.midiClient)]
    aseqDump = threading.Thread( target=executeCmdAndQueueStdout, 
                                 args=(aseqDumpArgs, lineQ) )
    aseqDump.daemon = True
    aseqDump.start()

    mixer.pre_init(44100, -16, 2, 2048)
    mixer.init()
    mixer.set_num_channels( st.polyphony )

    createSoundTable()
    evalNoteAndPlaySound( 'ready' )

    while True:
        line = lineQ.get() # get std output of aseqdump line by line
        lineSegments = parseAseqdumpLine( line )
        note = filterMidiCmdsForNoteOn( lineSegments )
        if note:
            checkExitOnNote( note )
            evalNoteAndPlaySound( note )


''' END '''
        
