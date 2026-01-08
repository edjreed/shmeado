// Place cursor in player stats search
window.setTimeout(function () {
  document.getElementById("homeSearchTabInput").focus();
}, 0);

// Search tab management
const searchTabClickHandler = function (tab) {
  return function () {
    // Update metadata
    [currentSearchTab, tab].forEach((t) => {
      document
        .getElementById("searchTab" + t)
        .classList.toggle("navTabSelected");
      document.getElementById("searchTabButton" + t).classList.toggle("bold");
    });

    // Get input elements
    const input = document.getElementById("homeSearchTabInput");
    const inputContainer = document.getElementById(
      "homeSearchTabInputContainer"
    );
    const inputCompare = document.getElementById("homeSearchTabInputCompare");
    const inputCompareContainer = document.getElementById(
      "homeSearchTabInputCompareContainer"
    );

    // Update inputs
    if (tab === "Comparison") {
      // Display the additional searchbar
      if (input.value !== "") {
        inputCompare.value = input.value;
        input.value = "";
      }
      input.placeholder = "Name 2...";
      inputContainer.style.marginTop = "12px";
      inputCompareContainer.classList.remove("hidden");
    } else {
      // Hide the additional searchbar for Stats and Calculator
      if (inputCompare.value !== "") {
        input.value = inputCompare.value;
        inputCompare.value = "";
      }
      input.placeholder = "Name...";
      inputContainer.style.marginTop = "25px";
      inputCompareContainer.classList.add("hidden");
    }

    currentSearchTab = tab;
  };
};

// Activate search tab buttons
searchTabs.forEach((t) => {
  document.getElementById("searchTabButton" + t.title).onclick =
    searchTabClickHandler(t.title);
});

// Search functionality
const searchInputs = ["homeSearchTabInput", "homeSearchTabInputCompare"];
searchInputs.forEach(function (input) {
  document.getElementById(input).addEventListener("keyup", function (event) {
    if (event.key === "Enter") {
      event.preventDefault();
      document.getElementById("homeSearchTabButton").click();
    }
  });
});

function search() {
  const name = cleanInput(document.getElementById(searchInputs[0]).value);

  if (name !== "") {
    // Stats
    if (currentSearchTab === "Stats") {
      window.location = statsUrl.replace("name", name);
    }

    // Calculator
    else if (currentSearchTab === "Calculator") {
      window.location = calculatorUrl.replace("name", name);
    }

    // Comparison
    else if (currentSearchTab === "Comparison") {
      const name2 = cleanInput(document.getElementById(searchInputs[1]).value);
      if (name2 !== "" && name !== name2) {
        window.location = comparisonUrl
          .replace("name1", name)
          .replace("name2", name2);
      }
    }
  }
}
