// Current price element
var currentPriceElement = document.getElementById("current_price");

// Strike price element
var strikePriceElement = document.getElementById("strike_price");

// Current price from attribute nam="" in html
var currentPrice = currentPriceElement.getAttribute("name");

// Strike price from attribute name="" in html
var strikePrice = strikePriceElement.getAttribute("name");


if (parseFloat(currentPrice) > parseFloat(strikePrice)) {
    // Toggle the red bootstrap class for the badge
    strikePriceElement.classList.toggle("badge-danger");

    // Our strike_warning element
    var strikeWarningElement = document.getElementById("strike_warning")

    // Set the warning message to visible
    strikeWarningElement.style.display = "block";

    strikeWarningElement.addEventListener(
        "click",
        () => {
            strikeWarningElement.style.display = "none";
        },
        false
      );



}
