// Logins
function loginToggle(typeOfLogin) {
  ["", "Ago"].forEach((suffix) => {
    document
      .getElementById(`${typeOfLogin}Login${suffix}`)
      .classList.toggle("hidden");
  });
}

// UUID toggle
function uuidToggle() {
  // Toggle between untrimmed and trimmed UUIDs
  ["Untrimmed", "Trimmed"].forEach((suffix) => {
    document.getElementById("uuid" + suffix).classList.toggle("hidden");
  });
  // Remove clipboard success notification if present
  resetCopyToClipboard("uuid");
}

// Parkour
let currentParkourGame = Object.keys(player.stats.general.parkour_times)[0];
function changeParkourGame(game) {
  [currentParkourGame, game].forEach((e) => {
    document
      .getElementById(e + "CheckpointContainer")
      .classList.toggle("hidden");
  });
  currentParkourGame = game;
}

//==============================================================================
// CLIENT-SIDE DATA POPULATION
//
// While all other stats data is populated in the HTML template, the data for
// Quests, Challenges, Achievements, Online Status, Recent Games, and Guild is
// populated using JS. Each of these areas require an additional API request
// seperate from the main stats API, and so are populated client side on user
// click to reduce requests and improve performance.
//
// The Games API is also used within the Online Status, Recent Games, and Guild
// functions if the player is either online has recent games to show, or is in a
// guild, respectively.
//
// Quests/Challenges/Achievements/Games: Hypixel resource API request directly
// from frontend (no API key required) Online Status/Recent Games/Guild: Hypixel
// API request via internal AJAX (Hypixel API key required)
//==============================================================================

//==============================================================================
// COMMON FUNCTIONS
//==============================================================================

let loadStates = {}; // Track which requests have been made, prevent repitition

// Make request and execute a following function
// There must be <div>s with id of [name]Error and [name]Container
function requestHandler(name, nextFunction) {
  if (!loadStates[name]) {
    urlToJson(apiUrls[name]).then((result) => {
      const errorElement = document.getElementById(name + "Error");
      const containerElement = document.getElementById(name + "Container");
      if (result.success) {
        loadStates[name] = true;
        console.log("Request Successful. Executing " + name + " function...");
        errorElement.classList.add("hidden");
        containerElement.classList.remove("hidden");
        nextFunction(result);
      } else {
        console.log("Error");
        console.log(result);
        errorElement.classList.remove("hidden");
        containerElement.classList.add("hidden");
      }
    });
  }
}

// Make request and execute a following function with game information
function requestHandlerWithGames(name, initialResponse, nextFunction) {
  // Get game information
  if (!loadStates["games"]) {
    let gameInfo = null;
    urlToJson(apiUrls["games"]).then((result) => {
      if (result.success) {
        gameInfo = result.games || {};
        loadStates["games"] = gameInfo;
        console.log("Request Successful. Executing " + name + " function...");
      } else {
        console.log("Error");
        console.log(result);
        gameInfo = {};
      }
      nextFunction(initialResponse, gameInfo);
    });
  } else {
    nextFunction(initialResponse, loadStates["games"]);
  }
}

// Fill remaining space in a container with empty elements
function fillEmptySlots(container, slots, text = false) {
  for (let i = 0; i < slots; i++) {
    const element = document.createElement("div");
    element.className = "placeHolder noSelect grayBorder gray bold center";

    const space = document.createElement("span");
    if (text && i == 0) {
      space.textContent = text;
    } else {
      space.textContent = " ";
    }
    element.appendChild(space);

    container.appendChild(element);
  }
}

// Create a simple text element
const makeCell = (text, hideOnMobile = false) => {
  const cell = document.createElement("div");
  cell.className = `evenFlex ${hideOnMobile ? "hideOnMobile" : ""}`;
  cell.innerHTML = `${text ?? ""}`;
  return cell;
};

// Create a simple placeHolder element
const makeLeftRightElement = (
  color,
  leftText,
  rightText,
  customClasses = false
) => {
  // Main wrapper
  const element = document.createElement("div");
  if (customClasses) {
    customClasses.forEach((c) => {
      element.classList.add(c);
    });
  } else {
    element.className = `placeHolder wrappedFlex pointer noSelect hoverOpacity ${color} ${color}Border`;
  }

  // Left text
  const leftDiv = document.createElement("div");
  leftDiv.className = `doubleFlex placeHolderText ${color}`;
  leftDiv.textContent = leftText;

  // Right text
  const rightDiv = document.createElement("div");
  rightDiv.className = `evenFlex placeHolderText ${color}`;
  rightDiv.style.textAlign = "right";
  rightDiv.textContent = rightText;

  // Append children
  element.appendChild(leftDiv);
  element.appendChild(rightDiv);

  return element;
};

//==============================================================================
// QUESTS
//==============================================================================

