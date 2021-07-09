''' 
 * SamplePiano.py
 *
 *   Created on:         29.06.2021
 *   Author:             Riven Hexagon      
 * 
 * General description:
 *   Evaluates an integer value (MIDI note index) and plays a corresponding audio
 *   file using the pygame mixer module. It requires a sample table in form of a
 *   native python dict containing the note index and the path to the correspon-
 *   ding audio sample. The _polyphony parameter adjusts how many samples can be
 *   played simultaneously.
'''

import sys
from pygame import mixer


class SamplePiano:

    def __init__(self, _sampleTable, _polyphony, _exitNote):
        self.soundTable  = {}
        self.exitNote = _exitNote

        self.initMixer( _polyphony )
        self.createSoundTable( _sampleTable )


    def initMixer(self, _polyphony):
        mixer.pre_init(44100, -16, 2, 2048)
        mixer.init()
        mixer.set_num_channels( _polyphony )


    def createSoundTable(self, _sampleTable):
        print("\nCreating sound table...")

        for noteIndex in _sampleTable:
            filename = _sampleTable[noteIndex]
            try:
                self.soundTable[noteIndex] = mixer.Sound(filename)
                print(" Note", noteIndex, "plays", filename)
            except:
                print("Invalid file")

        print(" ...done\n")


    def evalNoteAndPlaySound(self, _noteIndex):
        self.checkExitOnNote( _noteIndex )
        try:
            sample = self.soundTable[_noteIndex]
            sample.play()
            print("Playing sample for Note", _noteIndex)
        except:
            print("No sample for Note", _noteIndex)


    def checkExitOnNote(self, _noteIndex):
        if _noteIndex == self.exitNote:
            mixer.stop()
            mixer.quit()
            print( "sys.exit() on note", self.exitNote )
            sys.exit()


if '__main__' == __name__: # for testing purposes

    import time

    sampleTable = { 48: 'sounds/cat-meow.wav', 
                    50: 'sounds/dog-barking.wav'}

    polyphony = 2
    exitNote  = 36

    myPiano = SamplePiano( sampleTable, polyphony, exitNote )
    myPiano.evalNoteAndPlaySound( 48 )
    myPiano.evalNoteAndPlaySound( 50 )

    time.sleep(2)

''' END '''
        
