// listener for when document loads
window.addEventListener("DOMContentLoaded", function() {
    // get progress field 
    const progress = document.getElementById("showProgress");
    progress.addEventListener("change", function() {
        hideAll();
        if (this.value == "In Progress"){
            console.log("in progress selected");
            showProgressDetails();
        } else if (this.value == "Custom") {
            console.log("custom selected");
            showCustom();
        } else {
            console.log("other");
        }
    });
});

function hideAll(){
    const inProgressDetails = document.getElementById("inProgressDetails");
    inProgressDetails.classList.add("hide");
    const customProgress = document.getElementById("customProgress");
    customProgress.classList.add("hide");
}

function showProgressDetails(){
    const inProgressDetails = document.getElementById("inProgressDetails");
    inProgressDetails.classList.remove("hide");
}

function showCustom(){
    const customProgress = document.getElementById("customProgress");
    customProgress.classList.remove("hide");
}