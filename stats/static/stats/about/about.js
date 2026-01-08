// Apply FAQ accordion functionality on page load
document.addEventListener("DOMContentLoaded", function () {
  document.addEventListener("click", function (event) {
    // Identify if the clicked element is a question
    if (event.target.classList.contains("q")) {
      // Toggle visibility
      event.target.classList.toggle("qActive");

      let panel = event.target.nextElementSibling;
      if (panel.style.maxHeight) {
        panel.style.maxHeight = null;
      } else {
        panel.style.maxHeight = panel.scrollHeight + "px";
      }

      panel.classList.toggle("aActive");
    }
  });
});
