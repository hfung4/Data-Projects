$( function() {
    $( "#overallslider" ).slider({
      range: "max",
      min: 0,
      max: 10,
      value:0,
	  step: 0.1,
      slide: function( event, ui ) {
        $( "#overallamount" ).val( ui.value );
		
		var curVal = ui.value;
        $('#overalldisplayAmount').text(curVal);
      }
    });
    $( "#overallamount" ).val( $( "#overallslider" ).slider( "value" ) );
  } );
  
  
  
  $( function() {
    $( "#incomeslider" ).slider({
      range: "max",
      min: 0,
      max: 10,
      value:0,
	  step: 0.1,
      slide: function( event, ui ) {
        $( "#incomeamount" ).val( ui.value );
		
		var curVal = ui.value;
        $('#incomedisplayAmount').text(curVal);
      }
    });
    $( "#incomeamount" ).val( $( "#incomeslider" ).slider( "value" ) );
  } );
  
  
  
  
  $( function() {
    $( "#jobslider" ).slider({
      range: "max",
      min: 0,
      max: 10,
      value:0,
	  step: 0.1,
      slide: function( event, ui ) {
        $( "#jobamount" ).val( ui.value );
		
		var curVal = ui.value;
        $('#jobdisplayAmount').text(curVal);
      }
    });
    $( "#jobamount" ).val( $( "#jobslider" ).slider( "value" ) );
  } );
  
  
  
  
  $( function() {
    $( "#socialslider" ).slider({
      range: "max",
      min: 0,
      max: 10,
      value:0,
	  step: 0.1,
      slide: function( event, ui ) {
        $( "#socialamount" ).val( ui.value );
		
		var curVal = ui.value;
        $('#socialdisplayAmount').text(curVal);
      }
    });
    $( "#socialamount" ).val( $( "#socialslider" ).slider( "value" ) );
  } );
  
  
  
  $( function() {
    $( "#healthslider" ).slider({
      range: "max",
      min: 0,
      max: 10,
      value:0,
	  step: 0.1,
      slide: function( event, ui ) {
        $( "#healthamount" ).val( ui.value );
		
		var curVal = ui.value;
        $('#healthdisplayAmount').text(curVal);
      }
    });
    $( "#healthamount" ).val( $( "#healthslider" ).slider( "value" ) );
  } );
  
  
  

$( function() {
    $( "#job1slider" ).slider({
      range: "max",
      min: 0,
      max: 10,
      value:0,
	  step: 0.1,
      slide: function( event, ui ) {
        $( "#job1amount" ).val( ui.value );
		
		var curVal = ui.value;
        $('#job1displayAmount').text(curVal);
      }
    });
    $( "#job1amount" ).val( $( "#job1slider" ).slider( "value" ) );
  } );
  
  
  
  $( function() {
    $( "#Vig2slider" ).slider({
      range: "max",
      min: 0,
      max: 10,
      value:0,
	  step: 0.1,
	  
      slide: function( event, ui ) {
        $( "#Vig2amount" ).val( ui.value );
        $("#Vig2Triggered").val(1);
		
		var curVal = ui.value;
        $('#Vig2displayAmount').text(curVal);
      }
    });
    $( "#Vig2amount" ).val( $( "#Vig2slider" ).slider( "value" ) );
  } );
  
  
  $( function() {
    $( "#Vig3slider" ).slider({
      range: "max",
      min: 0,
      max: 10,
      value:0,
	  step: 0.1,
	 
      slide: function( event, ui ) {
        $( "#Vig3amount" ).val( ui.value );
        $("#Vig3Triggered").val(1);
        
		var curVal = ui.value;
        $('#Vig3displayAmount').text(curVal);
      }
    });
    $( "#Vig3amount" ).val( $( "#Vig3slider" ).slider( "value" ) );
  } );
  
  
  
  
  $( function() {
    $( "#Vig4slider" ).slider({
      range: "max",
      min: 0,
      max: 10,
      value:0,
	  step: 0.1,
	  
      slide: function( event, ui ) {
        $( "#Vig4amount" ).val( ui.value );
        $("#Vig4Triggered").val(1);
		
		var curVal = ui.value;
        $('#Vig4displayAmount').text(curVal);
      }
    });
    $( "#Vig4amount" ).val( $( "#Vig4slider" ).slider( "value" ) );
  } );
  
  
  
  
  
  $( function() {
    $( "#Vig5slider" ).slider({
      range: "max",
      min: 0,
      max: 10,
      value:0,
	  step: 0.1,
      slide: function( event, ui ) {
        $( "#Vig5amount" ).val( ui.value );
        $("#Vig5Triggered").val(1);
		
		var curVal = ui.value;
        $('#Vig5displayAmount').text(curVal);
      }
    });
    $( "#Vig5amount" ).val( $( "#Vig5slider" ).slider( "value" ) );
  } );
  
  
  
 
$( function() {
	
	
	var $mySlider = $( "#Vig1slider" );
    $mySlider.slider({
      range: "max",
      min: 0,
      max: 10,
      value:0,
	  step: 0.1,
      slide: function( event, ui ) {
        $( "#Vig1amount" ).val( ui.value );
        $("#Vig1Triggered").val(1);
        
		
		var curVal = ui.value;
        $('#Vig1displayAmount').text(curVal);
      }
    });
    
    
    
    $( "#Vig1amount" ).val( $( "#Vig1slider" ).slider( "value" ) );
  } );
  
  
  
 $( function() {
	 
	 $('.ui-slider-handle').hide();
 
		$('.ui-slider').mousedown(function(){
			$('.ui-slider-handle', this).show();
		});
	 
 } );
  
  
  
  
  
  
  
  
