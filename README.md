# SamplePiano
This Python3 script reads MIDI data on Linux via aseqdump from a MIDI device and
plays corresponding audio samples using the pygame mixer module.

## Configuration of sampleTable.py
The samples are assigned to the according MIDI note by the dict `sampleTable` in
the file `sampleTable.py` The `polyphony` value in the same file adjusts how many
sounds can be played simultaneously. The MIDI device is adressed by the `midiClient`
parameter.

To identify the MIDI client number use a helper program on the console:

`$ aconnect -i`

The output may look like this:

    client 0: 'System' [type=kernel]
        0 'Timer           '
        1 'Announce        '
    client 14: 'Midi Through' [type=kernel]
        0 'Midi Through Port-0'
    client 20: 'Keystation Mini 32' [type=kernel,card=1]
        0 'Keystation Mini 32 MIDI 1'

To identify the note numbers of your MIDI keyboard's keys, just run aseqdump manually with the client number of your MIDI devicde as a parameter and act on some keys and controllers:

`$ aseqdump -p 20`

The output may look like this:

    Source  Event           Ch  Data
    20:0    Pitch bend       0, value 207
    20:0    Note on          0, note 47, velocity 30

Exit the program with `Ctrl+C`.

## Make it run on a Raspberry Pi
As of July 2021 make sure you apply the following update and installation:

    $ pip3 install pygame --update
    $ sudo apt install libsdl2-mixer-2.0

Start the script manually with

    $ python3 StartSamplePiano.py

You can also add the script to an autostart file such as `/etc/xdg/lxsession/LXDE-pi/autostart`.
Add the Script to the end of the file by keeping the existing entrys:

    @lxpanel --profile LXDE-pi
    @pcmanfm --desktop --profile LXDE-pi
    @xscreensaver -no-splash
    @python3 /home/pi/SamplePiano/StartSamplePiano.py
