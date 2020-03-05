import kees_lib

## source
source   = [11.0, 2.0, -3.0, 4.0, -5.0]


for i in xrange(0,5):
	print "source:"+ str(source)
	packet = kees_lib.encode(source)
	print "data:"+ str(packet)
	estimation = kees_lib.decode(packet)
	print "estimated:"+ str(estimation)
	print ""


