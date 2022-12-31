# SamplePiano
This Python3 script reads **MIDI** data on Linux via aseqdump from a MIDI device and **plays** corresponding **audio samples** using the pygame mixer module. You can use it for example to play audio files with a MIDI keyboard.

## Edit sampleTable.py

The file `sampleTable.py` needs to be edited in order to **identify** your **MIDI device** and to **assign** the **audio files** to the correspondig keys on your MIDI input device.

### Identify the MIDI client id
Your MIDI device is adressed by its **MIDI client id**. Unfortunately the client id may be subject to **change** after you reboot the system. This may happen if you run the script on a headless Raspberry Pi (with no monitor and input devices).

The `midiClientId` can be fetched **automatically** if you provide the parameter `midiDeviceName`.

To identify the **name** of your MIDI controller - as well as its client id - use the helper program `aconnect` on the **console** of the system where you wanna use the script on:

`$ aconnect -i`

The output may look like this:

    client 0: 'System' [type=kernel]
        0 'Timer           '
        1 'Announce        '
    client 14: 'Midi Through' [type=kernel]
        0 'Midi Through Port-0'
    client 24: 'Keystation Mini 32' [type=kernel,card=1]
        0 'Keystation Mini 32 MIDI 1'

Exit the program with `Ctrl+C`.

Use the **name string** after the client id and keep the **quotes**, for e.g.: `midiDeviceName = "'Keystation Mini 32'"`.

Alternatively you can provide the client id **manually**: `midiClientId = 24`. This parameter will only be **recognized** if you **define** `midiDeviceName = None`.

### Edit the sample table
To identify the **note numbers** of your MIDI keyboard's keys, run the helper program `aseqdump`. Give the **client number** of your MIDI devicde as a **parameter** and act on some keys and controllers:

`$ aseqdump -p 24`

The output may look like this:

    Source  Event           Ch  Data
    24:0    Pitch bend       0, value 207
    24:0    Note on          0, note 47, velocity 30
    24:0    Note off         0, note 47, velocity 0
    24:0    Note on          0, note 48, velocity 34
    24:0    Note off         0, note 48, velocity 0

Exit the program with `Ctrl+C`.

Now edit the **sample table** to **match** the **keys** with the corresponding **audio samples** you wanna play on key press.

    sampleTable = { 47: soundDir + 'cat-meow.wav',
                    48: soundDir + 'dog-barking.wav',
                    49: soundDir + 'cow-moos.wav',
                    50: soundDir + 'ringing.wav',
                    0:  soundDir + 'unit-ready.wav',
                   -1:  soundDir + 'shutdown.wav' }

### Polyphony

The `polyphony` parameter defines how many sounds can be played **simultaneously**.

## Make it run on a Raspberry Pi
As of July 2021 make sure you **apply** the following **update** and **installation**:

    $ pip3 install pygame --update
    $ sudo apt install libsdl2-mixer-2.0

Start the script manually with

    $ python3 StartSamplePiano.py

You can also add the script to an **autostart** file such as `/etc/xdg/lxsession/LXDE-pi/autostart`.
Add the Script to the **end** of the file by keeping the existing entrys:

    @lxpanel --profile LXDE-pi
    @pcmanfm --desktop --profile LXDE-pi
    @xscreensaver -no-splash
    @python3 /home/pi/SamplePiano/StartSamplePiano.py
