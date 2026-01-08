// Game selection
const navGameClickHandler = function (navGame) {
  return function () {
    // Update game title
    document.getElementById("gameTitle").innerText = navGame;

    // Execute change
    [currentNavGame, navGame].forEach((game) => {
      document
        .getElementById("navGame" + game)
        .classList.toggle("navGameSelected");

      const mainStatsElement = document.getElementById("mainStatsElement");

      if (game === "Modes") {
        mainStatsElement.classList.toggle("hidden");
        document
          .getElementById("navTabBar")
          .classList.toggle("navTabBarModesSelected");
        document
          .getElementById("tabbedStatsElement")
          .classList.toggle("tabbedStatsElementModesSelected");
      } else {
        mainStatsElement.classList.toggle("navGameSelectedTarget");
        if (game === navGames[0]) {
          mainStatsElement.classList.toggle("navGameSelectedTargetLeft");
        }

        document
          .getElementById("mainStats" + game)
          .classList.toggle("mainStatsSelected");
        document
          .getElementById("moreStats" + game)
          .classList.toggle("moreStatsSelected");
      }

      document
        .getElementById("navTabBar" + game)
        .classList.toggle("navTabSelected");
      document
        .getElementById("navTabContainer" + game)
        .classList.toggle("navTabSelected");

      // Manage prestige visibility
      if (["BedWars", "SkyWars"].includes(game)) {
        document
          .getElementById("playerPrestige" + game)
          .classList.toggle("hidden");
      }
    });

    // Final updates
    currentNavGame = navGame;
    updateURL();
    prestigeCheck();

    // Trigger client-side request if needed
    if (currentNavTabs[currentNavGame] == "Quests") {
      requestHandler("quests", quests);
    }
  };
};

// Activate click handlers for navGame elements
navGames.forEach((game) => {
  document.getElementById("navGame" + game).onclick = navGameClickHandler(game);
});

// Tab selection
const navTabClickHandler = function (navTab) {
  return function () {
    // Execute change
    [currentNavTabs[currentNavGame], navTab].forEach((tab) => {
      document
        .getElementById("navTab" + currentNavGame + tab)
        .classList.toggle("navTabSelected");
      document
        .getElementById("navTabButton" + currentNavGame + tab)
        .classList.toggle("navTabButtonSelected");
    });

    // Final updates
    currentNavTabs[currentNavGame] = navTab;
    updateURL();
    prestigeCheck();

    // Trigger client-side request if needed
    if (navTab == "Quests") {
      requestHandler("quests", quests);
    }
    if (navTab == "Challenges") {
      requestHandler("challenges", challenges);
    }
    if (navTab == "Achievements") {
      requestHandler("achievements", achievements);
    }
  };
};
// Click on page load in case client-side request is needed
document.addEventListener("DOMContentLoaded", function () {
  document
    .getElementById(
      "navTabButton" + currentNavGame + currentNavTabs[currentNavGame]
    )
    .click();
});

const navSubTabClickHandler = function (navSubTab) {
  return function () {
    // Execute change
    let navTab = currentNavTabs[currentNavGame];

    [currentNavSubTabs[currentNavGame][navTab], navSubTab].forEach((tab) => {
      document
        .getElementById("navTab" + currentNavGame + navTab + tab)
        .classList.toggle("navTabSelected");
      document
        .getElementById("navTabButton" + currentNavGame + navTab + tab)
        .classList.toggle("navTabButtonSelected");
    });

    // Final updates
    currentNavSubTabs[currentNavGame][navTab] = navSubTab;
  };
};

Object.entries(navTabs).forEach((game) => {
  game[1].forEach((tab) => {
    document.getElementById("navTabButton" + game[0] + tab).onclick =
      navTabClickHandler(tab);

    if (navSubTabs[game[0]].hasOwnProperty(tab)) {
      navSubTabs[game[0]][tab].forEach((subTab) => {
        document.getElementById(
          "navTabButton" + game[0] + tab + subTab
        ).onclick = navSubTabClickHandler(subTab);
      });
    }
  });
});

