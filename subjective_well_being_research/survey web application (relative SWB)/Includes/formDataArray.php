<?php

/** formDataArray.php
 *
 * This module contains an assoicative array $formDataArray. 
 * The keys of each element in the array corresponds to the column name of the 
 * data in the mysql table vignettes_live.USA_responses_2017
 * With the array formatted in this manner, we can use a php function
 * array_keys() to retrieve the field columns to be used to append data 
 * and construct the query variable.
 */


//Init the  associative array "formDataArray" 

$formDataArray = array(
'ID' => 0
);

//Welcome Page
$formDataArray['ID'] = 0;
$formDataArray['IPADDRESS1'] = 0;
$formDataArray['TimeWelcome'] = 0;
$formDataArray['Language'] = 0;

//Self Report Life Satisfaction

$formDataArray['Overall_LS'] = 0;
$formDataArray['Health_LS'] = 0;
$formDataArray['Income_LS'] = 0;
$formDataArray['Job_LS'] = 0;
$formDataArray['Social_LS'] = 0;
$formDataArray['SelfReportTimeLoad'] = 0;
$formDataArray['SelfTotalTime'] = 0;

//Vignette 1 Response
$formDataArray['Vignette1Answer']  = -1;
$formDataArray['V1TimeLength'] = 0;
$formDataArray['Vignette1LoadTime'] = 0;

//Vignette 2 Response
$formDataArray['Vignette2Answer']  = -1;
$formDataArray['V2TimeLength'] = 0;
$formDataArray['Vignette2LoadTime'] = 0;

//Vignette 3 Response
$formDataArray['Vignette3Answer']  = -1;
$formDataArray['V3TimeLength'] = 0;
$formDataArray['Vignette3LoadTime'] = 0;

//Vignette 4 Response
$formDataArray['Vignette4Answer']  = -1;
$formDataArray['V4TimeLength'] = 0;
$formDataArray['Vignette4LoadTime'] = 0;

//Vignette 5 Response
$formDataArray['Vignette5Answer']  = -1;
$formDataArray['V5TimeLength'] = 0;
$formDataArray['Vignette5LoadTime'] = 0;


//Vignette 1 Relative Buttons Pressed
$formDataArray['relIncomeBt1'] = 0;
$formDataArray['relWorkBt1'] = 0;
$formDataArray['relUnemployBt1'] = 0;
$formDataArray['relCommunityBt1'] = 0;
$formDataArray['relExerciseBt1'] = 0;
$formDataArray['relPainBt1'] = 0;
$formDataArray['relBMIBt1'] = 0;
$formDataArray['relNumFrdBt1'] = 0;
$formDataArray['relFreqFrdBt1'] = 0;
$formDataArray['relPartnerBt1'] = 0;
$formDataArray['relTrustBt1'] = 0;
$formDataArray['PreviousVigBt1'] = 0;


//Vignette 2 Relative Buttons Pressed
$formDataArray['relIncomeBt2'] = 0;
$formDataArray['relWorkBt2'] = 0;
$formDataArray['relUnemployBt2'] = 0;
$formDataArray['relCommunityBt2'] = 0;
$formDataArray['relExerciseBt2'] = 0;
$formDataArray['relPainBt2'] = 0;
$formDataArray['relBMIBt2'] = 0;
$formDataArray['relNumFrdBt2'] = 0;
$formDataArray['relFreqFrdBt2'] = 0;
$formDataArray['relPartnerBt2'] = 0;
$formDataArray['relTrustBt2'] = 0;
$formDataArray['PreviousVigBt2'] = 0;


//Vignette 3 Relative Buttons Pressed
$formDataArray['relIncomeBt3'] = 0;
$formDataArray['relWorkBt3'] = 0;
$formDataArray['relUnemployBt3'] = 0;
$formDataArray['relCommunityBt3'] = 0;
$formDataArray['relExerciseBt3'] = 0;
$formDataArray['relPainBt3'] = 0;
$formDataArray['relBMIBt3'] = 0;
$formDataArray['relNumFrdBt3'] = 0;
$formDataArray['relFreqFrdBt3'] = 0;
$formDataArray['relPartnerBt3'] = 0;
$formDataArray['relTrustBt3'] = 0;
$formDataArray['PreviousVigBt3'] = 0;

//Vignette 4 Relative Buttons Pressed
$formDataArray['relIncomeBt4'] = 0;
$formDataArray['relWorkBt4'] = 0;
$formDataArray['relUnemployBt4'] = 0;
$formDataArray['relCommunityBt4'] = 0;
$formDataArray['relExerciseBt4'] = 0;
$formDataArray['relPainBt4'] = 0;
$formDataArray['relBMIBt4'] = 0;
$formDataArray['relNumFrdBt4'] = 0;
$formDataArray['relFreqFrdBt4'] = 0;
$formDataArray['relPartnerBt4'] = 0;
$formDataArray['relTrustBt4'] = 0;
$formDataArray['PreviousVigBt4'] = 0;

