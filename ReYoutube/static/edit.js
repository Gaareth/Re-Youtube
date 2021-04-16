function save_comment(comment_id) {
    var save_value = document.getElementById("comment-"+comment_id+"-save-value");
    var save_submit = document.getElementById("comment-"+comment_id+"-save-submit");

    var comment_edit_textarea = document.getElementById("comment-"+comment_id+"-input-textarea");
    console.log(comment_edit_textarea)
    save_value.value = comment_edit_textarea.value;
    save_submit.click();
}

function edit_comment(comment_id) {
    var comment_edit_textarea = document.getElementById("comment-"+comment_id+"-edit");
    var comment_edit_textarea_actual = document.getElementById("comment-"+comment_id+"-input-textarea");

    var edit_option = document.getElementById("comment-"+comment_id+"-edit-option");
    var save_option = document.getElementById("comment-"+comment_id+"-save-option");
    var comment_content = document.getElementById("comment-content-"+comment_id);

    if (comment_edit_textarea.style.display == "block") {
    //Pressed Abort
        comment_edit_textarea.style.display = "none";
        edit_option.innerHTML = "Edit";
        edit_option.style = "margin-bottom: .5rem; margin-top: -0.4rem;";

        comment_content.style.display = "block";

        save_option.style.display = "none";
    }else {
    // Pressed Edit
        comment_edit_textarea.style.display = "block";
        edit_option.innerHTML = "Abort";
        edit_option.style = "margin-bottom: .5rem; margin-top: -0.4rem; color: black;";

        comment_content.style.display = "none";

        save_option.style.display = "block";
        comment_edit_textarea_actual.value = comment_content.innerHTML.trim();
    }
}