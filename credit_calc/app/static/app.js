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
        // alert($preqsubcat.val())
        $("#preq").val($preqsubcat.val());
        // Confirm that the selected value was stored in hidden input for preq course
        // console.log($('#preq').val());
    });

    var $coreqcat = $("#cat2"),
        $coreqsubcat = $("#subcat2");

    /*
      Code for prerequiste courses
    */

    // Only display related courses for the selected department
    $coreqcat.on("change",function(){
        var _rel = $(this).val();
        $coreqsubcat.find("option").attr("style","");
        $coreqsubcat.val("");
        if(!_rel) return $coreqsubcat.prop("disabled",true);
        $coreqsubcat.find("[rel="+_rel+"]").show();
        $coreqsubcat.prop("disabled",false);
    });

    // Trigger function when preq course selection is made and store its value in hidden input
    $coreqsubcat.on("change", function() {
        // Show value of selected preq course value
        // alert($coreqsubcat.val())
        $("#coreq").val($coreqsubcat.val());
        // Confirm that the selected value was stored in hidden input for preq course
        // console.log($('#preq').val());
    });




});