function quests(questInfo) {
  const questStats = player.stats.general.quests;

  // Display the details of a given quest
  const setQuestDetails = (title, description, rewards) => {
    document.getElementById("questsQuestTitle").innerHTML = title;

    // Insert description (remove color tags)
    document.getElementById("questsQuestDescription").innerHTML =
      description.replace(/%%.*?%%/g, "");

    // Insert rewards
    const questRewardsElement = document.getElementById("questsQuestRewards");
    questRewardsElement.innerHTML = "";

    rewards.forEach((reward) => {
      const rewardSpan = document.createElement("span");

      const rewardInfo = questRewards[reward.type] || {};
      const rewardName = rewardInfo.name || reward.type;
      const rewardColor = rewardInfo.color || "gray";
      const rewardAmount = reward.amount || 1;

      rewardSpan.textContent = `${rewardAmount?.toLocaleString()} ${rewardName} `;
      rewardSpan.className = rewardColor;
      questRewardsElement.appendChild(rewardSpan);
    });
  };

  // Display all the quests for a given game mode
  const renderQuests = (quests) => {
    const container = document.getElementById("placeHolderContainerQuestsGame");
    container.innerHTML = "";
    container.scrollTop = 0;

    quests.forEach((quest, index) => {
      const element = makeLeftRightElement(
        "darkGreen",
        quest.name,
        quest.completions.toLocaleString()
      );
      element.onclick = () =>
        setQuestDetails(quest.name, quest.description, quest.rewards);
      container.appendChild(element);
      if (index === 0) element.click();
    });

    // Add empty placeholders if there are fewer than 4 quests
    fillEmptySlots(container, 4 - quests.length);
  };

  // Display the key quest information for a given game mode
  const handleModeClick = (mode, modeCompletions) => {
    document.getElementById("questsModeTitle").innerHTML =
      gameInformation[mode];
    document.getElementById("questsModeCompletions").innerHTML =
      modeCompletions.toLocaleString();
    document.getElementById(
      "questCompletionsCompletions"
    ).innerHTML = `Completion${modeCompletions === 1 ? "" : "s"}`;

    // Get quests and sort by descending completions
    const quests = questInfo.quests[mode]
      .map((quest) => ({
        name: quest.name,
        description: quest.description,
        completions: questStats.completions[quest.id] || 0,
        rewards: quest.rewards,
      }))
      .sort((a, b) => b.completions - a.completions);

    // Display the completions
    renderQuests(quests);
  };

  // Calculate total completions for each game mode
  const questsModeTotals = Object.entries(questInfo.quests)
    .map(([mode, quests]) => {
      const modeCompletions = quests.reduce((total, quest) => {
        return total + (questStats.completions[quest.id] || 0);
      }, 0);
      return { mode, completions: modeCompletions };
    })
    .sort((a, b) => b.completions - a.completions);

  // Identify most-quested game mode
  const mainMode = questsModeTotals[0].completions
    ? gameInformation[questsModeTotals[0].mode]
    : "N/A";
  document.getElementById("questsMainMode").innerHTML = mainMode;

  // Populate game mode list
  const container = document.getElementById("placeHolderContainerQuests");
  container.innerHTML = "";

  questsModeTotals.forEach((modeInfo, index) => {
    const element = makeLeftRightElement(
      "darkAqua",
      gameInformation[modeInfo.mode],
      modeInfo.completions.toLocaleString()
    );
    element.onclick = () =>
      handleModeClick(modeInfo.mode, modeInfo.completions);
    container.appendChild(element);
    if (index === 0) element.click();
  });
}

//==============================================================================
// CHALLENGES
//==============================================================================

