$("#save_recipe").change(function() {
    if ($(this).is(":checked")) {
        $("#name").prop("disabled", false)
    } else {
        $("#name").prop("disabled", true)
    }
})