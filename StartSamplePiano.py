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

def fetchMidiClientId():
    autoClientId = autoFetchMidiClientId( st.midiDeviceName )
    if autoClientId:
        return autoClientId
    else:
        print("Using manually defined MIDI client id", st.midiClientId)
        return st.midiClientId


def autoFetchMidiClientId( _midiDevName ):
    if None == _midiDevName:
        return None

    aConnectOutput = subprocess.run( ['aconnect', '-i'],
                          stdout=subprocess.PIPE )
    myAcp          = acp.AconnectParser()
    midiClientId   = myAcp.fetchDeviceNumber( _midiDevName,
                                              aConnectOutput )
    if midiClientId:
        print(_midiDevName, "has MIDI client id:", midiClientId)
        return midiClientId
    else:
        print("Auto fetch MIDI client id failed")
        return None


def isNoteOn(_midiCmd):
    return ('Note on' == _midiCmd['command'])


if '__main__' == __name__:
    #FIXME use https://pypi.org/project/alsa-midi/
    sleep(st.startupDelay) # wait for RaspPi to fully boot
    print("")

    midiClientId = fetchMidiClientId()
    myParser      = adp.AseqDumpParser( midiClientId )
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