function challenges(challengeInfo) {
  const challengeStats = player.stats.general.challenges;

  // Display the details of a given challenge
  const setChallengeDetails = (title, rewards) => {
    document.getElementById("challengesChallengeTitle").innerHTML = title;
    document.getElementById("challengesChallengeRewardXP").innerHTML = (
      rewards[0]?.amount || 0
    ).toLocaleString();
  };

  // Display all the challenges for a given game mode
  const renderChallenges = (challenges) => {
    const container = document.getElementById(
      "placeHolderContainerChallengesGame"
    );
    container.innerHTML = "";
    container.scrollTop = 0;

    challenges.forEach((challenge, index) => {
      const element = makeLeftRightElement(
        "darkGreen",
        challenge.name,
        challenge.completions.toLocaleString()
      );
      element.onclick = () =>
        setChallengeDetails(challenge.name, challenge.rewards);
      container.appendChild(element);
      if (index === 0) element.click();
    });

    // Add empty placeholders if there are fewer than 4 challenges
    fillEmptySlots(container, 4 - challenges.length);
  };

  // Display the key quest information for a given game mode
  const handleModeClick = (mode, modeCompletions) => {
    document.getElementById("challengesModeTitle").innerHTML =
      gameInformation[mode];
    document.getElementById("challengesModeCompletions").innerHTML =
      modeCompletions.toLocaleString();
    document.getElementById("challengesModeSuffix").innerHTML =
      modeCompletions === 1 ? "Completion" : "Completions";

    // Get challenges and sort by descending completions
    const challenges = challengeInfo.challenges[mode]
      .map((challenge) => ({
        name: challenge.name,
        description: challenge.description,
        completions: challengeStats.completions[challenge.id] || 0,
        rewards: challenge.rewards,
      }))
      .sort((a, b) => b.completions - a.completions);

    // Display the completions
    renderChallenges(challenges);
  };

  // Calculate total completions for each game mode
  const challengesModeTotals = Object.entries(challengeInfo.challenges)
    .map(([mode, challenges]) => {
      const modeCompletions = challenges.reduce((total, challenge) => {
        return total + (challengeStats.completions[challenge.id] || 0);
      }, 0);
      return { mode, completions: modeCompletions };
    })
    .sort((a, b) => b.completions - a.completions);

  // Identify most-challenged game mode
  const mainMode = challengesModeTotals[0].completions
    ? gameInformation[challengesModeTotals[0].mode]
    : "N/A";
  document.getElementById("challengesMainMode").innerHTML = mainMode;

  // Populate game mode list
  const container = document.getElementById("placeHolderContainerChallenges");
  container.innerHTML = "";

  challengesModeTotals.forEach((modeInfo, index) => {
    const element = makeLeftRightElement(
      "darkAqua",
      gameInformation[modeInfo.mode],
      modeInfo.completions.toLocaleString()
    );
    element.onclick = () =>
      handleModeClick(modeInfo.mode, modeInfo.completions);
    container.appendChild(element);
    if (index === 0) element.click();
  });
}

//==============================================================================
// ACHIEVEMENTS
//==============================================================================

// Toggle between One Time and Tiered achievements
let currentAchievementView = "oneTime";

function oneTimeTiered(type) {
  if (type != currentAchievementView) {
    // Toggle the elements
    ["OneTime", "Tiered"].forEach((e) => {
      document
        .getElementById("placeHolderContainerAchievementsMode" + e)
        .classList.toggle("hidden");
    });

    // Style the buttons accordingly
    ["oneTime", "tiered"].forEach((e) => {
      ["pillSelected", "pointer", "noSelect", "hoverOpacity"].forEach((c) => {
        document.getElementById(e + "Button").classList.toggle(c);
      });
    });

    // Update the status
    currentAchievementView = type;
  }
}

// Toggle between Minimised and Expanded views
let currentAchievementExpansion = "minimised";

function minimisedExpanded(expansion) {
  if (expansion != currentAchievementExpansion) {
    // Minimise or expand the elements
    const achievementBars = document.querySelectorAll(".achievementExtra");
    achievementBars.forEach((bar) => {
      if (expansion == "minimised") {
        if (!bar.classList.contains("hidden")) {
          bar.classList.add("hidden");
        }
      }
      if (expansion == "expanded") {
        if (bar.classList.contains("hidden")) {
          bar.classList.remove("hidden");
        }
      }
    });

    // Style the buttons accordingly
    ["minimised", "expanded"].forEach((e) => {
      ["pillSelected", "pointer", "noSelect", "hoverOpacity"].forEach((c) => {
        document.getElementById(e + "Button").classList.toggle(c);
      });
    });

    // Update the current state
    currentAchievementExpansion = expansion;
  }
}

// Populate achievement info
const achievementStats = player.stats.general.achievements;
let achievementInfo = null;
let currentAchievementType = null;

