
from asker import *

def test_checkArgs(): 
	# [1] categoriesFile: a .json of keywords and categories
	# [2] outfile: where the result is written to
	# [3+] csv, dir, or multiple csvs of transactions

	[transactionFiles, categoriesFile, outfile] = checkArgs()
	print("categoriesFile: ", categoriesFile)
	print("transactionFiles: ", transactionFiles)
	print("outfile: ", outfile)	

#---------------------------------#

def test_checkFiles():
	# test checkFiles by checking 3 sample dirs
	
	# cat.txt
	# trans.txt

	import os
	import pdb


	testDir1 = "/home/mario/Documents/Code/Accountant/Accountant/TestingData"
	os.chdir(testDir1)

	failure = "test_checkFiles failed, "
	status = "success"

	print("testing checkFiles")

	# bad files
	if (checkFiles("asdf.csv", "asdf/2.csv", "asdf3.json") == "success"):
		print("failed fake files")

	# good files
	if (checkFiles("Statement.csv", "Statement.csv", "asdf3.json") != "success"):
		print("failed correct single transaction file")
	# import pdb
	# pdb.set_trace()
	if (checkFiles(["Statement.csv", "Statement_pt2.csv"], "Statement.csv", "asdf3.json") != "success"):
		print("failed correct list transaction files")
		
 


#---------------------------------#

def test_priceFromLine():
	line1 = "\"2/28/2017\",\"\",\"ALAMO RENT-A-CAR         SPOKANE      WA\",\"195.46\",\"\""
	line2 = "\"2/22/2017\",\"\",\"ALASKA AIR  0272133977675SEATTLE      WA\",\"312.40\",\"\""

	status = "success"

	print("testing priceFromLine")

	print("testing normal cases...")	
	line1_result = priceFromLine(line1)
	line2_result = priceFromLine(line2)


	if ((line1_result == 195.46) and (line2_result == 312.40)):
		print("...passed!")		
	else:
		print("...failed!")
		status = "failure"

	line3 = "\"2/28/2017\",\"\",\"PAYMENT - THANK YOU\",\"\",\"-405.10\""

	print("testing payment case...")	
	if priceFromLine(line3) < 0:
		print("...passed!")		
	else: 
		print("...failed!")
		status = "failure"

	return status


#---------------------------------#

def test_searchForKeys():

	status = "success"
	line1 = "\"2/28/2017\",\"\",\"ALAMO RENT-A-CAR         SPOKANE      WA\",\"195.46\",\"\""
	line2 = "\"2/22/2017\",\"\",\"ALASKA AIR  0272133977675SEATTLE      WA\",\"312.40\",\"\""

	sampleDict = {'AIR':'Airfare', 'SAFEWAY': 'Groceries'}

	print("testing searchForKeys")

	
	print("testing key not found...")
	line1_result = searchForKeys(line1, sampleDict)

	if (line1_result == False):
		print("passed!")
	else: 
		print("failed!")
		status = "failure"

	print("testing key found...")
	line2_result = searchForKeys(line2, sampleDict)
	if (line2_result == "AIR"):
		print("passed!")
	else: 
		print("failed!")
		status = "failure"

#---------------------------------#

def test_catSet():
	status = "success"
	print("testing catSet...")
	sampleDict = {'AIR':'Airfare', 'SAFEWAY': 'Groceries', 'QFC': 'Groceries'}
	sampleDict_result = catSet(sampleDict)
	print(sampleDict_result)
	if sampleDict_result == ['Airfare', 'Groceries'] or ['Airfare', 'Groceries']:
		print("passed!")
	else:
		status = "failure"
		print("failed!")

#---------------------------------#

def test_friend():
	sampleDict = {'AIR':'Airfare', 'SAFEWAY': 'Groceries', 'QFC': 'Groceries'}
	sampleDict_result = getCatSet(sampleDict)

	print("ORIGINAL " + "'AIR':'Airfare', 'SAFEWAY': 'Groceries', 'QFC': 'Groceries'")
	
	line1 = "\"2/28/2017\",\"\",\"ALAMO RENT-A-CAR         SPOKANE      WA\",\"195.46\",\"\""
	line2 = "\"2/22/2017\",\"\",\"CARPET STORE  0272133977675SEATTLE      WA\",\"312.40\",\"\""

	[retCategory, retKey] = friend(line1, sampleDict_result)
	print("retCategory: "  + retCategory + " retKey: " +  retKey)

	[retCategory, retKey] = friend(line2, sampleDict_result)
	print("retCategory: "  + retCategory + " retKey: " +  retKey)

#---------------------------------#

def test_rw():

	testfile = "/home/mario/Documents/Code/BECU console/Testing Data/test.json"
	open(testfile, 'w+').close()

	# read empty
	testDict = categoriesReader(testfile)

	if (testDict == dict()):
		print("Empty case success")
	else:
		print("Empty case failure")
		return	

	# add stuff
	testDict['Safeway']='Groceries'

	# write nonempty
	categoriesWriter(testfile, testDict)

	# read nonempty
	testDict2 = categoriesReader(testfile)
	if(testDict2 == {'Safeway' : 'Groceries'}):
		print("write nonempty, read nonempty success")
	else:
		print("write nonempty, read nonempty failure")