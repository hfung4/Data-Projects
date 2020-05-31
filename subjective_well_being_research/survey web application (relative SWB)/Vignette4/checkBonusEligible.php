<?php

/* This module performs check at the START of Vignette 4 whether
 * the user is eligible for a bonus based on the amount of time they
 * spent on Vignettes 1,2, and 3.  
 * 
 * We fetch the recorded time duration of Vignettes 1-3 (VXTimeLength)
 * from the sql database. IF the time duration passes a defined threshold,
 * then we display a prompt to the user in the Vignette 4 page, indicating that
 * he/she is eligible for a bonus.
 */  

/*The user is eligible for a bonus if the following conditions are fulfilled:
 * $vignettesDurSat: If Vignettes 1-3 has a duration of 15 s or more. 
*/

//time duration threshold
$vignetteDurThreshold = 70; 

//Check if time duration condition is satisifed
$bonusEligible = ($vignette1TimeDur >= $vignetteDurThreshold) && ($vignette2TimeDur >= $vignetteDurThreshold) && ($vignette3TimeDur >= $vignetteDurThreshold) && ($vignette1Answer != -1) && ($vignette2Answer != -1) && ($vignette3Answer != -1);
; 

//If conditions are met, indicate on the Vignette 4 page that the user is eligible for a bonus payment
if($bonusEligible)
{
	$bonusArray['BONUS'] = 'YES';	
} 
else 
{
	$bonusArray['BONUS'] = 'NO';		
}

//Record if the user is eligible for bonus in mysql table
sqlRowUpdate('USA_responses_2017', $bonusArray, $_POST['ID']);


?>