function achievements(achievementInfoInitial, type = "current") {
  // Assign global resource on first execution only
  if (Object.entries(achievementInfoInitial).length > 0) {
    achievementInfo = achievementInfoInitial;
    console.log(achievementStats);
    console.log(achievementInfo);
  }

  // Record the scroll position to be maintained
  let currentScroll = document.documentElement.scrollTop;

  // Update the Current and Legacy buttons accordingly
  if (currentAchievementType == null) {
    // Do nothing - first execution
  } else if (type != currentAchievementType && currentAchievementType != null) {
    ["current", "legacy"].forEach((e) => {
      ["pillSelected", "pointer", "noSelect", "hoverOpacity"].forEach((c) => {
        document.getElementById(e + "Button").classList.toggle(c);
      });
    });
  } else {
    return; // Exit the function if the selected type is already displayed
  }
  currentAchievementType = type;

  // Prepare data structures
  let achievementsModes = {};
  let possibleAchievementsModes = {};
  let pointsModes = {};
  let possiblePointsModes = {};

  // Logic object for checking whether or not to include an achievement:
  // Do not show a legacy achievement if type == "current"
  // Do show a legacy achievement if type == "legacy"
  const typeLogic = { current: false, legacy: true };

  // Loop through each mode as defined by the resource API
  for (const [mode, value] of Object.entries(achievementInfo["achievements"])) {
    // Prepare counters (PER MODE)
    // Total number of achievements completed by the player
    let achievementsTotal = 0;
    // Maximum possible number of achievements that can be earned
    let possibleAchievementsTotal = 0;
    // Total number of achievement points earned by the player
    let pointsTotal = 0;
    // Maximum possible number of achievement points that can be earned
    let possiblePointsTotal = 0;

    // Increment for one time achievements
    for (const [name, details] of Object.entries(value["one_time"])) {
      if (Object.keys(details).includes("legacy") == typeLogic[type]) {
        possibleAchievementsTotal++;
        possiblePointsTotal += details["points"];
        // If the achievement given by the resource API is completed
        if (
          achievementStats["achievements_one_time"].includes(
            mode + "_" + name.toLowerCase()
          )
        ) {
          achievementsTotal++;
          pointsTotal += details["points"];
        }
      }
    }

    // Increment for tiered achievements
    for (const [name, details] of Object.entries(value["tiered"])) {
      if (Object.keys(details).includes("legacy") == typeLogic[type]) {
        // Account for all tiers when calculating the possible points
        possibleAchievementsTotal += details["tiers"].length;
        for (i = 0; i < details["tiers"].length; i++) {
          possiblePointsTotal += details["tiers"][i]["points"];
        }
        // If any tier of the achievement given by the resource API is completed
        if (
          Object.keys(achievementStats["achievements"]).includes(
            mode + "_" + name.toLowerCase()
          )
        ) {
          for (i = 0; i < details["tiers"].length; i++) {
            if (
              achievementStats["achievements"][
                mode + "_" + name.toLowerCase()
              ] >= details["tiers"][i]["amount"]
            ) {
              achievementsTotal++;
              pointsTotal += details["tiers"][i]["points"];
            }
          }
        }
      }
    }

    // Make a record of each value for this mode in the main data structures
    if (possibleAchievementsTotal > 0) {
      achievementsModes[mode] = achievementsTotal;
      possibleAchievementsModes[mode] = possibleAchievementsTotal;
      pointsModes[mode] = pointsTotal;
      // For user consistency, take the resource API value unless it's legacy
      if (type == "current") {
        possiblePointsModes[mode] = value["total_points"];
      } else {
        possiblePointsModes[mode] = possiblePointsTotal;
      }
    }
  }

  // Calculate the achievement point progress for each mode
  let pointsModesProgressArray = [];
  for (const [mode, value] of Object.entries(pointsModes)) {
    let pointsModeProgress = { mode: mode };
    if (possiblePointsModes[mode] > 0) {
      pointsModeProgress["progress"] = parseInt(
        (value / possiblePointsModes[mode]) * 100
      );
    } else {
      pointsModeProgress["progress"] = -1;
    }
    pointsModesProgressArray.push(pointsModeProgress);
  }

  // Sort modes in descending order of achievement points progress for display
  pointsModesProgressArray.sort(function (a, b) {
    return b.progress - a.progress;
  });

  // Calculate overall totals for all the modes combined
  function sumArray(arr) {
    return arr.reduce((a, b) => a + b, 0);
  }
  const achievements = sumArray(Object.values(achievementsModes));
  const possibleAchievements = sumArray(
    Object.values(possibleAchievementsModes)
  );
  const achievementPoints = sumArray(Object.values(pointsModes));
  const possiblePoints = sumArray(Object.values(possiblePointsModes));

  // Display the overall achievement totals
  // (these won't change when browsing the modes)
  document.getElementById("achievements").innerHTML =
    achievements.toLocaleString();
  document.getElementById("achievementsTotal").innerHTML =
    possibleAchievements.toLocaleString();

  document.getElementById("achievement_points").innerHTML =
    achievementPoints.toLocaleString();
  document.getElementById("achievementsPointsTotal").innerHTML =
    possiblePoints.toLocaleString();
  document.getElementById("achievementsPointsPercentage").innerHTML =
    ((achievementPoints / possiblePoints) * 100).toFixed(2) + "%";

  // Display the per-mode achievments information
  const createClickHandlerAchievements = function (mode) {
    return function () {
      // Display the name and totals
      document.getElementById("achievementsModeTitle").innerHTML =
        gameInformation[mode] || mode;

      document.getElementById("achievementsMode").innerHTML =
        achievementsModes[mode].toLocaleString();
      document.getElementById("achievementsModePossible").innerHTML =
        possibleAchievementsModes[mode].toLocaleString();
      document.getElementById("achievementsModeProgress").innerHTML = (
        (achievementsModes[mode] / possibleAchievementsModes[mode]) *
        100
      ).toFixed(0);

      document.getElementById("achievementsModePoints").innerHTML =
        pointsModes[mode].toLocaleString();
      document.getElementById("achievementsModePointsPossible").innerHTML =
        possiblePointsModes[mode].toLocaleString();
      document.getElementById("achievementsModePointsProgress").innerHTML = (
        (pointsModes[mode] / possiblePointsModes[mode]) *
        100
      ).toFixed(0);

      // Get raw achievement data for selected mode and prepare an new array
      let achievementsModeInfo = achievementInfo["achievements"][mode];

      // Populate the achievement data
      ["OneTime", "Tiered"].forEach((view) => {
        // Convert to snake_case used by Hypixel in the API
        let alias = {
          OneTime: "one_time",
          Tiered: "tiered",
        };

        // Reset the achievement list
        let containerId = "placeHolderContainerAchievementsMode" + view;
        document.getElementById(containerId).innerHTML = "";
        document.getElementById(containerId).scrollTop = 0;

        // Create empty array for processed achievement data
        let achievementsModeFinal = [];

        // For each one time achievement of the selected mode
        for (const [id, value] of Object.entries(
          achievementsModeInfo[alias[view]]
        )) {
          if (Object.keys(value).includes("legacy") == typeLogic[type]) {
            // One Time
            if (view == "OneTime") {
              // Determine whether player has unlocked the achievement
              let completionStatus = "locked";
              if (
                achievementStats["achievements_one_time"].includes(
                  mode + "_" + id.toLowerCase()
                )
              ) {
                completionStatus = "unlocked";
              }

              // Get game and global unlock percentage
              let gamePercentUnlocked = "N/A";
              if (Object.keys(value).includes("gamePercentUnlocked")) {
                gamePercentUnlocked = value["gamePercentUnlocked"].toFixed(2);
              }
              let globalPercentUnlocked = "N/A";
              if (Object.keys(value).includes("globalPercentUnlocked")) {
                globalPercentUnlocked =
                  value["globalPercentUnlocked"].toFixed(2);
              }

              // Add the processed data to the new array
              achievementsModeFinal.push({
                name: value["name"],
                description: value["description"],
                points: value["points"],
                status: completionStatus,
                gamePercentUnlocked: gamePercentUnlocked,
                globalPercentUnlocked: globalPercentUnlocked,
              });
            }

            // Tiered
            if (view == "Tiered") {
              // Determine if player has unlocked the achievement and which tier
              let currentTier = 0;
              if (
                Object.keys(achievementStats["achievements"]).includes(
                  mode + "_" + id.toLowerCase()
                )
              ) {
                value["tiers"].forEach((t) => {
                  if (
                    achievementStats["achievements"][
                      mode + "_" + id.toLowerCase()
                    ] >= t["amount"]
                  ) {
                    currentTier++;
                  }
                });
              }

              // Add the processed data to the new array
              achievementsModeFinal.push({
                name: value["name"],
                description: value["description"],
                tierInfo: value["tiers"],
                currentTier: currentTier,
                currentProgress:
                  achievementStats["achievements"][
                    mode + "_" + id.toLowerCase()
                  ] || 0,
              });
            }
          }
        }

        // extraContainer is the achievement description which is hidden by 
        // default in minimised view.
        // Only one extraContainer should be visible at a time when minimised 
        // view is active. 
        // Therefore, previousExtraContainer is needed to hide the previous 
        // upon showing the next.
        let previousExtraContainer = null;
        let createClickHandlerAchievementsMode = function (extraContainer) {
          return function () {
            // Open the description if not already open
            if (extraContainer.classList.contains("hidden")) {
              extraContainer.classList.remove("hidden");
              // Close the previous description if applicable
              if (
                previousExtraContainer !== null &&
                previousExtraContainer != extraContainer
              ) {
                previousExtraContainer.classList.add("hidden");
              }
              previousExtraContainer = extraContainer;
              // Close the description if already open
            } else {
              extraContainer.classList.add("hidden");
            }
          };
        };

        // Display the achievements
        achievementsModeFinal.forEach((a) => {
          // Identify color based on unlock status
          let mainColor = "red";
          if (view == "OneTime") {
            if (a["status"] == "unlocked") {
              mainColor = "darkGreen";
            }
          } else if (view == "Tiered") {
            if (a["currentTier"] == a["tierInfo"].length) {
              mainColor = "darkGreen";
            } else if (a["currentTier"] > 0) {
              mainColor = "orange";
            }
          }

          // Create element and populate visible information
          const element = document.createElement("div");
          element.className = `${mainColor}Border placeHolder pointer noSelect hoverOpacity`;

          const mainContainer = makeLeftRightElement(
            mainColor,
            a["name"],
            view == "OneTime"
              ? a["points"] + " Points"
              : a["currentTier"] + "/" + a["tierInfo"].length,
            ["wrappedFlex"]
          );
          mainContainer.classList.add("wrappedFlex");
          element.appendChild(mainContainer);

          // Populate description
          let extraContainer = document.createElement("div");
          extraContainer.className = "achievementExtra hidden placeHolderText";
          extraContainer.style.marginTop = "8px";

          if (view == "OneTime") {
            // Main description
            extraContainer.appendChild(
              document.createTextNode(a["description"])
            );

            // Unlock percentages
            if (
              a["gamePercentUnlocked"] != "N/A" &&
              a["globalPercentUnlocked"] != "N/A"
            ) {
              let modePlayerCompletions = document.createElement("h3");
              modePlayerCompletions.style.marginTop = "8px";
              modePlayerCompletions.appendChild(
                document.createTextNode(
                  (gameInformation[mode] || mode) +
                    " Players Unlocked: " +
                    a["gamePercentUnlocked"] +
                    "%"
                )
              );
              modePlayerCompletions.appendChild(document.createElement("br"));
              modePlayerCompletions.appendChild(
                document.createTextNode(
                  "Global Players Unlocked: " + a["globalPercentUnlocked"] + "%"
                )
              );
              extraContainer.appendChild(modePlayerCompletions);
            }
          } else if (view == "Tiered") {
            // Tier breakdown
            a["tierInfo"].forEach((t, index) => {
              let textLine = document.createElement("div");

              let span = document.createElement("span");
              span.className = "gray";
              span.textContent = index + 1 + ". ";
              textLine.appendChild(span);

              let descriptionText = a["description"].replace(
                "%%value%%",
                t["amount"].toLocaleString()
              );
              textLine.appendChild(document.createTextNode(descriptionText));

              if (a["currentTier"] >= index + 1) {
                textLine.classList.add("darkGreen");
              } else if (a["currentTier"] == index) {
                textLine.classList.add("orange");
                textLine.innerHTML += ` (${a[
                  "currentProgress"
                ].toLocaleString()}/${t["amount"].toLocaleString()} • ${(
                  (a["currentProgress"] / t["amount"]) *
                  100
                ).toFixed(0)}%)`;
              } else if (a["currentTier"] < index + 1) {
                textLine.classList.add("red");
              }
              extraContainer.appendChild(textLine);
            });
          }

          // Finalise and insert the element
          element.appendChild(extraContainer);
          element.onclick = createClickHandlerAchievementsMode(extraContainer);
          document.getElementById(containerId).appendChild(element);
        });

        // Fill any empty space with blank elements
        function camelToText(str) {
          return str.replace(/([a-z0-9])([A-Z])/g, "$1 $2").toLowerCase();
        }

        if (achievementsModeFinal.length <= 10) {
          fillEmptySlots(
            document.getElementById(containerId),
            10 - achievementsModeFinal.length,
            achievementsModeFinal.length == 0
              ? `There are no ${camelToText(view)} achievements for this mode`
              : false
          );
        }

        // Ensure initial view is minimised by default
        if (currentAchievementExpansion == "expanded") {
          minimisedExpanded();
        }
      });
    };
  };

  document.getElementById("placeHolderContainerAchievements").innerHTML = "";
  pointsModesProgressArray.forEach((m, index) => {
    let mainColor = "gray";
    if (m["progress"] == 100) {
      mainColor = "darkGreen";
    } else if (m["progress"] == 0) {
      mainColor = "red";
    } else {
      mainColor = "orange";
    }

    const element = makeLeftRightElement(
      mainColor,
      gameInformation[m["mode"]],
      m["progress"] != -1 ? m["progress"] + "%" : ""
    );
    element.onclick = createClickHandlerAchievements(m["mode"]);
    if (index === 0) {
      element.click();
    }
    document
      .getElementById("placeHolderContainerAchievements")
      .appendChild(element);

    // Apply the previously-recorded scroll position
    document.documentElement.scrollTop = currentScroll;
  });
}

