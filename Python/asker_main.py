#!/usr/bin/python3


# MAIN
# transactionsFile: a csv of transactions
# [1] categoriesFile: a .json of keywords and categories
# [2][opt .json] outfile: where the result is written to
# [3+] csv, dir, or multiple csvs

from asker import *
from pprint import pprint

[transactionsFiles, categoriesFile, outfile] = argCheck()


fileStatus = checkFiles(transactionsFile, categoriesFile)

if (fileStatus != "success"):
	import sys
	sys.exit(fileStatus)


# list of tuples: (cat, price)
result = []

# read in the categories
# keys: keywords, values: categories
catDict = categoriesReader(categoriesFile)

# gets set of categories
catSet =  getCatSet(catDict)

with open(transactionsFile) as f:
	for line in f:
		
		price = priceFromLine(line)

		if (price < 0):
			continue

		# if a key is found, key is returned (otherwise False)
		key = searchForKeys(line, catDict)
		
		if key:

			result.append((catDict[key], price))

		# otherwise, interact
		else:

			[retCategory, retKey] = friend(line, catSet)
			
			# all cases make a new result line
			result.append((retCategory, price))

			# if we get a nonFalse key, add it to the dict
			if retKey:
				catDict[retKey] = retCategory

			# if we get a new category, add it to the set	
			if ((retCategory not in catSet) and (retCategory != "")):
				catSet.append(retCategory)

# now save the categories file
categoriesWriter(categoriesFile, catDict)		

# aggregate the results and print to outfile
addTotals(result, outfile)