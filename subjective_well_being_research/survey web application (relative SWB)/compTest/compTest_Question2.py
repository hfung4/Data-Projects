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
	Q2FalseRaw = Series(["Hours of volunteer work per week", "Number of promotions at work in the past three years", "Number of vacations per year", "Number of layoffs in the workplace in the past 12 months" ], index=['Attr_F1', 'Attr_F2', 'Attr_F3', 'Attr_F4']);
	
	Q2TrueRaw = Series(["Income", "Hours Worked", "Reported trust in the community", "Body Mass Index (BMI)", "Number of close friends", "Frequency of seeing friends", "Unemployment rate", "Living with a partner"], index=['Attr_T1', 'Attr_T2', 'Attr_T3', 'Attr_T4', 'Attr_T5', 'Attr_T6', 'Attr_T7', 'Attr_T8']) 
	
	#Shuffle correct ans array
	Q2TrueShuffled = Q2TrueRaw.reindex(np.random.permutation(Q2TrueRaw.index)) 
	
	#Truncate the first 4 elements from the array
	Q2_TrueTrun = Q2TrueShuffled.drop(Q2TrueShuffled.index[[0, 1, 2, 3]])
	
	#Combine array with correct ans, and array with incorrect ans 
	Q2Raw = Q2FalseRaw.append(Q2_TrueTrun)
	
	#Shuffle the array
	Q2_P = Q2Raw.reindex(np.random.permutation(Q2Raw.index))
	
	#convert to dictionary
	Q2_dict = Q2_P.to_dict()
	
	#In Question 2:  There will be 4 incorrect answer choices, and 4 correct choices
	print json.dumps(Q2_dict)
    

   
    
if __name__=="__main__":
	main()
