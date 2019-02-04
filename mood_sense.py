


import json
from device.device_functions import get_mood, get_location, get_loc_position
from decimal import Decimal
from geopy.distance import geodesic


print "\nMOOD SENSE\n"

def get_moood_loc():
	mood = get_mood()
	location = get_location()

	with open("mood_saver.json", "r") as jsonFile:
		jsonData = json.load(jsonFile)

	mood_num = jsonData[mood]
	mood_num += 1
	jsonData[mood] = mood_num
	print "mood: " + mood + ", mood_num: " + str(mood_num)

	happy_locations = jsonData["HAPPY_LOCATIONS"]
	if mood == "HAPPY":
		print "add happy location " + location
		if location not in happy_locations:
			happy_locations.append(location)
			print "happy_locations now: " + str(happy_locations)
			jsonData["HAPPY_LOCATIONS"] = happy_locations
		else:
			print location + " already in happy_locations"

	with open("mood_saver.json", "w") as jsonFile:
		json.dump(jsonData, jsonFile)

	return mood, location


def happy_proximity(lon, lat):

	#print "happy_proximity: " + str(lon) + "," + str(lat)
	with open("mood_saver.json", "r") as jsonFile:
		jsonData = json.load(jsonFile)

	proximityies = []
	happy_locations = jsonData["HAPPY_LOCATIONS"]
	#print "happy_locations: " + str(happy_locations)
	for l in happy_locations:
		position = get_loc_position(str(l))
		proximity = geodesic(position, (lon, lat))
		print "proximity to " + l + " (position): " + str(position) + " is: " + str(proximity)
		proximityies.append(str(proximity))

	with open("mood_saver.json", "w") as jsonFile:
		json.dump(jsonData, jsonFile)

	return proximityies

def mood_freq_distribution():

	with open("mood_saver.json", "r") as jsonFile:
		jsonData = json.load(jsonFile)

	happy = float(jsonData["HAPPY"])
	sad = float(jsonData["SAD"])
	neutral = float(jsonData["NEUTRAL"])

	print "happy: " + str(happy) + ", sad: " + str(sad) + ", neutral: " + str(neutral)
	happy_freq = (happy / (happy + sad + neutral))*100
	sad_freq = (sad / (happy + sad + neutral))*100
	neutral_freq = (neutral / (happy + sad + neutral))*100	
	return str(round(happy_freq, 2)), str(round(sad_freq, 2)), str(round(neutral_freq, 2))

def reset():

	with open("mood_saver.json", "r") as jsonFile:
		jsonData = json.load(jsonFile)

	jsonData["HAPPY"] = 0
	jsonData["SAD"] = 0
	jsonData["NEUTRAL"] = 0

	with open("mood_saver.json", "w") as jsonFile:
		json.dump(jsonData, jsonFile)
	return 0



######################################################################
# TEST
######################################################################

m, l = get_moood_loc()
print m + " @ " + l
h, s, n = mood_freq_distribution()
print "h: " + h + "%, s: " + s + "%, n: " + n + "%"
proximityies = happy_proximity(46.987654, 21.123456)
print "proximityies: " + str(proximityies)
#reset()