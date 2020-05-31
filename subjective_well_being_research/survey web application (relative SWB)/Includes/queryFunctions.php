<?php
/*
 * query_functions.php
 * 
 * This module contains various functions that are used to init, insert
 * and update the mysql database
 * 
 */



/**rowInit()
 * 
 * This function intialize an empty row in the table for the current user.  
 * Since the columns are not set to nullible, we will use '0' as the placeholder.  
 * We will update each column as data becomes available from the survey.
 * Inputs  VOID
 *
 * Outputs VOID
 * 
 */ 
function rowInit()
{
	
   // need to use Myconnection and $randself (ID) in this function
	global $myConnection; 
	global $randself;  

	$query0 = "INSERT INTO myTestTable VALUES('$randself', '0', '0', '0' )";
	$query0Result = mysqli_query($myConnection,$query0);
	
	if(!$query0Result)
	{ 
		echo("Cannot INIT the record. Error description: " . mysqli_error($myConnection));
	}
	
}


/** sqlRowInsert()
 * 
 * This function constructs a query that CREATES a record in mysql database
 * 
 * INPUTS  
 * $table_name:  name of the table in mysql database
 * $form_data:  An assoicative array that contains keys that corresponds to column names in the table
 * and values for those columns
 *
 * OUTPUTS
 * Void
 * 
 */ 
function sqlRowInsert($table_name, $form_data)
{
	global $myConnection; 
	
	//Use array_keys() to get the keys of the array (which are also the column names in mysql table)
	$fields = array_keys($form_data);

	//Construct the query
	$sql = "INSERT INTO ".$table_name."
	(`".implode('`,`', $fields)."`)
	VALUES('".implode("','", $form_data)."')";

	$query_result = mysqli_query($myConnection, $sql);
	
	if(!$query_result)
	{ 
		echo("Cannot CREATE the record! Error description: " . mysqli_error($myConnection));

	}	
}



/** sqlRowUpdate()
 * 
 * This function constructs a query that UPDATES a record in mysql database
 * 
 * INPUTS  
 * $table_name:  name of the table in mysql database
 * $form_data:  An assoicative array that contains keys that corresponds to column names in the table
 * and values for those columns
 * $where_arg: The where clause that is used to filter records.  For now, we will assume the user ID is always used.
 * This function can be expanded further in the future...
 *
 * OUTPUTS
 * Void
 * 
 */ 
function sqlRowUpdate($table_name, $form_data, $where_arg)
{
	global $myConnection; 
	$whereSQL = '';
	
    if(!empty($where_arg))
	{
		//Add WHERE keyword 
		$whereSQL = "WHERE  ID = " .$where_arg;  
    }
   
    // Construct the SQL statement
    $sql = "UPDATE ".$table_name." SET ";
	
	// loop and build the column 
	$sets = array();

    foreach($form_data as $column => $value)
	{
         $sets[] = "`".$column."` = '".$value."'";
    }    
	
	$sql .= implode(', ', $sets);
 
    //Append WHERE to the statement
    $sql .= $whereSQL;
    
    // run query and check error 
	$query_result = mysqli_query($myConnection, $sql);
	
	if(!$query_result)
	{ 
		die("Cannot UPDATE the record. Error description: " . mysqli_error($myConnection));

	}
}



/** sqlRowDelete()
 * 
 * This function constructs a query that DELETES a record in mysql database
 * 
 * INPUTS  
 * $table_name:  name of the table in mysql database
 * $where_arg: The where clause that is used to filter records.  For now, we will assume the user ID is always used.
 * This function can be expanded further in the future...
 *
 * OUTPUTS
 * Void
 * 
 */ 
function sqlRowDelete($table_name, $where_arg)
{
	global $myConnection; 
	$whereSQL = '';
	
	if(!empty($where_arg))
	{
		//Add WHERE keyword 
		$whereSQL = "WHERE  ID = " .$where_arg;     
    }
	
	// Construct the DELETE query
	$sql = "DELETE FROM ".$table_name." ".$whereSQL;
	
	// run query and check error 
	$query_result = mysqli_query($myConnection, $sql);
	
	if(!$query_result)
	{ 
		die("Cannot DELETE the record. Error description: " . mysqli_error($myConnection));

	}
}



/** sqlRowRead()
 * 
 * This function constructs a query that SELECTS a record in mysql database
 * 
 * INPUTS  
 * $table_name:  name of the table in mysql database
 * $select: A string containing the names of the columns the user wishes to select (separated by comma)
 * For example: $select = "Vignette1Text, Language"
 * $where_arg: The where clause that is used to filter records.  For now, we will assume the user ID is always used.
 *
 * OUTPUTS
 * $result from the query, which can be used as input to the FETCH function to READ the selected data from mysql
 * 
 */ 
function sqlRowSelect($table_name, $select, $where_arg)
{
	global $myConnection; 
    
    if(!empty($where_arg))
    {
		$whereSQL = "WHERE  ID = " .$where_arg;        
    }
    
    // Construct the actual SQL statement
    $sql = "SELECT ".$select." FROM ".$table_name." ";
    // append the where statement
    $sql .= $whereSQL;
    
    // run query and check error 
	$query_result = mysqli_query($myConnection, $sql);
	
	if(!$query_result)
	{ 
		die("Cannot SELECT the record. Error description: " . mysqli_error($myConnection));
	}
	
	return $query_result;
	

}


/** formCompleted()
 * 
 * This function checks if a Vignette has already been completed by checking for an answer 
 * that is NOT NULL in the sql database
 * 
 * INPUTS  
 * $table_name:  name of the table in mysql database
 * $columnName: A string containing the names of the column that the user wishes to check 
 * For example: $columnName = "Vignette1Answer"
 * $where_arg: The where clause that is used to filter records.  For now, we will assume the user ID is always used.
 *
 * OUTPUTS
 * Returns a boolean $isCompleted:  TRUE: Vignette has already been completed.  FALSE: Vignette is not completed. 
 * 
 */ 

function formCompleted($table_name, $columnName, $ID)
{
	//Get the column value using sqlRowSelect and mysqli_fetch_assoc functions
	$result = sqlRowSelect($table_name, $columnName, $ID);  //Select columns in mysql table
	$row = mysqli_fetch_assoc($result);
	
	$fetchedResponse= $row[$columnName];  //read value stored in $columnName from mysql database

	$vigCompleted = (strcmp($fetchedResponse, 'NULL') != 0); //Answer is not NULL (which indicates Vignette has been completed previously)
	
	return $vigCompleted;
	
}






?>
