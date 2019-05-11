import datetime

def logError(errorType, errorMessage):
	# Set log Filename
	filename = "log/errorLog.log"

	# Open log file for appending
	logfile = open(filename,"a+")

	# Get current Time
	now = datetime.datetime.now()
	formattedTime = now.strftime("%Y-%m-%d %H:%M:%S")

	fullMessage = (formattedTime +" : "+ errorType + " - " + str(errorMessage) + "\n\r")

	# log error message
	logfile.write(fullMessage)

	# close file
	logfile.close()