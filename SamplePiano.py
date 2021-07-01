''' 
 * SamplePiano.py
 *
 *   Created on:         29.06.2021
 *   Author:             Riven Hexagon      
 * 
 * General description:
 *   Reads MIDI data on Linux via aseqdump from a piano andplays corresponding
 *   audio files using playsound module. 
'''

import subprocess
import sys
import threading
from queue  import Queue
from playsound import playsound

import sampleTable as st


def executeCmdAndQueueStdout(_cmd, _lineQ):
    popen = subprocess.Popen( _cmd, stdout=subprocess.PIPE,
                              universal_newlines=True )

    for stdout_line in iter(popen.stdout.readline, ""):
        _lineQ.put( stdout_line )

    popen.stdout.close()
    return_code = popen.wait()

    if return_code:
        raise subprocess.CalledProcessError(return_code, _cmd)


#TODO make parser for those lines that gives full content
def parseAseqdumpLine(_line):
    singleBlanksLine = " ".join( _line.split() ) # remove consecutive blanks
    lineSegments     = singleBlanksLine.split( "," )
    return lineSegments


def filterMidiCmdsForNoteOn(_lineSegments):
    if isNoteOn( _lineSegments[0] ):
        note = _lineSegments[1][1:] # [1:] ommits leading blank
        return note


def isNoteOn(_lineSegment):
    findCount = _lineSegment.find( 'Note on' )

    if -1 != findCount:
        return True
    else:
        return False


def evalNoteAndPlaySound(_note):
    try:
        audioFileName = st.sampleTable[_note]
        if noSoundIsPlaying():
            print( "Playing sample for", _note )
            makeNoise( audioFileName )
    except:
        print( "No sample for", _note )


def checkExitOnNote(_note):
    if "note 36" == _note:
        print("sys.exit() on note 36")
        sys.exit()


def noSoundIsPlaying():
    cnt = threading.active_count()

    if cnt < 3:
        return True
    else:
        return False


def makeNoise(_title):
        t1 = threading.Thread( target=playsound, args=(_title,) )
        t1.start()


if __name__ == "__main__":

    lineQ  = Queue()
    aseqDumpArgs = ["aseqdump", "-p", "28"]
    aseqDump = threading.Thread( target=executeCmdAndQueueStdout, 
                                 args=(aseqDumpArgs, lineQ) )
    aseqDump.daemon = True
    aseqDump.start()

    while True:
        line = lineQ.get()
        lineSegments = parseAseqdumpLine( line )
        note = filterMidiCmdsForNoteOn( lineSegments )
        checkExitOnNote( note )
        evalNoteAndPlaySound( note )


''' END '''
        
