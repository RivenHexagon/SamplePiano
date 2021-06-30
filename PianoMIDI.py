import subprocess
import sys
import threading
import AseqdumpParser as adp
from playsound import playsound

def execute(cmd):
    popen = subprocess.Popen(cmd, stdout=subprocess.PIPE, universal_newlines=True)
    for stdout_line in iter(popen.stdout.readline, ""):
        yield stdout_line 
    popen.stdout.close()
    return_code = popen.wait()
    if return_code:
        raise subprocess.CalledProcessError(return_code, cmd)

def evalNote(_params):
    findRes = _params[0].find('Note on')
    if -1 != findRes:
        print( _params[1] )
        if " note 48" == _params[1]:
            makeNoise('3-2-10027.mp3')
        elif " note 36" == _params[1]:
            sys.exit()

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

    for path in lineDump:
        strip  = " ".join(path.split()) #path.replace(" ","")
        params = strip.split(",")
        evalNote(params)

#pygame.mixer.init()
#pygame.mixer.music.load("file.mp3")
#pygame.mixer.music.play()

#$ pip install playsound
#from playsound import playsound
#playsound('/path/to/a/sound/file/you/want/to/play.mp3')

#Buy Raspi Pi 3A+ at segor
