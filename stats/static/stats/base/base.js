// Domain glint animation
function headerDomainGlint() {
  const string = "shmeado.club";
  const increment = 25;

  // Turn characters yellow
  string.split("").forEach((c, index) => {
    setTimeout(
      function (char) {
        document.getElementById(char).classList.add("emojiColor");
      },
      index * increment,
      c
    );
  });

  // Turn characters white
  string.split("").forEach((c, index) => {
    setTimeout(
      function (char) {
        document.getElementById(char).classList.replace("emojiColor", "white");
      },
      (index + string.length) * increment,
      c
    );
  });
}
headerDomainGlint();

// Randomise base template icon and background
function randomInteger(max) {
  return Math.floor(Math.random() * Math.floor(max));
}

function randomEmoji() {
  const emojiChoices = [
    "1f601",
    "1f603",
    "1f600",
    "1f604",
    "1f60b",
    "1f607",
    "1f61b",
    "1f633",
  ];
  let emojiIndex = randomInteger(emojiChoices.length);
  let emojiChoice = emojiChoices[emojiIndex];
  let emojiUrl = "https://abs.twimg.com/emoji/v2/svg/" + emojiChoice + ".svg";

  document.getElementById("metaIcon").href = emojiUrl;
  document.getElementById("headerIconImage").src = emojiUrl;
  document.getElementById("headerIconImage").classList.remove("hidden");
  document.getElementById("headerIconPlaceholder").classList.add("hidden");
}
randomEmoji();

function randomBackground() {
  let backgroundChoice = randomInteger(4) + 1;
  document.body.style.backgroundImage =
    "url(" + backgroundsUrl + backgroundChoice + ".png)";
} // Excuted later during theme management

// Dark theme background
function darkBackground() {
  document.body.style.background = "#111111";
}

// Header search bar
const headerSearchTerm = document.getElementById("headerSearchBar");
headerSearchTerm.addEventListener("keyup", function (event) {
  if (event.key === "Enter") {
    event.preventDefault();
    headerSearchBarSearch();
  }
});

function cleanInput(input) {
  return input.replace(/\W/g, "");
}

function headerSearchBarSearch() {
  let name = cleanInput(headerSearchTerm.value);
  if (name !== "") {
    window.location = statsUrl.replace("name", name);
  }
}

// Header API status
function toggleApiStatus() {
  document.getElementById("apiStatus").classList.toggle("apiStatusShown");
}

// Sidebar
function sidebar() {
  const sidebar = document.getElementById("sidebar");
  if (sidebar.style.display === "block") {
    document.getElementById("sidebar").style.display = "none";
  } else {
    document.getElementById("sidebar").style.display = "block";
  }
}

function checkSidebar() {
  // Ensure sidebar is shown when moving above 561px
  const showSidebar = window.matchMedia("screen and (min-width: 561px)");
  showSidebar.addEventListener("change", () => {
    if (showSidebar.matches) {
      document.getElementById("sidebar").style.display = "block";
    }
  });

  // Ensure sidebar is hidden up to 560px
  const hideSidebar = window.matchMedia("screen and (max-width: 560px)");
  hideSidebar.addEventListener("change", () => {
    if (hideSidebar.matches) {
      document.getElementById("sidebar").style.display = "none";
    }
  });
}
checkSidebar();

// Theme management
let activeTheme = "";
const themeToggleIcons = ["themeToggleIcon", "sidebarThemeToggleIcon"];
const themeToggleIconClasses = [
  // [light, dark]
  ["sun", "moon"], // Icon
  ["emojiColor", "white"], // Color
];

function lightThemeActive() {
  // Icons
  themeToggleIcons.forEach((i) => {
    const themeToggleIcon = document.getElementById(i);
    themeToggleIconClasses.forEach((c) => {
      themeToggleIcon.className = themeToggleIcon.className.replace(c[0], c[1]);
    });
  });

  // Sidebar Text
  document.getElementById("sidebarThemeToggleText").innerHTML = "Dark";

  // Background
  randomBackground();

  // Meta
  activeTheme = "light";
}

function darkThemeActive() {
  // Icons
  themeToggleIcons.forEach((i) => {
    let themeToggleIcon = document.getElementById(i);
    themeToggleIconClasses.forEach((c) => {
      themeToggleIcon.className = themeToggleIcon.className.replace(c[1], c[0]);
    });
  });

  // Sidebar Text
  document.getElementById("sidebarThemeToggleText").innerHTML = "Light";

  // Background
  document.body.style.background = "#111111";

  // Meta
  activeTheme = "dark";
}

const currentTheme = localStorage.getItem("theme");
if (currentTheme === "dark") {
  document.body.classList.add("dark-theme");
  darkThemeActive();
} else {
  lightThemeActive();
}

// Modify transitions for theme toggle
function modifyTransitions(duration) {
  const transitioningElements = [
    ".popularTile",
    ".showMoreButton",
    "#showKitsButton",
    ".q",
    ".qActive",
    ".navTabButton",
    ".pill",
  ];
  transitioningElements.forEach((element) => {
    const elements = document.querySelectorAll(element);
    elements.forEach((e) => {
      e.style.transition = duration + "s";
    });
  });
}

// Execute the theme toggle
function toggleTheme() {
  // Prevent background-color transitions from running during the theme change
  modifyTransitions(0);

  // Execute the theme change
  document.body.classList.toggle("dark-theme");
  let theme = "light";
  if (document.body.classList.contains("dark-theme")) {
    theme = "dark";
    darkThemeActive();
  } else {
    lightThemeActive();
  }

  // Re-enable transitions
  setTimeout(function () {
    modifyTransitions(0.2);
  }, 100);

  localStorage.setItem("theme", theme);
}
