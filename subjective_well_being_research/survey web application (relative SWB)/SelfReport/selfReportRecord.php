<?php

/** selfReportRecord.php
 * 
 * Description:
 * 
 * This module contains script that extract data from the Self Report of Life Satisfication Survey
 * and update the corresponding columns in mysql table.  
 * 
 * The data collected from Self Report of Life Satisfication include:
 * 
 * 1) income: "How satisfied are you with the total income of your household?", 
 * 2) job: "How satisfied are you with your job and/or other daily activities?"
 * 3) job1: Repeated of the "job" question, used for consistency test.
 * 4) social: "How satisfied are you with your social contacts and family life?"
 * 5) health: "How satisfied are you with your overall health?"
 * 6) overall: "How satisified with your life overall?"
 * 
 * Please see dictionaries.php for more details
 */  




/* 
 * Assess the recorded user response from the Self Reported Life Satisification Survey from the super global array $_POST
 * Pass the responses (string data) through the "checkans" function to convert into an integer (range 1-10)
 * Compuete the time duration of the Self Reported Survey and query it to mysql.
 * 
 */ 

$vignette1_startTime = date('h:i:s a', time()); // get start time of Vignette 1 (page 2) 


//Create an array that contains Self Report survey responses that we will used to update mysql table
$selfReportArray['SelfReportTimeLoad'] = $_POST['selfReport_startTime'];  //time at the start of the survey
$selfReportArray['Overall_LS']  = checkans($_POST['overall'], TRUE);   //overall LS  
$selfReportArray['Health_LS']   = checkans($_POST['health'], TRUE);    //health statisfaction
$selfReportArray['Income_LS']   = checkans($_POST['income'], TRUE);    //income statisfaction
$selfReportArray['Job_LS']      = checkans($_POST['job'], TRUE);       //job statisfaction
$selfReportArray['Social_LS']   = checkans($_POST['social'], TRUE);    //social network statisfaction 
$selfReportArray['SelfTotalTime'] = computeTimeDuration($_POST['selfReport_startTime'], $vignette1_startTime); // time duration of the Self Report 


if(isSet($_POST['selfReportSubmit'])) //If new_welcome form is submitted
{
	//update mysql row
	sqlRowUpdate('USA_responses_2017', $selfReportArray, $_POST['ID']);
}



?>
