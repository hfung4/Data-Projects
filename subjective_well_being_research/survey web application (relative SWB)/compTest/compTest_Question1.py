#!/usr/bin/python

#Importing packages we need
import random  
import sys
import json

# standard
import numpy as np
import pandas as pd
from pandas import Series, DataFrame


def main():
	
	if healthOrSocial == "0":
		healthQ1Raw = Series(["Pain or discomfort", "Amount of physical exercise per day", "Amount of fruits and vegetables consumed per day", "Number of chronic diseases such as diabetes and asthma", "Depression or anxiety"], index=['Health_t1', 'Health_t2', 'Health_f1', 'Health_f2', 'Health_f3'])
	
		healthQ1Shuffled = healthQ1Raw.reindex(np.random.permutation(healthQ1Raw.index))
	  
		healthDict = healthQ1Shuffled.to_dict()
		
		print json.dumps(healthDict)
		
	else:
		
		socQ1Raw = Series(["Frequency of seeing friends", "Number of organizations involved in, in the past 12 months", "Number of conflicts with family", "Time spent on social media per day", "Number of close relatives"], index=['Soc_t1', 'Soc_t2', 'Soc_f1', 'Soc_f2', 'Soc_f3'])  
		
		socQ1Shuffled = socQ1Raw.reindex(np.random.permutation(socQ1Raw.index))
		
		socDict = socQ1Shuffled.to_dict()
		
		#In Question 1, there will be 2 correct answer choices, and 3 incorrect choices
		print json.dumps(socDict)
	
  
    
if __name__=="__main__":
	healthOrSocial = sys.argv[1]
	main()
