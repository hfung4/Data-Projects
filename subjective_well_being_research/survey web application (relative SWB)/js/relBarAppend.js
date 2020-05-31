 $(document).ready(function(){

 $("#IncomeBt").click(function () {
  $("#IncomeBar").clone().css({"display":"none"}).prependTo("#DisplayRelBars").fadeIn(5000); 
});


 $("#WorkBt").click(function () {
  $("#WorkBar").clone().css({"display":"none"}).prependTo("#DisplayRelBars").fadeIn(5000);  
});
     
  
 $("#PartnerBt").click(function () {
  $("#PartnerBar").css({"display":"none"}).prependTo("#DisplayRelBars").fadeIn(5000);  
});
     
 
  $("#UnemployBt").click(function () {
  $("#UnemployBar").css({"display":"none"}).prependTo("#DisplayRelBars").fadeIn(5000);
});
     
     
  $("#CommunityBt").click(function () {
  $("#CommunityBar").clone().css({"display":"none"}).prependTo("#DisplayRelBars").fadeIn(5000);  
});
     

$("#ExerciseBt").click(function () {
  $("#ExerciseBar").clone().css({"display":"none"}).prependTo("#DisplayRelBars").fadeIn(5000);  
});
     

$("#PainBt").click(function () {
  $("#PainBar").clone().css({"display":"none"}).prependTo("#DisplayRelBars").fadeIn(5000);  
});

     
$("#BMIBt").click(function () {
  $("#BMIBar").clone().css({"display":"none"}).prependTo("#DisplayRelBars").fadeIn(5000);  
});

     
$("#TrustBt").click(function () {
  $("#TrustBar").clone().css({"display":"none"}).prependTo("#DisplayRelBars").fadeIn(5000);  
});
     
    
$("#NumFrdBt").click(function () {
  $("#NumFrdBar").clone().css({"display":"none"}).prependTo("#DisplayRelBars").fadeIn(5000);  
});
     
     
     
 $("#FreqFrdBt").click(function () {
  $("#FreqFrdBar").clone().css({"display":"none"}).prependTo("#DisplayRelBars").fadeIn(5000);  
});
     
     
     
     
     
$("#previousVigBt").click(function () {
  $("#previousVigDisplay").fadeToggle(1000);  
});

     
     




});
