<?php

/** vignette3Record.php
 * This module records the Vignette 3 answer and the amount of time to complete 
 * Vignette 3 in mysql database.
 */ 

/* Enter Vignette 3 Response, Vignette 3 Start time and Vingette 3 Time Duration into an Array 
 * Pass array to sql UPDATE function to update sql table */


//Record Vignette 3 response
$vignette3Answer = checkans($_POST['vignetteans']);

if($_POST['vignettetrigger'] == 1){
	$vignette3Array['Vignette3Answer'] = $vignette3Answer;
}
else
{
	$vignette3Array['Vignette3Answer'] = -1;
}



//Record Vignette 3 start time
$vignette3Array['Vignette3LoadTime'] = $_POST['vignette3_startTime'];  


//Compute and record Vignette 3 time duration 
$vignette4_startTime = date('h:i:s a', time()); // get start time of Vignette 4 (page 5) 
$vignette3Array['V3TimeLength'] = computeTimeDuration($_POST['vignette3_startTime'], $vignette4_startTime); 

//update mysql row
sqlRowUpdate('USA_responses_2017', $vignette3Array, $_POST['ID']);
 


?>


