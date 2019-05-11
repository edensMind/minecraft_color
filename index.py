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
import pymongo
import sqlite3
def dbConnect():
	try:
		database = 'example.db'
		conn = sqlite3.connect(database)
		return conn
	except Exception as error:
		logError("DB Connection",error)
		return "CONN_ERROR"

# APP ######################################################################
@app.route("/")
def hello():
	title = "Flask App"
	return render_template('index.html',
		title=title
	)




# END ######################################################################
if __name__ == "__main__":
    app.run()