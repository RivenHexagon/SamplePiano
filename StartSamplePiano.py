''' 
 * StartSamplePiano.py
 *
 *   Created on:         09.07.2021
 *   Author:             Riven Hexagon      
 * 
 * General description:
 *   Reads MIDI data on Linux via aseqdump from a piano and plays corresponding
 *   audio files using pygame mixer module.
 *   Add your your files to sampleTable.py and adapt the midiClient parameter.
'''

import subprocess
from time import sleep
import sys

import sampleTable as st
import SamplePiano as sp
import AseqDumpParser as adp
import AconnectParser as acp


def autoSetupMidiDeviceNumber( _midiDevName ):
    aConnectOutput = subprocess.run( ['aconnect', '-i'],
                          stdout=subprocess.PIPE )
    myAcp          = acp.AconnectParser()
    midiDevNumber  = myAcp.fetchDeviceNumber( _midiDevName,
                                              aConnectOutput )
    if midiDevNumber:
        print(_midiDevName, "has MIDI device number:", midiDevNumber)
        return midiDevNumber


def isNoteOn(_midiCmd):
    return ('Note on' == _midiCmd['command'])


if '__main__' == __name__:
    #FIXME use https://pypi.org/project/alsa-midi/
    sleep(st.startupDelay) # wait for RaspPi to fully boot

    midiDevNumber = autoSetupMidiDeviceNumber( st.midiDeviceName )
    myParser      = adp.AseqDumpParser( midiDevNumber )
    myPiano       = sp.SamplePiano( st.sampleTable,
                                    st.polyphony,
                                    st.exitNote )

    sleep(1)    
    myPiano.evalNoteAndPlaySound( 0 )

    while True:
        midiCmd = myParser.getNextMidiCommand()
        #print( midiCmd )
        if isNoteOn( midiCmd ):
            myPiano.evalNoteAndPlaySound( midiCmd['note'] )

''' END '''

