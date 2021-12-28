// listener for when document loads
window.addEventListener("DOMContentLoaded", function() {
    // get progress field 
    const progress = document.getElementById("progress");
    progress.addEventListener("change", function() {
        if (this.value == "In Progress"){
            console.log("in progress selected");
        } else {
            console.log("in progress not selected");
        }
    });
});
