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

    def __init__(self):
        self.noteQ = Queue()


    def executeCmdAndQueueStdout(_cmd, _lineQ):
        popen = subprocess.Popen( _cmd, stdout=subprocess.PIPE,
                                  universal_newlines=True )

        for stdout_line in iter( popen.stdout.readline, "" ):
            _lineQ.put( stdout_line )

        popen.stdout.close()
        return_code = popen.wait()

        if return_code:
            raise subprocess.CalledProcessError(return_code, _cmd)


    def parseAseqdumpLine(_line):
        lineSegments = self.getLineSegments( _line )


    def getLineSegments(self, _line):
        singleBlanksLine = " ".join( _line.split() ) # remove consecutive blanks
        lineSegments     = singleBlanksLine.split( "," )
        return lineSegments


def filterMidiCmdsForNoteOn(_lineSegments):
    if isNoteOn( _lineSegments[0] ):
        note = _lineSegments[1][1:] # [1:] ommits leading blank
        return note
    else:
        return None


def isNoteOn(_lineSegment):
    findCount = _lineSegment.find( 'Note on' )

    if -1 != findCount:
        return True
    else:
        return False


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
        
