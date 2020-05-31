<?php

/** vignette4Record.php
 * This module records the Vignette 4 answer and the amount of time to complete 
 * Vignette 4 in mysql database.
 */ 

/* Enter Vignette 4 Response, Vignette 4 Start time and Vingette 4 Time Duration into an Array 
 * Pass array to sql UPDATE function to update sql table */

//Record Vignette 4 response
$vignette4Answer = checkans($_POST['vignetteans']);

if($_POST['vignettetrigger'] == 1){
	$vignette4Array['Vignette4Answer'] = $vignette4Answer;
}
else
{
	$vignette4Array['Vignette4Answer'] = -1;
}


//Record Vignette 4 start time
$vignette4Array['Vignette4LoadTime'] = $_POST['vignette4_startTime'];  


//Compute and record Vignette 4 time duration 
$vignette5_startTime = date('h:i:s a', time()); // get start time of Vignette 5 (page 6) 
$vignette4Array['V4TimeLength'] = computeTimeDuration($_POST['vignette4_startTime'], $vignette5_startTime);

//update mysql row
sqlRowUpdate('USA_responses_2017', $vignette4Array, $_POST['ID']);

?>
 