//==============================================================================
// ONLINE STATUS
//==============================================================================

function toggleOnlineDetails() {
  document.getElementById("onlineStatusDetails").classList.toggle("zeroHeight");
}

function onlineStatus(onlineStatusInfo) {
  console.log(onlineStatusInfo);
  const PREFIX = "onlineStatus";
  const s = onlineStatusInfo.session;

  if (s.online) {
    // Get game information and populate details
    requestHandlerWithGames(
      "online details",
      onlineStatusInfo,
      onlineStatusDetails
    );
  } else {
    // Show as offline
    document.getElementById(PREFIX + "Dot").classList.add("redBackground");
    document.getElementById(PREFIX + "Offline").classList.remove("hidden");

    // Remove entry points to online details
    ["Container", "Button"].forEach((e) => {
      ["pointer", "hoverOpacity"].forEach((c) => {
        document.getElementById(PREFIX + e).classList.remove(c);
      });
    });
  }

  // Show core elements
  ["Dot", "Text", "Currently"].forEach((e) => {
    document.getElementById(PREFIX + e).classList.toggle("hidden");
  });
}

function onlineStatusDetails(onlineStatusInfo, gameInfo) {
  console.log(gameInfo);
  const s = onlineStatusInfo.session;
  const PREFIX = "onlineStatus";

  // Core online status elements
  document.getElementById(PREFIX + "Dot").classList.add("greenBackground");
  document.getElementById(PREFIX + "Online").classList.remove("hidden");
  document.getElementById(PREFIX + "Details").classList.remove("zeroHeight");

  // Populate online details
  const i = gameInfo[s.gameType] ?? { name: s.gameType ?? "Unknown Game" };
  document.getElementById(PREFIX + "Game").innerHTML = i.name;
  document.getElementById(PREFIX + "Mode").innerHTML =
    s.mode == "LOBBY" ? "Lobby" : i.modeNames?.[s.mode] ?? "";
  if ("map" in s) {
    document.getElementById(PREFIX + "Map").classList.remove("hidden");
    document.getElementById(PREFIX + "MapText").innerHTML = s.map;
  }

  // Modify buttons to toggle online details
  ["Container", "Button"].forEach((e) => {
    document.getElementById(PREFIX + e).onclick = toggleOnlineDetails;
  });
}

