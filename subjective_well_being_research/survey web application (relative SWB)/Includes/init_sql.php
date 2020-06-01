<?php

/** init_sql.php
 * 
 * This module grabs data generated in the new_welcomes page and creates 
 * a new record in mysql table
 */
 
 
/*Create record for the user with the following basic information set at the start of the survey:
 * $ID
 * $ipaddress: IP address of the user
 * $timewelcome: start time of the survey
 * $language: language of the user
*/ 


$formDataArray['ID'] = (int)$_POST['ID'];
$formDataArray['IPADDRESS1'] = $_POST['ipaddress1'];
$formDataArray['TimeWelcome'] = $_POST['timewelcome'];
$formDataArray['Language'] = $_POST['lang'];

$vigGenDataArray['ID'] = (int)$_POST['ID'];
$vigGenOrderArray['ID'] = (int)$_POST['ID'];

if(isSet($_POST['newWelcomeSubmit'])) //If new_welcome form is submitted
{
	//Insert row
	sqlRowInsert('USA_responses_2017', $formDataArray);
	sqlRowInsert('USA_vignettes_2017', $vigGenDataArray);
	sqlRowInsert('USA_vignettes_order_2017', $vigGenOrderArray);
}

 
?>

