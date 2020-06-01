<?php

/** vignette1Record.php
 * This module records the Vignette 1 answer and the amount of time to complete 
 * Vignette 1 in mysql database.
 */ 

/* Enter Vignette 1 Response, Vignette 1 Start time and Vingette 1 Time Duration into an Array 
 * Pass array to sql UPDATE function to update sql table */

//Record Vignette 1 response
$vignette1Answer = checkans($_POST['vignetteans']);

if($_POST['vignettetrigger'] == 1){
	$vignette1Array['Vignette1Answer'] = $vignette1Answer;
}
else
{
	$vignette1Array['Vignette1Answer'] = -1;
}
 
//Record Vignette 1 start time
$vignette1Array['Vignette1LoadTime'] = $_POST['vignette1_startTime'];  

//Compute and record Vignette 1 time duration 
$vignette2_startTime = date('h:i:s a', time()); // get start time of Vignette 2 (page 3) 
$vignette1Array['V1TimeLength'] = computeTimeDuration($_POST['vignette1_startTime'], $vignette2_startTime); 


//Update mysql table with Vignette 1 response, start time, and time duration 
sqlRowUpdate('USA_responses_2017', $vignette1Array, $_POST['ID']);
 


?>