//==============================================================================
// RECENT GAMES
//==============================================================================

// Format a timestamp as DD/MM/YY HH:MM
function formatDate(timestamp) {
  const d = new Date(timestamp);
  const pad = (n) => n.toString().padStart(2, "0");
  return `${pad(d.getDate())}/${pad(d.getMonth() + 1)}/${d
    .getFullYear()
    .toString()
    .slice(-2)} ${pad(d.getHours())}:${pad(d.getMinutes())}`;
}

// Format a duration in seconds in smallest two non-zero units)
function formatDuration(ms, suffix = "") {
  const units = [
    { label: "d", ms: 86400000 },
    { label: "h", ms: 3600000 },
    { label: "m", ms: 60000 },
    { label: "s", ms: 1000 },
  ];

  let diff = ms;
  const parts = [];

  for (const { label, ms: unitMs } of units) {
    const value = Math.floor(diff / unitMs);
    if (value > 0) {
      parts.push(`${value.toLocaleString()}${label}`);
      diff -= value * unitMs;
    }
    if (parts.length === 2) break;
  }

  return parts.length ? parts.join(" ") + suffix : suffix ? "Just now" : "0s";
}

// Determine if there are any recent games
function recentGames(recentGamesInfo) {
  console.log(recentGamesInfo);
  let games = recentGamesInfo.games;

  if (!games.length) {
    document.getElementById("noRecentGames").classList.remove("hidden");
    document.getElementById("recentGames").classList.add("hidden");
  } else {
    // Get game information and populate details
    requestHandlerWithGames("recent", recentGamesInfo, recentGamesDetails);
  }

  // Update the UI
  ["navTabButtonGeneralRecent", "recentGamesLoaded"].forEach((e) => {
    document.getElementById(e).classList.remove("hidden");
  });
  document.getElementById("navTabButtonGeneralRecent").click();
  document.getElementById("recentGamesButton").onclick =
    navTabClickHandler("Recent");
}

