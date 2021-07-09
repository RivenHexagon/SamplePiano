''' 
 * StartSamplePiano.py
 *
 *   Created on:         09.07.2021
 *   Author:             Riven Hexagon      
 * 
 * General description:
 *   Reads MIDI data on Linux via aseqdump from a piano and plays corresponding
 *   audio files using pygame mixer module.
 *   Find your MIDI device client number with 'aconnect -i' on the console. Use
 *   client number as aseqdump argument for the MIDI port number for e.g. -p 28:
 *   aseqDumpArgs = ["aseqdump", "-p", "<client_number>"] Add the client number
 *   and your your audio files to sampleTable.py
'''

import subprocess
import threading

import sampleTable as st
import SamplePiano as sp
import AseqDumpParser as adp


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
    aseqDump.daemon = True # kills thread on sys.exit()
    aseqDump.start()
    return aseqDump


def isNoteOn(_midiCmd):
    return ('Note on' == _midiCmd['command'])


if '__main__' == __name__:

    myPiano  = sp.SamplePiano( st.sampleTable, st.polyphony )
    myParser = adp.AseqDumpParser()

    aseqDump = startAseqDump( executeCmdAndProcessStdout, 
                              myParser.parseLineAndQueueCmdParams,
                              st.midiClient )

    myPiano.evalNoteAndPlaySound( 0 )

    while True:
        midiCmd = myParser.getNextMidiCommand()
        #print( midiCmd )
        if isNoteOn( midiCmd ):
            myPiano.evalNoteAndPlaySound( midiCmd['note'] )


''' END '''

