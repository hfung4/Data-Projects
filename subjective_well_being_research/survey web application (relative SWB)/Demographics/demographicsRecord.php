<?php

/** demographicsRecord.php
 * This module records the Demographics Survey responses and the amount of time to complete 
 * the Demographic Section in mysql database.
 */ 


/*Demographics Responses  
 * NOTE: For inputs that require user to type in answer in a field, use mysqli_real_escape_string() 
 * to get rid of special char set that might cause error when inserting strings into mysql table.
 */
$demographicArray['Age1'] = mysqli_real_escape_string($myConnection,$_POST['Age1']);
$demographicArray['Gender'] = $_POST['Gender'];
$demographicArray['Education'] = $_POST['Education'];
$demographicArray['Employ'] = $_POST['employanswer'];
$demographicArray['IndIncome'] = $_POST['indincomeanswer'];
$demographicArray['IndIncomeNumInput'] = mysqli_real_escape_string($myConnection,$_POST['indincomeanswertext']);
$demographicArray['HHIncomeNumInput'] = mysqli_real_escape_string($myConnection,$_POST['householdIncomeanswertext']);
$demographicArray['HHIncome'] = $_POST['householdIncomeanswer'];
$demographicArray['NumFamContributeIncome'] = $_POST['contrincomeanswer'];
$demographicArray['NumFamHousehold'] = $_POST['NumFamHousehold'];
$demographicArray['Age2'] = $_POST['ageanswer2'];
$demographicArray['Country1'] = mysqli_real_escape_string($myConnection,$_POST['Country1']);
$demographicArray['Country2'] = mysqli_real_escape_string($myConnection,$_POST['Country2']);
$demographicArray['Country3'] = mysqli_real_escape_string($myConnection,$_POST['Country3']);
$demographicArray['Country4'] = mysqli_real_escape_string($myConnection,$_POST['Country4']);
$demographicArray['Country5'] = mysqli_real_escape_string($myConnection,$_POST['Country5']);
$demographicArray['State'] = $_POST['state'];
$demographicArray['Comments'] = mysqli_real_escape_string($myConnection,$_POST['Comments']);


//Record discretes for married/separated based on marriage answer
list($dMarriedAns, $dSeparatedAns) = marriageDiscretes($_POST['maranswer']); 
$demographicArray['Dmarried_demographics'] = $dMarriedAns;
$demographicArray['Dseparated'] = $dSeparatedAns;


//Record IP address of the visitor
$demographicArray['IPADDRESS_END'] = $_SERVER['REMOTE_ADDR'];

//Record user's browser
$demographicArray['Browser'] = $_SERVER['HTTP_USER_AGENT'];


/*User Code */

//Generate and record the final code used by the user to get compensation by concatenating the code letters and the age input by the user

$codeLetter =completionCodeGen();
$codeAnsAge=$_POST['codeAnsAge'];
$FinalCode = $codeLetter.$codeAnsAge;

$demographicArray['Code'] = $FinalCode;

/*Survey Time Duration */

//Record Demographics Survey start time
$demographicArray['DemTimeLoad'] = $_POST['demographics_startTime'];  

//Compute and record Demographics Survey time duration 
$exit_startTime = date('h:i:s a', time()); // get start time of the exit page (page 9) 
$demographicArray['ExitTimeLoad'] = $exit_startTime;  //record start time at exit page
$demographicArray['DemTimeTotal'] = computeTimeDuration($_POST['demographics_startTime'], $exit_startTime);

//Compute and record the total time duration of the Life Satisfaction Survey
$WelcomeTimeResult = sqlRowSelect('USA_responses_2017', "TimeWelcome", $_POST['ID']);  //Select columns in mysql 
$WelcomeTimeRow = mysqli_fetch_assoc($WelcomeTimeResult);
$welcomeStartTime= $WelcomeTimeRow['TimeWelcome'];  //read the starttime of the welcome page that is recorded in mysql table
$demographicArray['TotalTIme'] = computeTimeDuration($welcomeStartTime, $exit_startTime);

//update mysql row
sqlRowUpdate('USA_responses_2017', $demographicArray, $_POST['ID']);
 

?>
