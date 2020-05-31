<?php

/** vignette2Record.php
 * This module records the Vignette 2 answer and the amount of time to complete 
 * Vignette 2 in mysql database.
 */ 

/* Enter Vignette 2 Response, Vignette 2 Start time and Vingette 2 Time Duration into an Array 
 * Pass array to sql UPDATE function to update sql table */

//Record Vignette 2 response
$vignette2Answer = checkans($_POST['vignetteans']);

if($_POST['vignettetrigger'] == 1){
	$vignette2Array['Vignette2Answer'] = $vignette2Answer;
}
else
{
	$vignette2Array['Vignette2Answer'] = -1;
}


//Record Vignette 2 start time
$vignette2Array['Vignette2LoadTime'] = $_POST['vignette2_startTime'];  

//Compute and record Vignette 2 time duration 
$vignette3_startTime = date('h:i:s a', time()); // get start time of Vignette 3 (page 4) 
$vignette2Array['V2TimeLength'] = computeTimeDuration($_POST['vignette2_startTime'], $vignette3_startTime); 


//update mysql row
sqlRowUpdate('USA_responses_2017', $vignette2Array, $_POST['ID']);
 


?>

