window.addEventListener("DOMContentLoaded", function() {

    const searchBar = document.getElementById("search-bar");
    searchBar.addEventListener("input", search)
});

function search() {
    const searchBar = document.getElementById("search-bar");
    const str = searchBar.value;

    let matchFound = false;
	const table = document.querySelector("table");

    for (let r = 1; r < table.rows.length; r++){
		table.rows[r].classList.remove("highlight");
	}
	if (str !== "") {
		// iterate over all rows after the first one (don't search headings)
		let row;
		for (let r = 1; r < table.rows.length; r++) {
			row = table.rows[r];
			// keep track of whether any cells match
			matchFound = false;
			// iterate over every cell (td) in this row
			for (const cell of row.cells) {
				const data = cell.textContent;
				if (data.toLowerCase().includes(str.toLowerCase())){
					matchFound = true;
				}
			}
			if (matchFound){
				row.classList.add("highlight");
			}

		}
    }
}