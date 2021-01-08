// Holders dropdown button
var moreBtnElement = document.getElementById("more");

// Major holders dropdown button
var mHoldersBtnElement = document.getElementById("mH");

// Institutional holders dropdown button
var iHoldersBtnElement = document.getElementById("iH");

// Institutional holders Institutions dropdown button
var iHoldersInstBtnElement = document.getElementById("iHI");

// Holders button press event listener
moreBtnElement.addEventListener(
  "click",
  () => {
    // Target element to toggle dropup class on
    var mTargetElement = document.getElementById("moreToggle");

    // Toggle the class
    mTargetElement.classList.toggle("dropup");
  },
  false
);

// Major holders button press event listener
mHoldersBtnElement.addEventListener(
  "click",
  () => {
    // Target element to toggle dropup class on
    var mhTargetElement = document.getElementById("caretToggleMh");

    // Toggle the class
    mhTargetElement.classList.toggle("dropup");
  },
  false
);

// Institutional holder button press event listener
iHoldersBtnElement.addEventListener(
  "click",
  () => {
    // Target element to toggle dropup class on
    var ihTargetElement = document.getElementById("caretToggleIh");

    // Toggle the class
    ihTargetElement.classList.toggle("dropup");
  },
  false
);

if (iHoldersInstBtnElement) {
  // Institutional holder button press event listener
  iHoldersInstBtnElement.addEventListener(
    "click",
    () => {
      // Target element to toggle dropup class on
      var ihITargetElement = document.getElementById("caretToggleIhI");

      // Toggle the class
      ihITargetElement.classList.toggle("dropup");
    },
    false
  );
}
