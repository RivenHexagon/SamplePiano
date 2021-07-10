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
midiClient = 24

# Absolute path to audio files. Allows you to start the script from anywhere.
soundDir = '/home/pi/Sample-Piano/sounds/'

# Identify key/note indices by running 'aseqdump -p <client_number>' on console
# and act on your MIDI keyboard.
sampleTable = { 48: soundDir + 'cat-meow.wav', 
                50: soundDir + 'dog-barking.wav',
                52: soundDir + 'cow-moos.wav',
                53: soundDir + 'ringing.wav',
                 0: soundDir + 'unit-ready.wav',
                -1: soundDir + 'shutdown.wav' }

# Adjusts how many samples can be played simultaneously.
polyphony = 2

# Startup delay when StartSamplePiano.py is called by a startup script.
# This allows the environment time to setup in time, such as the audio system.
startupDelay = 5 # seconds

# End program when this note is pressed
exitNote = 36 # use -1 or -2 to disable

''' END '''

