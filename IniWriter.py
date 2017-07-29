#!/usr/bin/python
# coding=utf8
#########################################################################################################
# dieses Skript soll seine übergebenen Argumente auslesen. Das erste Argument ist der Name des Skrpts
# das zweite Argument soll ein ParameterName sein (z.B. Prescaler_a), das dritte Argument ist der neue
# Wert des zu manipulierenden Parameters.
# Nach gründlicher Prüfung der Argumente soll der ParameterName im zugehörigen ini-File gesucht werden.
# Wurde er gefunden wird der Wert entsprechend eingetragen.
#
########################################################################################################

import sys
import ConfigParser
import pprint

def readIniFile():
	#print "readIniFile called ..."
        # erstellen einer conigParser instanz
        Config = ConfigParser.ConfigParser()
        ini_path = "..//TestDir//GardeningSys.ini"

        # file über path öffnen
        Config.read( ini_path )

	my_dict = {}
        # lesen der sections ... ich erwarte eine
        my_section = Config.sections()

	for i in range(0, len( my_section )):
		#print "i = %d"%i
		my_dict[ my_section[i] ] = {}
		sect_elems = Config.options( my_section[i] )
		for j in range(0, len( sect_elems )):
			#print "j = %d"%j
			my_dict[ my_section[i] ][ sect_elems[j] ] = Config.get( my_section[i], sect_elems[j] )

        	        if my_dict[ my_section[i] ][ sect_elems[j] ] == -1:
                        	print ">>>Warning read elem from ini was -1"
                        	continue

	return my_dict

def writeIniFile(ini_dict):
	#print "writeIniFile called ..."

        Config = ConfigParser.ConfigParser()
        ini_path = "..//TestDir//GardeningSys.ini"
	ini_file = open( ini_path, 'w' )
		
	for key in ini_dict:
		#print "> " + key
		Config.add_section( key )
		for param in ini_dict[ key ]:
			#print ">>> " + param + ", " + ini_dict[key][param]
			Config.set( key, param, ini_dict[key][param] )

	Config.write( ini_file )
	ini_file.close()


def main():
	print "try to update ini parameter ..."

	if len(sys.argv) != 3:
		print ">>>USAGE: to much paramter=> Parameter: Value(dezimal)"
		return 1

	if len( sys.argv[1] ) > 15:
		print "Unknown Parameter - to long"
		return 1
	try:
		myIntValue = int( sys.argv[2], 10 )
		type(myIntValue)
		if myIntValue < 1 or myIntValue > 10:
			print ">>>USAGE: Value needs to be between 1 and 10"
			return 1
	except Exception, e:
		print ">>>ERROR - unable to convert handled value (argument 2 needs to be dez)"
		return 1	

	#print 'Number of arguments:', len(sys.argv), 'arguments.'
	#print 'Argument List:', str(sys.argv)
	
	# lese ini-File
	ini_dict = readIniFile()

	#print "ini_dict BEFORE change"
        #pp = pprint.PrettyPrinter(indent=2)
        #pp.pprint( ini_dict )	

	elem_found = False

	#print sys.argv[1]
	for elem_0 in ini_dict:
		#print ">" + elem_0   # elem_0 section level
		if elem_found: break
		for elem_1 in ini_dict[elem_0]:
			#print ">>> " + elem_1 + " == " + sys.argv[1]	 #elem_1 parameter level
			if sys.argv[1] == elem_1:
				elem_found = True
				ini_dict[elem_0][elem_1] = sys.argv[2]
				break

	#print "ini_dict AFTER change"
        #pp = pprint.PrettyPrinter(indent=2)
        #pp.pprint( ini_dict )


	if elem_found:
		print "Okay - parameter updated"
        	# schreibe manipuliertes dict in ini-File
	        writeIniFile(ini_dict)
	else:
		print ">>>Bad - parameter NOT found in ini-file - no parameter update"
		return 1
	
	print "done fine ..."
	return 0

if __name__ == "__main__":
   main()
