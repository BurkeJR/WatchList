// listener for when document loads
window.addEventListener("DOMContentLoaded", function() {
    const titleInput = document.getElementById("showTitle");
    titleInput.addEventListener("keyup", search)
});

function search(){
    const titleInput = document.getElementById("showTitle");
    let searchVal = titleInput.value;

    const imdbShowSearchURL = `https://imdb-api.com/en/API/SearchSeries/k_2v2sxps1/${searchVal}`;

    const autocom_box = document.getElementById("imdbSearchResults");
    
    while (autocom_box.lastChild){
        autocom_box.removeChild(autocom_box.lastChild);
    }

    fetch(imdbShowSearchURL)
        .then(validateJSON)
        .then(insertSuggestions)
        .catch(error => {
            console.log("Show Search Failed: ", error);
    });

}

function insertSuggestions(data){
    const autocom_box = document.getElementById("imdbSearchResults");

    for (const result of data.results){
        const resultItem = document.createElement("li");
        resultItem.innerText = result.title;
        autocom_box.appendChild(resultItem);
    }
}

/**
 * Validate a response to ensure the HTTP status code indcates success.
 * 
 * @param {Response} response HTTP response to be checked
 * @returns {object} object encoded by JSON in the response
 */
 function validateJSON(response) {
    if (response.ok) {
        return response.json();
    } else {
        return Promise.reject(response);
    }
}