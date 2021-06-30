import subprocess
import sys
import threading
import AseqdumpParser as adp
from playsound import playsound

def execute(_cmd):

    popen = subprocess.Popen(_cmd, stdout=subprocess.PIPE, universal_newlines=True)

    for stdout_line in iter(popen.stdout.readline, ""):
        yield stdout_line 

    popen.stdout.close()
    return_code = popen.wait()

    if return_code:
        raise subprocess.CalledProcessError(return_code, _cmd)


def parseLine(_line):

        blankFreeLine = " ".join( _line.split() ) # remove consecutive blanks
        lineSplits    = blankFreeLine.split( "," )
        findResults   = lineSplits[0].find( 'Note on' )

        if -1 != findResults:
            note = lineSplits[1] 
            evalNote( note[1:] ) # ommit leading blank


def evalNote(_note):

    sampleTable = { "note 48": '3-2-10027.mp3', 
                    "note 50": 'dog-barking.wav',}

    if "note 36" == _note:
        print(_note, "sys.exit()")
        sys.exit()

    try:
        audioFileName = sampleTable[_note]
        print("Playing sample for", _note)
        makeNoise( audioFileName )
    except:
        print("No sample for", _note)


def makeNoise(_title):

    global flag
    if False == flag:
        flag = True
        t1 = threading.Thread( target=startSoundThread, args=(_title,) )
        t1.start()

            
def startSoundThread(_title):

    global flag
    playsound(_title)
    flag = False


if __name__ == "__main__":

    flag = False

    myParser = adp.AseqdumpParser()
    lineDump = execute(["aseqdump", "-p", "24"])
    #t1 = threading.Thread( target=playsound, args=('3-2-10027.mp3',) )

    for line in lineDump:
        parseLine( line )

#path.replace(" ","")
#pygame.mixer.init()
#pygame.mixer.music.load("file.mp3")
#pygame.mixer.music.play()

#$ pip install playsound
#from playsound import playsound
#playsound('/path/to/a/sound/file/you/want/to/play.mp3')

#Buy Raspi Pi 3A+ at segor
