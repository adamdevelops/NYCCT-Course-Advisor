$(function(){

    var $preqcat = $("#cat1"),
        $preqsubcat = $("#subcat1");

    /*
      Code for prerequiste courses
    */

    // Only display related courses for the selected department
    $preqcat.on("change",function(){
        var _rel = $(this).val();
        $preqsubcat.find("option").attr("style","");
        $preqsubcat.val("");
        if(!_rel) return $preqsubcat.prop("disabled",true);
        $preqsubcat.find("[rel="+_rel+"]").show();
        $preqsubcat.prop("disabled",false);
    });

    // Trigger function when preq course selection is made and store its value in hidden input
    $preqsubcat.on("change", function() {
        // Show value of selected preq course value
        alert($preqsubcat.val())
        $("#prereq").val($preqsubcat.val());
        // Confirm that the selected value was stored in hidden input for preq course
        console.log($('#prereq').val());
    });

    // Cancel button for Preqs
    // Clear multiselect options for preqs
    $('#cancelpreq').click(function(){
      // alert("Cancel");
      // Show value of selected preq course value
      $("#prereq").val("");
      // Confirm that the selected value was stored in hidden input for preq course
      console.log($('#prereq').val());
    });

    var $coreqcat = $("#cat2"),
        $coreqsubcat = $("#subcat2");

    /*
      Code for corequiste courses
    */


    $coreqcat.on("change",function(){
        var _rel = $(this).val();
        $coreqsubcat.find("option").attr("style","");
        $coreqsubcat.val("");
        if(!_rel) return $coreqsubcat.prop("disabled",true);
        $coreqsubcat.find("[rel="+_rel+"]").show();
        $coreqsubcat.prop("disabled",false);
    });

    $coreqsubcat.on("change", function() {
      //  Show value of selected preq course value
      alert($coreqsubcat.val())
      $("#coreq").val($coreqsubcat.val());
    //    Confirm that the selected value was stored in hidden input for preq course
       console.log($('#coreq').val());
    });

    // Cancel button for Coreqs
    // Clear multiselect options for coreqs
    $('#cancelcoreq').click(function() {
        // alert("Cancel");
        $("#coreq").val("");
        console.log($('#coreq').val());
    });


  $('.first-button').on('click', function () {

    $('.animated-icon1').toggleClass('open');
  });

  function openNav() {
  document.getElementById("mySidenav").style.width = "250px";
  }

  function closeNav() {
    document.getElementById("mySidenav").style.width = "0";
  }




});
