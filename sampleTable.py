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

# To identify your MIDI device, configure the MIDI device name to auto detect
# its ALSA MIDI client id, because the id may change after the system reboots.
# Identify the MIDI device name by running 'aconnect -i' on the system console.
# The output may look like this:
#
# client 14: 'Midi Through' [type=kernel]
#     0 'Midi Through Port-0'
# client 24: 'SmartPAD' [type=kernel,card=2]
#     0 'SmartPAD MIDI 1 '
#
# Use the string after the client number, for e.g. 'SmartPAD '. Keep the name in
# quotes.
#midiDeviceName = "'USB-MIDI'"
midiDeviceName = "'SmartPAD'"
#midiDeviceName = None 
# Use midiDeviceName = None to recognize manually defined client id below.

# Manually set ALSA MIDI device client id.
# Identify the MIDI client id by running 'aconnect -i' on console.
# midiClientId = 24
midiClientId = 24 # only recognized if midiDeviceName = None

# Absolute path to audio files. Allows you to start the script from anywhere.
# Don't forget the "/" at the end of the path!
soundDir = '/home/user0/Workstation/SamplePiano/sounds/'
#soundDir = '/home/pi/SamplePiano/sounds/'

# Identify key/note indices by running 'aseqdump -p <client_number>' on the
# system console and act on your MIDI keyboard. Fill the sound table with the
# indices of the keys and the corresponding sound files to be played.
sampleTable = { 4: soundDir + 'cat-meow.wav', 
                3: soundDir + 'dog-barking.wav',
                2: soundDir + 'cow-moos.wav',
                1: soundDir + 'ringing.wav',
                0: soundDir + 'unit-ready.wav',
               -1: soundDir + 'shutdown.wav' }

# Adjusts how many samples can be played simultaneously.
polyphony = 2

# Startup delay when StartSamplePiano.py is called by a startup script.
# This allows the environment time to setup in time, such as the audio system.
# startupDelay = 5 # seconds (rapberry pi)
startupDelay = 1

# End program when this note is pressed
exitNote = -2 # use -1 or -2 to disable

''' END '''

