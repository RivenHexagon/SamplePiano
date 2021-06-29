'''
 * Parser for aseqdump output:
 * $ aseqdump -p <client_id_of_the_device>
 *
 *  Created on: 25.06.2021
 *  Author: Riven Hexagon  
 *
'''

class AseqdumpParser:

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


    def separateParameters(self, _receivedData, _separator):
        return _receivedData.split( _separator )


    def stripSpecialCharacters(self, _receivedData, _toStrip="b'\\r\\n"):           
        #stripped input example: "w(t): 149, u(t): 38, y(t): 145, e(t): 4"
        return _receivedData.strip( _toStrip )


    def covertDataToString(self, _receivedData):
        return str( _receivedData )

    def parse(self, _receivedLine):
        separatedParameters = self.separateParameters( strippedData, " " )
        #return separatedParameters


''' END '''

if __name__ == "__main__":
    pass

    



''' END '''
