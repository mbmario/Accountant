
def argCheck():
	# haven't figured out how to write a unit test for this one

	import sys

	if (len(sys.argv) < 3):     
		print("Please link a transaction CSV file and categories file")
		sys.exit(0)

	transactionFiles = str(sys.argv[1])
	categoriesFiles = str(sys.argv[2])

	if (len(sys.argv) == 4):     
		outfile = sys.argv[3]
	else:
		outfile = "./categories.json" 

	return [transactionFiles, categoriesFiles, outfile]

#---------------------------------#

def checkFiles(transactionFile, categoriesFile):
	# ensures that there are 2 existing files, and returns them or error
	# transactions file has to exist
	# will create a categories file if it doesn't exist

	import os
	import sys

	import pdb
	#pdb.set_trace()
	transactionFile = os.getcwd() + "/" + transactionFile
	categoriesFile = os.getcwd() + "/" + categoriesFile


	if not (os.path.isfile(transactionFile)):
		return("File not found")

	if not "csv" == transactionFile.split(".")[-1]:
		return("transactions must be .csv")

	
	if not (os.path.isfile(categoriesFile)):
		catStream = open(categoriesFile, 'w')

	return "success"

#---------------------------------#

def priceFromLine(line):

	# returns the 2nd to last item, if it is a number
	# otherwise, -1

	price = line.split(",")[-2].replace("\"", "")

	if price.replace(".","").isdigit():

		return float(price)
	
	return -1

#---------------------------------#

def searchForKeys(line, catDict):
	# iterates through the dictionary keys
	# if the key is found in the input line, breaks and returns that key 
	# otherwise return False

	desc = line.split(",")[2]

	for key in catDict.keys():
		if key in desc:
			return key

	return False


#---------------------------------#

def getCatSet(catDict):
	# returns a SET of unique categories, which are the values
	catSet = list(set(catDict.values()))
	#if not "<NO CATEGORY>" in catSet:
	#	catSet.insert(0,"<NO CATEGORY>")
	return catSet

#---------------------------------#

def friend(line, catSet):
	# given the line and existing categoires, interacts with user to
	# determine 
	# what category the item is in, or a new category
	# if there is a key
	# returns category (may be in set or new) and key (string or false)

	print("What category is this entry in? \n" + line)

	print("Enter the corresponding number, or the name of a new category, or nothing for no category:")

	#print("1: No category")
	#import pdb; pdb.set_trace()
	for i in range(0, len(catSet)):
		print (str(i + 1) + ": " + catSet[i])

	catAnswer = input()

	#if (catAnswer == "1"): #"1: No category"
	#	retCategory = "<NO CATEGORY>"
	if (catAnswer == ""):
		return ["", False]

	elif (catAnswer.isdigit()): # a selection
		retCategory = catSet[int(catAnswer) - 1]

	else: # new category
		retCategory = catAnswer

	validKey = False

	# ask until we get a valid key

	while not validKey:

		print("Is there is a key phrase in this line? If so, please type it and press Enter. If not, press Enter without typing anything.")

		keyAnswer = input()

		if ((keyAnswer == "") or (keyAnswer in line)):
			validKey = True
			break

		print("Key not found in line. Please try again.")
		
		from time import sleep
		sleep(1)

	return [retCategory, keyAnswer]

#---------------------------------#

def categoriesReader(categoriesFile):
	# reads the categories file and  and returns categories dictionary
	# if categoriesFile is empty, return an empty dictionary
	# if nonempty, return the read json object

	# catDict dictionary (str to str) object:
	#		keys are the keywords (i.e.QFC)
	#		values are category names (i.e. food)
	# if categoriesFile is empty, return an empty dictionary
	# if nonempty, return the read json object

	import os 
	import json


	#import pdb
	#pdb.set_trace()
	if os.stat(categoriesFile).st_size == 0:
		return dict()

	with open(categoriesFile, 'r') as f:
		catDict = json.load(f)

	return catDict
	

#---------------------------------#

def categoriesWriter(outfile, catDict):
	# saves categories dictionary as a json object

	import json

	with open(outfile, 'w') as f:
		json.dump(catDict, f)




	