// Prestige tab background check
function prestigeCheck() {
  if (currentNavTabs[currentNavGame] == "Prestige") {
    document.getElementById("navTabs").classList.add("mainElementTransparent");
  } else {
    document
      .getElementById("navTabs")
      .classList.remove("mainElementTransparent");
  }
}

// URL management
function updateURL() {
  window.history.pushState(
    "",
    "",
    statsUrlCustom
      .replace("param:game", currentNavGame)
      .replace("param:tab", currentNavTabs[currentNavGame])
  );
}
window.onload = function () {
  updateURL();
};

// Show more
let showMoreButtons = ["Upper", "Lower"];
let showingMore = false;

function showMore() {
  document.getElementById("moreStatsContainer").classList.toggle("showingMore");

  showMoreButtons.forEach((button) => {
    document.getElementById("showMore" + button).innerText =
      "Show " + (showingMore ? "More" : "Less");
  });

  showingMore = !showingMore;
}

showMoreButtons.forEach((button) => {
  document.getElementById("showMore" + button).onclick = function () {
    showMore();
  };
});

// Copy to clipboard
function copyToClipboard(prefix) {
  const text = document.getElementById(prefix + "Text").innerText;

  // Create a temporary textarea element to hold and copy the text
  let textarea = document.createElement("textarea");
  textarea.value = text;
  document.body.appendChild(textarea);
  textarea.select();
  document.execCommand("copy");
  document.body.removeChild(textarea);

  // Success indication
  document
    .getElementById(prefix + "CopyIcon")
    .classList.replace("bi-clipboard2-minus", "bi-clipboard2-check");
  document
    .getElementById(prefix + "CopyIcon")
    .classList.add("makeDarkGreenLightGreen");
  document
    .getElementById(prefix + "CopyConfirmation")
    .classList.replace("hidden", "inline");
}

function resetCopyToClipboard(prefix) {
  // Remove success indication
  document
    .getElementById(prefix + "CopyIcon")
    .classList.replace("bi-clipboard2-check", "bi-clipboard2-minus");
  document
    .getElementById(prefix + "CopyIcon")
    .classList.remove("makeDarkGreenLightGreen");
  document
    .getElementById(prefix + "CopyConfirmation")
    .classList.replace("inline", "hidden");
}

// SkyWars prestige easter egg
const bracketChars = ["Î", "Ï", "I", "t", "[", "]"];
function randomBrackets() {
  ["front", "back"].forEach((b) => {
    document.getElementById(b + "_bracket").innerHTML =
      bracketChars[Math.floor(Math.random() * 6)];
  });
}

let bracketInterval;
let bracketsActive = false;
let presElement = document.getElementById("playerPrestigeSkyWars");
if (player.stats.skywars.active_scheme.includes("mythic")) {
  presElement.innerHTML = presElement.innerHTML.replace(
    "[",
    "<span id='front_bracket'>[</span>"
  );
  presElement.innerHTML = presElement.innerHTML.replace(
    "]",
    "<span id='back_bracket'>]</span>"
  );

  presElement.onclick = function () {
    if (!bracketsActive) {
      bracketInterval = setInterval(randomBrackets, 10);
      bracketsActive = true;
    } else {
      clearInterval(bracketInterval);
      document.getElementById("front_bracket").innerHTML = "[";
      document.getElementById("back_bracket").innerHTML = "]";
      bracketsActive = false;
      bracketInterval = null;
    }
  };
}

// SkyWars kits tab navigation
let skywarsKitTabSelections = {};
["normal", "insane", "mythic", "mega"].forEach((mode) => {
  skywarsKitTabSelections[mode] = "stats";
});

function skywarsKitsToggle(tab, pill) {
  // If clicked pill is not already selected
  if (skywarsKitTabSelections[tab] !== pill) {
    ["Stats", "Prestige"].forEach((p) => {
      // Toggle hidden class on both sections
      const id = `${tab}Kit${p.charAt(0).toUpperCase() + p.slice(1)}`;
      document.getElementById(id).classList.toggle("hidden");

      // Toggle selected class on both pills
      ["pillSelected", "pointer", "noSelect", "hoverOpacity"].forEach((c) =>
        document.getElementById(id + "Button").classList.toggle(c)
      );
    });
    skywarsKitTabSelections[tab] = pill;
  }
}
