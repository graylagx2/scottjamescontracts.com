// Contract data submit button
var SubmitBtnElement = document.getElementById("submit");
// Home button
var homeBtnElement = document.getElementById("home-btn");

// Contract data button press event listener
SubmitBtnElement.addEventListener(
  "click",
  () => {
    var tickerInputField = document.forms["input"].ticker_input;
    var formSelectField = document.forms["input"].form_select;

    if (tickerInputField) {
      // Form input field for ticker
      var tickerInput = tickerInputField.value;

      // Check if text field has text using name attributes
      if (tickerInput !== "") {
        // Make the loader visible by setting the css of element to display block
        document.getElementById("loader").style.display = "block";

        // Event listener to wait for page to finish loading
        window.addEventListener(
          "load",
          () => {
            // Hide the loader element by setting css to display none
            document.getElementById("loader").style.display = "none";
          },
          false
        );
      }
    }

    if (formSelectField) {
      // Form input field for ticker
      var formSelect = formSelectField.value;

      // Check if text field has text using name attributes
      if (formSelect !== "") {
        // Make the loader visible by setting the css of element to display block
        document.getElementById("loader").style.display = "block";

        // Event listener to wait for page to finish loading
        window.addEventListener(
          "load",
          () => {
            // Hide the loader element by setting css to display none
            document.getElementById("loader").style.display = "none";
          },
          false
        );
      }
    }
  },
  false
);

if (homeBtnElement) {
  homeBtnElement.addEventListener(
    "click",
    () => {
      // Make the loader visible by setting the css of element to display block
      document.getElementById("loader").style.display = "block";

      // Event listener to wait for page to finish loading
      window.addEventListener(
        "load",
        () => {
          // Hide the loader element by setting css to display none
          document.getElementById("loader").style.display = "none";
        },
        false
      );
    },
    false
  );
}
