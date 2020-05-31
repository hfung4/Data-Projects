#!/usr/bin/python

import mysql.connector
import sys

def main():
  dbConnect = mysql.connector.connect(user="henryfung", password="mtuarsftqq", database="vignettes_live", charset='utf8')
  # cursor to execute queries
  cur = dbConnect.cursor()
  # select variables used to check whether the user was careful in their survey-taking
  selectQuery = "SELECT Job, Job1, ContrIncome, Houseanswer, V1TimeLength, V2TimeLength, V3TimeLength, V4TimeLength, V5TimeLength, NumberHealthOld, NumberMarOld, Healthop1, Healthop2, Healthop3, Healthop4, Healthop5, Maritalop1, Maritalop2, Maritalop3, Maritalop4, Maritalop5, Leisureop1, Leisureop2, Leisureop3, Leisureop4, Leisureop5, Leisureop6, Leisureop7, Leisureop8, Age1, Age2 FROM answers_india_dev WHERE ID="+str(userID)
  cur.execute(selectQuery)
  row = cur.fetchone()
  
  # difference in answer to job satisfaction question -- to test consistency
  if row[0] != '' and row[1] != '':
    jobDiff = float(row[0]) - float(row[1])
  else:
    # set job consistency to failing number
    jobDiff = -5
  
  # number of people who contribute to household
  contrinc = row[2]
  
  # number of people living in household
  household = row[3]
  
  # time taken for each vignette
  v1time = row[4]
  v2time = row[5]
  v3time = row[6]
  v4time = row[7]
  v5time = row[8]
  
  # variables for checking comprehension questions
  #numhealtholdvig = row[9]
  #nummaroldvig = row[10]
  # NOTE: Healthop5 and Maritalop5 (row[15] and row[20]) are both now obsolete. Only the first four options are used in survey
  healthTuple = row[11], row[12], row[13], row[14] #row[15]
  marTuple = row[16], row[17], row[18], row[19]  #row[20]
  leisureTuple = row[21], row[22], row[23], row[24], row[25], row[26], row[27], row[28]
  
  #reported age and reported age category
  if row[29] != '':
    age = int(row[29])
  else:
     age = -1
  if row[30] != '':
    agecat = int(row[30])
  else:
    agecat = -1

  # Check comprehension questions
  if healthOrMaritalQs == '0': #health questions
    errorhealth = 0
    errormar = 0
    answerCount = 0
    for answer in healthTuple:
      if answer == "on":
        answerCount += 1
    if answerCount != 1:
      errorhealth = 4
    else:
      if healthTuple[0] == "on":
        errorhealth += 1
      if healthTuple[1] == "on":
        errorhealth += 1
      if healthTuple[2] == "on":
        errorhealth += 1
      if healthTuple[3] == None:
        errorhealth += 1
  elif healthOrMaritalQs == '1': #marital questions
    errorhealth = 0
    errormar = 0
    answerCount = 0
    for answer in marTuple:
      if answer == "on":
        answerCount += 1
    if answerCount != 1:
      errormar = 4
    else:
      if marTuple[0] == "on":
        errormar += 1
      if marTuple[1] == "on":
        errormar += 1
      if marTuple[2] == "on":
        errormar += 1
      if marTuple[3] == None:
        errormar += 1

  # Other attribute question
  errorleisure = 0
  if leisureTuple[0] == "on":
    errorleisure += 1
  if leisureTuple[1] == "on":
    errorleisure += 1
  if leisureTuple[2] == None:
    errorleisure += 1
  if leisureTuple[3] == None:
    errorleisure += 1
  if leisureTuple[4] == "on":
    errorleisure += 1
  if leisureTuple[5] == None:
    errorleisure += 1
  if leisureTuple[6] == None:
    errorleisure += 1
  if leisureTuple[7] == "on":
    errorleisure += 1
  

  # Total error on comprehension questions:
  totalCompError = errorhealth + errormar + errorleisure

  # Check if age matches reported age category
  if age < 20 and agecat == 0:
    ageTest = 0
  elif 20 <= age <= 30 and agecat == 1:
    ageTest = 0
  elif 31 <= age <= 40 and agecat == 2:
    ageTest = 0
  elif 41 <= age <= 50 and agecat == 3:
    ageTest = 0
  elif 51 <= age <= 60 and agecat == 4:
    ageTest = 0
  elif 61 <= age <= 70 and agecat == 5:
    ageTest = 0
  elif age >= 71 and agecat == 6:
    ageTest = 0
  else:
    ageTest = 1

  # check amount of time spent on vignettes
  timeTuple = int(v1time), int(v2time), int(v3time), int(v4time), int(v5time)
  badTime = 0
  for num in range(5):
    if timeTuple[num] < 15:
      badTime = badTime + 1
 
  # make sure num of people in household is >= num of people who provide
  if contrinc != '':
    contrinc = int(contrinc)
  else:
    contrinc = 100 #failing number if nothing submitted
  
  if household != '':
    household = int(household)
  else:
    household = 0 #failing number if nothing submitted

  failIncHouse = 0
  if contrinc > household:
    failIncHouse = 1


  # now give them a grade and give remarks based on what they did poorly
  remarks = ""
  score = 0
  if jobDiff != 0:
    if abs(jobDiff) > 2:
      remarks = remarks + "Subject varied a lot in reports of their own job satisfaction."
      score = score + 2
    else:
      remarks = remarks + "Subject was a little inconsistent in reports of their own job satisfaction."
      score = score + 1
  if ageTest == 1:
    score = score + 2
    remarks = remarks + " Subject failed the age test."
  if badTime > 0: 
    score = score + badTime
    remarks = remarks + " Subject rushed at least one vignette."
  if failIncHouse == 1:
    score = score + 2
    remarks = remarks + " Subject failed the providers vs household population test."
  if totalCompError > 0:
    score = score + totalCompError
    if totalCompError > 2:
      remarks = remarks + " Subject did poorly on the comprehension questions."
    else:
      remarks = remarks + " Subject missed 1-2 comprehension questions."

  # SCORE BREAKDOWN:
  # Higher scores = worse grades
  # Job satisfaction test: 2 points added if very inconsistent, 1 if only a little
  # Age test: 2 points added if failed
  # Vignette time test: 1 point added for each rushed vignette
  # Income contributors test: 2 points added if subject reported more people providing than there are in the household
  # Comprehension questions: 1 point for each incorrect answer (be it a missed checkbox or an incorrectly checked box)

  # put remarks in single quotes for SQL
  remarks = "'" + remarks + "'"

  # set remarks to perfect if score still == 0
  if score == 0:
    remarks = "Perfect!"

  #print remarks

  scoreString = "UPDATE answers_india_dev SET Score=%d, Remarks=%s WHERE ID=%s" % (score, remarks, userID)
  #print scoreString
  cur.execute(scoreString)
  dbConnect.commit()
  
  cur.close()
  dbConnect.close()
  

if __name__ == "__main__":
  # check arguments
  if len(sys.argv) <= 2:
    print "Error: not enough arguments passed."
  userID = sys.argv[1]
  healthOrMaritalQs = sys.argv[2]
  main()