// Populate the recent games
function recentGamesDetails(recentGamesInfo, gameInfo) {
  console.log(gameInfo);
  games = recentGamesInfo.games;

  document.getElementById("recentGamesCount").innerHTML = games.length;
  const recentGamesDiv = document.getElementById("recentGames");

  games.forEach((game) => {
    const durationMs = game.ended ? game.ended - game.date : null;

    const startedStr = formatDate(game.date);
    const durationStr = durationMs ? formatDuration(durationMs) : "Ongoing";
    const endedStr = durationMs
      ? formatDuration(Date.now() - game.ended, " ago")
      : "Ongoing";

    const row = document.createElement("div");
    row.className = "scrollRow wrappedFlex center shmeadoColor";

    const i = gameInfo[game.gameType] ?? { name: game.gameType ?? "Unknown" };

    row.appendChild(makeCell(i.name));
    row.appendChild(makeCell(i.modeNames?.[game.mode] ?? "N/A"));
    row.appendChild(makeCell(game.map || "N/A", true));  // Hidden on mobile
    row.appendChild(makeCell(startedStr, true));  // Hidden on mobile
    row.appendChild(makeCell(durationStr, true));  // Hidden on mobile
    row.appendChild(makeCell(endedStr));

    recentGamesDiv.appendChild(row);
  });
}

//==============================================================================
// GUILD
//==============================================================================

// Convert SNAKE_CASE to camelCase
function snakeToCamel(str) {
  return str
    .toLowerCase() // make it all lowercase first
    .replace(/_([a-z])/g, (_, letter) => letter.toUpperCase());
}

