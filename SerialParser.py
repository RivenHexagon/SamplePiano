'''
 * ArduSerial.py
 *
 *  Created on: 01.04.2020
 *  Author: Kolja Funkmeyer
 *
'''

class Parser:

    def __init__(self):
        self.parameterDict  = {}


    def nameValuePairsAsDict(self, _receivedData):
        
        nameValuePairs = extractNameValuePairs( _receivedData )

        for nameValuePair in nameValuePairs:

            name = str( nameValuePair[0] )
            value = int( nameValuePair[1] )
            self.parameterDict.update( {name: value} )

        return self.parameterDict


    def extractNameValuePairs(self, _receivedData):
        nameValuePairs = []

        for parameter in separatedParameters:
            nameValuePairs.append( parameter.split( ':' ) )

        return nameValuePairs


    def separateParameters(self, _receivedData):
        return _receivedData.split( ', ' )


    def stripSpecialCharacters(self, _receivedData, _toStrip="b'\\r\\n"):           
        #stripped input example: "w(t): 149, u(t): 38, y(t): 145, e(t): 4"
        return _receivedData.strip( _toStrip )


    def covertDataToString(self, _receivedData):
        return str( _receivedData )

    def parseSerial(_receivedData):
        dataAsString = self.covertDataToString( _receivedData )
        strippedData = self.stripSpecialCharacters( dataAsString )
        separatedParameters = self.separateParameters( strippedData )
        nameValuePairs = extractNameValuePairs( separatedParameters )
        return self.nameValuePairsAsDict(nameValuePairs)


''' END '''

if __name__ == "__main__":

    

