from flask import Flask
from flask import render_template
from flask import request, session, redirect, url_for

app = Flask(__name__)

# import tools
import csv
import json
import re

# Set Project Root directory
import os
project_root = os.path.dirname(__file__)

# Define template and static folders for flask app
template_path = os.path.join(project_root, './templates')
static_path = os.path.join(project_root, './static')

# LOGGING ##################################################################
from logError import logError

# DATABASE ##################################################################
from pymongo import MongoClient

def dbConnect():
	try:
		address = 'localhost'
		db_name = 'minecraftColor'
		coll_name = 'drawings'

		client = MongoClient(address, 27017)
		db = client[db_name]
		coll = db[coll_name]

		return coll

		#insert: coll.insert_one(document).inserted_id
		#find: coll.find_one()  or,  for doc in coll.find():

	except Exception as error:
		logError("ERROR DB Connection",error)
		return "CONN_ERROR"


# GET CSV DATA ##################################################################
def getCSVData():
	try:
		csv_data = []
		with open('map_colors.csv',encoding='utf-8-sig') as csv_file:
			csv_reader = csv.reader(csv_file)
			for row in csv_reader:
				csv_data.append(row)
			
		return csv_data
	except Exception as error:
		logError("ERROR Read CSV",error)
		return "CSV_ERROR"


# APP ######################################################################
@app.route("/")
def hello():

	title = "Minecraft Color"

	# GET MAP COLORS ######################################################################
	# color holders
	GREENS = []
	YELLOWS = []
	GRAYSCALE = []
	REDS = []
	BLUES = []
	BROWNS = []
	ORANGES = []
	PURPLES = []
	PINKS = []

	csv_reader = getCSVData()
	for row in csv_reader:
		# logError("DEBUG CSV 2 ",row[3])
		if row[0] == "GREENS":
			GREENS.append([row[1], row[2]]);
		elif row[0] == "YELLOWS":
			YELLOWS.append([row[1], row[2]]);
		elif row[0] == "GRAYSCALE":
			GRAYSCALE.append([row[1], row[2]]);
		elif row[0] == "REDS":
			REDS.append([row[1], row[2]]);
		elif row[0] == "BLUES":
			BLUES.append([row[1], row[2]]);
		elif row[0] == "BROWNS":
			BROWNS.append([row[1], row[2]]);
		elif row[0] == "ORANGES":
			ORANGES.append([row[1], row[2]]);
		elif row[0] == "PURPLES":
			PURPLES.append([row[1], row[2]]);
		elif row[0] == "PINKS":
			PINKS.append([row[1], row[2]]);


	#logError("DEBUG CSV 1 ",GREENS)
	# coll = dbConnect()
	# logError("DEBUG DB Connected?",str(coll))

	return render_template('index.html',
		title=title,
		GREENS = GREENS,
		YELLOWS = YELLOWS,
		GRAYSCALE = GRAYSCALE,
		REDS = REDS,
		BLUES = BLUES,
		BROWNS = BROWNS,
		ORANGES = ORANGES,
		PURPLES = PURPLES,
		PINKS = PINKS
	)


# getBlock csv ref ######################################################################
def getBlock(rgb):
	# logError("DEBUG getBlock 3",len(csv_global_data))
	if rgb == "" or rgb == "transparent":
		return "NONE"
	else:
		csv_reader = getCSVData()
		for row in csv_reader:
			# logError("DEBUG getBlock 1",rgb)
			# logError("DEBUG getBlock 2",row)
			if row[2] in rgb:
				return row[3]




# get x, y from id ######################################################################
def getXY(cell_id):
	xy = re.match(r"x(?P<int>\d+)y(\d*)", cell_id)
	return [xy.group(1), xy.group(2)]



# APP ######################################################################
@app.route("/ahk", methods=['GET','POST'])
def ahk():
	jsonDataString = request.form.get('drawingDocJSON')

	# start AHK script
	message = ";;; Making pixel art...\n"
	ahk = message
	ahk += "^r::\n"


	try:
		#Get JSON DATA
		jsonDataObj = json.loads(jsonDataString)
		lastitem = list(jsonDataObj.items())[-1]
		xy = getXY(lastitem[0])

		max_x = xy[0]
		max_y = xy[1]

		# total_cells = max_x*max_y

		#cell # counter
		num_cells = 0

		# for each row y
		for y in range(1,int(max_y)+1):
			#for each x in every row
			x = 1
			while x <= int(max_x):
				#Get JSON object for this cell
				this_cell = list(jsonDataObj.items())[num_cells]
				#Get the X and Y from this cell's ID
				this_cell_id = getXY(this_cell[0])

				# This cell's X, Y
				this_cell_x = this_cell_id[0]
				this_cell_y = this_cell_id[1]

				#make sure the ID xy matches loop xy - (make sure data is correct)
				if int(this_cell_y) == y and int(this_cell_x) == x:
					# Get this cell's block type
					this_cell_block = getBlock(this_cell[1])

					#process if next block in row is the same block (more efficient)
					next_x = 0
					while True:
						if x+1 >= int(max_x):
							break

						if this_cell_block == getBlock(list(jsonDataObj.items())[num_cells+1][1]):
							logError("DEBUG AHK 9","reached")
							next_x += 1
							num_cells += 1
							x += 1
						else:
							logError("DEBUG AHK 9","break")
							break

					# If block type is not empty...
					if this_cell_block != "NONE":
						#write out AHK place command
						ahk += """
							;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
							Send, /
							Sleep 250
							Send, fill ~"""+str(this_cell_x)+""" ~ ~"""+str(this_cell_y)+""" ~"""+str(int(this_cell_x)+next_x)+""" ~ ~"""+str(this_cell_y)+""" minecraft:"""+this_cell_block+"""
							Send, {Enter}\n
							"""
				else:
					logError("DEBUG AHK 8","MISSING ONE!")

				num_cells += 1
				x += 1


		try:
			# write to art_test.ahk
			file = "art_test"
			f = open(file+".ahk", "w")
			f.write(ahk)
			f.close()

		except Exception as error:
			logError("ERROR Write AHK: ",error)

	except Exception as error:
		logError("ERROR Create JSON: ",error)

	return "ok"




# END ######################################################################
if __name__ == "__main__":
    app.run()