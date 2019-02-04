from flask import Flask, request
from flask_restful import Api, Resource, reqparse
import json
from device.device_functions import get_mood, get_location, get_loc_position
from decimal import Decimal
from geopy.distance import geodesic


print "MOOD SENSE RESTFUL API"


app = Flask(__name__)
api = Api(app)

class Mood_Locaction(Resource):
	def get(self):
		# http://127.0.0.1:5002/mood_location
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

		return {mood : location}


	def put(self):
		
		location_dict = request.get_json()
		location = location_dict["loc"]
		print "PUT f-tion location: " + location
		with open("mood_saver.json", "r") as jsonFile:
			jsonData = json.load(jsonFile)

		happy_locations = jsonData["HAPPY_LOCATIONS"]
		if location not in happy_locations:
			happy_locations.append(location)
			print "happy_locations now: " + str(happy_locations)
			jsonData["HAPPY_LOCATIONS"] = happy_locations
		else:
			print location + " already in happy_locations"

		with open("mood_saver.json", "w") as jsonFile:
			json.dump(jsonData, jsonFile)

		return {"all locations now" : str(happy_locations)}

	
	def delete(self):

		with open("mood_saver.json", "r") as jsonFile:
			jsonData = json.load(jsonFile)

		jsonData["HAPPY"] = 0
		jsonData["SAD"] = 0
		jsonData["NEUTRAL"] = 0

		with open("mood_saver.json", "w") as jsonFile:
			json.dump(jsonData, jsonFile)
	
		return 0



class Happy_Proximity(Resource):
	def get(self, lon, lat):
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

class Mood_Freq_Distribution(Resource):
	def get(self):
		with open("mood_saver.json", "r") as jsonFile:
			jsonData = json.load(jsonFile)

		happy = float(jsonData["HAPPY"])
		sad = float(jsonData["SAD"])
		neutral = float(jsonData["NEUTRAL"])

		print "happy: " + str(happy) + ", sad: " + str(sad) + ", neutral: " + str(neutral)
		happy_freq = (happy / (happy + sad + neutral))*100
		sad_freq = (sad / (happy + sad + neutral))*100
		neutral_freq = (neutral / (happy + sad + neutral))*100


		return {"happy_freq" : str(round(happy_freq, 2)), "sad_freq" : str(round(sad_freq, 2)), "neutral_freq" : str(round(neutral_freq, 2))}




api.add_resource(Mood_Locaction, '/')
api.add_resource(Happy_Proximity, '/happy_proximity/<float:lon>/<float:lat>')
api.add_resource(Mood_Freq_Distribution, '/mood_freq_distribution')
#api.add_resource(Mood_Statistics, '/mood_statistics/<float:lon>/<float:lat>')
#api.add_resource(Employees_Param, '/employees/<num>')

if __name__ == '__main__':
     app.run(port='5002')

