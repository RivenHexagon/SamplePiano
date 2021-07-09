''' 
 * sampleTable.py
 *
 *   Created on:         29.06.2021
 *   Author:             Riven Hexagon      
 * 
 * General description:
 *   Config file for StartSamplePiano.py. Add the file path of your audio
 *   samples to sampleTable and associate them with the MIDI note indices.
'''

# ALSA MIDI device port/client number (adapt).
# Identify by running 'aconnect -i' on console.
midiClient = 28 

# Identify key/note indices by running 'aseqdump -p <client_number>' on console
# and act on your MIDI keyboard.
sampleTable = { 48: 'sounds/cat-meow.wav', 
                50: 'sounds/dog-barking.wav',
                52: 'sounds/cow-moos.wav',
                53: 'sounds/ringing.wav',
                 0: 'sounds/unit-ready.wav',
                -1: 'sounds/shutdown.wav' }

# Adjusts how many samples can be played simultaneously.
polyphony = 2

# End program when this note is pressed
exitNote = 36

''' END '''

