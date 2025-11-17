// const uploadModel = document.getElementById("uploadModel");
// const loginModel =document.getElementById("loginModel");

// const uploadBtn = document.getElementById("uploadBtn");
// const loginBtn = document.getElementById("loginBtn");
// const closeBtns = document.querySelectorAll(".close");

// uploadBtn.onclick = () =>{
//     uploadModel.style.display = "flex";
// };

// loginBtn.onclick = () =>{
//     loginModel.style.display = "flex";
// };

// closeBtns.forEach(btn =>{
//     btn.onclick = () =>{
//         uploadModel.style.display = "none";
//         loginModel.style.display = "none";
//     };
// });

// window.onclick = (e) =>{
//     if(e.target === uploadModel||e.target ===loginModel){
//         uploadModel.style.display="none";
//         loginModel.style.display ="none";
//     }
// };
// Wait until the page is fully loaded
document.addEventListener("DOMContentLoaded", () => {
  // Get modals
  const uploadModal = document.getElementById("uploadModal");
  const loginModal = document.getElementById("loginModal");

  // Get buttons
  const uploadBtn = document.getElementById("uploadBtn");
  const loginBtn = document.getElementById("loginBtn");

  // Get all close buttons
  const closeBtns = document.querySelectorAll(".close");

  // Show Upload modal
  uploadBtn.addEventListener("click", (e) => {
    e.preventDefault();
    uploadModal.style.display = "flex";
  });

  // Show Login modal
  loginBtn.addEventListener("click", (e) => {
    e.preventDefault();
    loginModal.style.display = "flex";
  });

  // Close modals when clicking X
  closeBtns.forEach((btn) => {
    btn.addEventListener("click", () => {
      uploadModal.style.display = "none";
      loginModal.style.display = "none";
    });
  });

  // Close modal when clicking outside
  window.addEventListener("click", (e) => {
    if (e.target === uploadModal) uploadModal.style.display = "none";
    if (e.target === loginModal) loginModal.style.display = "none";
  });
});
