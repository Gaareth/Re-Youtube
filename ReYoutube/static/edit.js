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
    var abort_option = document.getElementById("comment-"+comment_id+"-abort-option");

    var save_option = document.getElementById("comment-"+comment_id+"-save-option");
    var comment_content = document.getElementById("comment-content-"+comment_id);
    var comment_content_wrapper = document.getElementById("comment-content-wrapper-"+comment_id);

    if (comment_edit_textarea.style.display == "block") {
    //Pressed Abort
        comment_edit_textarea.style.display = "none";
        edit_option.style.display = "block";
        abort_option.style.display = "none";

        comment_content_wrapper.style.display = "block";

        save_option.style.display = "none";
    }else {
    // Pressed Edit
        comment_edit_textarea.style.display = "block";
        edit_option.style.display = "none";
        abort_option.style.display = "block";

        comment_content_wrapper.style.display = "none";

        save_option.style.display = "block";
        comment_edit_textarea_actual.value = (comment_content.innerText || comment_content.textContent).trim();
    }

}