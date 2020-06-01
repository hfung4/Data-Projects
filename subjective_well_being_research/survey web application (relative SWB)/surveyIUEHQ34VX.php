<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
<title>Life Conditions Survey</title>
<link rel="stylesheet" type="text/css" href="css/view.css" media="all">
<link rel="stylesheet" href="css/circle.css">
<link rel="stylesheet" href="//code.jquery.com/ui/1.12.1/themes/base/jquery-ui.css">
<link rel="stylesheet" href="/resources/demos/style.css">
<link rel="stylesheet" href="https://www.w3schools.com/w3css/4/w3.css">
<script src="https://code.jquery.com/jquery-1.12.4.js"></script>
<script src="https://code.jquery.com/ui/1.12.1/jquery-ui.js"></script>
<script type="text/javascript" src="js/view.js"></script>
<script type="text/javascript" src="js/slider.js"></script>
<script type="text/javascript" src="js/relBarAppend.js"></script>
<script type="text/javascript" src="js/buttonClick.js"></script> 
<script type="text/javascript" src="js/relPieChart.js"></script> 
<script type="text/javascript" src="https://www.gstatic.com/charts/loader.js"></script>


<!--disable back button-->
<script type="text/javascript">
	window.location.hash="no-back-button";
	window.location.hash="Again-No-back-button";//again because google chrome don't insert first hash into history
	window.onhashchange=function(){window.location.hash="no-back-button";}
</script>



</head>


<!-- The headers for ALL pages of the survey should be placed above.  This is because we are only appending html markups for each page.
     Think of this as a large single html pages pieced together from different modules. -->



<?php

/** Some refactoring:
*
* conn3ctMe.php
* Connect to the SQL database using mysql command "mysqi_connect".
* Select the SQL database using mysql command "mysql_select_db" 
*
* util.php
* Contains a function checks the user response from the slider. Converts the 
* user input (string value) to a float value. 
*
* dictionaries.php: Contains the text that are displayed on the survey pages organized in assoicative arrays.
* 
* queryFunctions.php:
* Contains command functions used to work with mysql database (init, cretate, update, and delete records).
* 
* formDataArray.php:
* Contains handlers for the columns in mysql database
*/

include_once('Includes/conn3ctMe.php');  //connect to mysql database
include_once('Includes/util.php');  //contains utility functions
include_once('Includes/dictionaries.php'); //contain texts to display on surveys
include_once('Includes/queryFunctions.php');  //command functions for mysql database
include_once('Includes/formDataArray.php');  //data array
include_once('Includes/vigGenDataArray.php');  //data array
include_once('Includes/vigGenOrderArray.php');  //data array



/** State Machine
 * 
 * Used to select the webpage to display
 * "State" is given by $pagenumber
 * "State transition" occurs when the user submit the form currently displayed
 * After the form is submitted, then the user can advance to the next page.
*/
$pagenumber = $_POST['page'];  

switch ($pagenumber)  
{

/** CASE 1
 * 
 * A. Create record after submitting form in new_welcome page.    
 * B. Self Report on Life Satisfication (page 1). 
 * C. Vignettes Generation (Python).
 */
case 1:


include_once('Includes/init_sql.php'); //Create new record in mysql database for the user

//Run python modules to generate vignettes and relative parameters
$cmd = "python domainGen/vignetteGen.py ".$_POST['ID'];
$output = shell_exec($cmd);

include_once('SelfReport/selfReportMarkup.php'); //display self report on Life Satisifcation Page.

break;


/** CASE 2
 * 
 * A. Update mysql table with data collected from the Self Report Survey.
 * B. Display Vignette 1 (page 2).
 */ 
case 2:
include_once('SelfReport/selfReportRecord.php'); //update mysql table with Self Report responses
include_once('Vignette1/showVignette1.php'); // display Vignette 1
break;



/** CASE 3
 * 
 * A. Update mysql table with data collected from Vignette 1.
 * B. Display Vignette 2 (page 3).
 */ 
case 3:
include_once('Vignette1/vignette1Record.php'); //update mysql table with Vignette 1 response
include_once('Vignette2/showVignette2.php'); //display Vignette 2
break;



/** CASE 4
 * 
 * A. Update mysql table with data collected from Vignette 2.
 * B. Display Vignette 3 (page 4).
 */ 
case 4:
include_once('Vignette2/vignette2Record.php'); //update mysql table with Vignette 2 response
include_once('Vignette3/showVignette3.php'); //display Vignette 3
break;


/** CASE 5
 * 
 * A. Update mysql table with data collected from Vignette 3.
 * B. Display Vignette 4 (page 5).
 * C. Check if the user has accessed the comprehension test page before, 
 *    if yes, the survey will automatically end and go back to page 0 (new_welcome page)
 * D. Check if user is eligible for BONUS
 */
case 5:
include_once('Vignette3/vignette3Record.php'); //update mysql table with Vignette 3 response
include_once('Vignette4/showVignette4.php');  //display Vignette 4, check comprehension test and bonus 
break;


/** CASE 6
 * 
 * A. Update mysql table with data collected from Vignette 4.
 * B. Display Vignette 5 (page 6).
 */ 
case 6:
include_once('Vignette4/vignette4Record.php'); //update mysql table with Vignette 4 response
include_once('Vignette5/showVignette5.php'); //display Vignette 5
break;



/** CASE 7
 * 
 * A. Update mysql table with data collected from Vignette 5.
 * B. Display Comprehension Test (page 7).
 */
case 7:
include_once('Vignette5/vignette5Record.php'); //update mysql table with Vignette 5 response
include_once('compTest/compQuestions.php');
break;


/** CASE 8
 * 
 * A. Update mysql table with data collected from comprehension test.
 * B. Display Demographic Survey (page 8).
 */
case 8:
include_once('compTest/compTestRecord.php'); //update mysql table with compTest response
include_once('Demographics/demographics.php');

break;


/** CASE 9
 * A. Update mysql table with data collected from Demographic Survey. 
 * B. Response Quality Check. 
 * C. Display Exit Page (page 9).
 */
case 9:
include_once('Demographics/demographicsRecord.php');

 // Check the quality of the users' responses
   //$cmd = "python respQualityCheck.py ".$_POST['ID']." ".$_POST['marOrHealth'];		
   //$output = shell_exec($cmd);

include_once('exit.php');
break;


/** New Welcome Page (page 0)   
 *  This is the starting point of the survey
 */  
default:

include_once('new_welcome.php');

break;

}

?>

