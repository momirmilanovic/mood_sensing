from random import randint, choice

'''
MOODS = {
	1 : "HAPPY",
	2 : "SAD",
	3 : "NEUTRAL"
}
'''


LOCATIONS = {
	"home" : (44.311122, 20.123456),
	"shopping" : (45.276006, 19.825982),
	"park" : (44.276006, 18.825982),
	"bar" : (45.276900, 20.025931),
	"gym" : (46.276996, 21.825931)
}

MOODS = ["HAPPY", "SAD", "NEUTRAL"]



def get_mood():

	return MOODS[randint(0, 2)] 


def get_location():

	#loc = choice(LOCATIONS.keys())
	#long_lat = LOCATIONS[loc]
	#print "loc: " + str(loc) + "long_lat: " + str(long_lat)
	#print locations[randint(0, 4)]
	return choice(LOCATIONS.keys())


def get_loc_position(loc):

	return LOCATIONS[loc]

