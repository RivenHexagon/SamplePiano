
# https://stackoverflow.com/questions/4760215/running-shell-command-and-capturing-the-output?rq=1

def getClientNumberFromLine(_line):
    segments = _line.split(" ")
    clientNumber = int( segments[1][:-1] ) #[:-1] ommits ":" after client number
    return clientNumber

if '__main__' == __name__:

    import subprocess
    import AseqDumpParser as ap

    myAp = ap.AseqDumpParser()

    res = subprocess.run(['aconnect', '-i'], stdout=subprocess.PIPE)
    resStr = res.stdout.decode('utf-8')

    lines = resStr.split("\n")
    for line in lines:
        if myAp.lineContainesWords(["'Midi Through'"], line):
            print(line)
            clientNumber = getClientNumberFromLine(line)
            print("client number:", clientNumber)




''' END '''

