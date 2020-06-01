<?php 

/*Make a connection to the server*/
$myConnection = mysqli_connect ("localhost","henryfung","mtuarsftqq");

/**
 * Check mysql connection
 * Output error message with additional sql error if connection fails
 */
if (!$myConnection)
{
	die("Cannot connect to the database. Error description: " . mysqli_error($myConnection));

}

/**Select database name here
 * Select the default mysql database
 * Input: 1) $myConnection, the identifer returned by mysqli_connect()
 *        2) String [Name of the selected database]
 */ 
mysqli_select_db($myConnection,"vignettes_live") or die("Cannot select the database. Error description: " . mysqli_error($myConnection));

?>

