function togglePercent(tableId, tableCol) {
  const table = document.getElementById(tableId);
  const rows = table.getElementsByTagName("tr");

  // Loop through each row and toggle the percentage
  for (let i = 1; i < rows.length; i++) {
    const cells = rows[i].getElementsByTagName("td");

    // Check if the current row has a cell at the specified column index
    if (cells[tableCol]) {
      let cellText = cells[tableCol].innerText.trim();

      // Toggle between percentage and decimal
      if (cellText.endsWith("%")) {
        // Swap percentage with original decimal value
        cells[tableCol].innerText = cells[tableCol].dataset.decimal;
      } else {
        // Convert decimal to percentage
        let decimalValue = parseFloat(cellText);
        cells[tableCol].setAttribute("data-decimal", decimalValue.toFixed(3)); // Save decimal for toggling back
        cells[tableCol].innerText =
          ((decimalValue / (decimalValue + 1)) * 100).toFixed(2) + "%";
      }
    }
  }
}

function toggleColumns(tableId, cols) {
  const table = document.getElementById(tableId);

  // Loop through each row of the table (including the header)
  for (let i = 0; i < table.rows.length; i++) {
    let row = table.rows[i];

    // Loop through each cell of the row
    for (let j = 0; j < row.cells.length; j++) {
      if (cols.includes(j)) {
        // Show the cell if its column is in the cols array
        row.cells[j].style.display = "";
      } else {
        // Hide the cell if it's not in the cols array
        row.cells[j].style.display = "none";
      }
    }
  }
}

function showAllColumns(tableId) {
  const table = document.getElementById(tableId);
  const cells = table.querySelectorAll("th, td");

  // Loop through each cell and reset the display property
  cells.forEach(function (cell) {
    cell.style.display = "";
  });
}

function mobileColumns(mobileWidth, tableId, cols) {
  if (mobileWidth.matches) {
    // If media query matches
    toggleColumns(tableId, cols);
  } else {
    showAllColumns(tableId);
  }
}
