$(function(){

    var $cat = $("#cat"),
        $subcat = $("#subcat");

    $cat.on("change",function(){
        var _rel = $(this).val();
        $subcat.find("option").attr("style","");
        $subcat.val("");
        if(!_rel) return $subcat.prop("disabled",true);
        $subcat.find("[rel="+_rel+"]").show();
        $subcat.prop("disabled",false);
    });

    var selection = $subcat.val()

    $subcat.on("change", function() {
        alert($subcat.val())
        $("#myField").val($subcat.val());
        console.log($('#myField').val());
    });


});
