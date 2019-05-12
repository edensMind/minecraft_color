from flask import Flask
from flask import render_template
from flask import request, session, redirect, url_for

app = Flask(__name__)


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
		logError("DB Connection",error)
		return "CONN_ERROR"

# APP ######################################################################
@app.route("/")
def hello():
	title = "Minecraft Color"

	coll = dbConnect()

	logError("DEBUG DB Connected?",str(coll))

	return render_template('index.html',
		title=title
	)


# END ######################################################################
if __name__ == "__main__":
    app.run()