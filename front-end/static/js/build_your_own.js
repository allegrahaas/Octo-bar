$("#save_recipe").change(function() {
    if ($("#save_recipe").is(":checked")) {
        console.log("checked")
        $("#name-field").removeClass("d-none")
    } else {
        console.log("unchecked")
        $("#name-field").addClass("d-none")
    }
})