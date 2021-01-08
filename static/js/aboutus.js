var aboutUsBtnElement = document.getElementById("aboutUs");
if (aboutUsBtnElement) {
  aboutUsBtnElement.addEventListener(
    "click",
    () => {
      window.location = "/aboutus";
    },
    false
  );
}

const forms = document.getElementsByClassName("needs-validation");
const messageElement = document.getElementById("messageSentFlash");

// Form validation for application and email submit and action to do
var validation = Array.prototype.filter.call(forms, (form) => {
  form.addEventListener(
    "submit",
    (e) => {
      if (form.checkValidity() === false) {
        e.preventDefault();
        e.stopPropagation();
        form.scrollIntoView();
      }
      form.classList.add("was-validated");

      if (form.checkValidity() === true) {
        if (form.id == "contactUs") {
          messageElement.style.display = "block";
          messageElement.scrollIntoView({
            behavior: "smooth",
            block: "end",
            inline: "nearest",
          });
        }
      }
    },
    false
  );
});