//Vignette 5 Relative Buttons Pressed
$formDataArray['relIncomeBt5'] = 0;
$formDataArray['relWorkBt5'] = 0;
$formDataArray['relUnemployBt5'] = 0;
$formDataArray['relCommunityBt5'] = 0;
$formDataArray['relExerciseBt5'] = 0;
$formDataArray['relPainBt5'] = 0;
$formDataArray['relBMIBt5'] = 0;
$formDataArray['relNumFrdBt5'] = 0;
$formDataArray['relFreqFrdBt5'] = 0;
$formDataArray['relPartnerBt5'] = 0;
$formDataArray['relTrustBt5'] = 0;
$formDataArray['PreviousVigBt5'] = 0;


//Comprehension Test
$formDataArray['CompTimeTotal'] = 0;
$formDataArray['CompTimeLoad'] = 0;
$formDataArray['SocialTestSelected'] = 0;  //0 is Health Test Selected, 1 is Social Test selected
$formDataArray['visitedComp'] = 0; //visited Comp page flag


//Comprehension Health/Social Test response (Q1)
// t1 or t2 are the "correct" selections in the test, 
//f1...f3 are the incorrect selections in the test

$formDataArray['Health_t1'] = 0;
$formDataArray['Health_t2'] = 0;
$formDataArray['Health_f1'] = 0;
$formDataArray['Health_f2'] = 0;
$formDataArray['Health_f3'] = 0;
$formDataArray['Soc_t1'] = 0;
$formDataArray['Soc_t2'] = 0;
$formDataArray['Soc_f1'] = 0;
$formDataArray['Soc_f2'] = 0;
$formDataArray['Soc_f3'] = 0;

//Comprehension Attribute test response (Q2)
$formDataArray['Attr_T1'] = 0;
$formDataArray['Attr_T2'] = 0;
$formDataArray['Attr_T3'] = 0;
$formDataArray['Attr_T4'] = 0;
$formDataArray['Attr_T5'] = 0;
$formDataArray['Attr_T6'] = 0;
$formDataArray['Attr_T7'] = 0;
$formDataArray['Attr_T8'] = 0;
$formDataArray['Attr_F1'] = 0;
$formDataArray['Attr_F2'] = 0;
$formDataArray['Attr_F3'] = 0;
$formDataArray['Attr_F4'] = 0;

//Demographics
$formDataArray['DemTimeTotal'] = 0;
$formDataArray['DemTimeLoad'] = 0;

$formDataArray['Age1'] = 0;  //Age was asked several time
$formDataArray['Gender'] = 0;
$formDataArray['Education'] = 0;  //Highest level of education
$formDataArray['Dmarried_demographics'] = 0;  //Married in the demographics
$formDataArray['Dseparated'] = 0;  //Divorced or Widowed
$formDataArray['Employ'] = 0;  //Currently employed?
$formDataArray['IndIncomeNumInput'] = 0;  //Individual income numerical input
$formDataArray['IndIncome'] = 0;
$formDataArray['HHIncomeNumInput'] = 0; // Household income numerical input
$formDataArray['HHIncome'] = 0;
$formDataArray['NumFamContributeIncome'] = 0; //Number of members in the household who contribute to Household income
$formDataArray['NumFamHousehold'] = 0; //Number of people in the household
$formDataArray['Age2'] = 0; //What is your age (again)?
$formDataArray['Country1'] = 0; //What country did you live in?
$formDataArray['Country2'] = 0;
$formDataArray['Country3'] = 0;
$formDataArray['Country4'] = 0;
$formDataArray['Country5'] = 0;
$formDataArray['State'] = 0;  //What state do you live in?
$formDataArray['Code'] = 0;  //final Mturk code 
$formDataArray['Comments'] = 0; //Let us know if you have any comments
$formDataArray['IPADDRESS_END'] = 0; //ipaddress recorded at the end of the survey
$formDataArray['browser'] = 0; //browser type recorded at the end of the survey


//Exit Page
$formDataArray['ExitTimeLoad'] = 0;
$formDataArray['TotalTime'] = 0;

//Misc
$formDataArray['ACCEPT'] = 0;  //Survey response accepted
$formDataArray['REJECT'] = 0;  //Survey response rejected
$formDataArray['BONUS'] = 0;  //Whether the respondent received bonus
$formDataArray['Score'] = 0;  //For QC purposes, score that the respondent received, a high score indicates a high qual response

//Additional parameters
//$formDataArray['blahblah'] = 0;















