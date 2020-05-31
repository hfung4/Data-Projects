<?php

/** compTestRecord.php
 * This module records the compTest answer and the amount of time to complete 
 * the comprehension test in mysql database.
 */ 


/* Enter Comprehension Test Response, Comprehension Test Start time and Time Duration into an Array 
 * Pass array to sql UPDATE function to update sql table */

/*Record Comp test response
 */ 



//Health (Q1)

if($_POST['Health_t1'] ==1)
{
	$compTestArray['Health_t1'] = $_POST['Health_t1'];
	
}

if($_POST['Health_t2']==1)
{
	$compTestArray['Health_t2'] = $_POST['Health_t2'];
	
}

if($_POST['Health_f1']==1)
{
	$compTestArray['Health_f1'] = $_POST['Health_f1'];
	
}

if($_POST['Health_f2']==1)
{
	$compTestArray['Health_f2'] = $_POST['Health_f2'];
	
}

if($_POST['Health_f3']==1)
{
	$compTestArray['Health_f3'] = $_POST['Health_f3'];
	
}



//Social (Q1)


if($_POST['Soc_t1']==1)
{
	$compTestArray['Soc_t1'] = $_POST['Soc_t1'];
	
}

if($_POST['Soc_t2']==1)
{
	$compTestArray['Soc_t2'] = $_POST['Soc_t2'];
	
}

if($_POST['Soc_f1']==1)
{
	$compTestArray['Soc_f1'] = $_POST['Soc_f1'];
	
}

if($_POST['Soc_f2']==1)
{
	$compTestArray['Soc_f2'] = $_POST['Soc_f2'];
	
}

if($_POST['Soc_f3']==1)
{
	$compTestArray['Soc_f3'] = $_POST['Soc_f3'];
	
}


if($_POST['Attr_T1']==1)
{
	$compTestArray['Attr_T1'] = $_POST['Attr_T1'];
}

if($_POST['Attr_T2']==1)
{
	$compTestArray['Attr_T2'] = $_POST['Attr_T2'];
}

if($_POST['Attr_T3']==1)
{
	$compTestArray['Attr_T3'] = $_POST['Attr_T3'];
}

if($_POST['Attr_T4']==1)
{
	$compTestArray['Attr_T4'] = $_POST['Attr_T4'];
}

if($_POST['Attr_T5']==1)
{
	$compTestArray['Attr_T5'] = $_POST['Attr_T5'];
}

if($_POST['Attr_T6']==1)
{
	$compTestArray['Attr_T6'] = $_POST['Attr_T6'];
}

if($_POST['Attr_T7'] ==1)
{
	$compTestArray['Attr_T7'] = $_POST['Attr_T7'];
}

if($_POST['Attr_T8'] ==1)
{
	$compTestArray['Attr_T8'] = $_POST['Attr_T8'];
}


if($_POST['Attr_F1'] ==1)
{
	$compTestArray['Attr_F1'] = $_POST['Attr_F1'];
}

if($_POST['Attr_F2'] ==1)
{
	$compTestArray['Attr_F2'] = $_POST['Attr_F2'];
}


if($_POST['Attr_F3'] ==1)
{
	$compTestArray['Attr_F3'] = $_POST['Attr_F3'];
}

if($_POST['Attr_F4'] ==1)
{
	$compTestArray['Attr_F4'] = $_POST['Attr_F4'];
}



//Record Comp Test start time
$compTestArray['CompTimeLoad'] = $_POST['compTest_startTime'];  


//Compute and record Comprehension Test time duration 
$demographics_startTime = date('h:i:s a', time()); // get start time of Demographics Survey (page 8) 
$compTestArray['CompTimeTotal'] = computeTimeDuration($_POST['compTest_startTime'], $demographics_startTime);


//update mysql row
sqlRowUpdate('USA_responses_2017', $compTestArray, $_POST['ID']);
 




?>
