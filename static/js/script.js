function toggle_form_widget() {
    var form_widget = document.getElementById("form_widget");
    if (form_widget.style.display === "none") {
        form_widget.style.display = "block";
    } else {
        form_widget.style.display = "none";
    }
} 