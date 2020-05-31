<?php

//The purpose of this module is to send the $_POST clicked button status to SQL database

//Need to include the SQL query functions again since vignette1Button.php is not part 
//of surveyIUEHQ34VX.php

include_once('../Includes/conn3ctMe.php');  //connect to mysql database
include_once('../Includes/queryFunctions.php');  //command functions for mysql database


//The _$POST array has two elements: buttonName and ID.  
//We want to get the buttonName to update mysql (first element of $_POST)

$keys = array_keys($_POST);


if(isset($_POST[$keys[0]]))
{
    
$vigBt4Array[$keys[0]] = $_POST[$keys[0]];
//update mysql row
sqlRowUpdate('USA_responses_2017', $vigBt4Array, $_POST['ID']);

    
}




?>
