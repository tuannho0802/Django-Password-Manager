//display  modal on click

const modalWrapper = document.querySelector(
  ".modals-wrapper"
);
if (modalWrapper) {
  function displayModal(id) {
    const modal = document.getElementById(id);
    modalWrapper.style.display = "flex";
    modal.style.display = "flex";
    //close modal
    const close = document.getElementById(
      "close-modal"
    );
    close.addEventListener("click", () => {
      modalWrapper.style.display = "none";
      modal.style.display = "none";
      //I added this later, didn't cover it on the tutorial
      document.querySelector(
        "header"
      ).style.display = "unset";
    });

    //I added this later, didn't cover it on the tutorial
    document.querySelector(
      "header"
    ).style.display = "none";
  }
}

// show password
function togglePassword() {
  var passwordInput =
    document.getElementById("password");
  var icon = document.querySelector(
    ".toggle-password"
  );

  if (passwordInput.type === "password") {
    passwordInput.type = "text";
    icon.classList.remove("fa-eye");
    icon.classList.add("fa-eye-slash");
  } else {
    passwordInput.type = "password";
    icon.classList.remove("fa-eye-slash");
    icon.classList.add("fa-eye");
  }
}

//copy to clipboard
const copies =
  document.querySelectorAll(".copy");
copies.forEach((copy) => {
  copy.onclick = () => {
    let elemntToCopy =
      copy.previousElementSibling;
    elemntToCopy.select();
    document.execCommand("copy");
  };
});

//I added this later, didn't cover it on the tutorial
//Display the actions of the password card for mobile devices
const actions =
  document.querySelectorAll(".actions");
if (actions) {
  actions.forEach((action) => {
    action.onclick = () => {
      const links =
        action.querySelectorAll("a");
      links.forEach((link) => {
        link.style.display = "flex";
      });
      setTimeout(function () {
        links.forEach((link) => {
          link.style.display = "none";
        });
      }, 3000);
    };
  });
}

// logout popup
function confirmLogout() {
  let confirmAction = confirm(
    "Are you sure you want to logout?"
  );
  if (confirmAction) {
    document
      .getElementById("logout-form")
      .submit();
  }
}

function confirmLogout() {
  let confirmAction = confirm(
    "Are you sure you want to logout?"
  );
  if (confirmAction) {
    document
      .getElementById("logout-form")
      .submit(); // Ensure this submits
  }
}

// delete popup
function confirmDelete(passwordId) {
  let isConfirmed = confirm(
    "Are you sure you want to delete this password?"
  );
  if (isConfirmed) {
    document
      .getElementById("delete-btn" + passwordId)
      .click();
  }
}