// Convert guild experience to guild level
function guildExpToLevel(exp) {
  // Experience required per level (not cumulative)
  const requirements = [
    100000, // 1
    150000, // 2
    250000, // 3
    500000, // 4
    750000, // 5
    1000000, // 6
    1250000, // 7
    1500000, // 8
    2000000, // 9
    2500000, // 10
    2500000, // 11
    2500000, // 12
    2500000, // 13
    2500000, // 14
  ];

  let level = 0;
  let remaining = exp;

  for (let i = 0; i < requirements.length; i++) {
    const req = requirements[i];
    if (remaining < req) {
      // Partial progress in this level
      return (i + remaining / req).toFixed(2);
    }
    remaining -= req;
    level++;
  }

  // Level 15 and above requires 3,000,000 exp per level
  const req = 3000000;
  return (level + remaining / req).toFixed(2);
}

// Populate the guild information
function guild(guildInfo) {
  console.log(guildInfo);
  guildInfo = guildInfo.guild;

  if (!guildInfo) {
    document.getElementById("noGuild").classList.remove("hidden");
    document.getElementById("guildButton").classList.add("hidden");
  } else {
    // Get game information and populate details
    requestHandlerWithGames("guild", guildInfo, guildDetails);
  }
}

function guildDetails(guildInfo, gameInfo) {
  console.log(gameInfo);

  // Guild tag
  if (guildInfo?.tag) {
    tagId = "playerPrestigeGuildTag";
    document.getElementById(tagId).classList.remove("hidden");
    [tagId, "guildTag"].forEach((e) => {
      document
        .getElementById(e)
        .classList.add(snakeToCamel(guildInfo.tagColor ?? "gray"));
      document.getElementById(e).innerHTML = `[${guildInfo.tag}]`;
    });
  }

  // Info
  document.getElementById("guildName").innerHTML = guildInfo.name;

  document.getElementById("guildMembers").innerHTML = guildInfo.members.length;
  document.getElementById("guildCreated").innerHTML = formatDate(
    guildInfo.created
  );
  document.getElementById("guildCreatedAgo").innerHTML = formatDuration(
    Date.now() - guildInfo.created,
    " ago"
  );

  document.getElementById("guildDescription").innerHTML =
    guildInfo.description ?? "None";

  document.getElementById("guildLevel").innerHTML = guildExpToLevel(
    guildInfo.exp
  );
  document.getElementById("guildExperience").innerHTML =
    guildInfo.exp.toLocaleString();
  document.getElementById("guildLegacyRanking").innerHTML =
    guildInfo.legacyRanking
      ? `#${guildInfo.legacyRanking.toLocaleString()}`
      : "N/A";

  document.getElementById("guildExperienceKings").innerHTML =
    guildInfo.achievements.EXPERIENCE_KINGS.toLocaleString();
  document.getElementById("guildWinners").innerHTML =
    guildInfo.achievements.WINNERS.toLocaleString();
  document.getElementById("guildOnlinePlayers").innerHTML =
    guildInfo.achievements.ONLINE_PLAYERS.toLocaleString();

  let preferredGames = "None";
  if (guildInfo?.preferredGames) {
    preferredGames = guildInfo.preferredGames
      .map((game) => gameInfo[game]?.name ?? game)
      .join(", ");
  }
  document.getElementById("guildPreferredGames").innerHTML = preferredGames;

  // Experience
  const totalGameExp = Object.values(guildInfo.guildExpByGameType).reduce(
    (sum, exp) => sum + exp,
    0
  );

  Object.entries(guildInfo.guildExpByGameType)
    .sort((a, b) => b[1] - a[1]) // Sort descending amount
    .forEach(([game, exp]) => {
      const row = document.createElement("div");
      row.className = "scrollRow wrappedFlex center shmeadoColor";

      row.appendChild(makeCell(`${gameInfo?.[game]?.name ?? game}`));
      row.appendChild(makeCell(`${exp.toLocaleString()}`));
      row.appendChild(makeCell(`${((exp / totalGameExp) * 100).toFixed(2)}%`));

      document.getElementById("guildExperienceContainer").appendChild(row);
    });

  // Ranks
  guildInfo.ranks
    .sort((a, b) => b.priority - a.priority) // Sort descending priority
    .forEach((rank) => {
      const row = document.createElement("div");
      row.className = "scrollRow wrappedFlex center shmeadoColor";

      row.appendChild(makeCell(rank.name));

      if (!rank.tag) {
        row.appendChild(makeCell("None"));
      } else {
        let tag = document.createElement("div");
        tag.className = `smallPrestige ${snakeToCamel(
          guildInfo?.tagColor ?? "gray"
        )}`;
        tag.textContent = `[${rank.tag}]`;
        row.appendChild(tag);
      }

      row.appendChild(makeCell(formatDate(rank.created)));

      document.getElementById("guildRanksContainer").appendChild(row);
    });

  // Update the UI
  ["navTabButtonGeneralGuild", "guildLoaded"].forEach((e) => {
    document.getElementById(e).classList.remove("hidden");
  });
  document.getElementById("navTabButtonGeneralGuild").click();
  document.getElementById("guildButton").onclick = navTabClickHandler("Guild");
}
