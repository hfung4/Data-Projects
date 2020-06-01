<?php

/** vignette5Record.php
 * This module records the Vignette 5 answer and the amount of time to complete 
 * Vignette 5 in mysql database.
 */ 

/* Enter Vignette 5 Response, Vignette 5 Start time and Vingette 5 Time Duration into an Array 
 * Pass array to sql UPDATE function to update sql table */

//Record Vignette 5 response
$vignette5Answer = checkans($_POST['vignetteans']);

if($_POST['vignettetrigger'] == 1){
	$vignette5Array['Vignette5Answer'] = $vignette5Answer;
}
else
{
	$vignette5Array['Vignette5Answer'] = -1;
}



//Record Vignette 5 start time
$vignette5Array['Vignette5LoadTime'] = $_POST['vignette5_startTime'];  


//Compute and record Vignette 5 time duration 
$compTest_startTime = date('h:i:s a', time()); // get start time of Comprehension Test (page 7) 
$vignette5Array['V5TimeLength'] = computeTimeDuration($_POST['vignette5_startTime'], $compTest_startTime);



//update mysql row
sqlRowUpdate('USA_responses_2017', $vignette5Array, $_POST['ID']); 

?>


