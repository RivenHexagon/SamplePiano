''' 
 * SamplePiano.py
 *
 *   Created on:         29.06.2021
 *   Author:             Riven Hexagon      
 * 
 * General description:
 *   Reads MIDI data on Linux from a piano and plays corresponding audio files. 
'''

#import AseqdumpParser as adp

import subprocess
import sys
import threading
from queue  import Queue
from playsound import playsound

sampleTable = { "note 48": 'cat-moaning.mp3', 
                "note 50": 'dog-barking.wav',}

def executeAndYieldStdout(_cmd, _lineQ):
    #global stop_flag
    popen = subprocess.Popen( _cmd, stdout=subprocess.PIPE,
                              universal_newlines=True )

    for stdout_line in iter(popen.stdout.readline, ""):
        _lineQ.put( stdout_line )
        #if stop_flag:
            #break
        #yield stdout_line 

    popen.stdout.close()
    return_code = popen.wait()

    if return_code:
        raise subprocess.CalledProcessError(return_code, _cmd)


#TODO make parser for those lines that gives full content
def parseAseqdumpLine(_line):
    singleBlanksLine = " ".join( _line.split() ) # remove consecutive blanks
    lineSegments     = singleBlanksLine.split( "," )

    if isNoteOn( lineSegments[0] ):
        note = lineSegments[1][1:] # [1:] ommits leading blank
        evalNote( note )


def isNoteOn(_lineSegment):
    findCount = _lineSegment.find( 'Note on' )

    if -1 != findCount:
        return True
    else:
        return False


def evalNote(_note):
    checkExitOnNote( _note )

    try:
        audioFileName = sampleTable[_note]
        if noSoundIsPlaying():
            print( "Playing sample for", _note )
            makeNoise( audioFileName )
    except:
        print( "No sample for", _note )


def checkExitOnNote(_note):
    global stop_flag
    if "note 36" == _note:
        #stop_flag = True
        print("sys.exit() on note 36")
        sys.exit()


def noSoundIsPlaying():
    cnt = threading.active_count()
    print("active cnt:", cnt)

    if cnt < 3:
        return True
    else:
        return False


def makeNoise(_title):
        t1 = threading.Thread( target=playsound, args=(_title,) )
        t1.start()


if __name__ == "__main__":

    stop_flag = False
    lineQ  = Queue()
    aseqDumpArgs = ["aseqdump", "-p", "28"]
    aseqDump = threading.Thread( target=executeAndYieldStdout, 
                                 args=(aseqDumpArgs, lineQ) )
    aseqDump.daemon = True
    aseqDump.start()
    while True:
        line = lineQ.get()
        #print( line )
        parseAseqdumpLine( line )
        #if stop_flag:
            #break

    aseqDump.join()
    #myParser = adp.AseqdumpParser()
    #aseqdumpLines = executeAndYieldStdout(["aseqdump", "-p", "28"])

    #for line in aseqdumpLines:
        #parseAseqdumpLine( line )

''' END '''

#line.replace(" ","")
        
