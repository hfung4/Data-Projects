//post data to php for each clicked button
function get(clicked_name, IDinput, pageNum) {
    
     
    var postData={ };
     
    /* If the button is clicked, I record the timestamp.  If the button is not clicked,
     * the sql value for the button will remain at 0 (its intial value).  Therefore, 
     * the sql value for each button is used to record the following info: 
     * 1) Whether the button was clicked, and 
     * 2) The time at which it was clicked.
     */  
    
    
    var btTimeStamp = { };
    var d = new Date();
    var date_str = d.toString()
    
    btTimeStamp[clicked_name] = date_str;
         
    postData[clicked_name] = date_str;
    postData["ID"] = IDinput;
    
    
    
    
    
     if(pageNum ==2)
     {
		 $.post('Vignette1/vignette1Button.php', postData);
	 }
	 else if(pageNum ==3)
	 {
		 $.post('Vignette2/vignette2Button.php', postData);
	 }
	 else if(pageNum ==4)
	 {
		 $.post('Vignette3/vignette3Button.php', postData);
	 }
	 else if(pageNum ==5)
	 {
		 $.post('Vignette4/vignette4Button.php', postData);
	 }
	 else if(pageNum ==6)
	 {
		 $.post('Vignette5/vignette5Button.php', postData);
	 }
         
   }




//Set button disable flag with timer
function btDisable(obj) {
   
    //1. Define id array
    var idArray=["IncomeBt", "PartnerBt","TrustBt","ExerciseBt", "WorkBt", "NumFrdBt",
                 "UnemployBt", "PainBt", "CommunityBt", "BMIBt", "FreqFrdBt"]; 
    
    //2. Disable current button
    obj.disabled = true;


    //3. Check if a button is active. Disable all active buttons for 5s.
    for(var i=0; i<11; i++)
    {
        var disableFlag = document.getElementById(idArray[i]).disabled == false;
        if(disableFlag)
        {
           document.getElementById(idArray[i]).disabled = true;
        
            setTimeout(function(x) { 
                return function() { 
                document.getElementById(idArray[x]).disabled= false;
            }; 
            }(i), 5000);
        }   

    }
   
    
}


function confirmBox(vigAmountID)
{
	var x= document.getElementById(vigAmountID).value;

	if(x>0)  //We have vignette response 
	{
		return true;
	}
	else  // We have no vignette response
	{
		var confirmResp = confirm('You have not responded to the vignette using the slider. Are you sure you want to continue?');
		if(!confirmResp) // User does not want to continue.
		{
			event.preventDefault();
		}
		
	}
		
	
	
	
	
	
	
}







