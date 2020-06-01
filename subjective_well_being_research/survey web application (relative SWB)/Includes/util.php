<?php 
/* This module contains utility functions */


/** checkans
 * 
 * This function ctakes string input from the slider (used by the user 
 * to rank each questions on the scale of 1-10) and output the float value of the string
 * 
 * INPUT: $sliderval (string input from slider)
 *        $stringBool (a boolean: true if the expected output is a string)     
 *   
 * OUTPUT:$sliderval (float output)
 * 
 */  
	
function checkans($sliderval, $stringBool) 
{
	$sliderValFloat = floatval($sliderval); //get float value of string input from $_POST[element]
	
	if ($sliderValFloat > 0)  //user slider response is larger than 0
	{
		if($stringBool)
		{
			return $sliderval; //output string format
		}
		else
		{
			return $sliderValFloat; //output float format
		}
	}
	else if (strcmp($sliderval,"0") == 0)  // string input is exactly 0
	{
		return 0;
	}
	else //slider input is not valid, return -1  (ex: the user did not respond to question and the slider val is "Use Slider Bar")
	{
		return -1;
	}
}
			

/** shuffle_assoc
 * 
 * This function shuffles the order of an associative array 
 * 
 * INPUT: $array 
 * OUTPUT:$new (suffled arrays)
 * 
 */
function shuffle_assoc(&$array) {
	
	$keys = array_keys($array);

    shuffle($keys);

    foreach($keys as $key) {
		$new[$key] = $array[$key];
		}
		
		return $new;
    }
    
    

/** computeTimeDuration
 * 
 * This function compute the time differences between the current time stamp
 * (when the function is called), and the input time stamp 
 * 
 * INPUT: $oldTimeStr (str) 
 * OUTPUT:$timeDifference (int)
 * 
 */

function computeTimeDuration($oldTimeStr, $currentTimeStr)
{	
	$oldTimeInt = strtotime($oldTimeStr); //convert old time from string to int
    $currentTimeInt = strtotime($currentTimeStr); // convert current time from str to int
    
    $timeDifference = $currentTimeInt - $oldTimeInt;  //compute time duration
	
	return $timeDifference;
		
}




/** compTestCheck
 * This function checks if the user has previously accessed the comprehension test page.
 * The comprehension test is used for quality control: it asks the user a few questions about 
 * Vignettes 1-4 to check whether the user had read the Vignettes carefully and assess the 
 * Life Satisification of the hypothetical subject.
 * 
 * In order to prevent the user from cheating by going back to the Vignettes and look for answers
 * to the comprehension questions.  This module will check whether the user as already seen the 
 * comprehension page.  If yes, then the user cannot advance further than Vignette 4 . Instead, they will
 * be automatically redirected back to the new_welcome page.
 * 
 * INPUT: sql table name and user ID
 * OUTPUT: visitCompTrue: a boolean that is set to TRUE if the user has visited the comprehension test page before.
 */  
	

function compTestCheck($tableName, $userID)
{
	/*Get the variable called "vistedComp" that is stored in the mysql database for the current user.
	 * Note that this variable is initialized to FALSE, and it is only updated to TRUE
	 * if the user access the comprehension test page.
	 */ 	
	 $compTestResult = sqlRowSelect($tableName, "visitedComp", $userID);  
	 $compTestRow = mysqli_fetch_assoc($compTestResult);
	 $visitedCompTrue= $compTestRow['visitedComp'];  //$visitedCompTrue will only be set to 1 if comprehension test is visited.
	 
	 if($visitedCompTrue == 1)
	 {
		 return TRUE;
	 }
	 else
	 {
		 return FALSE;
	 }	
}



/** completionCodeGen 
 * 
 * This function generates the completion and provides it to the user
 * for him/her to enter in MTurk to receive compensation
 * 
 * INPUT: VOID 
 * OUTPUT:$codeGen (string)
 * 
 */

function completionCodeGen()
{
	//randomly generate the first letter
    $int_1 = rand(0,51);
    $a_z_1 = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ";
    $codeLetter1 = $a_z_1[$int_1];
    
    //randomly generate the second letter
    $int_2 = rand(0,51);
    $a_z_2 = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ";
    $codeLetter2 = $a_z_2[$int_2];
    
    //randomly generate the third letter
    $int_3 = rand(0,51);
    $a_z_3 = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ";
    $codeLetter3 = $a_z_3[$int_3];
    
    $codeGen = "{$codeLetter1}{$codeLetter2}{$codeLetter3}";
    
    return $codeGen;


}


/** marriageDiscretes 
 * 
 * This function computes the Dmaried, or Dseparate discretes
 * based on marriage answers in the Demographic Survey
 * 
 * INPUT: maranswer (string)
 * OUTPUT:$marDisList (array)
 * 
 */

function marriageDiscretes($answerStr)
{
	if(($answerStr =="widowed") || ($answerStr=="divorced"))  
	{
		$disMarried=0;
		$disSeparated=1;
	}
	else if($answerStr =="married")  
	{
		$disMarried=1;
		$disSeparated=0;
	}
	else
	{
		$disMarried=0;
		$disSeparated=0;
	}
	
	
	return array($disMarried, $disSeparated);
	
		
}


/**
* Formats numbers to the specified number of significant figures.
*
* @author: Bevan Rudge
* 
* INPUT: $number: The number to format.
         $sf: The number of significant figures to round and format the number to.
* @return string
*   The rounded and formatted number.
*/
function format_number_significant_figures($number, $sf) {
  // How many decimal places do we round and format to? @note May be negative.
  $dp = floor($sf - log10(abs($number)));
  
  // Round as a regular number.
  $number = round($number, $dp);
  
  // Leave the formatting to format_number(), but always format 0 to 0dp.
  return number_format($number, 0 == $number ? 0 : $dp);
}	




  


?>




